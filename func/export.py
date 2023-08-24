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

import time

class MaRDIExport(Export):

    def render(self):
        '''Function that renders User answers to MaRDI template
           (adjusted from csv export)'''
        
        # Check if MaRDI Questionaire is used
        if str(self.project.catalog) != 'MaRDI':
            return HttpResponse(response_temp.format(err1).format(self.project.catalog))

        # Get Data - Questions and User Answers
        queryset = self.project.values.filter(snapshot=None)
        data = {}
        for question in Question.objects.order_by_catalog(self.project.catalog):
            if question.questionset.is_collection and question.questionset.attribute:
                if question.questionset.attribute.uri.endswith('/id'):
                    set_attribute_uri = question.questionset.attribute
                else:
                    set_attribute_uri = question.questionset.attribute.uri.rstrip('/') + '/id'
                for value_set in queryset.filter(attribute__uri=question.questionset.attribute.uri):
                    values = queryset.filter(attribute=question.attribute, set_index=value_set.set_index) \
                                     .order_by('set_prefix', 'set_index', 'collection_index')
                    data[re.sub('b/','/',question.attribute.uri)+'_'+self.stringify(value_set.value)] = self.stringify_values(values)
            else:
                values = queryset.filter(attribute=question.attribute).order_by('set_prefix', 'set_index', 'collection_index')
                data[question.attribute.uri]=self.stringify_values(values)
        
        # Workflow Documentation
        if data[dec[0][0]] in (dec[0][1],dec[0][2]):
            # Generate Markdown File
            # Adjust raw MaRDI templates to User answers

            paper=self.wikibase_answers(data,ws[0])[0]
            res_obj=self.wikibase_answers(data,ws[5])[0]
            
            temp=self.dyn_template(data)
            if len(temp) == 0:
                return HttpResponse(response_temp.format(err5))
            
            #Check if Workflow with same label/description already on portal, stop if portal integration is desired
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                if self.entry_check(self.project.title,res_obj):
                    return HttpResponse(response_temp.format(err18))
            
            # Get Article information from mardi/wikidata/orcid, only necessary if portal integration is desired
            if data[dec[2][0]] == dec[2][2]:
                # Get User Answers related to publication
                doi=re.split(':',paper)
                if doi[0] == 'Yes':
                    #Get Citation and author information via DOI, stop if no information available by provided DOI
                    orcid,string,cit=GetCitation(doi[-1])
                    if not cit:
                        return HttpResponse(response_temp.format(err6))
                    
                    #Get User Answers and Citation information to query Wikidata and MaRDI KG

                    model, method, software, inputs, outputs, disciplines, wq, mq = self.sparql(data,orcid,doi,cit,ws)
                
                    #Check by DOI if Paper on MaRDI Portal
                    if mq['mqpub']["qid_doi"]["value"]:
               	        #If on Portal store QID
                        paper_qid=mq['mqpub']["qid_doi"]["value"]
                    else:
                        #If not on Portal, check by DOI if Paper on wikidata
                        if wq['wqpub']["qid_doi"]["value"]:
                            #Check if Entity with same label and description exists on MaRDI Portal
                            if mq['mqpub']["qid_ch1"]["value"]:
                                #If Entity exists store QID.
                                paper_qid=mq['mqpub']["qid_ch1"]["value"]
                            else:
                                #If only on wikidata, generate dummy entry and store QID. 
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
                                        #If only on wikidata, generate dummy entry, store QID.
                                        paper_qid=self.entry(wq['wqpub']["label_tit"]["value"],wq['wqpub']["quote_tit"]["value"],[(ExternalID,wq['wqpub']["qid_tit"]["value"],P2)])
                                    else:
                                        #If not on Portal/Wikidata, create new publication entry. Add ORCID authors, Journal, Language as required.
                                        author_qids=[]
                                        for i,aut in enumerate(orcid):
                                            #Create author entries for publication
                                            author_qids.append(self.paper_prop_entry(wq['wqaut'+str(i)],mq['mqaut'+str(i)],[aut[0],'researcher',
                                                                                     [(Item,Q7,P4),(Item,Q8,P21),(ExternalID,aut[1],P22)]]))
                                    
                                        if cit['language']:
                                            #Create language entry for publication
                                            cit['language']=self.paper_prop_entry(wq['wqlan'],mq['mqlan'],[lang_dict[cit['language']],'language',
                                                                                  [(Item,Q11,P4)]])

                                        if cit['journal']:
                                            #Create journal entry for publication                                                     
                                            cit['journal']=self.paper_prop_entry(wq['wqjou'],mq['mqjou'],[cit['journal'],'scientific journal',
                                                                                 [(Item,Q9,P4)]])

                                        #Create publication entry
                                        paper_qid=self.entry(cit['title'],'publication',[(Item,Q1 if cit['ENTRYTYPE'] == 'article' else Q10,P4)]+
                                                             [(Item,aut,P8) for aut in author_qids]+[(String,aut,P9) for aut in string]+
                                                             [(Item,cit['language'],P10),(Item,cit['journal'],P12),(MonolingualText,cit['title'],P7),
                                                              (Time,cit['pub_date']+'T00:00:00Z',P11),(String,cit['volume'],P13),(String,cit['number'],P14),
                                                              (String,cit['pages'],P15),(ExternalID,cit['doi'].upper(),P16)])  
                else:
                    paper_qid=[]

                # Integrate related model in wikibase
                if re.match(r"Q[0-9*]",model[1][-1]):
                    model_qid,entry=self.portal_wikidata_check(model[1],mq['mqmog'],wq['wqmog'],data)
                    if entry and model_qid:
                        #Updata User answers, i.e. use MaRDI ID, name and description
                        data.update({ws[1][0]:'mardi:'+model_qid,ws[1][1]:entry[0],ws[1][2]:entry[1]})
                    else:
                        return HttpResponse(response_temp.format(err7))
                elif model[1][0] == 'No':
                    if mq['mqmod']["qid2_model"]["value"]:
                        #Use existing Model Entity
                        model_qid=mq['mqmod']["qid2_model"]["value"]
                        # Update User answer, i.e. use existing MaRDI ID
                        data.update({ws[1][0]:'mardi:'+model_qid})
                    else:
                        #Get main subject of model
                        if re.match(r"Q[0-9*]",model[2][-1]):
                            model_ms_qid,entry=self.portal_wikidata_check(model[2],mq['mqmoms'],wq['wqmoms'],data)
                            if not model_ms_qid:
                                return HttpResponse(response_temp.format(err9))
                        else:
                            return HttpResponse(response_temp.format(err9))
                    
                        if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                            # Generate Model Entry in MaRDI KG 
                            model_qid=self.entry(model[0][1],model[0][2],[(Item,Q3,P4),(Item,model_ms_qid,P17)]+
                                                                   [(String,re.sub("\$","",form.lstrip()),P18) for form in re.split(';',model[0][4])]+
                                                                   [(ExternalID,model[0][5],P16)])
                            # Update User answer, i.e. include ID of newly created Model entity
                            data.update({ws[1][0]:'mardi:'+model_qid})
                        else:
                            # Update User answer, i.e. MaRDI ID to be determined if published on portal
                            data.update({ws[1][0]:'mardi:tbd'})
                else:
                    return HttpResponse(response_temp.format(err8))
            
                # Integrate related methods in wikibase
                methods_qid=[]
                for i,method_id in enumerate(method[2]):
                    method_qid=None
                    if re.match(r"Q[0-9*]",method_id[-1]):
                        method_qid,entry=self.portal_wikidata_check(method_id,mq['mqmeg'+str(i)],wq['wqmeg'+str(i)],data)
                        if entry and method_qid:
                            methods_qid.append(method_qid)
                            #Update User answers, i.e. use MaRDI ID and name
                            data.update({ws[2][0]+'_'+str(i):'mardi:'+method_qid,ws[2][1]+'_'+str(i):entry[0]})
                        else:
                            return HttpResponse(response_temp.format(err11.format(str(i))))
                    elif method_id[0] == 'No':
                        # Check if Method Entity exists
                        if mq['mqmet']["qid2_m_"+str(i)]["value"]:
                            #Use existing Model Entity
                            methods_qid.append(mq['mqmet']["qid2_m_"+str(i)]["value"])
                            #Update User answers, i.e. use existing MaRDI ID
                            data.update({ws[2][0]+'_'+str(i):'mardi:'+methods_qid[-1]})
                        else:
                            #Create new Method Entity
                            method_ms_id=method[3][i]
                            #Get main subject of method
                            if re.match(r"Q[0-9*]",method[3][-1]):
                                method_ms_qid,entry=self.portal_wikidata_check(method[3],mq['mqmems'+str(i)],wq['wqmems'+str(i)],data)
                                if not method_ms_qid:
                                    return HttpResponse(response_temp.format(err17))
                            else:
                                return HttpResponse(response_temp.format(err17))
                            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                                #Generate Method Entry in MaRDI KG
                                methods_qid.append(self.entry(method[4][i][1],method[4][i][2],[(Item,Q4,P4),(Item,method_ms_qid,P17),
                                                                               (String,re.sub("\$","",method[4][i][4]),P18),(ExternalID,method[4][i][5],P16)]))
                                #Update User answers, i.e. include MaRDI ID of newly created method entity
                                data[ws[2][1]+'_'+str(i)] = 'mardi:'+methods_qid[-1]
                            else:
                                #Update User answers, i.e. MaRDI ID to be determined when published on portal
                                data[ws[2][1]+'_'+str(i)] = 'mardi:tbd'
                    else:
                        return HttpResponse(response_temp.format(err11.format(str(i))))

                # Integrate related softwares in wikibase
                softwares_qid=[]
                for i,software_id in enumerate(software[2]):
                    software_qid=None
                    if re.match(r"Q[0-9*]",software_id[-1]):
                        software_qid,entry=self.portal_wikidata_check(software_id,mq['mqsog'+str(i)],wq['wqsog'+str(i)],data)
                        if entry and software_qid:
                            softwares_qid.append(software_qid)
                            #Update User answers, i.e. use MaRDI ID, name and description
                            data.update({ws[3][0]+'_'+str(i):'mardi:'+software_qid,ws[3][1]+'_'+str(i):entry[0],ws[3][2]+'_'+str(i):entry[1]})
                        if not software_qid:
                            return HttpResponse(response_temp.format(err12.format(str(i))))
                    elif software_id[0] == 'No':
                        # Check if Software Entity exists
                        if mq['mqsof']["qid2_s_"+str(i)]["value"]:
                            #Use existing Model Entity
                            softwares_qid.append(mq['mqsof']["qid2_s_"+str(i)]["value"])
                            #Update User answers, i.e. use existing MaRDI ID
                            data.update({ws[3][0]+'_'+str(i):'mardi:'+softwares_qid[-1]})
                        else:
                            #Create new Software entity
                            softwares_pl_qid=[]
                            for j,software_pl in enumerate(software[3][i]):
                                software_pl_qid=None
                                software_pl_id=software_pl.split(':')
                                if re.match(r"Q[0-9*]",software_pl_id[-1]):
                                    software_pl_qid,entry=self.portal_wikidata_check(software_pl_id,mq['mqsopl'+str(i)+'_'+str(j)],wq['wqsopl'+str(i)+'_'+str(j)],data)
                                    softwares_pl_qid.append(software_pl_qid)
                                    if not software_pl_qid:
                                        return HttpResponse(response_temp.format(err16))
                                else:
                                    return HttpResponse(response_temp.format(err16))
                            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                                #Generate Method Entry in MaRDI KG
                                softwares_qid.append(self.entry(software[4][i][1],software[4][i][2],[(Item,Q5,P4)]+
                                                                                [(Item,plang,P19) for plang in softwares_pl_qid]+
                                                                                [(ExternalID,re.split(':',software[4][i][4])[-1],P16 if re.split(':',software[4][i][4])[0] == 'doi' else P20)]))        
                                #Update User answers, i.e. include MaRDI ID of newly created software entity
                                data.update({ws[3][0]+'_'+str(i):'mardi:'+softwares_qid[-1]})
                            else:
                                #Update User answers, i.e. MaRDI ID to be determined when published on portal
                                data.update({ws[3][0]+'_'+str(i):'mardi:tbd'})
                    else:
                        return HttpResponse(response_temp.format(err12.format(str(i))))

                # Integrate related inputs in wikibase
                inputs_qid=[]
                for i,input_id in enumerate(inputs[2]):
                    input_qid=None
                    if re.match(r"Q[0-9*]",input_id[-1]):
                        input_qid,entry=self.portal_wikidata_check(input_id,mq['mqing'+str(i)],wq['wqing'+str(i)],data)
                        if entry and input_qid:
                            inputs_qid.append(input_qid)
                            #Update User answers, i.e. use MaRDI ID name 
                            data.update({ws[6][0]+'_'+str(i):'mardi:'+input_qid,ws[6][1]+'_'+str(i):entry[0]})
                        else:
                            return HttpResponse(response_temp.format(err13.format(str(i))))
                    elif input_id[0] == 'No':
                        # Check if Input Data Entity exists
                        if mq['mqinp']["qid2_in_"+str(i)]["value"]:
                            #Use existing Input Data Entity
                            inputs_qid.append(mq['mqinp']["qid2_in_"+str(i)]["value"])
                            #Update User answers, i.e. use existing MaRDI ID
                            data.update({ws[6][0]+'_'+str(i):'mardi:'+inputs_qid[-1]})
                        else:
                            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                                #Generate Input Entry in MaRDI KG
                                inputs_qid.append(self.entry(inputs[3][i][1],'data set',[(Item,Q6,P4),(ExternalID,re.split(':',inputs[3][i][2])[-1],P16)]))
                                #Update User answers, i.e. include MaRDI ID of newly created input entity
                                data.update({ws[6][0]+'_'+str(i):'mardi:'+inputs_qid[-1]})
                            else:
                                #Update User answers, i.e. MaRDI ID to be determined once published on portal
                                data.update({ws[6][0]+'_'+str(i):'mardi:tbd'})
                    else:
                        return HttpResponse(response_temp.format(err13.format(str(i))))
            
                # Integrate related outputs in wikibase
                outputs_qid=[]
                for i,output_id in enumerate(outputs[2]):
                    output_qid=None
                    if re.match(r"Q[0-9*]",output_id[-1]):
                        output_qid,entry=self.portal_wikidata_check(output_id,mq['mqoug'+str(i)],wq['wqoug'+str(i)],data)
                        if entry and output_qid:
                            outputs_qid.append(output_qid)
                            #Update User answers, i.e. use MaRDI ID and name 
                            data.update({ws[7][0]+'_'+str(i):'mardi:'+output_qid,ws[7][1]+'_'+str(i):entry[0]})
                        else:
                            return HttpResponse(response_temp.format(err14.format(str(i))))
                    elif output_id[0] == 'No':
                        # Check if Input Data Entity exists
                        if mq['mqout']["qid2_ou_"+str(i)]["value"]:
                            #Use existing Output Data Entity
                            outputs_qid.append(mq['mqout']["qid2_ou_"+str(i)]["value"])
                            #Update User answers, i.e. use existing MaRDI ID
                            data.update({ws[7][0]+'_'+str(i):'mardi:'+outputs_qid[-1]})
                        else:
                            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                                #Generate Input Entry in MaRDI KG
                                outputs_qid.append(self.entry(outputs[3][i][1],'data set',[(Item,Q6,P4),(ExternalID,re.split(':',outputs[3][i][2])[-1],P16)]))          
                                #Update User answers, i.e. include MaRDI ID of newly created output entity
                                data.update({ws[7][0]+'_'+str(i):'mardi:'+outputs_qid[-1]})
                            else:
                                #Update User answers, i.e. MaRDI ID to be determined once published on portal
                                data.update({ws[7][0]+'_'+str(i):'mardi:tbd'})
                    else:
                        return HttpResponse(response_temp.format(err14.format(str(i))))
            
                #Integrate involved disciplines in wikidata
                disciplines_qid=[]
                for i,discipline_id in enumerate(disciplines[1]):
                    if re.match(r"Q[0-9*]",discipline_id[-1]):
                        discipline_qid,entry=self.portal_wikidata_check(discipline_id,mq['mqdig'+str(i)],wq['wqdig'+str(i)],data)
                        if entry and discipline_qid:
                            disciplines_qid.append(discipline_qid)
                            #Update User answers, i.e. use entity label instead of ID for wiki page
                            if i == 0:
                                data.update({ws[4][0]:entry[0]})
                            else:
                                data.update({ws[4][0]:'; '.join([data[ws[4][0]],entry[0]])}) 
                        else:
                            return HttpResponse(response_temp.format(err15))
                    else:
                        return HttpResponse(response_temp.format(err15))
         
                if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                    workflow_qid=self.entry(self.project.title, res_obj,[(Item,Q2,P4),(Item,paper_qid,P3)]+
                                                                             [(Item,discipline,P5) for discipline in disciplines_qid]+
                                                                             [(Item,mmsi,P6) for mmsi in [model_qid]+methods_qid+softwares_qid+inputs_qid+outputs_qid])
            
            # Fill out MaRDI template
            for entry in data.items():
                temp=re.sub(";","<br/>",re.sub("Yes: |'","",re.sub(entry[0],repr(entry[1]),temp)))
            if data[dec[2][0]] == dec[2][1]: 
                # Download as Markdown
                response = HttpResponse(temp, content_type="application/md")
                response['Content-Disposition'] = 'filename="workflow.md"'
                return response
            elif data[dec[2][0]] == dec[2][2] and data[dec[3][0]] not in (dec[3][1],dec[3][2]):
                # Preview Markdown as HTML
                return HttpResponse(html_front+pypandoc.convert_text(temp,'html',format='md')+html_end)
            # Export to MaRDI Portal
            elif data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                # Export Workflow Documentation to mediawiki portal
                if lgname and lgpassword:
                    self.wikipage_export(self.project.title,re.sub('{\|','{| class="wikitable"',pypandoc.convert_text(temp,'mediawiki',format='md')))
                else:
                    return HttpResponse(response_temp.format(err19))

                return HttpResponse(done.format(export))

            # Not chosen
            else:
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
            return '; '.join([self.stringify(value.value_and_unit) for value in values])
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

        for char in range(len(post_content)//500+1):
            # Step 4: POST request to edit a page
            PARAMS_3 = {
                "action": "edit",
                "title": title,
                "token": CSRF_TOKEN,
                "format": "json",
                "appendtext": post_content[2000*char:2000*(char+1)]
            }
            R = S.post(URL, data=PARAMS_3)
            time.sleep(2)

#        PARAMS_3 = {
#            "action": "edit",
#            "title": title,
#            "token": CSRF_TOKEN,
#            "format": "json",
#            "appendtext": post_content
#            }

        R = S.post(URL , data=PARAMS_3)
        return

    def wikibase_answers(self, data, wiki):
        '''Takes data and extracts answers relevant for Wiki'''
        wiki_answers=[]
        for question in wiki:
            data_filter = dict(filter(lambda item: question in item[0], data.items()))
            wiki_answers.extend(list(data_filter.values()))
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
    
    def portal_wikidata_check(self,Id,mquery,wquery,data):
        '''Function checks if an entry is on MaRDI portal and returns its QID
           or on Wikidata and copies the entry to the MaRDI portal and returns
           its QID.'''
        if mquery["label"]["value"]:
            #If on Portal store QID
            qid = Id[1]
            entry = [mquery["label"]["value"],mquery["quote"]["value"]]
        elif wquery["label"]["value"]:
            entry = [wquery["label"]["value"],wquery["quote"]["value"]]
            if mquery["qid"]["value"]:
                qid = mquery["qid"]["value"]
            else:
                #Create dummy entry and store QID if portal publication ist desired
                if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                    #Create dummy entry and store QID
                    qid = self.entry(wquery["label"]["value"],wquery["quote"]["value"],[(ExternalID,Id[-1],P2)])
                else:
                    qid = 'mardi:tbd'
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

    def sparql(self,data,orcid,doi,cit,ws):
        '''This function takes user answers and performs SPARQL queries to Wikidata and MaRDI portal.'''
        
        #Get User Answers

        #Model
        model=[]
        model.append(self.wikibase_answers(data,ws[1]))
        model.append(re.split(':',model[0][0].removeprefix("Yes: ")))
        model.append(model[0][3].split(':'))
        #Method
        method=[]
        method.append(self.wikibase_answers(data,ws[2]))
        method.append(len(method[0])//6)
        method.append([re.split(':',method[0][i].removeprefix("Yes: ")) for i in range(method[1])])
        method.append([method[0][i].split(':')  for i in range(method[1]*3,method[1]*4)])
        method.append([method[0][i::method[1]] for i in range(method[1])])
        #Software
        software=[]
        software.append(self.wikibase_answers(data,ws[3]))
        software.append(len(software[0])//5)
        software.append([re.split(':',software[0][i].removeprefix("Yes: ")) for i in range(software[1])])
        software.append([software[0][i].split('; ')  for i in range(software[1]*3,software[1]*4)])
        software.append([software[0][i::software[1]] for i in range(software[1])])
        #Inputs
        inputs=[]
        inputs.append(self.wikibase_answers(data,ws[6]))
        inputs.append(len(inputs[0])//3)
        inputs.append([re.split(':',inputs[0][i].removeprefix("Yes: ")) for i in range(inputs[1])])
        inputs.append([inputs[0][i::inputs[1]] for i in range(inputs[1])])
        #Outputs
        outputs=[]
        outputs.append(self.wikibase_answers(data,ws[7]))
        outputs.append(len(outputs[0])//3)
        outputs.append([re.split(':',outputs[0][i].removeprefix("Yes: ")) for i in range(outputs[1])])
        outputs.append([outputs[0][i::outputs[1]] for i in range(outputs[1])])
        #Disciplines
        disciplines=[]
        disciplines.append(self.wikibase_answers(data,ws[4])[0].split('; '))
        disciplines.append([re.split(':',discipline) for discipline in disciplines[0]])
        
        #Create appropriate SPARQL Keys
        
        keys=dict(Keys)
        for inds in zip([orcid,method[2],software[2],inputs[2],outputs[2],disciplines[1]],['pub','met','sof','inp','out','dis']):
            for i,_ in enumerate(inds[0]):
                if type(keys_flex['wq'+inds[1]]) == str:
                    keys['wq'+inds[1]]+=keys_flex['wq'+inds[1]].format(i)
                    keys['mq'+inds[1]]+=keys_flex['mq'+inds[1]].format(i)
                else:
                    keys['wq'+inds[1]]+=keys_flex['wq'+inds[1]][0].format(i)
                    keys['mq'+inds[1]]+=keys_flex['mq'+inds[1]][0].format(i)
                    for j,_ in enumerate(software[3][i]):
                        keys['wq'+inds[1]]+=keys_flex['wq'+inds[1]][1].format(i,j)
                        keys['mq'+inds[1]]+=keys_flex['mq'+inds[1]][1].format(i,j)
        

        #SPARQL Queries to Wikidata and MaRDI Knowledge Graph

        wq = {}
        mq = {}

        qw = {'wqpub' : wini.format(keys['wqpub'],wbpub.format(doi[-1].upper(),cit['journal'].lower(),lang_dict[cit['language']],
                                    cit['language'],cit['title'],''.join([''.join(wbaut.format(i,aut[1])) for i,aut in enumerate(orcid)]))),

              'wqmod' : wini.format(keys['wqmod'],wbmod.format(model[1][1] if model[1][0] == 'wikidata' else '',model[2][1] if model[2][0] == 'wikidata' else '')),

              'wqmet' : wini.format(keys['wqmet'],''.join([''.join(wbmet.format(i,Id[1] if Id[0] == 'wikidata' else '',method[3][i][1] if method[3][i][0] == 'wikidata' 
                                    else '')) for i,Id in enumerate(method[2])])),

              'wqsof' : wini.format(keys['wqsof'],''.join([''.join(wbsof.format(i,Id[1] if Id[0] == 'wikidata' else '',''.join([''.join(wbpla.format(i,j,ID.split(':')[1]
                                    if ID.split(':')[0] == 'wikidata' else '')) for j,ID in enumerate(software[3][i])]))) for i,Id in enumerate(software[2])])),

              'wqinp' : wini.format(keys['wqinp'],''.join([''.join(wbinp.format(i,Id[1] if Id[0] == 'wikidata' else '')) for i,Id in enumerate(inputs[2])])),

              'wqout' : wini.format(keys['wqout'],''.join([''.join(wbout.format(i,Id[1] if Id[0] == 'wikidata' else '')) for i,Id in enumerate(outputs[2])])),

              'wqdis' : wini.format(keys['wqdis'],''.join([''.join(wbdis.format(i,Id[1] if Id[0] == 'wikidata' else '')) for i,Id in enumerate(disciplines[1])]))}


        for ind in ['pub','mod','met','sof','inp','out','dis']:
            wq.update({'wq'+ind:{**dict.fromkeys(keys['wq'+ind].split(' ?'),{"value":''}),**self.get_results(wikidata_endpoint,qw['wq'+ind])[0]}})

        qm = {'mqpub' : mini.format(keys['mqpub'],mbpub.format(doi[-1].upper(),wq['wqpub']["label_doi"]["value"],wq['wqpub']["quote_doi"]["value"],cit['journal'].lower(),
                                    wq['wqpub']["label_jou"]["value"],wq['wqpub']["quote_jou"]["value"],lang_dict[cit['language']],cit['language'],
                                    wq['wqpub']["label_lan"]["value"],wq['wqpub']["quote_lan"]["value"],cit['title'],''.join([''.join(mbaut.format(i,aut[1],
                                    wq['wqpub']['label_'+str(i)]['value'],wq['wqpub']['quote_'+str(i)]['value'],aut[0])) for i,aut in enumerate(orcid)]))),
             
              'mqmod' : mini.format(keys['mqmod'],mbmod.format(model[1][1] if model[1][0] == 'mardi' else '',wq['wqmod']["label_model"]["value"], 
                                    wq['wqmod']["quote_model"]["value"],model[0][1],model[0][2],model[2][1] if model[2][0] == 'mardi' else '', 
                                    wq['wqmod']["label_ms"]["value"],wq['wqmod']["quote_ms"]["value"])),

              'mqmet' : mini.format(keys['mqmet'],''.join([''.join(mbmet.format(i,Id[1] if Id[0] == 'mardi' else '',wq['wqmet']['label_m_'+str(i)]['value'],
                                    wq['wqmet']['quote_m_'+str(i)]['value'],method[0][i::method[1]][1],method[0][i::method[1]][2],method[3][i][1] if method[3][i][0] == 
                                    'mardi' else '',wq['wqmet']["label_ms_"+str(i)]["value"],wq['wqmet']["quote_ms_"+str(i)]["value"])) for i,Id in enumerate(method[2])])),

              'mqsof' : mini.format(keys['mqsof'],''.join([''.join(mbsof.format(i,Id[1] if Id[0] == 'mardi' else '',wq['wqsof']['label_s_'+str(i)]['value'],
                                    wq['wqsof']['quote_s_'+str(i)]['value'],software[0][i::software[1]][1],software[0][i::software[1]][2],''.join([''.join(mbpla.format(i,j,
                                    ID.split(':')[1] if ID.split(':')[0] == 'mardi' else '',wq['wqsof']['label_pl_'+str(i)+'_'+str(j)]['value'],
                                    wq['wqsof']['quote_pl_'+str(i)+'_'+str(j)]['value'])) for j,ID in enumerate(software[3][i])]))) for i,Id in enumerate(software[2])])),

              'mqinp' : mini.format(keys['mqinp'],''.join([''.join(mbinp.format(i,Id[1] if Id[0] == 'mardi' else '',wq['wqinp']['label_in_'+str(i)]['value'],
                                    wq['wqinp']['quote_in_'+str(i)]['value'],inputs[0][i::inputs[1]][1],'data set')) for i,Id in enumerate(inputs[2])])),

              'mqout' : mini.format(keys['mqout'],''.join([''.join(mbout.format(i,Id[1] if Id[0] == 'mardi' else '',wq['wqout']['label_ou_'+str(i)]['value'],
                                    wq['wqout']['quote_ou_'+str(i)]['value'],outputs[0][i::outputs[1]][1],'data set')) for i,Id in enumerate(outputs[2])])),

              'mqdis' : mini.format(keys['mqdis'],''.join([''.join(mbdis.format(i,Id[1] if Id[0] == 'mardi' else '',wq['wqdis']['label_di_'+str(i)]['value'],
                                    wq['wqdis']['quote_di_'+str(i)]['value'])) for i,Id in enumerate(disciplines[1])]))}

        for ind in ['pub','mod','met','sof','inp','out','dis']:
            mq.update({'mq'+ind:{**dict.fromkeys(keys['mq'+ind].split(' ?'),{"value":''}),**self.get_results(mardi_endpoint,qm['mq'+ind])[0]}})
        
        #Extract specific SPARQL resulta
        
        EXT = [['aut','pub','_',orcid],
               ['lan','pub','_lan'],
               ['jou','pub','_jou'],
               ['mog','mod','_model'],
               ['moms','mod','_ms'],
               ['meg','met','_m_',method[2]],
               ['mems','met','_ms_',method[2]],
               ['sog','sof','_s_',software[2]],
               ['sopl','sof','_pl_',software[2],software[3]],
               ['ing','inp','_in_',inputs[2]],
               ['oug','out','_ou_',outputs[2]],
               ['dig','dis','_di_',disciplines[1]]]

        for ext in EXT:
            if len(ext) == 3:
                wq.update({'wq'+ext[0]:{key.split('_')[0]: value for (key, value) in wq['wq'+ext[1]].items() if ext[2] in key}})
                mq.update({'mq'+ext[0]:{key.split('_')[0]: value for (key, value) in mq['mq'+ext[1]].items() if ext[2] in key}})
            elif len(ext) == 4:
                for i,_ in enumerate(ext[3]):
                    wq.update({'wq'+ext[0]+str(i):{key.split('_')[0]: value for (key, value) in wq['wq'+ext[1]].items() if ext[2]+str(i) in key}})
                    mq.update({'mq'+ext[0]+str(i):{key.split('_')[0]: value for (key, value) in mq['mq'+ext[1]].items() if ext[2]+str(i) in key}})
            else:
                for i,_ in enumerate(ext[3]):
                    for j,_ in enumerate(ext[4]):
                        wq.update({'wq'+ext[0]+str(i)+'_'+str(j):{key.split('_')[0]: value for (key, value) in wq['wq'+ext[1]].items() if ext[2]+str(i)+'_'+str(j) in key}})
                        mq.update({'mq'+ext[0]+str(i)+'_'+str(j):{key.split('_')[0]: value for (key, value) in mq['mq'+ext[1]].items() if ext[2]+str(i)+'_'+str(j) in key}})

        return model, method, software, inputs, outputs, disciplines, wq, mq



