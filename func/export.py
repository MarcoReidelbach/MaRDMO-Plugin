from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.conf import settings
from rdmo.projects.exports import Export
from rdmo.questions.models import Question
from rdmo.core.utils import render_to_csv
from django.shortcuts import render

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
            temp=self.dyn_template(data)
            if len(temp) == 0:
                return HttpResponse(response_temp.format(err5))
                                
            #Get Research Objective 
            wiki_res_obj=self.wikibase_answers(data,ws6)[0]
            
            #Check if Workflow with same label/description already on portal, stop if portal integration is desired
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                if self.entry_check(self.project.title,wiki_res_obj):
                    return HttpResponse(response_temp.format(err18))
            
            # Get Article information from mardi/wikidata/orcid, only necessary if portal integration is desired
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                paper=self.wikibase_answers(data,paper_doi)
                if paper[0]!= 'No':
                    #Get DOI
                    doi=re.split(':',paper[0])[-1]
                    #Check if Paper already on MaRDI Portal
                    mardi_paper_qid=self.get_results(mardi_endpoint,doi_query[0].format(doi.upper()))
                    if mardi_paper_qid:
               	        #If on Portal store QID
                        paper_qid=mardi_paper_qid[0]["qid"]["value"]
                    else:
                        #If not on Portal, check if Paper on wikidata
                        wikidata_paper_entry=self.get_results(wikidata_endpoint,doi_query[1].format(doi.upper()))
                        if wikidata_paper_entry:
                            #Check if Entity with same label and description exists on MaRDI Portal
                            paper_entry_check=self.entry_check(wikidata_paper_entry[0]["label"]["value"],wikidata_paper_entry[0]["quote"]["value"])
                            if paper_entry_check:
                                #If Entity exists store QID.
                                paper_qid=paper_entry_check[0]["qid"]["value"]
                            else:
                                #If only on wikidata, generate dummy entry and store QID. 
                                paper_qid=self.entry(wikidata_paper_entry[0]["label"]["value"],wikidata_paper_entry[0]["quote"]["value"],[(ExternalID,wikidata_paper_entry[0]["qid"]["value"],wikidata_qid)])   
                        else:
                            #If not on Portal / Wikidata get Paper via DOI
                            author_with_orcid,author_without_orcid,citation_dict=GetCitation(doi)
                            if not citation_dict:
                                return HttpResponse(response_temp.format(err6))
                            #Check if title from paper on MaRDI Portal
                            if citation_dict['title']:
                                mardi_title_qid=self.get_results(mardi_endpoint,title_query[0].format(citation_dict['title']))
                                if mardi_title_qid:
                                    #If on Portal store QID
                                    paper_qid=mardi_title_qid[0]["qid"]["value"]
                                else:
                                    #If not on Portal, check if title on Wikidata
                                    wikidata_title_entry=self.get_results(wikidata_endpoint,title_query[1].format(citation_dict['title']))
                                    if wikidata_title_entry:
                                        title_entry_check=self.entry_check(wikidata_title_entry[0]["label"]["value"],wikidata_title_entry[0]["quote"]["value"])
                                        if title_entry_check:
                                            #If on Portal, store QID.
                                            paper_qid=title_entry_check[0]["qid"]["value"]
                                        else:
                                            #If only on wikidata, generate dummy entry, store QID.
                                            paper_qid=self.entry(wikidata_title_entry[0]["label"]["value"],wikidata_title_entry[0]["quote"]["value"],[(ExternalID,wikidata_title_entry[0]["qid"]["value"],wikidata_qid)])
                                    else:
                                        #If not on Portal / Wikidata create journal entry
                                        entry_check=self.entry_check(citation_dict['title'],'publication')
                                        if entry_check:
                                            #If on Portal, store QID.
                                            paper_qid=entry_check[0]["qid"]["value"]
                                        else:
                                            author_qids=[]
                                            for author in author_with_orcid:
                                                #Create author entry for publication 
                                                author_qids.append(self.paper_prop_entry([query.format(author[1]) for query in author_query],
                                                                                          author[0],
                                                                                          ['researcher',[(Item,human,instance_of),(Item,researcher,occupation),(ExternalID,author[1],ORCID_iD)]]))
                                    
                                            if citation_dict['language']:
                                                #Create language entry publication
                                                citation_dict['language']=self.paper_prop_entry([query.format(lang_dict[citation_dict['language']],citation_dict['language']) for query in language_query],
                                                                                                 lang_dict[citation_dict['language']],
                                                                                                 ['language',[(Item,language,instance_of)]])
                                       
                                            if citation_dict['journal']:
                                                #Create journal entry for publication                                                     
                                                citation_dict['journal']=self.paper_prop_entry([query.format(citation_dict['journal'].lower()) for query in journal_query],
                                                                                                citation_dict['journal'],
                                                                                                ['scientific journal',[(Item,scientific_journal,instance_of)]])

                                            #Create publication entry
                                            paper_qid=self.entry(citation_dict['title'],'publication',[(Item,scholarly_article if citation_dict['ENTRYTYPE'] == 'article' else publication,instance_of)]+
                                                                 [(Item,aut,Author) for aut in author_qids]+[(String,aut,author_name_string) for aut in author_without_orcid]+
                                                                 [(Item,citation_dict['language'],language_of_work_or_name),(Item,citation_dict['journal'],published_in),
                                                                  (MonolingualText,citation_dict['title'],title),(Time,citation_dict['pub_date']+'T00:00:00Z',publication_date),
                                                                  (String,citation_dict['volume'],volume),(String,citation_dict['number'],issue),(String,citation_dict['pages'],pages),
                                                                  (ExternalID,citation_dict['doi'],DOI)])  
                else:
                    paper_qid=[]

            # Integrate related model in wikibase
            model=self.wikibase_answers(data,ws2)
            model_id=re.split(':',model[0].removeprefix("Yes: "))
            if re.match(r"Q[0-9*]",model_id[-1]):
                model_qid,entry=self.portal_wikidata_check(model_id,model_query,data)
                if entry and model_qid:
                    #Updata User answers, i.e. use MaRDI ID, name and description
                    data[ws2[0]] = 'mardi:'+model_qid
                    data[ws2[1]] = entry[0]["label"]["value"]
                    data[ws2[2]] = entry[0]["quote"]["value"]
                else:
                    return HttpResponse(response_temp.format(err7))
            elif model_id[0] == 'No':
                # Check if Model Entity exists
                model_entry_check=self.entry_check(model[1],model[2])
                if model_entry_check:
                    #Use existing Model Entity
                    model_qid=model_entry_check[0]["qid"]["value"]
                    # Update User answer, i.e. use existing MaRDI ID
                    data[ws2[0]] = 'mardi:'+model_qid
                else:
                    #Create new Model Entity
                    main_subject_id=model[3].split(':')
                    #Get main subject of model
                    print(main_subject_id)
                    if re.match(r"Q[0-9*]",main_subject_id[-1]):
                        main_subject_qid,entry=self.portal_wikidata_check(main_subject_id,main_subject_query,data)
                        print(main_subject_qid,entry)
                        if not main_subject_qid:
                            return HttpResponse(response_temp.format(err9))
                    else:
                        return HttpResponse(response_temp.format(err9))
                    
                    if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                        # Generate Model Entry in MaRDI KG 
                        model_qid=self.entry(model[1],model[2],[(Item,mathematical_model,instance_of),(Item,main_subject_qid,main_subject)]+
                                                               [(String,re.sub("\$","",form.lstrip()),defining_formula) for form in re.split(';',model[4])]+
                                                               [(ExternalID,model[5],DOI)])
                        # Update User answer, i.e. include ID of newly created Model entity
                        data[ws2[0]] = 'mardi:'+model_qid
                    else:
                        # Update User answer, i.e. MaRDI ID to be determined if published on portal
                        data[ws2[0]] = 'mardi:tbd'
            else:
                return HttpResponse(response_temp.format(err8))
            
            # Integrate related methods in wikibase
            methods=self.wikibase_answers(data,ws3)
            methods_qid=[]
            no_methods=len(methods)//6
            for i in range(no_methods):
                method_qid=None
                meth=methods[i::no_methods]
                method_id=re.split(':',meth[0].removeprefix("Yes: "))
                if re.match(r"Q[0-9*]",method_id[-1]):
                    method_qid,entry=self.portal_wikidata_check(method_id,method_query,data)
                    if entry and method_qid:
                        methods_qid.append(method_qid)
                        #Update User answers, i.e. use MaRDI ID and name
                        data[ws3[0]+'_'+str(i)] = 'mardi:'+method_qid
                        data[ws3[1]+'_'+str(i)] = entry[0]["label"]["value"]
                    else:
                        return HttpResponse(response_temp.format(err11.format(str(i))))
                elif method_id[0] == 'No':
                    # Check if Method Entity exists
                    method_entry_check=self.entry_check(meth[1],meth[2])
                    if method_entry_check:
                        #Use existing Model Entity
                        methods_qid.append(method_entry_check[0]["qid"]["value"])
                        #Update User answers, i.e. use existing MaRDI ID
                        data[ws3[0]+'_'+str(i)] = 'mardi:'+methods_qid[-1]
                    else:
                        #Create new Method Entity
                        main_subject_id=meth[3].split(':')
                        #Get main subject of method
                        if re.match(r"Q[0-9*]",main_subject_id[-1]):
                            main_subject_qid=self.portal_wikidata_check(main_subject_id,main_subject_query,data)
                            if not main_subject_qid:
                                return HttpResponse(response_temp.format(err17))
                        else:
                            return render(self.request,'error18.html')
                        if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                            #Generate Method Entry in MaRDI KG
                            methods_qid.append(self.entry(meth[1],meth[2],[(Item,method,instance_of),(Item,main_subject_qid,main_subject),
                                                                           (String,re.sub("\$","",meth[4]),defining_formula),(ExternalID,meth[5],DOI)]))
                            #Update User answers, i.e. include MaRDI ID of newly created method entity
                            data[ws3[1]+'_'+str(i)] = 'mardi:'+methods_qid[-1]
                        else:
                            #Update User answers, i.e. MaRDI ID to be determined when published on portal
                            data[ws3[1]+'_'+str(i)] = 'mardi:tbd'
                else:
                    return HttpResponse(response_temp.format(err11.format(str(i))))

            # Integrate related softwares in wikibase
            softwares=self.wikibase_answers(data,ws4)
            softwares_qid=[]
            no_softwares=len(softwares)//5
            for i in range(no_softwares):
                software_qid=None
                soft=softwares[i::no_softwares]
                software_id=re.split(':',soft[0].removeprefix("Yes: "))
                if re.match(r"Q[0-9*]",software_id[-1]):
                    software_qid,entry=self.portal_wikidata_check(software_id,software_query,data)
                    if entry and software_qid:
                        softwares_qid.append(software_qid)
                        #Update User answers, i.e. use MaRDI ID, name and description
                        data[ws4[0]+'_'+str(i)] = 'mardi:'+software_qid
                        data[ws4[1]+'_'+str(i)] = entry[0]["label"]["value"]
                        data[ws4[2]+'_'+str(i)] = entry[0]["quote"]["value"]
                    if not software_qid:
                        return HttpResponse(response_temp.format(err12.format(str(i))))
                elif software_id[0] == 'No':
                    # Check if Software Entity exists
                    software_entry_check=self.entry_check(soft[1],soft[2])
                    if software_entry_check:
                        #Use existing Model Entity
                        softwares_qid.append(software_entry_check[0]["qid"]["value"])
                        #Update User answers, i.e. use existing MaRDI ID
                        data[ws4[0]+'_'+str(i)] = 'mardi:'+softwares_qid[-1]
                    else:
                        #Get involved programming languages in software
                        wiki_planguages=soft[3].split('; ')
                        planguages_qid=[]
                        for planguage in wiki_planguages:
                            planguage_qid=None
                            planguage_id=re.search('\((.+?)\)',planguage).group(1).split(':')
                            if re.match(r"Q[0-9*]",planguage_id[-1]):
                                planguage_qid,entry=self.portal_wikidata_check(planguage_id,planguage_query,data)
                                planguages_qid.append(planguage_qid)
                                if not planguage_qid:
                                    return HttpResponse(response_temp.format(err16))
                            else:
                                return render(self.request,'error16.html')
                        if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                            #Generate Method Entry in MaRDI KG
                            softwares_qid.append(self.entry(soft[1],soft[2],[(Item,software,instance_of)]+
                                                                            [(Item,plang,programmed_in) for plang in planguages_qid]+
                                                                            [(ExternalID,re.split(':',soft[4])[-1],DOI if re.split(':',soft[4])[0] == 'doi' else swMath_work_ID)]))        
                            #Update User answers, i.e. include MaRDI ID of newly created software entity
                            data[ws4[0]+'_'+str(i)] = 'mardi:'+softwares_qid[-1]
                        else:
                            #Update User answers, i.e. MaRDI ID to be determined when published on portal
                            data[ws4[0]+'_'+str(i)] = 'mardi:tbd'
                else:
                    return HttpResponse(response_temp.format(err12.format(str(i))))

            # Integrate related inputs in wikibase
            inputs=self.wikibase_answers(data,ws7)
            inputs_qid=[]
            no_inputs=len(inputs)//3
            for i in range(no_inputs):
                input_qid=None
                inp=inputs[i::no_inputs]
                input_id=re.split(':',inp[0].removeprefix("Yes: "))
                if re.match(r"Q[0-9*]",input_id[-1]):
                    input_qid,entry=self.portal_wikidata_check(input_id,input_query,data)
                    if entry and input_qid:
                        inputs_qid.append(input_qid)
                        #Update User answers, i.e. use MaRDI ID name 
                        data[ws7[0]+'_'+str(i)] = 'mardi:'+input_qid
                        data[ws7[1]+'_'+str(i)] = entry[0]["label"]["value"]
                    else:
                        return HttpResponse(response_temp.format(err13.format(str(i))))
                elif input_id[0] == 'No':
                    # Check if Input Data Entity exists
                    input_entry_check=self.entry_check(inp[1],'data set')
                    if input_entry_check:
                        #Use existing Input Data Entity
                        inputs_qid.append(input_entry_check[0]["qid"]["value"])
                        #Update User answers, i.e. use existing MaRDI ID
                        data[ws7[0]+'_'+str(i)] = 'mardi:'+inputs_qid[-1]
                    else:
                        if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                            #Generate Input Entry in MaRDI KG
                            inputs_qid.append(self.entry(inp[1],'data set',[(ExternalID,re.split(':',inp[2])[-1],DOI)]))
                            #Update User answers, i.e. include MaRDI ID of newly created input entity
                            data[ws7[0]+'_'+str(i)] = 'mardi:'+inputs_qid[-1]
                        else:
                            #Update User answers, i.e. MaRDI ID to be determined once published on portal
                            data[ws7[0]+'_'+str(i)] = 'mardi:tbd'
                else:
                    return HttpResponse(response_temp.format(err13.format(str(i))))
               
            # Integrate related outputs in wikibase
            outputs=self.wikibase_answers(data,ws7a)
            outputs_qid=[]
            no_outputs=len(outputs)//3
            for i in range(no_outputs):
                output_qid=None
                out=outputs[i::no_outputs]
                output_id=re.split(':',out[0].removeprefix("Yes: "))
                if re.match(r"Q[0-9*]",output_id[-1]):
                    output_qid,entry=self.portal_wikidata_check(output_id,output_query,data)
                    if entry and output_qid:
                        outputs_qid.append(output_qid)
                        #Update User answers, i.e. use MaRDI ID and name 
                        data[ws7a[0]+'_'+str(i)] = 'mardi:'+output_qid
                        data[ws7a[1]+'_'+str(i)] = entry[0]["label"]["value"]
                    else:
                        return HttpResponse(response_temp.format(err14.format(str(i))))
                elif output_id[0] == 'No':
                    # Check if Input Data Entity exists
                    output_entry_check=self.entry_check(out[1],'data set')
                    if output_entry_check:
                        #Use existing Output Data Entity
                        outputs_qid.append(output_entry_check[0]["qid"]["value"])
                        #Update User answers, i.e. use existing MaRDI ID
                        data[ws7a[0]+'_'+str(i)] = 'mardi:'+outputs_qid[-1]
                    else:
                        if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                            #Generate Input Entry in MaRDI KG
                            outputs_qid.append(self.entry(out[1],'data set',[(ExternalID,re.split(':',out[2])[-1],DOI)]))          
                            #Update User answers, i.e. include MaRDI ID of newly created output entity
                            data[ws7a[0]+'_'+str(i)] = 'mardi:'+outputs_qid[-1]
                        else:
                            #Update User answers, i.e. MaRDI ID to be determined once published on portal
                            data[ws7a[0]+'_'+str(i)] = 'mardi:tbd'
                else:
                    return HttpResponse(response_temp.format(err14.format(str(i))))

            #Integrate involved disciplines in wikidata
            wiki_disciplines=self.wikibase_answers(data,ws5)[0].split('; ')
            disciplines_qid=[]
            for n,discipline in enumerate(wiki_disciplines):
                discipline_id=re.split(':',discipline)
                if re.match(r"Q[0-9*]",discipline_id[-1]):
                    discipline_qid,entry=self.portal_wikidata_check(discipline_id,discipline_query,data)
                    if entry and discipline_qid:
                        disciplines_qid.append(discipline_qid)
                        #Update User answers, i.e. use entity label instead of ID for wiki page
                        if n == 0:
                            data[ws5[0]] = entry[0]["label"]["value"]
                        else:
                            data[ws5[0]] = '; '.join([data[ws5[0]],entry[0]["label"]["value"]]) 
                    else:
                        return HttpResponse(response_temp.format(err15))
                else:
                    return HttpResponse(response_temp.format(err15))
            
            if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]):
                workflow_qid=self.entry(self.project.title, wiki_res_obj,[(Item,research_workflow,instance_of),(Item,paper_qid,cites_work)]+
                                                                         [(Item,discipline,field_of_work) for discipline in disciplines_qid]+
                                                                         [(Item,mmsi,uses) for mmsi in [model_qid]+methods_qid+softwares_qid+inputs_qid+outputs_qid])

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

                return HttpResponse(response_temp.format(export))

            # Not chosen
            else:
                return HttpResponse(response_temp.format(err2))

        # Workflow Search
        elif data[dec[0][0]] in (dec[0][3],dec[0][4]):
            #QID and String Entities to search for
            search_objs=self.wikibase_answers(data,ws8)
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
                        ITEMFINDER2=ITEMFINDER2+"?y wdt:P"+uses+" "+ent+";\n"
                    else:
                        ITEMFINDER2=ITEMFINDER2+"wdt:P"+uses+" "+ent+";\n"
                ITEMFINDER2=ITEMFINDER2+"wdt:P"+instance_of+" wd:"+research_workflow+".\n"

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
                        ITEMFINDER2=ITEMFINDER2+"?y wdt:P"+field_of_work+" "+ent+";\n"
                    else:
                        ITEMFINDER2=ITEMFINDER2+"wdt:P"+field_of_work+" "+ent+";\n"
                ITEMFINDER2=ITEMFINDER2+"wdt:P"+instance_of+" wd:"+research_workflow+".\n"

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
        req=requests.get(endpoint_url, params = {'format': 'json', 'query': query}).json()
        return req["results"]["bindings"]

    def entry_check(self,label,description):
        '''Check if wikibase entry with certain label and description exists.'''
        return self.get_results(mardi_endpoint,re.sub('LABEL',label,re.sub('DESCRIPTION',description,check_query)))
    
    def portal_wikidata_check(self,Id,query,data):
        '''Function checks if an entry is on MaRDI portal and returns its QID 
           or on Wikidata and copies the entry to the MaRDI portal and returns
           its QID.'''    
        if Id[0] == 'mardi':
            #Check if MaRDI QID exists
            entry = self.get_results(mardi_endpoint,query[0].format(Id[1]))
            if entry:
                #If on Portal store QID
                qid = Id[1]
            else:
                #QID not existing
                qid = None
        elif Id[0] == 'wikidata':
            #Check if Wikidata QID exists
            entry = self.get_results(wikidata_endpoint,query[1].format(Id[1]))
            if entry:
                #If on Wikidata, generate dummy entry in Portal and store QID
                entrycheck = self.entry_check(entry[0]["label"]["value"],entry[0]["quote"]["value"])
                if entrycheck:
                    #If Entity with same label and description is already on Portal use it.
                    qid = entrycheck[0]["qid"]["value"]
                else:
                    #Create dummy entry and store QID if portal publication ist desired
                    if data[dec[2][0]] == dec[2][2] and data[dec[3][0]] in (dec[3][1],dec[3][2]): 
                        #Create dummy entry and store QID
                        qid = self.entry(entry[0]["label"]["value"],entry[0]["quote"]["value"],[(ExternalID,Id[-1],wikidata_qid)])
                    else:
                        qid = 'tbd'
            else:
                #QID not existing
                qid = None
        else:
            #Specified entry not existing
            qid = None
            entry = None
        return qid, entry
        
    def paper_prop_entry(self,query,entity,props,author_with_orcid='',citation_dict=''):
        '''This function takes (a property of) a paper and creates the corresponding wikibase entries.'''
        mardi_qid=self.get_results(mardi_endpoint,query[0])
        if mardi_qid:
            #If on Portal store QID
            qid=mardi_qid[0]["qid"]["value"]
        else:
            #If not on Portal, check if on Wikidata
            wikidata_entry=self.get_results(wikidata_endpoint,query[1])
            if wikidata_entry:
                entry_check=self.entry_check(wikidata_entry[0]["label"]["value"],wikidata_entry[0]["quote"]["value"])
                if entry_check:
                    #If on Portal, store QID.
                    qid=entry_check[0]["qid"]["value"]
                else:
                    #If only on wikidata, generate dummy entry, store QID.
                    qid=self.entry(wikidata_entry[0]["label"]["value"],wikidata_entry[0]["quote"]["value"],[(ExternalID,wikidata_entry[0]["qid"]["value"],wikidata_qid)])
            else:
                #If not on Portal / Wikidata create entry
                entry_check=self.entry_check(entity,props[0])
                if entry_check:
                    #If on Portal, store QID.
                    qid=entry_check[0]["qid"]["value"]
                else:
                    #Create entry, store QID.
                    qid=self.entry(entity,props[0],props[1])
        return qid

