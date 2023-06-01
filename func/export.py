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
            return render(self.request,'error1.html')

        # Get Data - Questions and User Answers
        queryset = self.project.values.filter(snapshot=None)
        data = []
        for question in Question.objects.order_by_catalog(self.project.catalog):
            if question.questionset.is_collection and question.questionset.attribute:
                if question.questionset.attribute.uri.endswith('/id'):
                    set_attribute_uri = question.questionset.attribute
                else:
                    set_attribute_uri = question.questionset.attribute.uri.rstrip('/') + '/id'
                for value_set in queryset.filter(attribute__uri=question.questionset.attribute.uri):
                    values = queryset.filter(attribute=question.attribute, set_index=value_set.set_index) \
                                     .order_by('set_prefix', 'set_index', 'collection_index')
                    data.append([question.attribute.uri+'_'+self.stringify(value_set.value), self.stringify_values(values)])
            else:
                values = queryset.filter(attribute=question.attribute).order_by('set_prefix', 'set_index', 'collection_index')
                data.append([question.attribute.uri, self.stringify_values(values)])
            
        # Workflow Documentation
        if dec[0][0] in data or dec[0][1] in data :
            # Generate Markdown File
            # Adjust raw MaRDI templates to User answers
            temp,data_flat=self.dyn_template(data)
            if len(temp) == 0:
                return render(self.request,'error5.html')
            # Fill out MaRDI template
            for entry in data:
                temp=re.sub(";","<br/>",re.sub("Yes: |'","",re.sub(entry[0],repr(entry[1]),temp)))
            if dec[2][0] in data: 
                # Download as Markdown
                response = HttpResponse(temp, content_type="application/md")
                response['Content-Disposition'] = 'filename="workflow.md"'
                return response
            elif dec[2][1] in data and not (dec[8][0] in data or dec[8][1] in data):
                # Preview Markdown as HTML
                return HttpResponse(html_front+pypandoc.convert_text(temp,'html',format='md')+html_end)
            # Export to MaRDI Portal
            elif dec[2][1] in data and (dec[8][0] in data or dec[8][1] in data):
                # Export Workflow Documentation to mediawiki portal 
                self.wikipage_export(self.project.title,re.sub('{\|','{| class="wikitable"',pypandoc.convert_text(temp,'mediawiki',format='md')))
               
                #Get Research Objective 
                wiki_res_obj=self.wikibase_answers(data,ws6)[0]
                #Check if Entity with same label and description is already on portal
                if self.entry_check(self.project.title,wiki_res_obj):
                    return render(self.request,'error20.html')
                # Integrate related paper in wikibase
                paper=self.wikibase_answers(data,paper_doi)
                if paper[0]!= 'No':
                    #Check if Paper already on MaRDI Portal
                    mardi_paper_qid=self.get_results(mardi_endpoint,re.sub('DOI',re.split(':',paper[0])[-1].upper(),doi_query))
                    if mardi_paper_qid:
                        #If on Portal store QID
                        paper_qid=mardi_paper_qid[0]["qid"]["value"]
                    else:
                        #If not on Portal, check if Paper on wikidata
                        wikidata_paper_entry=self.get_results(wikidata_endpoint,re.sub('DOI',re.split(':',paper[0])[-1].upper(),doi_query_wikidata))
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
                            author_with_orcid,author_without_orcid,citation_dict=GetCitation(re.split(':',paper[0])[-1])
                            #Check if title from paper on MaRDI Portal
                            if citation_dict['title']:
                                mardi_title_qid=self.get_results(mardi_endpoint,re.sub('TITLE',citation_dict['title'],title_query))
                                if mardi_title_qid:
                                    #If on Portal store QID
                                    paper_qid=mardi_title_qid[0]["qid"]["value"]
                                else:
                                    #If not on Portal, check if title on Wikidata
                                    wikidata_title_entry=self.get_results(wikidata_endpoint,re.sub('TITLE',citation_dict['title'],title_query_wikidata))
                                    if wikidata_title_entry:
                                        title_entry_check=self.entry_check(wikidata_title_entry[0]["label"]["value"],wikidata_title_entry[0]["quote"]["value"])
                                        if title_entry_check:
                                            #If on Portal, store QID.
                                            paper_qid=title_entry_check[0]["qid"]["value"]
                                        else:
                                            #If only on wikidata, generate dummy entry, store QID.
                                            paper_qid=self.entry(wikidata_title_entry[0]["label"]["value"],wikidata_title_entry[0]["quote"]["value"],[(ExternalID,wikidata_title_entry[0]["qid"]["value"],wikidata_qid)])
                                    else:
                                        #If not on Portal / Wikidata create paper entry, with additional author, language and journal entries
                                        #Get IDs Portal for authors with ORCID or generate them
                                        author_qids=[]
                                        for author in author_with_orcid:
                                            mardi_author_qid=self.get_results(mardi_endpoint,re.sub('ORCID',author[1],author_query))
                                            if mardi_author_qid:
                                                #If on Portal store QID
                                                author_qids.append(mardi_author_qid[0]["qid"]["value"])
                                            else:
                                                #If not on Portal, check if author on Wikidata
                                                wikidata_author_qid=self.get_results(wikidata_endpoint,re.sub('ORCID',author[1],author_query_wikidata))
                                                if wikidata_author_qid:
                                                    #Check if Entity with same label and description exists on MaRDI Portal
                                                    author_entry_check=self.entry_check(wikidata_author_qid[0]["label"]["value"],wikidata_author_qid[0]["quote"]["value"])
                                                    if author_entry_check:
                                                        #If Entity exists store QID.
                                                        author_qids.append(author_entry_check[0]["qid"]["value"])
                                                    else:
                                                        #If only on wikidata, generate dummy entry and store QID.
                                                        author_qids.append(self.entry(wikidata_author_qid[0]["label"]["value"],wikidata_author_qid[0]["quote"]["value"],[(ExternalID,wikidata_author_qid[0]["qid"]["value"],wikidata_qid)]))
                                                else:
                                                    #If not on Portal / Wikidata create author entry
                                                    author_entry_check=self.entry_check(author[0],'researcher')
                                                    if author_entry_check:
                                                        #If entity exists store QID.
                                                        author_qids.append(author_entry_check[0]["qid"]["value"])
                                                    else:
                                                        #Create author entry, store QID.
                                                        author_qids.append(self.entry(author[0],'researcher',[(Item,human,instance_of),(Item,researcher,occupation),(ExternalID,author[1],ORCID_iD)]))
                                        #Check if language from paper on MaRDI portal
                                        if citation_dict['language']:
                                            mardi_language_qid=self.get_results(mardi_endpoint,re.sub('LANGUAGE',lang_dict[citation_dict['language']],re.sub('LANG_SHORT',citation_dict['language'],language_query)))
                                            if mardi_language_qid:
                                                #If on Portal store QID
                                                citation_dict['language']=mardi_language_qid[0]["qid"]["value"]
                                            else:
                                                #If not on Portal, check if language on Wikidata
                                                wikidata_language_entry=self.get_results(wikidata_endpoint,re.sub('LANGUAGE',lang_dict[citation_dict['language']],re.sub('LANG_SHORT',citation_dict['language'],language_query_wikidata)))
                                                if wikidata_language_entry:
                                                    language_entry_check=self.entry_check(wikidata_language_entry[0]["label"]["value"],wikidata_language_entry[0]["quote"]["value"])
                                                    if language_entry_check:
                                                        #If on Portal, store QID.
                                                        citation_dict['language']=language_entry_check[0]["qid"]["value"]
                                                    else:
                                                        #If only on wikidata, generate dummy entry, store QID.
                                                        citation_dict['language']=self.entry(wikidata_language_entry[0]["label"]["value"],wikidata_language_entry[0]["quote"]["value"],[(ExternalID,wikidata_language_entry[0]["qid"]["value"],wikidata_qid)])
                                                else:
                                                    #If not on Portal / Wikidata create language entry
                                                    citation_dict['language']=self.entry(lang_dict[citation_dict['language']],'language',[(Item,language,instance_of)])
                                        #Check if journal from paper on MaRDI portal
                                        if citation_dict['journal']:
                                            mardi_journal_qid=self.get_results(mardi_endpoint,re.sub('JOURNAL',citation_dict['journal'].lower(),journal_query))
                                            if mardi_journal_qid:
                                                #If on Portal store QID
                                                citation_dict['journal']=mardi_journal_qid[0]["qid"]["value"]
                                            else:
                                                #If not on Portal, check if journal on Wikidata
                                                wikidata_journal_entry=self.get_results(wikidata_endpoint,re.sub('JOURNAL',citation_dict['journal'].lower(),journal_query_wikidata))
                                                if wikidata_journal_entry:
                                                    journal_entry_check=self.entry_check(wikidata_journal_entry[0]["label"]["value"],wikidata_journal_entry[0]["quote"]["value"])
                                                    if journal_entry_check:
                                                        #If on Portal, store QID.
                                                        citation_dict['journal']=journal_entry_check[0]["qid"]["value"]
                                                    else:
                                                        #If only on wikidata, generate dummy entry, store QID.
                                                        citation_dict['journal']=self.entry(wikidata_journal_entry[0]["label"]["value"],wikidata_journal_entry[0]["quote"]["value"],[(ExternalID,wikidata_journal_entry[0]["qid"]["value"],wikidata_qid)])
                                                else:
                                                    #If not on Portal / Wikidata create journal entry
                                                    citation_dict['journal']=self.entry(citation_dict['journal'],'scientific journal',[(Item,scientific_journal,instance_of)])
                                        #Integrate related paper in MaRDI portal
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
                model_id=re.split(':',model[0])
                if model_id[0] == 'No':
                    # Check if Model Entity exists
                    model_entry_check=self.entry_check(model[1],model[2])
                    if model_entry_check:
                        #Use existing Model Entity
                        model_qid=model_entry_check[0]["qid"]["value"]
                    else:
                        #Create new Model Entity
                        main_subject_id=model[3].split(':')
                        #Get main subject of model
                        if re.match(r"Q[0-9*]",main_subject_id[-1]):
                            if main_subject_id[0] == 'mardi':
                                #Check if mardi qid exists
                                mardi_main_subject_entry=self.get_results(mardi_endpoint,re.sub('MAIN SUBJECT','wd:'+main_subject_id[-1],main_subject_query))
                                if mardi_main_subject_entry:
                                    #If on Portal store QID
                                    main_subject_qid=main_subject_id_id[-1]
                                else:
                                    #If QID does not exists, return error
                                    return render(self.request,'error17.html')
                            elif main_subject_id[0] == 'wikidata':
                                wikidata_main_subject_entry=self.get_results(wikidata_endpoint,re.sub('MAIN SUBJECT','wd:'+main_subject_id[-1],main_subject_query_wikidata))
                                if wikidata_main_subject_entry:
                                    #Check if Entity with same label and descrition exists on MaRDI Portal
                                    main_subject_entry_check=self.entry_check(wikidata_main_subject_entry[0]["label"]["value"],wikidata_main_subject_entry[0]["quote"]["value"])
                                    if main_subject_entry_check:
                                        #If Entity exists store QID.
                                        main_subject_qid=main_subject_entry_check[0]["qid"]["value"]
                                    else:
                                        #If only on wikidata, generate dummy entry in portal and store QID
                                        main_subject_qid=self.entry(wikidata_main_subject_entry[0]["label"]["value"],wikidata_main_subject_entry[0]["quote"]["value"],[(ExternalID,main_subject_id[-1],wikidata_qid)])
                                else:
                                    #If qid does not exist, return error
                                    return render(self.request,'error17.html')
                            else:
                                return render(self.request,'error17.html')
                        else:
                            return render(self.request,'error17.html')
                        model_qid=self.entry(model[1],model[2],[(Item,mathematical_model,instance_of),(Item,main_subject_qid,main_subject),(String,re.sub("\$","",model[4]),defining_formula)])
                elif re.match(r"Q[0-9*]",model_id[-1]):
                    if model_id[0] == 'mardi':
                        #Check if mardi qid exists
                        mardi_model_entry=self.get_results(mardi_endpoint,re.sub('MODEL','wd:'+model_id[1],model_query))
                        if mardi_model_entry:
                            #If on Portal store QID
                            model_qid=model_id[-1]
                        else:
                            #If qid does not exist, return error
                            return render(self.request,'error10.html')
                    elif model_id[0] == 'wikidata':
                        #Check if wikidata qid exists
                        wikidata_model_entry=self.get_results(wikidata_endpoint,re.sub('MODEL','wd:'+model_id[1],model_query_wikidata))
                        if wikidata_model_entry: 
                            #If on wikidata, generate dummy entry in portal and store QID
                            model_entry_check=self.entry_check(wikidata_model_entry[0]["label"]["value"],wikidata_model_entry[0]["quote"]["value"])
                            if model_entry_check:
                                #If Entity with same label and description is already on portal use it.
                                model_qid=model_entry_check[0]["qid"]["value"]
                            else:
                                #Create dummy entry and store QID
                                model_qid=self.entry(wikidata_model_entry[0]["label"]["value"],wikidata_model_entry[0]["quote"]["value"],[(ExternalID,model_id[-1],wikidata_qid)])
                        else:
                            #If qid does not exist, return error
                            return render(self.request,'error10.html')
                    else:
                        return render(self.request,'error10.html')
                else:
                    return render(self.request,'error10.html')

                # Integrate related methods in wikibase 
                methods=self.wikibase_answers(data,ws3)
                methods_qid=[]
                no_methods=len(methods)//5
                for i in range(no_methods):
                    method_id=re.split(':',methods[i])
                    if re.match(r"Q[0-9*]",method_id[-1]):
                        if method_id[0] == 'mardi':
                            #Check if mardi qid exists
                            mardi_method_entry=self.get_results(mardi_endpoint,re.sub('METHOD','wd:'+method_id[-1],method_query))
                            if mardi_method_entry:
                                #If on Portal store QID
                                methods_qid.append(method_id[-1])
                            else:
                                #If QID does not exists, return error
                                return render(self.request,'error12.html')
                        elif method_id[0] == 'wikidata':
                            #Check if wikidata qid exists
                            wikidata_method_entry=self.get_results(wikidata_endpoint,re.sub('METHOD','wd:'+method_id[-1],method_query_wikidata))
                            if wikidata_method_entry:
                                #Check if on MaRDI Portal
                                method_entry_check=self.entry_check(wikidata_method_entry[0]["label"]["value"],wikidata_method_entry[0]["quote"]["value"])
                                if method_entry_check:
                                    #If on Portal, store QID.
                                    methods_qid.append(method_entry_check[0]["qid"]["value"])
                                else:
                                    #If only on wikidata, generate dummy entry, store QID.
                                    methods_qid.append(self.entry(wikidata_method_entry[0]["label"]["value"],wikidata_method_entry[0]["quote"]["value"],[(ExternalID,method_id[-1],wikidata_qid)]))
                            else:
                                #If qid does not exist, return error
                                return render(self.request,'error12.html')
                    else:
                        #Generate new entity in Portal
                        method_entry_check=self.entry_check(methods[i::no_methods][1],methods[i::no_methods][2])
                        if method_entry_check:
                            #If on MaRDI Portal, store QID.
                            methods_qid.append(method_entry_check[0]["qid"]["value"])
                        else:
                            #Create new Method Entity
                            #Get main subject of method
                            main_subject_id=methods[i::no_methods][3].split(':')
                            if re.match(r"Q[0-9*]",main_subject_id[-1]):
                                if main_subject_id[0] == 'mardi':
                                    #Check if mardi qid exists
                                    mardi_main_subject_entry=self.get_results(mardi_endpoint,re.sub('MAIN SUBJECT','wd:'+main_subject_id[-1],main_subject_query))
                                    if mardi_main_subject_entry:
                                        #If on Portal store QID
                                        main_subject_qid=main_subject_id_id[-1]
                                    else:
                                        #If QID does not exists, return error
                                        return render(self.request,'error18.html')
                                elif main_subject_id[0] == 'wikidata':
                                    wikidata_main_subject_entry=self.get_results(wikidata_endpoint,re.sub('MAIN SUBJECT','wd:'+main_subject_id[-1],main_subject_query_wikidata))
                                    if wikidata_main_subject_entry:
                                        #If on wikidata, generate dummy entry in portal and store QID
                                        main_subject_entry_check=self.entry_check(wikidata_main_subject_entry[0]["label"]["value"],wikidata_main_subject_entry[0]["quote"]["value"])
                                        if main_subject_entry_check:
                                            #If on Portal, store QID.
                                            main_subject_qid=main_subject_entry_check[0]["qid"]["value"]
                                        else:
                                            #If only on wikidata, generate dummy entry, store QID.
                                            main_subject_qid=self.entry(wikidata_main_subject_entry[0]["label"]["value"],wikidata_main_subject_entry[0]["quote"]["value"],[(ExternalID,main_subject_id[-1],wikidata_qid)])
                                    else:
                                        #If qid does not exist, return error
                                        return render(self.request,'error18.html')
                                else:
                                    return render(self.request,'error18.html')
                            else:
                                return render(self.request,'error18.html')
                            if method_id[0] == 'doi':
                                external_method_id=method_id[-1]
                            else:
                                external_method_id=''
                            methods_qid.append(self.entry(methods[i::no_methods][1],methods[i::no_methods][2],[(Item,method,instance_of),(Item,main_subject_qid,main_subject),
                                                                                                               (String,re.sub("\$","",methods[i::no_methods][4]),defining_formula),
                                                                                                               (ExternalID,external_method_id,DOI)]))
                
                # Integrate related software and programming languages in wikibase
                softwares=self.wikibase_answers(data,ws4)
                softwares_qid=[]
                no_softwares=len(softwares)//4
                for i in range(no_softwares):
                    software_id=re.split(':',softwares[i])
                    if re.match(r"Q[0-9*]",software_id[-1]):
                        if software_id[0] == 'mardi':
                            #Check if mardi qid exists
                            mardi_software_entry=self.get_results(mardi_endpoint,re.sub('SOFTWARE','wd:'+software_id[-1],software_query))
                            if mardi_software_entry:
                                #If on Portal store QID
                                softwares_qid.append(software_id[-1])
                            else:
                                #If QID does not exists, return error
                                return render(self.request,'error13.html')
                        elif software_id[0] == 'wikidata':
                            #Check if wikidata qid exists
                            wikidata_software_entry=self.get_results(wikidata_endpoint,re.sub('SOFTWARE','wd:'+software_id[-1],software_query_wikidata))
                            if wikidata_software_entry:
                                #If on wikidata, check if also on MaRDI Portal
                                software_entry_check=self.entry_check(wikidata_software_entry[0]["label"]["value"],wikidata_software_entry[0]["quote"]["value"])
                                if software_entry_check:
                                    #If on MaRDI Portal, store QID.
                                    softwares_qid.append(software_entry_check[0]["qid"]["value"])
                                else:
                                    #If only on wikidata, generate dummy entry and store QID.
                                    softwares_qid.append(self.entry(wikidata_software_entry[0]["label"]["value"],wikidata_software_entry[0]["quote"]["value"],[(ExternalID,software_id[-1],wikidata_qid)]))
                            else:
                                #If qid does not exist, return error
                                return render(self.request,'error13.html')
                    else:
                        #Check if Entity on MaRDI Portal
                        software_entry_check=self.entry_check(softwares[i::no_softwares][1],softwares[i::no_softwares][2])
                        if software_entry_check:
                            #If on Portal, store QID.
                            softwares_qid.append(software_entry_check[0]["qid"]["value"])
                        else:
                            #Get involved programming languages in Workflow
                            wiki_planguages=softwares[i::no_softwares][3].split('; ')
                            planguages_qid=[]
                            for planguage in wiki_planguages:
                                planguage_id=re.search('\((.+?)\)',planguage).group(1).split(':')
                                if re.match(r"Q[0-9*]",planguage_id[-1]):
                                    if planguage_id[0] == 'mardi':
                                        #Check if mardi qid exists
                                        mardi_planguage_entry=self.get_results(mardi_endpoint,re.sub('LANGUAGE','wd:'+planguage_id[-1],plang_query))
                                        if mardi_planguage_entry:
                                            #If on Portal store QID
                                            planguages_qid.append(planguage_id[-1])
                                        else:
                                            #If QID does not exists, return error
                                            return render(self.request,'error16.html')
                                    elif planguage_id[0] == 'wikidata':
                                        wikidata_planguage_entry=self.get_results(wikidata_endpoint,re.sub('LANGUAGE','wd:'+planguage_id[-1],plang_query_wikidata))
                                        if wikidata_planguage_entry:
                                            #Check if on MaRDI Portal
                                            planguage_entry_check=self.entry_check(wikidata_planguage_entry[0]["label"]["value"],wikidata_planguage_entry[0]["quote"]["value"])
                                            if planguage_entry_check:
                                                #If on MaRDI Portal, store QID.
                                                planguages_qid.append(planguage_entry_check[0]["qid"]["value"])
                                            else:
                                                #If only on wikidata, generate dummy entry and store QID.
                                                planguages_qid.append(self.entry(wikidata_planguage_entry[0]["label"]["value"],wikidata_planguage_entry[0]["quote"]["value"],[(ExternalID,planguage_id[-1],wikidata_qid)]))
                                        else:
                                            #If qid does not exist, return error
                                            return render(self.request,'error16.html')
                                    else:
                                        return render(self.request,'error16.html')
                                else:
                                    return render(self.request,'error16.html')
                            if software_id[0] == 'doi' or software_id[0] == 'swmath':
                                external_software_id=software_id[-1]
                            else:
                                external_software_id=''
                            softwares_qid.append(self.entry(softwares[i::no_softwares][1],softwares[i::no_softwares][2],[(Item,software,instance_of)]+
                                                                                                                        [(Item,plang,programmed_in) for plang in planguages_qid]+
                                                                                                                        [(ExternalID,external_software_id,DOI if software_id[0] == 'doi' else 'swmath')]))
                # Integrate related inputs in wikibase
                inputs=self.wikibase_answers(data,ws7)
                inputs_qid=[]
                no_inputs=len(inputs)//2
                for i in range(no_inputs):
                    input_id=re.split(':',inputs[i])
                    if re.match(r"Q[0-9*]",input_id[-1]):
                        if input_id[0] == 'mardi':
                            #Check if mardi qid exists
                            mardi_input_entry=self.get_results(mardi_endpoint,re.sub('INPUT','wd:'+input_id[-1],input_query))
                            if mardi_input_entry:
                                #If on Portal store QID
                                inputs_qid.append(input_id[-1])
                            else:
                                #If QID does not exists, return error
                                return render(self.request,'error14.html')
                        elif input_id[0] == 'wikidata':
                            #Check if wikidata qid exists
                            wikidata_input_entry=self.get_results(wikidata_endpoint,re.sub('INPUT','wd:'+input_id[-1],input_query_wikidata))
                            if wikidata_input_entry:
                                #Check if on MaRDI Portal
                                input_entry_check=self.entry_check(wikidata_input_entry[0]["label"]["value"],wikidata_input_entry[0]["quote"]["value"])
                                if input_entry_check:
                                    #If on MaRDI Portal, store QID.
                                    inputs_qid.append(input_entry_check[0]["qid"]["value"])
                                else:
                                    #If only on wikidata, generate dummy entry and store QID.
                                    inputs_qid.append(self.entry(wikidata_input_entry[0]["label"]["value"],wikidata_input_entry[0]["quote"]["value"],[(ExternalID,input_id[-1],wikidata_qid)]))
                            else:
                                #If qid does not exist, return error
                                return render(self.request,'error14.html')
                    else:
                        #Check if on MaRDI Portal
                        input_entry_check=self.entry_check(inputs[i::no_inputs][1],'data set')
                        if input_entry_check:
                            #If on Portal, store QID
                            inputs_qid.append(input_entry_check[0]["qid"]["value"])
                        else:
                            #If not on Portal, create new Entity
                            if input_id[0] == 'doi':
                                external_input_id=input_id[-1]
                            else:
                                external_input_id=''
                            inputs_qid.append(self.entry(inputs[i::no_inputs][1],'data set',[(Item,data_set,instance_of),(ExternalID,external_input_id,DOI)]))
                            
                #Get involved Disciplines in Workflow
                wiki_disciplines=self.wikibase_answers(data,ws5)[0].split('; ')
                disciplines_qid=[]
                for discipline in wiki_disciplines:
                    discipline_id=re.search('\((.+?)\)',discipline).group(1).split(':')
                    if re.match(r"Q[0-9*]",discipline_id[-1]):
                        if discipline_id[0] == 'mardi':
                            #Check if mardi qid exists
                            mardi_discipline_entry=self.get_results(mardi_endpoint,re.sub('DISCIPLINE','wd:'+discipline_id[-1],discipline_query))
                            if mardi_discipline_entry:
                                #If on Portal store QID
                                disciplines_qid.append(discipline_id[-1])
                            else:
                                #If QID does not exists, return error
                                return render(self.request,'error15.html')
                        elif discipline_id[0] == 'wikidata':
                            wikidata_discipline_entry=self.get_results(wikidata_endpoint,re.sub('DISCIPLINE','wd:'+discipline_id[-1],discipline_query_wikidata))
                            if wikidata_discipline_entry:
                                #Check if on MaRDI Portal
                                discipline_entry_check=self.entry_check(wikidata_discipline_entry[0]["label"]["value"],wikidata_discipline_entry[0]["quote"]["value"])
                                if discipline_entry_check:
                                    #If on MaRDI Portal, store QID.
                                    disciplines_qid.append(discipline_entry_check[0]["qid"]["value"])
                                else:
                                    #If only on wikidata, generate dummy entry and store QID
                                    disciplines_qid.append(self.entry(wikidata_discipline_entry[0]["label"]["value"],wikidata_discipline_entry[0]["quote"]["value"],[(ExternalID,discipline_id[-1],wikidata_qid)]))
                            else:
                                #If qid does not exist, return error
                                return render(self.request,'error15.html')
                        else:
                            return render(self.request,'error15.html')
                    else:
                        return render(self.request,'error15.html')
                
                workflow_qid=self.entry(self.project.title, wiki_res_obj,[(Item,research_workflow,instance_of),(Item,paper_qid,cites_work)]+[(Item,discipline,field_of_work) for discipline in disciplines_qid]+
															[(Item,mmsi,uses) for mmsi in [model_qid]+methods_qid+softwares_qid+inputs_qid])
                return render(self.request,'export.html')

            # Not chosen
            else:
                return render(self.request,'error2.html')

        # Workflow Finding
        elif dec[1][0] in data or dec[1][1] in data:
            
            #QID and String Entities to search for
            ent_string=[]
            ent_qid=[]
            for entry in data:
                if entry[0] == ws8:
                    for entity in entry[1].split("; "):
                        if re.split(':',entity)[0] == 'mardi' and re.match(r"Q[0-9*]",re.split(':',entity)[-1]):
                            ent_qid.append('wd:'+re.split(':',entity)[-1])
                        else:
                            ent_string.append(entity)
         
            # Entity Type
            if dec[3][0] in data or dec[3][1] in data:
                # SPARQL Query for Research Objective
                if len(ent_qid) > 0:
                    return render(self.request,'error11.html')
                else:
                    FILTER=""
                    for ent in ent_string:
                        FILTER=FILTER+"FILTER(CONTAINS(?quote, '"+ent+"'@en)).\n"
                    query=re.sub("STATEMENT",statement_obj,re.sub("FILTER",FILTER,re.sub("ITEMFINDER","",query_base)))
            elif dec[4][0] in data or dec[4][1] in data:
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
                            
            elif dec[9][0] in data or dec[9][1] in data:
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
                return render(self.request,'error3.html')
         
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
            return render(self.request,'error4.html')

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
        if dec[6][0] in data or dec[6][1] in data:
            temp=math_temp
            tables=math_tables
            topics=math_topics
            ids=math_ids
        elif dec[7][0] in data or dec[7][1] in data:
            temp=exp_temp
            tables=exp_tables
            topics=exp_topics
            ids=exp_ids
        else:
            temp=[]
            return temp
        data_flat=sum(data,[])
        for n,table in enumerate(tables):
            t=self.create_table(topics[n],ids[n],sum(ids[n][0] in s for s in data_flat)+2)
            temp=re.sub(table,t,temp)
        return(temp,data_flat)
       
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
        print(len(post_content)) 
        return

    def wikibase_answers(self, data, wiki):
        '''Takes data and extracts answers relevant for Wiki'''
        wiki_answers=[]
        for question in wiki:
            for entry in data:
                if question in entry[0]:
                    wiki_answers.append(re.sub("Yes: ","",entry[1]))
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


