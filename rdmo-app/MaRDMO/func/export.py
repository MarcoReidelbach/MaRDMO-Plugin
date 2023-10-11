from django.http import HttpResponse
from rdmo.projects.exports import Export
from rdmo.questions.models import Question

from .para import *
from .config import *
from .citation import *
from .id import *
from .sparql import *
from .display import *
import requests

import pypandoc
import re

from wikibaseintegrator import wbi_login, WikibaseIntegrator
from wikibaseintegrator.datatypes import ExternalID, Item, String, Time, MonolingualText
from wikibaseintegrator.wbi_enums import ActionIfExists
from wikibaseintegrator.wbi_config import config as wbi_config

from rdmo.views.utils import ProjectWrapper
from rdmo.views.templatetags import view_tags

class MaRDIExport(Export):

    def render(self):
        '''Function that renders User answers to MaRDI template
           (adjusted from csv export)'''
 
        # Check if MaRDI Questionaire is used
        if str(self.project.catalog)[-5:] != 'MaRDI':
            return HttpResponse(response_temp.format(err1).format(self.project.catalog))

       # # Get Data - Questions and User Answers in data dict
       # queryset = self.project.values.filter(snapshot=None)
       # data = {}
       # for question in Question.objects.order_by_catalog(self.project.catalog):
       #     if question.questionset.is_collection and question.questionset.attribute:
       #         if question.questionset.attribute.uri.endswith('/id'):
       #             set_attribute_uri = question.questionset.attribute
       #         else:
       #             set_attribute_uri = question.questionset.attribute.uri.rstrip('/') + '/id'
       #         for value_set in queryset.filter(attribute__uri=question.questionset.attribute.uri):
       #             values = queryset.filter(attribute=question.attribute, set_index=value_set.set_index) \
       #                              .order_by('set_prefix', 'set_index', 'collection_index')
       #             data[re.sub('b/','/',question.attribute.uri)+'_'+self.stringify(value_set.value)] = self.stringify_values(values)
       #     else:
       #         values = queryset.filter(attribute=question.attribute).order_by('set_prefix', 'set_index', 'collection_index')
       #         data[question.attribute.uri]=self.stringify_values(values)
        
        # create project wrapper as for the views
        project_wrapper = ProjectWrapper(self.project, self.snapshot)

        data = {}
        #print(project_wrapper.questions[:2])
        for question in project_wrapper.questions:
            # use the same template tags as in project_answers_element.html
            # get labels and to correctly attribute for conditions
            set_prefixes = view_tags.get_set_prefixes({}, question['attribute'], project=project_wrapper)
            for set_prefix in set_prefixes:
                set_indexes = view_tags.get_set_indexes({}, question['attribute'], set_prefix=set_prefix,
                                                        project=project_wrapper)
                for set_index in set_indexes:
                    values = view_tags.get_values(
                        {}, question['attribute'], set_prefix=set_prefix, set_index=set_index, project=project_wrapper
                    )
                
                    labels = view_tags.get_labels(
                        {}, question, set_prefix=set_prefix, set_index=set_index, project=project_wrapper
                    )
                
                    result = view_tags.check_element(
                        {}, question, set_prefix=set_prefix, set_index=set_index, project=project_wrapper
                    )

                    #if result:
                    if labels:
                        data[question['attribute']+'_'+str(set_index)]=self.stringify_values(values)
                    else:
                        data[question['attribute']]=self.stringify_values(values)
                       # data.append({
                       #     'question': question['attribute'],
                       #     'set': ' '.join(labels),
                       #     'values': self.stringify_values(values)
                       # })

        
        # Workflow Documentation

        # Initialize dictionaries for MaRDI KG and Wikidata queries

        wq = {}
        mq = {}

        if data[dec[0][0]] in (dec[0][1],dec[0][2]):

            #Check if research objective if provided
            res_obj=self.wikibase_answers(data,ws[5])[0] 
            if not res_obj:
                return HttpResponse(response_temp.format(err20))
            
            #Check if workflow type (theo/exp) is chosen  
            temp=self.dyn_template(data)
            if len(temp) == 0:
                return HttpResponse(response_temp.format(err5))
            
            #Check if Workflow with same label/description already on portal, stop if portal integration is desired
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                if self.entry_check(self.project.title,res_obj):
                    return HttpResponse(response_temp.format(err18))
                
            # Get Article information from mardi/wikidata/orcid, only necessary if portal integration is desired
            paper=self.wikibase_answers(data,ws[0])[0]

            # If Portal integration is desired, get further information about publication 
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                # Extract DOI
                doi=re.split(':',paper)
                if doi[0] == 'Yes':
                    #Get Citation and author information via DOI, stop if no information available by provided DOI
                    if not doi[-1]:
                        return HttpResponse(response_temp.format(err6))
                    orcid,string,cit=GetCitation(doi[-1])
                    if not cit:
                        return HttpResponse(response_temp.format(err6))

                    #Get User Answers and Citation information to query Wikidata and MaRDI KG 
                    wq, mq = self.sparql(data,ws,orcid,doi,cit)

                    #Check by DOI if Paper on MaRDI Portal
                    if mq['mqpub']["qid_doi"]["value"]:
               	        #If on Portal store QID
                        paper_qid=mq['mqpub']["qid_doi"]["value"]
                    else:
                        #If not on Portal, check by DOI if Paper on wikidata
                        if wq['wqpub']["qid_doi"]["value"]:
                            #If in Wikidata check if Entity with same label and description exists on MaRDI Portal
                            if mq['mqpub']["qid_ch1"]["value"]:
                                #If Entity exists store QID.
                                paper_qid=mq['mqpub']["qid_ch1"]["value"]
                            else:
                                #If only on wikidata, generate dummy entry (with Wikidata label, quote, QID mapping) and store QID. 
                                paper_qid=self.entry(wq['wqpub']["label_doi"]["value"],wq['wqpub']["quote_doi"]["value"],[(ExternalID,wq['wqpub']["qid_doi"]["value"],P2)])
                        else:
                            #Check by Title if paper on MaRDI Portal
                            if cit['title']:
                                if mq['mqpub']["qid_tit"]["value"]:
                                    #If on Portal store QID
                                    paper_qid=mq['mqpub']["qid_tit"]["value"]
                                else:
                                    #If not on Portal, check by Title if paper on Wikidata
                                    if wq['wqpub']["qid_tit"]["value"]:
                                        #If only on wikidata, generate dummy entry (with wikidata label, quote, QID mapping) and store QID.
                                        paper_qid=self.entry(wq['wqpub']["label_tit"]["value"],wq['wqpub']["quote_tit"]["value"],[(ExternalID,wq['wqpub']["qid_tit"]["value"],P2)])
                                    else:
                                        #If not on Portal/Wikidata, create new publication entry. Add ORCID authors, Journal, Language as required.
                                        author_qids=[]
                                        for i,aut in enumerate(orcid):
                                            #If authors not in Portal, create entries for publication authors for which ORCID number was fetched
                                            author_qids.append(self.paper_prop_entry(wq['wqaut'+str(i)],mq['mqaut'+str(i)],[aut[0],'researcher',
                                                                                     [(Item,Q7,P4),(Item,Q8,P21),(ExternalID,aut[1],P22)]]))
                                    
                                        if cit['language']:
                                            #If language not in Portal, create language entry for publication
                                            cit['language']=self.paper_prop_entry(wq['wqlan'],mq['mqlan'],[lang_dict[cit['language']],'language',
                                                                                  [(Item,Q11,P4)]])

                                        if cit['journal']:
                                            #If journal not in Portal, create journal entry for publication                                                     
                                            cit['journal']=self.paper_prop_entry(wq['wqjou'],mq['mqjou'],[cit['journal'],'scientific journal',
                                                                                 [(Item,Q9,P4)]])

                                        #Create publication entry, using citation information and author, language, journal items created before
                                        paper_qid=self.entry(cit['title'],'publication',[(Item,Q1 if cit['ENTRYTYPE'] == 'article' else Q10,P4)]+
                                                             [(Item,aut,P8) for aut in author_qids]+[(String,aut,P9) for aut in string]+
                                                             [(Item,cit['language'],P10),(Item,cit['journal'],P12),(MonolingualText,cit['title'],P7),
                                                              (Time,cit['pub_date']+'T00:00:00Z',P11),(String,cit['volume'],P13),(String,cit['number'],P14),
                                                              (String,cit['pages'],P15),(ExternalID,cit['doi'].upper(),P16)])  
                else:
                    #Get User Answers to query Wikidata and MaRDI KG
                    paper_qid=[]

            if not (wq and mq):
                #Get User Answers to query Wikidata and MaRDI KG without citation queries
                wq, mq = self.sparql(data,ws)

            # Integrate related model in wikibase
            # Check if on Portal or in Wikidata, integrate Wikidata entry if desired
            model_qid,entry=self.portal_wikidata_check(mq['mqmod'],wq['wqmod'],data)
            if entry and model_qid:
                #Update User answers, i.e. use MaRDI ID, name and description
                data.update({ws[1][0]:'mardi:'+model_qid,ws[1][1]:entry[0],ws[1][2]:entry[1]})
            #Get main subject of model
            model_ms_qid=[]
            if wq['wqmod_sub']['qid'][0]:
                #Check if on Portal or in Wikidata, integrate Wikidata entry if desired
                model_ms_qid,entry=self.portal_wikidata_check(mq['mqmod_sub'],wq['wqmod_sub'],data)
            if not (model_qid or model_ms_qid):
                #Stop if model has no QID and it main subject has no QID
                return HttpResponse(response_temp.format(err9))
            if not model_qid:
                if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                    # Generate Model Entry on Portal 
                    if not (wq['wqmod']['label'] and wq['wqmod']['quote']):
                        #Stop if no label and quote is provided for the model
                        return HttpResponse(response_temp.format(err21))
                    model_qid=self.entry(wq['wqmod']['label'],wq['wqmod']['quote'],[(Item,Q3,P4),(Item,model_ms_qid,P17)]+
                                         [(String,re.sub("\$","",form.lstrip()),P18) for form in re.split(';',wq['wqmod']['form'])]+
                                         [(ExternalID,wq['wqmod']['id'].split(':')[-1],P16)])
                    # Update User answer, i.e. include ID of newly created Model entity
                    data.update({ws[1][0]:'mardi:'+model_qid})
                else:
                     # Update User answer, i.e. MaRDI ID to be determined if published on portal
                    data.update({ws[1][0]:'mardi:tbd'})
            
            # Integrate related methods in wikibase
            methods_qid=[]
            for i in range(wq['no']['met']):
                #Check if on Portal or in Wikidata, integrate Wikidata entry if desired
                method_qid,entry=self.portal_wikidata_check(mq['mqmet'+str(i)],wq['wqmet'+str(i)],data)
                if entry and method_qid:
                   #Store QID
                   methods_qid.append(method_qid)
                   #Update User answers, i.e. use MaRDI ID and name
                   data.update({ws[2][0]+'_'+str(i):'mardi:'+method_qid,ws[2][1]+'_'+str(i):entry[0]})
                   #Get main subject of method
                   method_ms_qid=[]
                   if wq['wqmet_sub'+str(i)]['qid'][0]:
                       #Check if on Portal or in Wikidata, integrate Wikidata entry if desired
                        method_ms_qid,entry=self.portal_wikidata_check(mq['mqmet_sub'+str(i)],wq['wqmet_sub'+str(i)],data)
                   if not (method_qid or method_ms_qid):
                       #Stop if method has no QID and its main subject has no QID
                       return HttpResponse(response_temp.format(err17.format(i)))
                if not method_qid:
                    if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                        #Generate Method Entry in MaRDI KG
                        if not (wq['wqmet'+str(i)]['label'] and wq['wqmet'+str(i)]['quote']):
                            #Stop if no label and quote is provided for the method
                            return HttpResponse(response_temp.format(err22.format(i)))
                        methods_qid.append(self.entry(wq['wqmet'+str(i)]['label'],wq['wqmet'+str(i)]['quote'],[(Item,Q4,P4),(Item,method_ms_qid,P17)]+
                                                                       [(String,re.sub("\$","",form.lstrip()),P18) for form in re.split(';',wq['wqmet'+str(i)]['form'])]+
                                                                       [(ExternalID,wq['wqmet'+str(i)]['id'].split(':')[-1],P16)]))
                         #Update User answers, i.e. include ID of newly created method entity
                        data[ws[2][0]+'_'+str(i)] = 'mardi:'+methods_qid[-1]
                    else:
                         #Update User answers, i.e. MaRDI ID to be determined when published on portal
                        data[ws[2][0]+'_'+str(i)] = 'mardi:tbd'

            # Integrate related softwares in wikibase
            softwares_qid=[]
            for i in range(wq['no']['sof']):
                  #Check if on Portal or in Wikidata, integrate Wikidata entry if desired
                software_qid,entry=self.portal_wikidata_check(mq['mqsof'+str(i)],wq['wqsof'+str(i)],data)
                if entry and software_qid:
                    #Store QID
                    softwares_qid.append(software_qid)
                    #Update User answers, i.e. use MaRDI ID, name and description
                    data.update({ws[3][0]+'_'+str(i):'mardi:'+software_qid,ws[3][1]+'_'+str(i):entry[0],ws[3][2]+'_'+str(i):entry[1]})
                #Get programming languages of software (only relevant for software without QID)
                softwares_pl_qid=[]
                softwares_pl_qid_string=''
                for j in range(wq['pl'+str(i)]['no']): 
                    if wq['wqsof_sub'+str(i)+'_'+str(j)]['qid'][0]:
                        #Check if on Portal or in Wikidata, integrate Wikidata entry if desired
                        software_pl_qid,entry=self.portal_wikidata_check(mq['mqsof_sub'+str(i)+'_'+str(j)],wq['wqsof_sub'+str(i)+'_'+str(j)],data)
                        #Store QID
                        softwares_pl_qid.append(software_pl_qid)
                        #Update User Answers, i.e. ID <|> Label <|> Description transformed to Label (ID)
                        softwares_pl_qid_string+=data[ws[3][3]+'_'+str(i)].split('; ')[j].split(' <|> ')[1]+' (mardi:'+software_pl_qid+');'
                if not (software_qid or software_pl_qid):
                    #Stop if software has no QID and its programming languages have no QID
                    return HttpResponse(response_temp.format(err16.format(i)))
                #Update User answers, i.e. enter refined programming languages
                data.update({ws[3][3]+'_'+str(i):softwares_pl_qid_string})
                if not software_qid:
                    #If not on Portal create new software entity if desired
                    if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                        #Generate Software Entry in MaRDI KG
                        if not (wq['wqsof'+str(i)]['label'] and wq['wqsof'+str(i)]['quote']):
                            #Stop if no label and quote is provided for the software
                            return HttpResponse(response_temp.format(err23.format(i)))
                        softwares_qid.append(self.entry(wq['wqsof'+str(i)]['label'],wq['wqsof'+str(i)]['quote'],[(Item,Q5,P4)]+
                                                                        [(Item,plang,P19) for plang in softwares_pl_qid]+
                                                                        [(ExternalID,wq['wqsof'+str(i)]['id'].split(':')[-1],P16 if wq['wqsof'+str(i)]['id'].split(':')[0] == 'doi' else P20)]))
                        #Update User answers, i.e. include MaRDI ID of newly created software entity
                        data.update({ws[3][0]+'_'+str(i):'mardi:'+softwares_qid[-1]})
                    else:
                         #Update User answers, i.e. MaRDI ID to be determined when published on portal
                        data.update({ws[3][0]+'_'+str(i):'mardi:tbd'})
                
            # Integrate related inputs in wikibase
            inputs_qid=[]
            for i in range(wq['no']['inp']):
                #Check if on Portal or in Wikidata, integrate Wikidata entry if desired
                input_qid,entry=self.portal_wikidata_check(mq['mqinp'+str(i)],wq['wqinp'+str(i)],data)
                if entry and input_qid:
                    #Store QID
                    inputs_qid.append(input_qid)
                    #Update User answers, i.e. use MaRDI ID name 
                    data.update({ws[6][0]+'_'+str(i):'mardi:'+input_qid,ws[6][1]+'_'+str(i):entry[0]})
                else:
                    if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                        #Generate Input Entry in MaRDI KG
                        if not (wq['wqinp'+str(i)]['label'] and wq['wqinp'+str(i)]['quote']):
                            #Stop if no label and quote provided for input data set
                            return HttpResponse(response_temp.format(err24.format(i)))
                        inputs_qid.append(self.entry(wq['wqinp'+str(i)]['label'],wq['wqinp'+str(i)]['quote'],[(Item,Q6,P4),(ExternalID,wq['wqinp'+str(i)]['id'].split(':')[-1],P16)]))
                        #Update User answers, i.e. include MaRDI ID of newly created input entity
                        data.update({ws[6][0]+'_'+str(i):'mardi:'+inputs_qid[-1]})
                    else:
                        #Update User answers, i.e. MaRDI ID to be determined once published on portal
                        data.update({ws[6][0]+'_'+str(i):'mardi:tbd'})
            
            # Integrate related outputs in wikibase
            outputs_qid=[]
            for i in range(wq['no']['out']):
                #Check if on Portal or in Wikidata, integrate Wikidata entry if desired
                output_qid,entry=self.portal_wikidata_check(mq['mqout'+str(i)],wq['wqout'+str(i)],data)
                if entry and output_qid:
                    #Store QID
                    outputs_qid.append(output_qid)
                    #Update User answers, i.e. use MaRDI ID and name 
                    data.update({ws[7][0]+'_'+str(i):'mardi:'+output_qid,ws[7][1]+'_'+str(i):entry[0]})
                else:
                    if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                        #Generate Input Entry in MaRDI KG
                        if not (wq['wqout'+str(i)]['label'] and wq['wqout'+str(i)]['quote']):
                            #Stop if no label is provided for the output data set
                            return HttpResponse(response_temp.format(err25.format(i)))
                        outputs_qid.append(self.entry(wq['wqout'+str(i)]['label'],wq['wqout'+str(i)]['quote'],[(Item,Q6,P4),(ExternalID,wq['wqout'+str(i)]['id'].split(':')[-1],P16)]))          
                        #Update User answers, i.e. include MaRDI ID of newly created output entity
                        data.update({ws[7][0]+'_'+str(i):'mardi:'+outputs_qid[-1]})
                    else:
                        #Update User answers, i.e. MaRDI ID to be determined once published on portal
                        data.update({ws[7][0]+'_'+str(i):'mardi:tbd'})
            
            #Integrate involved disciplines in wikidata
            disciplines_qid=[]
            for i in range(wq['no']['dis']):
                #Check if on Portal or in Wikidata, integrate Wikidata entry if desired
                discipline_qid,entry=self.portal_wikidata_check(mq['mqdis'+str(i)],wq['wqdis'+str(i)],data)
                if entry and discipline_qid:
                    #Store QID
                    disciplines_qid.append(discipline_qid)
                    #Update User answers, i.e. use entity label instead of ID for wiki page
                    if i == 0:
                        data.update({ws[4][0]:entry[0]})
                    else:
                        data.update({ws[4][0]:'; '.join([data[ws[4][0]],entry[0]])}) 
                else:
                    return HttpResponse(response_temp.format(err15))
         
            #If desired create new workflow entry on Portal using all items generated/fetched before
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                workflow_qid=self.entry(self.project.title, res_obj,[(Item,Q2,P4),(Item,paper_qid,P3)]+
                                                                    [(Item,discipline,P5) for discipline in disciplines_qid]+
                                                                    [(Item,mmsi,P6) for mmsi in [model_qid]+methods_qid+softwares_qid+inputs_qid+outputs_qid])
            
            # Fill out MaRDI template
            for entry in data.items():
                temp=re.sub(";","<br/>",re.sub("Yes: |'","",re.sub(entry[0],repr(entry[1]),temp)))
            #Remove IDs of unanswered questions
            temp=re.sub(BASE_URI+"Section_\d{1}/Set_\d{1}/Question_\d{2}_\d", "", temp)
            temp=re.sub(BASE_URI+"Section_\d{1}/Set_\d{1}/Question_\d{2}", "", temp)
            temp=re.sub(BASE_URI+"Section_\d{1}/Set_\d{1}/Wiki_\d{2}_\d", "", temp)
            temp=re.sub(BASE_URI+"Section_\d{1}/Set_\d{1}/Wiki_\d{2}", "", temp)
            if data[dec[2][0]] == dec[2][1]: 
                # Download as Markdown
                response = HttpResponse(temp, content_type="application/md")
                response['Content-Disposition'] = 'filename="workflow.md"'
                return response
            elif data[dec[2][0]] == dec[2][2] and data[dec[3][0]] not in (dec[3][1],dec[3][2]):
                # Preview Markdown as HTML
                return HttpResponse(html.format(pypandoc.convert_text(temp,'html',format='md')))
            # Export to MaRDI Portal
            elif data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                # Export Workflow Documentation to mediawiki portal
                if lgname and lgpassword:
                    self.wikipage_export(self.project.title,re.sub('{\|','{| class="wikitable"',pypandoc.convert_text(temp,'mediawiki',format='md')))
                else:
                    #Stop if no bot credentials available
                    return HttpResponse(response_temp.format(err19))
                #Successful Export to Portal
                return HttpResponse(done.format(export.format(mardi_wiki+self.project.title.replace(' ','_'),mardi_wiki+'Item:'+workflow_qid)))
            else:
                #Stop if no export type is chosen
                return HttpResponse(response_temp.format(err2))

        # Workflow Search
        elif data[dec[0][0]] in (dec[0][3],dec[0][4]):
            #QID and String Entities to search for
            search_objs=self.wikibase_answers(data,ws[8])
            ent_string=[]
            ent_qid=[]
            for search_obj in re.split('; ',search_objs[0]):
                if re.split(':',search_obj)[0] == 'mardi' and re.match(r"Q[0-9*]",re.split(':',search_obj)[-1]):
                    ent_qid.append('wd:'+re.split(':',search_obj)[-1])
                else:
                    ent_string.append(search_obj)
 
            # Entity Type
            if data[dec[4][0]] in (dec[4][1],dec[4][2]):
                # SPARQL Query for Research Objective
                if len(ent_qid) > 0:
                    return HttpResponse(response_temp.format(err11))
                else:
                    FILTER=""
                    for ent in ent_string:
                        FILTER=FILTER+"FILTER(CONTAINS(?quote, '"+ent+"'@en)).\n"
                    query=re.sub("STATEMENT",statement_obj,re.sub("FILTER",FILTER,re.sub("ITEMFINDER","",query_base)))
            elif data[dec[4][0]] in (dec[4][3],dec[4][4]):
                # SPARQL Query for Model, Methods, and Software
                ITEMFINDER1=""
                for n,ent in enumerate(ent_string):
                    ITEMFINDER1=ITEMFINDER1+"?item"+str(n)+" rdfs:label ?itemlabel"+str(n)+".\nFILTER(CONTAINS(?itemlabel"+str(n)+", '"+ent+"'@en)).\n"
                    ent_qid.append("?item"+str(n))
                ITEMFINDER2=""
                for n,ent in enumerate(ent_qid):
                    if n == 0:
                        ITEMFINDER2=ITEMFINDER2+"?y wdt:P"+P6+" "+ent+";\n"
                    else:
                        ITEMFINDER2=ITEMFINDER2+"wdt:P"+P6+" "+ent+";\n"
                ITEMFINDER2=ITEMFINDER2+"wdt:P"+P4+" wd:"+Q2+".\n"

                query=re.sub("STATEMENT",statement_mms,re.sub("ITEMFINDER",ITEMFINDER1+ITEMFINDER2,re.sub("FILTER","",query_base)))
                     
            elif data[dec[4][0]] in (dec[4][5],dec[4][6]):
                #SPARQL Query for Research Field
                ITEMFINDER1=""
                for n,ent in enumerate(ent_string):
                    ITEMFINDER1=ITEMFINDER1+"?item"+str(n)+" rdfs:label ?itemlabel"+str(n)+".\nFILTER(CONTAINS(?itemlabel"+str(n)+", '"+ent+"'@en)).\n"
                    ent_qid.append("?item"+str(n))
                ITEMFINDER2=""
                for n,ent in enumerate(ent_qid):
                    if n == 0:
                        ITEMFINDER2=ITEMFINDER2+"?y wdt:P"+P5+" "+ent+";\n"
                    else:
                        ITEMFINDER2=ITEMFINDER2+"wdt:P"+P5+" "+ent+";\n"
                ITEMFINDER2=ITEMFINDER2+"wdt:P"+P4+" wd:"+Q2+".\n"

                query=re.sub("STATEMENT",statement_mms,re.sub("ITEMFINDER",ITEMFINDER1+ITEMFINDER2,re.sub("FILTER","",query_base)))

            else:
                return HttpResponse(response_temp.format(err3))

            results = self.get_results(mardi_endpoint, query)
        
            top="""<!DOCTYPE html>
<html>
    <head>
        <title>Workflows Found!</title>
    </head>
    <body>
        <div align='center'>
           <img src="https://www.nfdi.de/wp-content/uploads/2021/12/MaRDI_Logo_rgba.png" style="vertical-align: middle;" width="400px"/>
           <p style="color:blue;font-size:30px;">We found """+str(len(results))+""" possibly matching Workflow(s) on the MaRDI Portal!</p>
           <p style="color:blue;font-size:30px;">Here are the Links to the Documentations:</p>"""

            middle=""
            for result in results:
                middle=middle+"<a href='"+mardi_wiki+re.sub(" ","_",result["label"]["value"])+"'>"+result["label"]["value"]+"</a><br>"
            end="""</div>
    </body>
</html>"""
            return HttpResponse(top+middle+end)
 
        # Not chosen
        else:
            return HttpResponse(response_temp.format(err4))

    def stringify_values(self, values):
        '''Original function from csv export'''
        if values is not None:
            return '; '.join([self.stringify(value['value_and_unit']) for value in values])
        else:
            return ''

    def stringify(self, el):
        '''Original function from csv export'''
        if el is None:
            return ''
        else:
            return re.sub(r'\s+', ' ', str(el))

    def create_table(self, column_topics, row_ids, rows):
        '''Function that creates a markdwon table with headers.
           Row number depends on user answers, dummy entries''' 
        table=''
        for row in range(rows):
            table=table+'| '
            for n,topic in enumerate(column_topics):
                if row==0:
                    table=table+topic+' | '
                elif row==1:
                    table=table+'-- | '
                else:
                    table=table+row_ids[n]+'_'+str(row-2)+' | '
            table=table+'\n'
        return table

    def dyn_template(self, data):
        '''Function that chooses proper raw MaRDI template and
           inserts appropriate tables depending on user answers.'''
        if data[dec[1][0]] in (dec[1][1],dec[1][2]):
            temp=math_temp
            tables=math_tables
            topics=math_topics
            ids=math_ids
        elif data[dec[1][0]] in (dec[1][3],dec[1][4]):
            temp=exp_temp
            tables=exp_tables
            topics=exp_topics
            ids=exp_ids
        else:
            temp=[]
            return temp
        for n,table in enumerate(tables):
            t=self.create_table(topics[n],ids[n],sum(ids[n][0] in s for s in data.keys())+2)
            temp=re.sub(table,t,temp)
        return(temp)
       
    def wikipage_export(self,title,content): 
        '''Genereic Mediawiki Example'''

        S = requests.Session()

        URL = mardi_api

        # Step 1: GET request to fetch login token
        PARAMS_0 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_0)
        DATA = R.json()
        
        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

        # Step 2: POST request to log in.
        PARAMS_1 = {
            "action": "login",
            "lgname": lgname,
            "lgpassword": lgpassword,
            "lgtoken": LOGIN_TOKEN,
            "format": "json"
        }

        R = S.post(URL, data=PARAMS_1)

        # Step 3: GET request to fetch CSRF token
        PARAMS_2 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_2)
        DATA = R.json()

        CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

        # Step 4: POST request to edit a page

        post_content=re.sub('<math display="block">','<math>',content)

        PARAMS_3 = {
            "action": "edit",
            "title": title,
            "token": CSRF_TOKEN,
            "format": "json",
            "appendtext": post_content
            }

        R = S.post(URL , data=PARAMS_3, files=dict(foo='bar'))
        return

    def set_lengths(self, data):
        '''Get length of the User sets'''
        length=[]
        sts=['Section_4/Set_2','Section_4/Set_3','Section_4/Set_6','Section_4/Set_7']
        for st in sts:
            i=0
            data_filter = dict(filter(lambda item: st in item[0], data.items()))
            for key in data_filter.keys():
                if int(key.split('_')[-1])>i:
                    i=int(key.split('_')[-1])+1
            length.append(i)
        return length

    def wikibase_answers(self, data, wiki, length=-1):
        '''Takes data and extracts answers relevant for Wiki'''
        wiki_answers=[]
        if length >= 0:
            for question in wiki:
                for idx in range(length):
                    if question+'_'+str(idx) in data:
                        wiki_answers.append(data[question+'_'+str(idx)])
                    else:
                        wiki_answers.append('')
        else:
            for question in wiki:
                if question in data:
                    wiki_answers.append(data[question])
                else:
                    wiki_answers.append('')
        return wiki_answers

    def wikibase_login(self):
        '''Login stuff for wikibase'''
        wbi_config['MEDIAWIKI_API_URL'] = mardi_api

        #login_instance = wbi_login.OAuth1(consumer_token, consumer_secret, access_token, access_secret)
        login_instance = wbi_login.Login(user=lgname, password=lgpassword)

        wbi = WikibaseIntegrator(login=login_instance)

        return wbi

    def entry(self,label,description,facts):
        '''Takes arbitrary information and generates MaRDI portal entry.'''
        wbi = self.wikibase_login()
        
        item = wbi.item.new()
        item.labels.set('en', label)
        item.descriptions.set('en', description)

        data=[]
        for fact in facts:
            if fact[1]:
                if fact[0] == MonolingualText:
                    data.append(fact[0](text=fact[1],prop_nr=fact[2]))
                elif fact[0] == Time:
                    data.append(fact[0](time=fact[1],prop_nr=fact[2]))
                else:
                    data.append(fact[0](value=fact[1],prop_nr=fact[2]))
        item.claims.add(data)
            
        item.write()

        return item.id

    def get_results(self,endpoint_url, query):
        '''Perform SPARQL Queries via Get requests'''
        req=requests.get(endpoint_url, params = {'format': 'json', 'query': query}, headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()
        return req["results"]["bindings"]

    def entry_check(self,label,description):
        '''Check if wikibase entry with certain label and description exists.'''
        return self.get_results(mardi_endpoint,re.sub('LABEL',label,re.sub('DESCRIPTION',description,check_query)))
    
    def portal_wikidata_check(self,mquery,wquery,data):
        '''Function checks if an entry is on MaRDI portal and returns its QID
           or on Wikidata and copies the entry to the MaRDI portal and returns
           its QID.'''
        if wquery['qid'][0] == 'mardi':
            qid = wquery['qid'][-1]
            entry = [wquery['label'],wquery['quote']]
        elif wquery['qid'][0] == 'wikidata':
            entry = [wquery['label'],wquery['quote']]
            if mquery['qid']['value']:
                qid = mquery['qid']['value']
            else:
                #Create dummy entry and store QID if portal publication is desired
                if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                    #Create dummy entry and store QID
                    qid = self.entry(wquery['label'],wquery['quote'],[(ExternalID,wquery['qid'][-1],P2)])
                else:
                    qid = 'tbd'
        elif mquery['qid']['value']:
            entry = [wquery['label'],wquery['quote']]
            qid = mquery['qid']['value']
        else:
            #QID not existing
            qid = None
            entry = None

        return qid, entry
        
    def paper_prop_entry(self,wquery,mquery,props):
        '''This function takes (a property of) a paper and creates the corresponding wikibase entries.'''
        if mquery["qid"]["value"]:
            #If on Portal store QID
            qid=mquery["qid"]["value"]
        else:
            #If not on Portal, check if on Wikidata
            if wquery["qid"]["value"]:
                if mquery["qid2"]["value"]:
                    #If on Portal, store QID.
                    qid=mquery["qid2"]["value"]
                else:
                    #If only on wikidata, generate dummy entry, store QID.
                    qid=self.entry(wquery["label"]["value"],wquery["quote"]["value"],[(ExternalID,wquery["qid"]["value"],P2)])
            else:
                #If not on Portal / Wikidata create entry
                if mquery["qid3"]["value"]:
                    #If on Portal, store QID.
                    qid=mquery["qid3"]["value"]
                else:
                    #Create entry, store QID.
                    qid=self.entry(props[0],props[1],props[2])
        return qid

    def sparql(self,data,ws,orcid=None,doi=None,cit=None):
        '''This function takes user answers and performs SPARQL queries to Wikidata and MaRDI portal.'''
        
        length=self.set_lengths(data)
        print(length)
        #Get User answers for Model
        model=[]
        model.append(self.wikibase_answers(data,ws[1]))
        model.append(re.split(' <\|> ',model[0][0]) if model[0][0] else ['',model[0][1],model[0][2]])
        model.append(re.split(' <\|> ',model[0][3]) if model[0][3] else ['','',''])
        print(model) 
        #Get User answers for Methods
        method=[]
        method.append(self.wikibase_answers(data,ws[2],length[0]))
        method.append(len(method[0])//6)
        method.append([re.split(' <\|> ',method[0][i]) if method[0][i] else ['',method[0][method[1]+i],method[0][method[1]*2+i]] for i in range(method[1])])
        method.append([re.split(' <\|> ',method[0][i]) if method[0][i] else ['','',''] for i in range(method[1]*3,method[1]*4)])
        method.append([[method[2][i][0],method[2][i][1],method[2][i][2],method[3][i][0],method[0][method[1]*4+i],method[0][method[1]*5+i]] for i in range(method[1])]) 
        print(method)
        #Get User answers for Softwares
        software=[]
        software.append(self.wikibase_answers(data,ws[3],length[1]))
        software.append(len(software[0])//5)
        software.append([re.split(' <\|> ',software[0][i]) if software[0][i] else ['',software[0][software[1]+i],software[0][software[1]*2+i]] for i in range(software[1])])
        software.append([[re.split(' <\|> ',X) if X else ['','',''] for X in software[0][i].split('; ')] for i in range(software[1]*3,software[1]*4)])
        software.append([[software[2][i][0],software[2][i][1],software[2][i][2],software[3][i],software[0][software[1]*4+i]] for i in range(software[1])])
        software.append([len(s) if s[0][0] else 0 for s in software[3]])
         
        #Get User answers for Inputs
        inputs=[]
        inputs.append(self.wikibase_answers(data,ws[6],length[2]))
        inputs.append(len(inputs[0])//3)
        inputs.append([re.split(' <\|> ',inputs[0][i]) if inputs[0][i] else ['',inputs[0][inputs[1]+i],'data set'] for i in range(inputs[1])])
        inputs.append([[inputs[2][i][0],inputs[2][i][1],inputs[2][i][2],inputs[0][inputs[1]*2+i]] for i in range(inputs[1])])
        
        #Get User answers for Outputs
        outputs=[]
        outputs.append(self.wikibase_answers(data,ws[7],length[3]))
        outputs.append(len(outputs[0])//3)
        outputs.append([re.split(' <\|> ',outputs[0][i]) if outputs[0][i] else ['',outputs[0][outputs[1]+i],'data set'] for i in range(outputs[1])])
        outputs.append([[outputs[2][i][0],outputs[2][i][1],outputs[2][i][2],outputs[0][outputs[1]*2+i]] for i in range(outputs[1])])
        
        #Get User answers for Disciplines
        disciplines=[]
        disciplines.append(self.wikibase_answers(data,ws[4])[0].split('; '))
        disciplines.append(len(disciplines[0]))
        disciplines.append([re.split(' <\|> ',discipline) for discipline in disciplines[0]])
        
        #SPARQL Queries to Wikidata and MaRDI Knowledge Graph (Wikidata queries already done by dynamic option set provider function)

        wq = {} ; qw = {}
        mq = {} ; qm = {} 
        
        #Number of Methods, Software, Inputs, Outputs, Disciplines entered by user
        wq.update({'no' : {'met':method[1], 'sof':software[1], 'inp':inputs[1], 'out':outputs[1], 'dis':disciplines[1]}})
        wq.update({'pl'+str(i) : {'no':sof} for i,sof in enumerate(software[5])})
    
        #Wikidata Info for Model + Main Subject
        wq.update({'wqmod': {'qid':model[1][0].split(':'), 'label':model[1][1], 'quote':model[1][2], 'name':model[0][1], 'form':model[0][4], 'id':model[0][5]}})
        wq.update({'wqmod_sub': {'qid':model[2][0].split(':'), 'label':model[2][1], 'quote':model[2][2]}})
                  
        #Wikidate Info for Methods + Main Subjects
        wq.update({'wqmet'+str(i): {'qid':m[0].split(':'), 'label':m[1], 'quote':m[2], 'form':m[4], 'id':m[5]} for i,m in enumerate(method[4])})
        wq.update({'wqmet_sub'+str(i): {'qid':method[4][i][3].split(':'), 'label':method[3][i][1], 'quote':method[3][i][2]} for i in range(method[1])})

        #Wikidata Info for Softwares + Programming Languages
        wq.update({'wqsof'+str(i): {'qid':s[0].split(':'), 'label':s[1], 'quote':s[2], 'id':s[4]} for i,s in enumerate(software[4])})
        wq.update({'wqsof_sub'+str(i)+'_'+str(j): {'qid': s[0].split(':'), 'label':s[1], 'quote':s[2]} for i,ss in enumerate(software[4]) for j,s in enumerate(ss[3])})

        #Wikidata Info for Inputs, Outputs and Disciplines
        wq.update({'wqinp'+str(i): {'qid':inp[0].split(':'), 'label':inp[1], 'quote':inp[2], 'id':inp[3]} for i,inp in enumerate(inputs[3])})
        wq.update({'wqout'+str(i): {'qid':out[0].split(':'), 'label':out[1], 'quote':out[2], 'id':out[3]} for i,out in enumerate(outputs[3])})
        wq.update({'wqdis'+str(i): {'qid':discipline[0].split(':'), 'label':discipline[1], 'quote':discipline[2]} for i,discipline in enumerate(disciplines[2])})

        #Model + Main Subject SPARQL query for MaRDI KG
        qm.update({'mqmod' : mini.format('?qid',mbody.format(wq['wqmod']['label'],wq['wqmod']["quote"]))})
        qm.update({'mqmod_sub' : mini.format('?qid',mbody.format(wq['wqmod_sub']['label'],wq['wqmod_sub']['quote']))})

        #Methods + Main Subjects SPARQL query for MaRDI KG
        qm.update({'mqmet'+str(i): mini.format('?qid',mbody.format(wq['wqmet'+str(i)]['label'],wq['wqmet'+str(i)]['quote'])) for i in range(method[1])})
        qm.update({'mqmet_sub'+str(i): mini.format('?qid',mbody.format(wq['wqmet_sub'+str(i)]['label'],wq['wqmet_sub'+str(i)]['quote'])) for i in range(method[1])})

        #Softwares + Programming Languages SPARQL query for MaRDI KG
        qm.update({'mqsof'+str(i) : mini.format('?qid',mbody.format(wq['wqsof'+str(i)]['label'],wq['wqsof'+str(i)]['quote'])) for i in range(software[1])}),
        qm.update({'mqsof_sub'+str(i)+'_'+str(j) : mini.format('?qid',mbody.format(wq['wqsof_sub'+str(i)+'_'+str(j)]['label'],wq['wqsof_sub'+str(i)+'_'+str(j)]['quote'])) 
                                                               for i,ss in enumerate(software[4]) for j,s in enumerate(ss[3])}) 
        
        #Inputs, Outputs, Disciplines SPARQL queries for MaRDI KG
        qm.update({'mqinp'+str(i) : mini.format('?qid',mbody.format(wq['wqinp'+str(i)]['label'],wq['wqinp'+str(i)]['quote'])) for i in range(inputs[1])})
        qm.update({'mqout'+str(i) : mini.format('?qid',mbody.format(wq['wqout'+str(i)]['label'],wq['wqout'+str(i)]['quote'])) for i in range(outputs[1])})
        qm.update({'mqdis'+str(i) : mini.format('?qid',mbody.format(wq['wqdis'+str(i)]['label'],wq['wqdis'+str(i)]['quote'])) for i in range(disciplines[1])})
        
        print(wq)

        for key in qm.keys():
            #Request Data from MaRDI KG
            mq.update({key:{**dict.fromkeys({'qid'},{'value':''}),**self.get_results(mardi_endpoint,qm[key])[0]}})
        
        if cit:
            
            #Generate Keys for Publication queries
            keys = dict(Keys)
            key_dat=[orcid]
            key_ind=['pub']

            for inds in zip(key_dat,key_ind):
                for i,_ in enumerate(inds[0]):
                    if type(keys_flex['wq'+inds[1]]) == str:
                        keys['wq'+inds[1]]+=keys_flex['wq'+inds[1]].format(i)
                        keys['mq'+inds[1]]+=keys_flex['mq'+inds[1]].format(i)
                    else:
                        keys['wq'+inds[1]]+=keys_flex['wq'+inds[1]][0].format(i)
                        keys['mq'+inds[1]]+=keys_flex['mq'+inds[1]][0].format(i)

            #Set up SPRQL query and request data from wikidata
            qw.update({'wqpub' : wini.format(keys['wqpub'],wbpub.format(doi[-1].upper(),cit['journal'].lower(),lang_dict[cit['language']],
                                    cit['language'],cit['title'],''.join([''.join(wbaut.format(i,aut[1])) for i,aut in enumerate(orcid)])))})
            
            wq.update({'wqpub':{**dict.fromkeys(keys['wqpub'].split(' ?'),{"value":''}),**self.get_results(wikidata_endpoint,qw['wqpub'])[0]}})

            #Set up SPARQL query and request data from MaRDI KG
            qm.update({'mqpub' : mini.format(keys['mqpub'],mbpub.format(doi[-1].upper(),wq['wqpub']["label_doi"]["value"],wq['wqpub']["quote_doi"]["value"],cit['journal'].lower(),
                                    wq['wqpub']["label_jou"]["value"],wq['wqpub']["quote_jou"]["value"],lang_dict[cit['language']],cit['language'],
                                    wq['wqpub']["label_lan"]["value"],wq['wqpub']["quote_lan"]["value"],cit['title'],''.join([''.join(mbaut.format(i,aut[1],
                                    wq['wqpub']['label_'+str(i)]['value'],wq['wqpub']['quote_'+str(i)]['value'],aut[0])) for i,aut in enumerate(orcid)])))})

            mq.update({'mqpub':{**dict.fromkeys(keys['mqpub'].split(' ?'),{"value":''}),**self.get_results(mardi_endpoint,qm['mqpub'])[0]}})
            
            #Separate author, language and journal data requested from Wikidata and MaRDI KG
            EXT=(['aut','_',orcid],
                 ['lan','_lan'],
                 ['jou','_jou'])

            for ext in EXT:
                if len(ext) == 2:
                    wq.update({'wq'+ext[0]:{key.split('_')[0]: value for (key, value) in wq['wqpub'].items() if ext[1] in key}})
                    mq.update({'mq'+ext[0]:{key.split('_')[0]: value for (key, value) in mq['mqpub'].items() if ext[1] in key}})
                else:
                    for i,_ in enumerate(ext[2]):
                        wq.update({'wq'+ext[0]+str(i):{key.split('_')[0]: value for (key, value) in wq['wqpub'].items() if ext[1]+str(i) in key}})
                        mq.update({'mq'+ext[0]+str(i):{key.split('_')[0]: value for (key, value) in mq['mqpub'].items() if ext[1]+str(i) in key}})

        return wq, mq #model, method, software, inputs, outputs, disciplines, wq, mq



