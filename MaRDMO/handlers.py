import re, os, json
import requests

from django.dispatch import receiver
from django.db.models.signals import post_save

from rdmo.projects.models import Value
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from .citation import GetCitation
from .utils import query_sparql, value_editor, extract_parts, splitVariableText
from .sparql import queryPublication, queryModelHandler, queryHandler, wini, mini, pl_query, pl_vars, pro_query, pro_vars
from .id import *
from .config import wd, wdt, mardi_api, wikidata_api, mardi_endpoint, wikidata_endpoint, BASE_URI

from difflib import SequenceMatcher

@receiver(post_save, sender=Value)
def PublicationCitationRetriever(sender, **kwargs): 

    instance = kwargs.get("instance", None)

    if instance and instance.attribute.uri == f"{BASE_URI}domain/Published":
    
        # Activate (Yes)  / Deactivate (No or nothin) Publication Information Section
        if instance.option_text == 'Yes':            
            value_editor(instance.project,f"{BASE_URI}domain/PublicationInformation",1)
        else: 
            value_editor(instance.project,f"{BASE_URI}domain/PublicationInformation",0)

        # Evaluate Information provided for Yes case
        if instance.text.split(':')[0] == 'url': 
            
            # If url provided, deactivate Publication Information section 
            value_editor(instance.project,f"{BASE_URI}domain/PublicationInformation",0)
        
        elif re.match(r'doi:10.\d{4,9}/[-._;()/:a-z0-9A-Z]+', instance.text):

            path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
            with open(path, "r") as json_file:
                option = json.load(json_file)
            
            # Extract DOI and Initialize different dictionaries
            doi = instance.text.split(':')[1]   
            
            dict_merged = {}
            author_dict_merged = {}
            
            # Define Prefix & Parameter for MaRDI KG search, Search Paper in MaRDI KG via DOI and merge results
            mardi_prefix = f"PREFIX wdt:{wdt} PREFIX wd:{wd}"
            mardi_query_parameter = [P16, doi.upper(), P8, P22, P4, P12, P10, P7, P9, P11, P13, P14, P15, P2, P23]
            mardi_dicts = query_sparql(mardi_prefix + queryPublication['All'].format(*mardi_query_parameter), mardi_endpoint)
            
            # Combine dictionaries from MaRDI Query
            for mardi_dict in mardi_dicts:
                for key in mardi_dict.keys():
                    if key == 'authorInfo':
                        if mardi_dict.get(key, {}).get('value'):
                            authorQid, authorLabel, authorDescription, authorOrcid, authorWikidataQid, authorZBmathID = mardi_dict[key]['value'].split(' <|> ')
                            if authorQid not in dict_merged.get('mardi_authorQid', []):
                                dict_merged.setdefault('mardi_authorQid', []).append(authorQid)
                                dict_merged.setdefault('mardi_authorLabel', []).append(authorLabel)
                                dict_merged.setdefault('mardi_authorDescription', []).append(authorDescription)
                                dict_merged.setdefault('mardi_authorOrcid', []).append(authorOrcid)
                                dict_merged.setdefault('mardi_authorWikidataQid', []).append(authorWikidataQid)
                                dict_merged.setdefault('mardi_authorZBmathID', []).append(authorZBmathID)
                    elif key == 'otherAuthor':
                        if mardi_dict.get(key, {}).get('value'):
                            if mardi_dict[key]['value'] not in dict_merged.get('mardi_'+key, []):
                                dict_merged.setdefault('mardi_'+key, []).append(mardi_dict[key]['value'])
                    elif key == 'publicationLabel':
                        dict_merged['publication'] = mardi_dict.get(key, {}).get('value')
                        dict_merged['mardi_'+key] = mardi_dict.get(key, {}).get('value')
                    else:
                        dict_merged['mardi_'+key] = mardi_dict.get(key, {}).get('value')
            
            if not dict_merged:
            
                # If results not found for Paper in MaRDI KG via DOI, define Parameters for Wikidata search, search paper via DOI and merge results
                wikidata_parameter = ['356', doi.upper(), '50', '496', '31', '1433', '407', '1476', '2093', '577', '478', '433', '304', '', '1556']
                wikidata_dicts = query_sparql(queryPublication['All'].format(*wikidata_parameter), wikidata_endpoint)
            
                # Combine dictionaries from Wikidata Query
                for wikidata_dict in wikidata_dicts:
                    for key in wikidata_dict.keys():
                        if key == 'authorInfo':
                            if wikidata_dict.get(key, {}).get('value'):
                                authorQid, authorLabel, authorDescription, authorOrcid, authorWikidataQid, authorZBmathID = wikidata_dict[key]['value'].split(' <|> ')
                                if authorQid not in dict_merged.get('wikidata_authorQid', []):
                                    dict_merged.setdefault('wikidata_authorQid', []).append(authorQid)
                                    dict_merged.setdefault('wikidata_authorLabel', []).append(authorLabel)
                                    dict_merged.setdefault('wikidata_authorDescription', []).append(authorDescription)
                                    dict_merged.setdefault('wikidata_authorOrcid', []).append(authorOrcid)
                                    dict_merged.setdefault('wikidata_authorWikidataQid', []).append(authorWikidataQid)
                                    dict_merged.setdefault('wikidata_authorZBmathID', []).append(authorZBmathID)
                        elif key == 'otherAuthor':
                            if wikidata_dict.get(key, {}).get('value'):
                                if wikidata_dict[key]['value'] not in dict_merged.get('wikidata_'+key, []):
                                    dict_merged.setdefault('wikidata_'+key, []).append(wikidata_dict[key]['value'])
                        elif key == 'publicationLabel':
                            dict_merged['publication'] = wikidata_dict.get(key, {}).get('value')
                            dict_merged['wikidata_'+key] = wikidata_dict.get(key, {}).get('value')
                        else:
                            dict_merged['wikidata_'+key] = wikidata_dict.get(key, {}).get('value')
                 
                if dict_merged:
            
                    # If results found for Paper in Wikidata use Wikidata QID to search MaRDI KG again
                    mardi_parameter = [P2, dict_merged.get('wikidata_publicationQid', '')]
                    mardi_dict = query_sparql(mardi_prefix+queryPublication['WikiCheck'].format(*mardi_parameter), mardi_endpoint)
            
                    if mardi_dict:
                        # If results found for Paper in MaRDI KG via Wikidata QID update results 
                        dict_merged['mardi_publicationQid'] = mardi_dict[0].get('publicationQid', {}).get('value')
                        dict_merged['mardi_publicationLabel'] = mardi_dict[0].get('publicationLabel', {}).get('value')
                        dict_merged['mardi_publicationDescription1'] = mardi_dict[0].get('publicationDescription1', []).get('value')
                else: 
            
                    # If no results found in MaRDI KG or Wikidata use DOI to get complete citation
                    orcid_authors, zbmath_authors, other_authors, citation_dictionary = GetCitation(doi)
            
                    if citation_dictionary:
            
                        # If citation found, extract ORCID and zbMath IDs
                        orcid_ids = [orcid_author[1] for orcid_author in orcid_authors]
                        zbmath_ids = [zbmath_author[1] for zbmath_author in zbmath_authors]
            
                        # Search Authors related to publication 
                        author_dict_merged = Author_Search(orcid_ids, zbmath_ids, orcid_authors, zbmath_authors)
            
                        # Define search objects, journal, for Wikidata API and MaRDI requests and store results 
                        search_objects_wikidata = [[citation_dictionary.get('journal', '')]]
                        make_api_requests(wikidata_api, search_objects_wikidata, dict_merged, 'cit_wikidata')
                        search_objects_mardi = [[citation_dictionary.get('journal', ''), dict_merged.get('cit_wikidata_journalLabel', '')]]
                        make_api_requests(mardi_api, search_objects_mardi, dict_merged, 'cit_mardi')
            
                        # Store Entrytype Data
                        entry_type_data = {'article': {'wikidata_qid': 'Q13442814', 
                                                       'mardi_qid': Q1, 
                                                       'label': 'scholarly article', 
                                                       'description': 'article in an academic publication, usually peer reviewed'},
                                           
                                           'publication': {'wikidata_qid': 'Q732577', 
                                                           'mardi_qid': Q10, 
                                                           'label': 'publication', 
                                                           'description': 'content made available to the general public'}}
            
                        # Update dictionary with citation information
                        dict_merged.update({
                            'cit_wikidata_entrytypeQid': entry_type_data[citation_dictionary['ENTRYTYPE']]['wikidata_qid'],
                            'cit_wikidata_entrytypeLabel': entry_type_data[citation_dictionary['ENTRYTYPE']]['label'],
                            'cit_wikidata_entrytypeDescription1': entry_type_data[citation_dictionary['ENTRYTYPE']]['description'],
                            'cit_mardi_entrytypeQid': entry_type_data[citation_dictionary['ENTRYTYPE']]['mardi_qid'],
                            'cit_mardi_entrytypeLabel': entry_type_data[citation_dictionary['ENTRYTYPE']]['label'],
                            'cit_mardi_entrytypeDescription1': entry_type_data[citation_dictionary['ENTRYTYPE']]['description'],
                            'cit_wikidata_languageQid': citation_dictionary.get('language',['','',''])[0], 
                            'cit_wikidata_languageLabel': citation_dictionary.get('language',['','',''])[1],
                            'cit_wikidata_languageDescription1': citation_dictionary.get('language',['','',''])[2],
                            'publication': citation_dictionary.get('title',''),
                            'volume': citation_dictionary.get('volume',''),
                            'issue': citation_dictionary.get('number',''),
                            'page': citation_dictionary.get('pages',''),
                            'publicationDate': citation_dictionary.get('pub_date',''),
                            'otherAuthor': other_authors,
                            'journal': citation_dictionary.get('journal',''),
                            'entrytypeQid': citation_dictionary.get('ENTRYTYPE','')})
        
            # Gather Data for fill out and storage for later export
            paper_information = {}
            
            # Store publication, entrytype, language and journal information
            citation_properties = [['publicationQid', 'publicationLabel', 'publicationDescription1'],
                                   ['entrytypeQid', 'entrytypeLabel', 'entrytypeDescription1'],
                                   ['languageQid', 'languageLabel', 'languageDescription1'],
                                   ['journalQid', 'journalLabel', 'journalDescription1']]
            
            for citation_property in citation_properties:
                prefix = 'mardi_' if dict_merged.get('mardi_' + citation_property[0]) else \
                         'wikidata_' if dict_merged.get('wikidata_' + citation_property[0]) else \
                         'cit_mardi_' if dict_merged.get('cit_mardi_' + citation_property[0]) else \
                         'cit_wikidata_'
                if dict_merged.get(prefix + citation_property[0]):
                    qid = prefix[:-1].removeprefix('cit_') + ':' + dict_merged[prefix + citation_property[0]]
                    if citation_property[0] == 'publicationQid':
                        paper_information[citation_property[0]] = [qid]
                    else:
                        paper_information[citation_property[0]] = [dict_merged[prefix + citation_property[1]]]
                    paper_information[citation_property[0] + '_back'] = [qid + ' <|> ' + dict_merged[prefix + citation_property[1]] + ' <|> ' + dict_merged[prefix + citation_property[2]]]
                else:
                    default_value = 'no information available'
                    if dict_merged.get(citation_property[0][:-3]):
                        if citation_property[0].startswith('publication'):
                            paper_information[citation_property[0]] = [default_value]
                            paper_information[citation_property[0] + '_back'] = ['no id <|> ' + dict_merged[citation_property[0][:-3]] + ' <|> ' + citation_property[0][:-3]]
                        else:
                            paper_information[citation_property[0]] = [dict_merged[citation_property[0][:-3]]]
                            paper_information[citation_property[0] + '_back'] = ['no id <|> ' + dict_merged[citation_property[0][:-3]] + ' <|> ' + citation_property[0][:-3]]
                    else:
                        paper_information[citation_property[0]] = [default_value]
                        paper_information[citation_property[0] + '_back'] = ['NONE']        
            
            # Store Author Information
            paper_information['author_label'] = []
            paper_information['author_label_back'] = []
            
            if 'mardi_authorQid' in dict_merged or 'mardi_otherAuthor' in dict_merged:
            
                # Store MaRDI Author QID /Label
                try:
                    for qid, label in zip(dict_merged['mardi_authorQid'], dict_merged['mardi_authorLabel']):
                    
                        if qid:
                            paper_information['author_label'].append(label+' (mardi:'+qid+')')
                        else:
                            paper_information['author_label'].append(label)
                    
                        paper_information['author_label_back'].append(['mardi:'+qid])
                except KeyError:
                    pass
                if dict_merged.get('mardi_otherAuthor', ''): 
                    paper_information['author_label'].extend(dict_merged['mardi_otherAuthor'])
            
            elif 'wikidata_authorQid' in dict_merged or 'wikidata_otherAuthor' in dict_merged:
            
                # Store Wikidata Author QID / Label
                try:
                    for qid, label in zip(dict_merged['wikidata_authorQid'], dict_merged['wikidata_authorLabel']):
                        
                        if qid:
                            paper_information['author_label'].append(label+' (wikidata:'+qid+')')
                        else:
                            paper_information['author_label'].append(label)

                        paper_information['author_label_back'].append(['wikidata:'+qid])
                except KeyError:
                    pass
                if dict_merged.get('wikidata_otherAuthor', ''):
                    paper_information['author_label'].extend(dict_merged['wikidata_otherAuthor'])
            
            elif author_dict_merged:
            
                # Store Publication Authors from Citation via ORCID and zbMath
                for author in author_dict_merged.keys():
                    if author_dict_merged[author]['mardiQID']:
                        paper_information['author_label'].append(author_dict_merged[author]['mardiLabel'] + ' (mardi:' + author_dict_merged[author]['mardiQID'] + ')')
                        paper_information['author_label_back'].append('mardi:' + author_dict_merged[author]['mardiQID'])
                    elif author_dict_merged[author]['wikiQID']:
                        paper_information['author_label'].append(author_dict_merged[author]['wikiLabel'] + ' (wikidata:' + author_dict_merged[author]['wikiQID'] + ')')
                        paper_information['author_label_back'].append('wikidata:' + author_dict_merged[author]['wikiQID'] +
                                                                          ' <|> ' + author_dict_merged[author]['wikiLabel'] +
                                                                          ' <|> ' + author_dict_merged[author]['wikiDescription'])
                    elif author_dict_merged[author]['orcid']:
                        if author_dict_merged[author]['zbmath']:
                            paper_information['author_label'].append(author+' (orcid:'+author_dict_merged[author]['orcid']+', zbmath:'+author_dict_merged[author]['zbmath']+')')
                            paper_information['author_label_back'].append('orcid:'+author_dict_merged[author]['orcid']+'; zbmath:'+author_dict_merged[author]['zbmath']+' <|> '+author+' <|> researcher (ORCID '+author_dict_merged[author]['orcid']+')')
                        else:
                            paper_information['author_label'].append(author+' (orcid:'+author_dict_merged[author]['orcid']+')')
                            paper_information['author_label_back'].append('orcid:'+author_dict_merged[author]['orcid']+' <|> '+author+' <|> researcher (ORCID '+author_dict_merged[author]['orcid']+')')
                    elif author_dict_merged[author]['zbmath']:
                        paper_information['author_label'].append(author+' (zbmath:'+author_dict_merged[author]['zbmath']+')')
                        paper_information['author_label_back'].append('zbmath:'+author_dict_merged[author]['zbmath']+' <|> '+author+' <|> researcher (zbMath '+author_dict_merged[author]['zbmath']+')')
                
                if dict_merged.get('otherAuthor', ''):
                    paper_information['author_label'].extend(dict_merged['otherAuthor'])
            
            else:
            
                if dict_merged.get('otherAuthor', ''):
                    paper_information['author_label'].extend(dict_merged['otherAuthor'])
                    paper_information['author_label_back'].append('')
                else:
                    paper_information['author_label'].append('no information available')
                    paper_information['author_label_back'].append('')
            
            # Store publication volume, issue, page and publication date
            citation_properties = ['volume', 'issue', 'page', 'publicationDate', 'publication']
            for citation_property in citation_properties:
                if dict_merged.get('mardi_'+citation_property):
                    # Store MaRDI Property
                    paper_information[citation_property] = [dict_merged['mardi_'+citation_property]]
                    paper_information[citation_property+'_back'] = [dict_merged['mardi_'+citation_property]]
                elif dict_merged.get('wikidata_'+citation_property):
                    # Store Wikidata Property
                    paper_information[citation_property] = [dict_merged['wikidata_'+citation_property]]
                    paper_information[citation_property+'_back'] = [dict_merged['wikidata_'+citation_property]]
                elif dict_merged.get(citation_property):
                    # Store Citation Property
                    paper_information[citation_property] = [dict_merged[citation_property]]
                    paper_information[citation_property+'_back'] = [dict_merged[citation_property]]
                else:
                    # No Publication Volume available
                    paper_information[citation_property] = ['no information available']
                    paper_information[citation_property+'_back'] = ['NONE']
            
            # Append paper information to question ids 
            paper_infos = [paper_information['publicationQid'], paper_information['publicationQid_back'],
                           paper_information['entrytypeQid'], paper_information['entrytypeQid_back'],
                           paper_information['publication'], paper_information['publication_back'],
                           paper_information['author_label'], paper_information['author_label_back'],
                           paper_information['languageQid'], paper_information['languageQid_back'],
                           paper_information['journalQid'], paper_information['journalQid_back'],
                           paper_information['volume'], paper_information['volume_back'],
                           paper_information['issue'], paper_information['issue_back'],
                           paper_information['page'], paper_information['page_back'],
                           paper_information['publicationDate'], paper_information['publicationDate_back']]
            
            object_uris = [f'{BASE_URI}domain/PublicationQID', f'{BASE_URI}domain/PublicationQID_hidden',
                           f'{BASE_URI}domain/PublicationType', f'{BASE_URI}domain/PublicationType_hidden',
                           f'{BASE_URI}domain/PublicationTitle', f'{BASE_URI}domain/PublicationTitle_hidden',
                           f'{BASE_URI}domain/PublicationAuthor', f'{BASE_URI}domain/PublicationAuthor_hidden',
                           f'{BASE_URI}domain/PublicationLanguage', f'{BASE_URI}domain/PublicationLanguage_hidden',
                           f'{BASE_URI}domain/PublicationJournal', f'{BASE_URI}domain/PublicationJournal_hidden',
                           f'{BASE_URI}domain/PublicationVolume', f'{BASE_URI}domain/PublicationVolume_hidden',
                           f'{BASE_URI}domain/PublicationIssue', f'{BASE_URI}domain/PublicationIssue_hidden',
                           f'{BASE_URI}domain/PublicationPage', f'{BASE_URI}domain/PublicationPage_hidden',
                           f'{BASE_URI}domain/PublicationDate', f'{BASE_URI}domain/PublicationDate_hidden']
            
            for paper_info, object_uri in zip(paper_infos, object_uris):
                if object_uri == f'{BASE_URI}domain/PublicationLanguage':
                    for idx,val in enumerate(paper_info):
                        if option.get(val) is not None:
                            value_editor(instance.project, object_uri, None, None, Option.objects.get(uri=option.get(val)))
                else:
                    for idx,val in enumerate(paper_info):
                        value_editor(instance.project, object_uri, val, None, None, idx)

            return

@receiver(post_save, sender=Value)
def WorkflowOrModel(sender, **kwargs):

    instance = kwargs.get("instance", None)

    if instance and instance.attribute.uri == f'{BASE_URI}domain/DocumentationType':
    
        path = os.path.join(os.path.dirname(__file__), 'data', 'modus.json')
        with open(path, "r") as json_file:
            OperationModus = json.load(json_file)

        path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
        with open(path, "r") as json_file:
            option = json.load(json_file)

        if instance.option == Option.objects.get(uri=option['Workflow']):
            # Activate Questions for Workflow Documentation
            val = [0,0,0,0,0]
        elif instance.option == Option.objects.get(uri=option['Model']):
            # Activate Questions for Model Documentation
            val = [1,0,0,0,1]
        else:
            # Deactivate all Documentation Questions
            val = [0,0,0,0,0]

        for idx, key in enumerate(OperationModus['WorkflowOrModel'].keys()):
            for uri in OperationModus['WorkflowOrModel'][key]:
                value_editor(instance.project,uri,val[idx])
    return

@receiver(post_save, sender=Value)
def SearchOrDocument(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    if instance and instance.attribute.uri == f'{BASE_URI}domain/OperationType':
        
        path = os.path.join(os.path.dirname(__file__), 'data', 'modus.json')
        with open(path, "r") as json_file:
            OperationModus = json.load(json_file)

        path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
        with open(path, "r") as json_file:
            option = json.load(json_file)

        if instance.option == Option.objects.get(uri=option['Search']):
            # Activate Questions for Search
            val = [1,0,1,0]
        else:
            # Deactivate all Questionss
            val = [0,0,0,0]

        for idx, key in enumerate(OperationModus['SearchOrDocument'].keys()):
            for uri in OperationModus['SearchOrDocument'][key]:
                value_editor(instance.project,uri,val[idx])
                        
    return

@receiver(post_save, sender=Value)
def ComputationalOrExperimental(sender, **kwargs):

    instance = kwargs.get("instance", None)
    
    if instance and instance.attribute.uri == f'{BASE_URI}domain/WorkflowType':

        path = os.path.join(os.path.dirname(__file__), 'data', 'modus.json')
        with open(path, "r") as json_file:
            OperationModus = json.load(json_file)

        path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
        with open(path, "r") as json_file:
            option = json.load(json_file)

        if instance.option == Option.objects.get(uri=option['Analysis']):
            # Activate Questions for Experimental Workflow
            val = [1,0,1]
        elif instance.option == Option.objects.get(uri=option['Computation']):
            # Activate Questions for Computational Workflow
            val = [1,1,0]
        else:
            # Deactivate all Questions
            val = [0,0,0]

        for idx, key in enumerate(OperationModus['ComputationalOrExperimental'].keys()):
            for uri in OperationModus['ComputationalOrExperimental'][key]:
                value_editor(instance.project,uri,val[idx])
    return

@receiver(post_save, sender=Value)
def ModelHandler(sender, **kwargs):
    
    instance = kwargs.get("instance", None)
    
    if instance and instance.attribute.uri == f'{BASE_URI}domain/main-model/id':

        if instance.external_id and instance.external_id != 'not found':        
            IdMM = instance.external_id
        else:
            return
        
        # Get Model, Research Field, Research Problem, Quantity, Mathematical Formulation and Task Information        
        results = query_sparql(queryModelHandler['All'].format(f":{IdMM.split(':')[1]}"))
        
        if results:
            # Add Research Field Information to Questionnaire
            add_entity(instance.project, results, 'field')
            
            # Add Research Problem Information to Questionnaire
            add_entity(instance.project, results, 'problem')
            
            # Add Quantity Information to Questionnaire
            add_entity(instance.project, results, 'quantity')
            
            # Add Mathematical Model Information to Questionnaire
            add_entity(instance.project, results, 'model')
            
            # Add Formulation Information to Questionnaire
            add_entity(instance.project, results, 'formulation')

            # Add Task Information to Questionnaire
            add_entity(instance.project, results, 'task')

    return

@receiver(post_save, sender=Value)
def programmingLanguages(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/SoftwareQID':
       
        software_id = instance.external_id.split(' <|> ')[0]
        
        if software_id.split(':')[0] == 'wikidata':
            
            res = query_sparql(wini.format(pl_vars,pl_query.format(software_id.split(':')[-1],'P277'),'100'), wikidata_endpoint)
            for idx, r in enumerate(res):
                if r.get('qid',{}).get('value'): 
                    attribute_object = Attribute.objects.get(uri=f'{BASE_URI}domain/SoftwareProgrammingLanguages')
                    obj, created = Value.objects.update_or_create(
                    project=instance.project,
                    attribute=attribute_object,
                    set_index=instance.set_index,
                    collection_index=idx,
                    defaults={
                              'project': instance.project,
                              'attribute': attribute_object,
                              'external_id': f"wikidata:{res[idx]['qid']['value']} <|> {res[idx]['label']['value']} <|> {res[idx]['quote']['value']}",
                              'text': f"{res[idx]['label']['value']} ({res[idx]['quote']['value']})"
                             }
                    )

        elif software_id.split(':')[0] == 'mardi':
            
            res = query_sparql(mini.format(pl_vars,pl_query.format(software_id.split(':')[-1],P19),'100'), mardi_endpoint) 
            for idx, r in enumerate(res):
                if r.get('qid',{}).get('value'):
                    attribute_object = Attribute.objects.get(uri=f'{BASE_URI}domain/SoftwareProgrammingLanguages')
                    obj, created = Value.objects.update_or_create(
                    project=instance.project,
                    attribute=attribute_object,
                    set_index=instance.set_index,
                    collection_index=idx, 
                    defaults={
                              'project': instance.project,
                              'attribute': attribute_object,
                              'external_id': f"mardi:{res[idx]['qid']['value']} <|> {res[idx]['label']['value']} <|> {res[idx]['quote']['value']}",
                              'text': f"{res[idx]['label']['value']} ({res[idx]['quote']['value']})"
                             }
                    )

    return

@receiver(post_save, sender=Value)
def processor(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/HardwareProcessor':
        try:
            url, label, quote = instance.external_id.split(' <|> ')
            
            # Get "real" URL
            r = requests.get(url)
            tmp = r.text.replace('<link rel="canonical" href="', 'r@ndom}-=||').split('r@ndom}-=||')[-1]
            idx = tmp.find('"/>')
            
            if 'https://en.wikichip.org/wiki/' in tmp[:idx]:
                real_link = tmp[:idx].replace('https://en.wikichip.org/wiki/','')
            else:
                real_link = url.replace('https://en.wikichip.org/wiki/','')
            
            res = query_sparql(wini.format(pro_vars,pro_query.format('P12029',real_link),'1'), wikidata_endpoint)
            
            if res[0]:
                info = 'wikidata:'+res[0]['qid']['value'] + ' <|> ' + res[0]['label']['value'] + ' <|> ' + res[0]['quote']['value']
            else:
                info = real_link + ' <|> ' + label + ' <|> ' + quote
            
            attribute_object = Attribute.objects.get(uri=f'{BASE_URI}domain/HardwareProcessor')
            obj, created = Value.objects.update_or_create(
                project=instance.project,
                attribute=attribute_object,
                set_index=instance.set_index,
                defaults={
                    'project': instance.project,
                    'attribute': attribute_object,
                    'external_id': info
                    }
            )
        except:
            pass

@receiver(post_save, sender=Value)
def RP2RF(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/problem/field-relatant':

        path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
        with open(path, "r") as json_file:
            mathmoddb = json.load(json_file)

        value_editor(instance.project, f'{BASE_URI}domain/problem/field-relation', mathmoddb['containedInField'], None, None, instance.collection_index, 0, instance.set_prefix)


@receiver(post_save, sender=Value)
def RP2MM(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/model/problem-relatant':

        path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
        with open(path, "r") as json_file:
            mathmoddb = json.load(json_file)

        value_editor(instance.project, f'{BASE_URI}domain/model/problem-relation', mathmoddb['models'], None, None, instance.collection_index, 0, instance.set_prefix)


@receiver(post_save, sender=Value)
def T2MM(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/task/model-relatant':

        path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
        with open(path, "r") as json_file:
            mathmoddb = json.load(json_file)

        value_editor(instance.project, f'{BASE_URI}domain/task/model-relation', mathmoddb['appliesModel'], None, None, instance.collection_index, 0, instance.set_prefix)


@receiver(post_save, sender=Value)
def RFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/field/id':
        if instance.text and instance.text != 'not found':
            label, description, _ = extract_parts(instance.text)
            value_editor(instance.project, f'{BASE_URI}domain/field/name', label, None, None, None, 0, instance.set_index)
            value_editor(instance.project, f'{BASE_URI}domain/field/description', description, None, None, None, 0, instance.set_index)
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['researchFieldInformation'].format(f":{Id}"))
                path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
                with open(path, "r") as json_file:
                    mathmoddb = json.load(json_file)
                if results:
                    # Add relations of the Research Field to the Questionnaire
                    idx = 0
                    for prop in ['generalizedByField','generalizesField','similarToField']:
                        if results[0].get(prop, {}).get('value'):
                            fieldIDs = results[0][prop]['value'].split(' / ')
                            fieldLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            fieldDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for fieldID, fieldLabel, fieldDescription in zip(fieldIDs, fieldLabels, fieldDescriptions):
                                value_editor(instance.project, f'{BASE_URI}domain/field/field-relation', None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, instance.set_index)
                                value_editor(instance.project, f'{BASE_URI}domain/field/field-relatant', f"{fieldLabel} ({fieldDescription}) [mathmoddb]", f'mathmoddb:{fieldID}', None, None, idx, instance.set_index)
                                idx += 1

@receiver(post_save, sender=Value)
def RPInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/problem/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            label, description, _ = extract_parts(instance.text)
            value_editor(instance.project, f'{BASE_URI}domain/problem/name', label, None, None, None, 0, instance.set_index)
            value_editor(instance.project, f'{BASE_URI}domain/problem/description', description, None, None, None, 0, instance.set_index)
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['researchProblemInformation'].format(f":{Id}"))
                path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
                with open(path, "r") as json_file:
                    mathmoddb = json.load(json_file)
                if results:
                    # Add related Research Fields to questionnaire
                    idx = 0
                    for prop in ['containedInField']:
                        if results[0].get(prop, {}).get('value'):
                            fieldIDs = results[0][prop]['value'].split(' / ')
                            fieldLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            fieldDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for fieldID, fieldLabel, fieldDescription in zip(fieldIDs, fieldLabels, fieldDescriptions):
                                value_editor(instance.project,f'{BASE_URI}domain/problem/field-relatant', f"{fieldLabel} ({fieldDescription}) [mathmoddb]", f'mathmoddb:{fieldID}', None, idx, 0, instance.set_index)
                                idx += 1
                    # Add related Research Problems to questionnaire
                    idx = 0
                    for prop in ['generalizedByProblem','generalizesProblem','similarToProblem']:
                        if results[0].get(prop, {}).get('value'):
                            problemIDs = results[0][prop]['value'].split(' / ')
                            problemLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            problemDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for problemID, problemLabel, problemDescription in zip(problemIDs, problemLabels, problemDescriptions):
                                value_editor(instance.project, f'{BASE_URI}domain/problem/problem-relation', None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, instance.set_index)
                                value_editor(instance.project, f'{BASE_URI}domain/problem/problem-relatant', f"{problemLabel} ({problemDescription}) [mathmoddb]", f'mathmoddb:{problemID}', None, None, idx, instance.set_index)
                                idx += 1
 
@receiver(post_save, sender=Value)
def MMInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/model/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            label, description, _ = extract_parts(instance.text)
            value_editor(instance.project, f'{BASE_URI}domain/model/name', label, None, None, None, 0, instance.set_index)
            value_editor(instance.project, f'{BASE_URI}domain/model/description', description, None, None, None, 0, instance.set_index)
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['mathematicalModelInformation'].format(f":{Id}"))
                path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
                with open(path, "r") as json_file:
                    mathmoddb = json.load(json_file)
                path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
                with open(path, "r") as json_file:
                    option = json.load(json_file)
                if results:
                    # Add the Mathematical Model Properties to the Questionnaire
                    for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless',
                                                'isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']):
                        if results[0].get(prop, {}).get('value') == 'true':
                            value_editor(instance.project, f'{BASE_URI}domain/model/properties', None, None, Option.objects.get(uri=mathmoddb[prop]), idx, 0, instance.set_index)
                    # Add modelled Research Problems to questionnaire
                    idx = 0
                    for prop in ['models']:
                        if results[0].get(prop, {}).get('value'):
                            modelIDs = results[0][prop]['value'].split(' / ')
                            modelLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            modelDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for modelID, modelLabel, modelDescription in zip(modelIDs, modelLabels, modelDescriptions):
                                value_editor(instance.project,f'{BASE_URI}domain/model/problem-relatant', f"{modelLabel} ({modelDescription}) [mathmoddb]", f'mathmoddb:{modelID}', None, idx, 0, instance.set_index)
                                idx += 1
                    # Add Main Model Information
                    if instance.set_index == 0:
                        value_editor(instance.project, f'{BASE_URI}domain/model/is-main', None, None, Option.objects.get(uri=option['Yes']), None, instance.set_index, None)
                    else:
                        value_editor(instance.project, f'{BASE_URI}domain/model/is-main', None, None, Option.objects.get(uri=option['No']), None, instance.set_index, None)
                    # Add related mathematical models to questionnaire
                    idx = 0
                    for prop in ['generalizedByModel','generalizesModel','discretizedByModel','discretizesModel','containedInModel','containsModel','approximatedByModel',
                                 'approximatesModel','linearizedByModel','linearizesModel','similarToModel']:
                        if results[0].get(prop, {}).get('value'):
                            modelIDs = results[0][prop]['value'].split(' / ')
                            modelLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            modelDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for modelID, modelLabel, modelDescription in zip(modelIDs, modelLabels, modelDescriptions):
                                value_editor(instance.project, f'{BASE_URI}domain/model/model-relation', None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, instance.set_index)
                                value_editor(instance.project, f'{BASE_URI}domain/model/model-relatant', f"{modelLabel} ({modelDescription}) [mathmoddb]", f'mathmoddb:{modelID}', None, None, idx, instance.set_index)
                                idx +=1

@receiver(post_save, sender=Value)
def QQKInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/quantity/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            label, description, _ = extract_parts(instance.text)
            value_editor(instance.project, f'{BASE_URI}domain/quantity/name', label, None, None, None, 0, instance.set_index)
            value_editor(instance.project, f'{BASE_URI}domain/quantity/description', description, None, None, None, 0, instance.set_index)
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['quantityOrQuantityKindInformation'].format(f":{Id}"))
                path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
                with open(path, "r") as json_file:
                    mathmoddb = json.load(json_file)
                path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
                with open(path, "r") as json_file:
                    option = json.load(json_file)
                if results:
                    # Add Type of Quantity
                    if results[0].get('class',{}).get('value'):
                        value_editor(instance.project, f'{BASE_URI}domain/quantity/is-quantity-or-quantity-kind', None, None, Option.objects.get(uri=mathmoddb[results[0]['class']['value']]), None, 0, instance.set_index)
                    # Add the Quantity Properties to the Questionnaire
                    for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless',
                                                'isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']):
                        if results[0].get(prop, {}).get('value') == 'true':
                            value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-properties', None, None, Option.objects.get(uri=mathmoddb[prop]), idx, 0, instance.set_index)
                    # Add the Quantity Kind Properties to the Questionnaire
                    for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless',
                                                'isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']):
                        if results[0].get(prop, {}).get('value') == 'true':
                            value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-kind-properties', None, None, Option.objects.get(uri=mathmoddb[prop]), idx, 0, instance.set_index)
                    # Add related quantities or quantity kinds to questionnaire
                    idx_qq = 0; idx_qkqk = 0; idx_qqk = 0; idx_qkq = 0
                    for prop in ['generalizedByQuantity','generalizesQuantity','approximatedByQuantity','approximatesQuantity','linearizedByQuantity',
                                 'linearizesQuantity','nondimensionalizedByQuantity','nondimensionalizesQuantity','similarToQuantity']:
                        if results[0].get(prop, {}).get('value'):
                            for result in results[0][prop]['value'].split(' / '):
                                quantityID, quantityLabel, quantityDescription, quantityClass = result.split(' | ')
                                if results[0]['class']['value'] == 'Quantity' and quantityClass == 'Quantity':
                                    # If source class is Quantity and target class is quantity
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-to-quantity/relation', None, None, Option.objects.get(uri=mathmoddb[prop]), 0, idx_qq, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-to-quantity/relatant', f"{quantityLabel} ({quantityDescription}) [mathmoddb]", f'mathmoddb:{quantityID}', None, 0, idx_qq, f"{instance.set_index}|0")
                                    idx_qq +=1
                                elif results[0]['class']['value'] == 'QuantityKind' and quantityClass == 'QuantityKind':
                                    # If source class is Quantity and target class is quantity
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-kind-to-quantity-kind/relation', None, None, Option.objects.get(uri=mathmoddb[prop]), 0, idx_qkqk, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-kind-to-quantity-kind/relatant', f"{quantityLabel} ({quantityDescription}) [mathmoddb]", f'mathmoddb:{quantityID}', None, 0, idx_qkqk, f"{instance.set_index}|0")
                                    idx_qkqk +=1
                                elif results[0]['class']['value'] == 'Quantity' and quantityClass == 'QuantityKind':
                                    # If source class is Quantity and target class is quantity
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-to-quantity-kind/relation', None, None, Option.objects.get(uri=mathmoddb[prop]), 0, idx_qqk, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-to-quantity-kind/relatant', f"{quantityLabel} ({quantityDescription}) [mathmoddb]", f'mathmoddb:{quantityID}', None, 0, idx_qqk, f"{instance.set_index}|0")
                                    idx_qqk +=1
                                elif results[0]['class']['value'] == 'QuantityKind' and quantityClass == 'Quantity':
                                    # If source class is Quantity and target class is quantity
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-kind-to-quantity/relation', None, None, Option.objects.get(uri=mathmoddb[prop]), 0, idx_qkq, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/quantity/quantity-kind-to-quantity/relatant', f"{quantityLabel} ({quantityDescription}) [mathmoddb]", f'mathmoddb:{quantityID}', None, 0, idx_qkq, f"{instance.set_index}|0")
                                    idx_qkq +=1

@receiver(post_save, sender=Value)
def MFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/formulation/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            label, description, _ = extract_parts(instance.text)
            value_editor(instance.project, f'{BASE_URI}domain/formulation/name', label, None, None, None, 0, instance.set_index)
            value_editor(instance.project, f'{BASE_URI}domain/formulation/description', description, None, None, None, 0, instance.set_index)
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['mathematicalFormulationInformation'].format(f":{Id}"))
                path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
                with open(path, "r") as json_file:
                    mathmoddb = json.load(json_file)
                path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
                with open(path, "r") as json_file:
                    option = json.load(json_file)
                if results:
                    # Add the Mathematical Model Properties to the Questionnaire
                    for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless',
                                                'isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']):
                        if results[0].get(prop, {}).get('value') == 'true':
                            value_editor(instance.project, f'{BASE_URI}domain/formulation/properties', None, None, Option.objects.get(uri=mathmoddb[prop]), idx, 0, instance.set_index)
                    # Add the defined Quantity
                    if results[0].get('defines', {}).get('value',''):
                        value_editor(instance.project, f'{BASE_URI}domain/formulation/is-definition', None, None, Option.objects.get(uri=option['Yes']), None, 0, instance.set_index)
                        mfIDs = results[0]['defines']['value'].split(' / ')
                        mfLabels = results[0]['definesLabel']['value'].split(' / ')
                        mfDescriptions = results[0]['definesDescription']['value'].split(' / ')
                        for mfID, mfLabel, mfDescription in zip(mfIDs, mfLabels, mfDescriptions):
                            value_editor(instance.project, f'{BASE_URI}domain/formulation/defined-quantity', f"{mfLabel} ({mfDescription}) [mathmoddb]", f'mathmoddb:{mfID}', None, None, 0, instance.set_index)
                    else:
                        value_editor(instance.project, f'{BASE_URI}domain/formulation/is-definition', None, None, Option.objects.get(uri=option['No']), None, 0, instance.set_index)
                    # Add the Formula to the Questionnaire
                    if results[0].get('formulas', {}).get('value',''):
                        formulas = results[0]['formulas']['value'].split(' / ')
                        for idx, formula in enumerate(formulas):
                            value_editor(instance.project, f'{BASE_URI}domain/formulation/formula', formula, None, None, idx, 0, instance.set_index)
                    # Add the Elements to the Questionnaire
                    if results[0].get('terms', {}).get('value',''):
                        terms = results[0]['terms']['value'].split(' / ')
                        qIDs = results[0].get('containsQuantity', {}).get('value','').split(' / ')
                        qLabels = results[0].get('containsQuantityLabel', {}).get('value','').split(' / ')
                        qDescriptions = results[0].get('containsQuantityDescription', {}).get('value','').split(' / ')
                        for idx, term in enumerate(terms):
                            symbol, quantity = splitVariableText(term)
                            for qID, qLabel, qDescription in zip(qIDs, qLabels, qDescriptions):
                                if quantity == qLabel:
                                    #value_editor(instance, 'MathematicalFormulation/Element', None, None, None, None, idx, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/formulation/element-symbol', symbol, None, None, None, idx, f"{instance.set_index}|0")
                                    value_editor(instance.project, f'{BASE_URI}domain/formulation/element-quantity', f"{qLabel} ({qDescription}) [mathmoddb]", f'mathmoddb:{qID}', None, None, idx, f"{instance.set_index}|0")
                    # Add the contained in Model statements
                    idx = 0
                    for prop in ['containedAsAssumptionIn','containedAsFormulationIn','containedAsBoundaryConditionIn','containedAsConstraintConditionIn','containedAsCouplingConditionIn','containedAsInitialConditionIn','containedAsFinalConditionIn']:
                        if results[0].get(f"{prop}MM", {}).get('value'):
                            mmIDs = results[0][f"{prop}MM"]['value'].split(' / ')
                            mmLabels = results[0][f'{prop}MMLabel']['value'].split(' / ')
                            mmDescriptions = results[0][f'{prop}MMDescription']['value'].split(' / ')
                            for mmID, mmLabel, mmDescription in zip(mmIDs, mmLabels, mmDescriptions):
                                value_editor(instance.project, f'{BASE_URI}domain/formulation/model-relation', None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, f"{instance.set_index}|0")
                                value_editor(instance.project, f'{BASE_URI}domain/formulation/model-relatant', f"{mmLabel} ({mmDescription}) [mathmoddb]", f'mathmoddb:{mmID}', None, None, idx, f"{instance.set_index}|0")
                                idx += 1
                    # Add the contained in / contains Formulation statements
                    idx = 0
                    for prop in ['containedAsAssumptionIn','containedAsFormulationIn','containedAsBoundaryConditionIn','containedAsConstraintConditionIn','containedAsCouplingConditionIn','containedAsInitialConditionIn','containedAsFinalConditionIn','containsAssumption','containsFormulation','containsBoundaryCondition','containsConstraintCondition','containsCouplingCondition','containsInitialCondition','containsFinalCondition']:
                        if results[0].get(f"{prop}MF", {}).get('value'):
                            mfIDs = results[0][f"{prop}MF"]['value'].split(' / ')
                            mfLabels = results[0][f'{prop}MFLabel']['value'].split(' / ')
                            mfDescriptions = results[0][f'{prop}MFDescription']['value'].split(' / ')
                            for mfID, mfLabel, mfDescription in zip(mfIDs, mfLabels, mfDescriptions):
                                value_editor(instance.project, f'{BASE_URI}domain/formulation/formulation-relation-1', None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, f"{instance.set_index}|0")
                                value_editor(instance.project, f'{BASE_URI}domain/formulation/formulation-relatant-1', f"{mfLabel} ({mfDescription}) [mathmoddb]", f'mathmoddb:{mfID}', None, None, idx, f"{instance.set_index}|0")
                                idx += 1
                    # Add relations of the Mathematical Model to the Questionnaire
                    idx = 0
                    for prop in ['generalizedByFormulation','generalizesFormulation','discretizedByFormulation','discretizesFormulation','approximatedByFormulation','approximatesFormulation',
                                 'linearizedByFormulation','linearizesFormulation','nondimensionalizedByFormulation','nondimensionalizesFormulation','similarToFormulation']:
                        if results[0].get(prop, {}).get('value'):
                            mfIDs = results[0][prop]['value'].split(' / ')
                            mfLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            mfDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for mfID, mfLabel, mfDescription in zip(mfIDs, mfLabels, mfDescriptions):
                                value_editor(instance.project, f'{BASE_URI}domain/formulation/formulation-relation-2', None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, instance.set_index)
                                value_editor(instance.project, f'{BASE_URI}domain/formulation/formulation-relatant-2', f"{mfLabel} ({mfDescription}) [mathmoddb]", f'mathmoddb:{mfID}', None, None, idx, instance.set_index)
                                idx +=1

@receiver(post_save, sender=Value)
def TInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    if instance and instance.attribute.uri == f'{BASE_URI}domain/task/id':
        if instance.text and instance.text != 'not found':
            # Get Label and Description of Item and add to questionnaire
            label, description, _ = extract_parts(instance.text)
            value_editor(instance.project, f'{BASE_URI}domain/task/name', label, None, None, None, 0, instance.set_index)
            value_editor(instance.project, f'{BASE_URI}domain/task/description', description, None, None, None, 0, instance.set_index)
            # Get source and ID of Item
            source, Id = instance.external_id.split(':')
            if source== 'mathmoddb':
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                results = query_sparql(queryHandler['taskInformation'].format(f":{Id}"))
                path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
                with open(path, "r") as json_file:
                    mathmoddb = json.load(json_file)
                if results:
                    # Add the Task Properties to the Questionnaire
                    for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless',
                                                'isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']):
                        if results[0].get(prop, {}).get('value') == 'true':
                            value_editor(instance.project, f'{BASE_URI}domain/task/properties', None, None, Option.objects.get(uri=mathmoddb[prop]), idx, 0, instance.set_index)
                    # Add the Category to the Questionnaire
                    value_editor(instance.project, f'{BASE_URI}domain/task/category', None, None, Option.objects.get(uri=mathmoddb['ComputationalTask']), None, 0, instance.set_index)
                    # Add applied Model to the Questionnaire
                    idx = 0
                    for prop in ['appliesModel']:
                        if results[0].get(prop, {}).get('value'):
                            modelIDs = results[0][prop]['value'].split(' / ')
                            modelLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            modelDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for modelID, modelLabel, modelDescription in zip(modelIDs, modelLabels, modelDescriptions):
                                value_editor(instance.project,f'{BASE_URI}domain/task/model-relatant', f"{modelLabel} ({modelDescription}) [mathmoddb]", f'mathmoddb:{modelID}', None, idx, 0, instance.set_index)
                                idx += 1
                    # Add Formulations contained in Task
                    idx = 0
                    for prop in ['containsAssumption','containsFormulation','containsBoundaryCondition','containsConstraintCondition','containsCouplingCondition','containsInitialCondition','containsFinalCondition']:
                        if results[0].get(f"{prop}", {}).get('value'):
                            mfIDs = results[0][f"{prop}"]['value'].split(' / ')
                            mfLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            mfDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for mfID, mfLabel, mfDescription in zip(mfIDs, mfLabels, mfDescriptions):
                                value_editor(instance.project, f'{BASE_URI}domain/task/formulation-relation', None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, f"{instance.set_index}|0")
                                value_editor(instance.project, f'{BASE_URI}domain/task/formulation-relatant', f"{mfLabel} ({mfDescription}) [mathmoddb]", f'mathmoddb:{mfID}', None, None, idx, f"{instance.set_index}|0")
                                idx += 1
                    # Add Quantity contained in Task
                    idx = 0
                    for prop in ['containsInput','containsOutput','containsObjective','containsParameter','containsConstant']:
                        if results[0].get(f"{prop}", {}).get('value'):
                            mfIDs = results[0][f"{prop}"]['value'].split(' / ')
                            mfLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            mfDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for mfID, mfLabel, mfDescription in zip(mfIDs, mfLabels, mfDescriptions):
                                value_editor(instance.project, f'{BASE_URI}domain/task/quantity-relation', None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, f"{instance.set_index}|0")
                                value_editor(instance.project, f'{BASE_URI}domain/task/quantity-relatant', f"{mfLabel} ({mfDescription}) [mathmoddb]", f'mathmoddb:{mfID}', None, None, idx, f"{instance.set_index}|0")
                                idx += 1
                    # Add related Task to questionnaire
                    idx = 0
                    for prop in ['generalizedByTask','generalizesTask','discretizedByTask','discretizesTask','containedInTask','containsTask','approximatedByTask',
                                 'approximatesTask','linearizedByTask','linearizesTask','similarToTask']:
                        if results[0].get(prop, {}).get('value'):
                            modelIDs = results[0][prop]['value'].split(' / ')
                            modelLabels = results[0][f'{prop}Label']['value'].split(' / ')
                            modelDescriptions = results[0][f'{prop}Description']['value'].split(' / ')
                            for modelID, modelLabel, modelDescription in zip(modelIDs, modelLabels, modelDescriptions):
                                value_editor(instance.project, f'{BASE_URI}domain/task/task-relation', None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, instance.set_index)
                                value_editor(instance.project, f'{BASE_URI}domain/task/task-relatant', f"{modelLabel} ({modelDescription}) [mathmoddb]", f'mathmoddb:{modelID}', None, None, idx, instance.set_index)
                                idx +=1

def Author_Search(orcid_ids, zbmath_ids, orcid_authors, zbmath_authors):
    '''Function that takes orcid and zbmath ids and queries wikidata and MaRDI Portal to get
       further Information and map orcid and zbmath authors.'''
    
    # Initialize orcid and zbmath dicts   
    author_merged_orcid = {}
    author_merged_zbmath = {}
    
    # Define parameters for author queries
    query_parameters = [(orcid_ids, '496', author_merged_orcid, P22), (zbmath_ids, '1556', author_merged_zbmath, P23)]
    
    # Loop through each set of IDs
    for ids, property_id, author_merged_dict, mardi_property_id in query_parameters:
        if ids:
            
            # Define parameters for author queries to Wikidata and query data
            wikidata_parameter = ["'{}'".format(id_) for id_ in ids]
            wikidata_author_dicts = query_sparql(queryPublication['AuthorViaOrcid'].format(' '.join(wikidata_parameter), property_id), wikidata_endpoint)

            # Sort author data according to the IDs
            for dic in wikidata_author_dicts:
                author_id = dic['authorId']['value']
                author_merged_dict[author_id] = {
                    'wikidata_authorLabel': dic.get('authorLabel', {}).get('value'),
                    'wikidata_authorDescription': dic.get('authorDescription', {}).get('value'),
                    'wikidata_authorQid': dic.get('authorQid', {}).get('value')}
        
            # Define parameters for author queries to MaRDI KG and query data
            mardi_parameter = [["'{}'".format(id_) for id_ in ids], 
                               ["'{}'".format(author_merged_dict[k]['wikidata_authorQid']) for k in author_merged_dict if author_merged_dict[k]['wikidata_authorQid']]]
            
            # Query MaRDI KG for Authors by IDs and Wikidata QID
            mardi_author_dicts_1 = query_sparql(queryPublication['AuthorViaOrcid'].format(' '.join(mardi_parameter[0]), mardi_property_id), mardi_endpoint)
            mardi_author_dicts_2 = query_sparql(queryPublication['AuthorViaWikidataQID'].format(' '.join(mardi_parameter[1]), P2), mardi_endpoint)
        
            # Add QIDs from MaRDI KG to sorted authors 
            for dic in mardi_author_dicts_1:
                author_id = dic['authorId']['value']
                if author_id in author_merged_dict:
                    author_merged_dict[author_id].update({
                        'mardi_authorLabel': dic.get('authorLabel', {}).get('value'),
                        'mardi_authorDescription': dic.get('authorDescription', {}).get('value'),
                        'mardi_authorQid': dic.get('authorQid', {}).get('value')})
        
            for dic in mardi_author_dicts_2:
                wikidata_qid = dic['wikidataQid']['value']
                for author_id, author_data in author_merged_dict.items():
                    if author_data['wikidata_authorQid'] == wikidata_qid:
                        try:
                            author_data.update({
                                'mardi_authorQid': dic['mardiQid']['value'],
                                'mardi_authorLabel': dic['authorLabel']['value'],
                                'mardi_authorDescription': dic['authorDescription']['value']})
                        except KeyError:
                            pass
                            
    # Combine orcid and zbmath Authors, defined by User 
    
    author_dict_merged = {}
    
    for author_id, orcid_id in orcid_authors:
        author_data = {
            'orcid': orcid_id,
            'zbmath': None,
            'wikiQID': author_merged_orcid[orcid_id].get('wikidata_authorQid'),
            'wikiLabel': author_merged_orcid[orcid_id].get('wikidata_authorLabel'),
            'wikiDescription': author_merged_orcid[orcid_id].get('wikidata_authorDescription'),
            'mardiQID': author_merged_orcid[orcid_id].get('mardi_authorQid'),
            'mardiLabel': author_merged_orcid[orcid_id].get('mardi_authorLabel'),
            'mardiDescription': author_merged_orcid[orcid_id].get('mardi_authorDescription')}
        
        author_dict_merged[author_id] = author_data
    
    for author_id, zbmath_id in zbmath_authors:
        score = [0.0, '']
        for author in author_dict_merged:
            s = SequenceMatcher(None, re.sub('[^a-zA-Z ]',' ',author_id), re.sub('[^a-zA-Z ]',' ',author)).ratio()
            if s > score[0]:
                score = [s, author]
        if round(score[0]):
            author_dict_merged[score[1]].update({
                'zbmath': zbmath_id,
                'wikiQID': author_dict_merged[score[1]]['wikiQID'] or author_merged_zbmath[zbmath_id]['wikidata_authorQid'],
                'wikiLabel': author_dict_merged[score[1]]['wikiLabel'] or author_merged_zbmath[zbmath_id]['wikidata_authorLabel'],
                'wikiDescription': author_dict_merged[score[1]]['wikiDescription'] or author_merged_zbmath[zbmath_id]['wikidata_authorDescription'],
                'mardiQID': author_dict_merged[score[1]]['mardiQID'] or author_merged_zbmath[zbmath_id]['mardi_authorQid'],
                'mardiLabel': author_dict_merged[score[1]]['mardiLabel'] or author_merged_zbmath[zbmath_id]['mardi_authorLabel'],
                'mardiDescription': author_dict_merged[score[1]]['mardiDescription'] or author_merged_zbmath[zbmath_id]['mardi_authorDescription']})
        else:
            author_data = {
                'orcid': None,
                'zbmath': zbmath_id,
                'wikiQID': author_merged_zbmath[zbmath_id]['wikidata_authorQid'],
                'wikiLabel': author_merged_zbmath[zbmath_id]['wikidata_authorLabel'],
                'wikiDescription': author_merged_zbmath[zbmath_id]['wikidata_authorDescription'],
                'mardiQID': author_merged_zbmath[zbmath_id]['mardi_authorQid'],
                'mardiLabel': author_merged_zbmath[zbmath_id]['mardi_authorLabel'],
                'mardiDescription': author_merged_zbmath[zbmath_id]['mardi_authorDescription']}
    
            author_dict_merged[author_id] = author_data
    return author_dict_merged
    
def make_api_requests(api, search_objects, dict_merged, prefix):
    req = {}
    for index, search_object in enumerate(search_objects):
        for item in search_object:
            try:
                req.update({index: requests.get(api + '?action=wbsearchentities&format=json&language=en&type=item&limit=10&search={0}'.format(item), 
                                                headers={'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['search'][0]})
            except (KeyError, IndexError):
                pass
    
    properties = ['journal']
    for index, prop in enumerate(properties):
        if index in req:
            display_label = req[index]['display']['label']['value'] if 'display' in req[index] and 'label' in req[index]['display'] else ''
            display_desc = req[index]['display']['description']['value'] if 'display' in req[index] and 'description' in req[index]['display'] else ''
            dict_merged.update({
                '{0}_{1}Qid'.format(prefix, prop): req[index]['id'],
                '{0}_{1}Label'.format(prefix, prop): display_label,
                '{0}_{1}Description1'.format(prefix, prop): display_desc
            })


def add_entity(project, results, kind):
    '''Function that adds the Entities of a query to the Questionnaire'''

    Ids =[]
    Labels = []
    Descriptions = []

    if results[0].get(kind,{}).get('value'):
        entities = results[0][kind]['value'].split(' / ')
        for entity in entities:
            id, label, description = entity.split(' | ')
            if id and label and description:
                if id not in Ids:
                    Ids.append(id)
                    Labels.append(label)
                    Descriptions.append(description)

        for idx, (Id, Label, Description) in enumerate(zip(Ids,Labels,Descriptions)):
            # Set up Qauntity / Quantity Kind Page
            value_editor(project, f'{BASE_URI}domain/{kind}', idx, None, None, None, idx)
            # Add Quantity / Quantity Kind Values
            value_editor(project, f'{BASE_URI}domain/{kind}/id', f'{Label} ({Description}) [mathmoddb]', f"mathmoddb:{Id}", None, None, idx)

    return