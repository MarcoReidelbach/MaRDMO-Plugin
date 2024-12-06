import re, os, json
import requests

from django.dispatch import receiver
from django.db.models.signals import post_save

from rdmo.projects.models import Value
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from .utils import query_sparql, query_sparql_pool, value_editor, extract_parts, splitVariableText
from .sparql import queryPublication, queryModelHandler, queryHandler, wini, mini, pl_query, pl_vars, pro_query, pro_vars
from .id import *
from .config import wd, wdt, mardi_endpoint, wikidata_endpoint, mathmoddb_endpoint, BASE_URI, crossref_api, datacite_api, doi_api
from .models import Author, Journal, Publication
from multiprocessing.pool import ThreadPool


from difflib import SequenceMatcher

@receiver(post_save, sender=Value)
def PInformation(sender, **kwargs): 

    instance = kwargs.get("instance", None)

    if instance and instance.attribute.uri == f"{BASE_URI}domain/publication/get-details":

        path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
        with open(path, "r") as json_file:
            option = json.load(json_file)

        path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')
        with open(path, "r") as json_file:
            mathmoddb = json.load(json_file)
        
        # Source of Information
        getDetails = instance.external_id

        # Autmatic or manual Search
        automatic_or_manual = index_check(instance,'option',f'{BASE_URI}domain/publication/automatic-or-manual')
        if automatic_or_manual == Option.objects.get(uri=option['User']):
            return
        
        # Citation already in Questionnaire?
        publication_id = index_check(instance,'text',f'{BASE_URI}domain/publication/id')
        if publication_id:
            return

        # ID of Publication
        publication_id = index_check(instance,'text',f'{BASE_URI}domain/publication/doi').split(':')
        if len(publication_id) == 1:
            return
        else:
            prefix = publication_id[0]
            if prefix == 'doi':
                DOI = publication_id[1]
            elif prefix == 'url':
                URL = publication_id[1]            

        if re.match(r'10.\d{4,9}/[-._;()/:a-z0-9A-Z]+', DOI):

            choice = None
            
            # Define MaRDI Portal / Wikidata / MathModDB / MathAlgoDB SPARQL Queries
            mardi_query = queryPublication['All_MaRDI'].format(P16, DOI.upper(), P8, P22, P4, P12, P10, P7, P9, P11, P13, P14, P15, P2, P23, wdt, wd)
            wikidata_query = queryPublication['All_Wikidata'].format('356', DOI.upper(), '50', '496', '31', '1433', '407', '1476', '2093', '577', '478', '433', '304', '', '1556')
            mathmoddb_query = queryPublication['PublicationMathModDB'].format(DOI)
            mathalgodb_query = queryPublication['PublicationMathAlgoDB'].format(DOI)
            
            # Get Citation Data from MaRDI Portal / Wikidata / MathModDB / MathAlgoDB
            results = {}
            if getDetails == '0':
                results = query_sparql_pool({'mathmoddb':(mathmoddb_query, mathmoddb_endpoint)})
            elif getDetails == '1':
                results = query_sparql_pool({'mathalgodb':(mathalgodb_query, mathmoddb_endpoint)})
            elif getDetails == '2':
                results = query_sparql_pool({'wikidata':(wikidata_query, wikidata_endpoint), 'mardi':(mardi_query, mardi_endpoint)})
            elif getDetails == '3':
                results = query_sparql_pool({'wikidata':(wikidata_query, wikidata_endpoint), 'mardi':(mardi_query, mardi_endpoint), 'mathmoddb':(mathmoddb_query, mathmoddb_endpoint), 'mathalgodb':(mathalgodb_query, mathmoddb_endpoint)})

            # Structure Publication Information            
            publication = {}
            for key in ['mardi', 'wikidata', 'mathmoddb', 'mathalgodb']:
                try:
                    publication[key] = Publication.from_query(results.get(key))
                except:
                    publication[key] = None
 
            if not (publication['mardi'] or publication['wikidata']) and getDetails == '3':
                
                # If no Citation Data in KGs and additional sources requested by User, get Citation Information from CrossRef, DataCite, DOI, zbMath 
                pool = ThreadPool(processes=4)
                results = pool.map(lambda fn: fn(DOI), [get_crossref_data, get_datacite_data, get_doi_data, get_zbmath_data])
                
                for idx, source in enumerate(['crossref', 'datacite', 'doi', 'zbmath']):
                    try:
                        publication[source] = Publication.from_crossref(results[idx])
                    except:
                        publication[source] = None

                # Get Authors assigned to publication from ORCID
                publication['orcid'] = {}
                response = get_orcids(DOI)
                if response.status_code == 200:
                    orcids = response.json().get('result')
                    if orcids:
                        for idx, entry in enumerate(orcids):
                            orcid_id = entry.get('orcid-identifier', {}).get('path', '')
                            response = get_author_by_orcid(orcid_id)
                            if response.status_code == 200:
                                orcid_author = response.json()
                                publication['orcid'][idx] = Author.from_orcid(orcid_author)

                # Add (missing) ORCID IDs to authors
                for choice in ['zbmath', 'crossref', 'datacite', 'doi']:
                    if publication[choice]:
                        assign_orcid(publication, choice)
                        break
                else:
                    choice = None
                
                # Additional for chosen information source
                if choice:
                    # Check if Authors already in MaRDI Portal or Wikidata
                    orcid_id = ' '.join(f'"{author.orcid_id}"' if author.orcid_id else '""' for author in publication[choice].authors)
                    zbmath_id = ' '.join(f'"{author.zbmath_id}"' if author.zbmath_id else '""' for author in publication[choice].authors)
                    if orcid_id and zbmath_id:
                        additional_queries(publication, choice, 'authors', [orcid_id, zbmath_id, P22, P23, P2], [orcid_id, zbmath_id, '496', '1556', ''], extract_authors)
                    # Check if Journal already in MaRDI Portal or Wikidata
                    journal_id = publication[choice].journal[0].issn
                    if journal_id:
                        additional_queries(publication, choice, 'journal', [journal_id, P33], [journal_id, '236'], extract_journals)
            
            # Add Citation Information to Questionnaire
            if getDetails == '0':
                cit = publication['mathmoddb']
                if cit:
                    value_editor(instance.project, f'{BASE_URI}domain/publication/id', f"{cit.label} ({cit.description}) [mathmoddb]" if cit.id else 'not found', cit.id if cit.id else 'not found', None, None, 0, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/name', cit.label if cit.label else None, None, None, None, 0, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/description', cit.description if cit.description else None, None, None, None, 0, instance.set_index)
                else:
                    value_editor(instance.project, f'{BASE_URI}domain/publication/id', 'not found', None, None, None, 0, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/name', None, None, None, None, 0, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/description', None, None, None, None, 0, instance.set_index)
            elif getDetails == '1':
                cit = publication['mathalgodb']
                if cit:  
                    value_editor(instance.project, f'{BASE_URI}domain/publication/id', f"{cit.label} ({cit.description}) [mathalgodb]" if cit.id else 'not found', cit.id if cit.id else 'not found', None, None, 0, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/name', cit.label if cit.label else None, None, None, None, 0, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/description', cit.description if cit.description else None, None, None, None, 0, instance.set_index)
                else:
                    value_editor(instance.project, f'{BASE_URI}domain/publication/id', 'not found', None, None, None, 0, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/name', None, None, None, None, 0, instance.set_index)
                    value_editor(instance.project, f'{BASE_URI}domain/publication/description', None, None, None, None, 0, instance.set_index)       
            elif getDetails == '2' or getDetails == '3':
                
                # Choose existing Citation Information from appropriate source 
                cit = publication.get('mardi') or publication.get('wikidata') or publication.get(choice) or None

                if cit:
                    if cit.id:
                        # Add ID to Questionnaire
                        value_editor(instance.project, f'{BASE_URI}domain/publication/id', f"{cit.label} ({cit.description}) [{cit.id.split(':')[0]}]", cit.id, None, None, 0, instance.set_index)
                        value_editor(instance.project, f'{BASE_URI}domain/publication/name', cit.label if cit.label else None, None, None, None, 0, instance.set_index)
                        value_editor(instance.project, f'{BASE_URI}domain/publication/description', cit.description if cit.description else None, None, None, None, 0, instance.set_index)
                    elif publication['mathmoddb']:
                        value_editor(instance.project, f'{BASE_URI}domain/publication/id', f"{publication['mathmoddb'].label} ({publication['mathmoddb'].description}) [mathmoddb]", publication['mathmoddb'].id, None, None, 0, instance.set_index)
                        value_editor(instance.project, f'{BASE_URI}domain/publication/name', publication['mathmoddb'].label if publication['mathmoddb'].label else None, None, None, None, 0, instance.set_index)
                        value_editor(instance.project, f'{BASE_URI}domain/publication/description', publication['mathmoddb'].description if publication['mathmoddb'].description else None, None, None, None, 0, instance.set_index)
                    elif publication['mathalgodb']:
                        value_editor(instance.project, f'{BASE_URI}domain/publication/id', f"{publication['mathalgodb'].label} ({publication['mathalgodb'].description}) [mathalgodb]", publication['mathalgodb'].id, None, None, 0, instance.set_index)
                        value_editor(instance.project, f'{BASE_URI}domain/publication/name', publication['mathalgodb'].label if publication['mathalgodb'].label else None, None, None, None, 0, instance.set_index)
                        value_editor(instance.project, f'{BASE_URI}domain/publication/description', publication['mathalgodb'].description if publication['mathalgodb'].description else None, None, None, None, 0, instance.set_index)
                    else:
                        value_editor(instance.project, f'{BASE_URI}domain/publication/id', "not found", "not found", None, None, 0, instance.set_index)
                        value_editor(instance.project, f'{BASE_URI}domain/publication/name', None, None, None, None, 0, instance.set_index)
                        value_editor(instance.project, f'{BASE_URI}domain/publication/description', None, None, None, None, 0, instance.set_index)
                    # Add Publication Type to Questionnaire
                    value_editor(instance.project, f'{BASE_URI}domain/publication/type', None, None, Option.objects.get(uri=option['ScholarlyArticle']) if cit.entrytype == 'scholarly article' else Option.objects.get(uri=option['GeneralPublication']), None, 0, instance.set_index)
                    # Add Publication Title to Questionnaire
                    value_editor(instance.project, f'{BASE_URI}domain/publication/title', cit.title if cit.title else '', None, None, None, 0, instance.set_index)
                    # Add Authors to Questionnaire
                    for idx, author in enumerate(cit.authors):
                        value_editor(instance.project, f'{BASE_URI}domain/publication/author', f"{author.label} [{', '.join(([author.id] if author.id else []) + [f'{pre}:{suf}' for pre, suf in {'orcid': author.orcid_id, 'zbmath': author.zbmath_id}.items() if suf])}]" if any([author.id, author.orcid_id, author.zbmath_id]) else author.label, author.id if author.id else None, None, idx, 0, instance.set_index)
                    # Add Language to Questionnaire
                    value_editor(instance.project, f'{BASE_URI}domain/publication/language', None, None, Option.objects.get(uri=cit.language) if cit.language else None, None, 0, instance.set_index)
                    # Add Journal of the Publication
                    for journal in cit.journal:
                        value_editor(instance.project, f'{BASE_URI}domain/publication/journal', f"{journal.label} ({journal.description}) [{journal.id}]" if journal.id else f"{journal.label} (issn:{journal.issn})" if journal.label and journal.issn else '', journal.id if journal.id else None, None, None, 0, instance.set_index)
                    # Add Volume of the publication
                    value_editor(instance.project, f'{BASE_URI}domain/publication/volume', cit.volume if cit.volume else '', None, None, None, 0, instance.set_index)
                    # Add Issue of the Publication
                    value_editor(instance.project, f'{BASE_URI}domain/publication/issue', cit.issue if cit.issue else '', None, None, None, 0, instance.set_index)
                    # Add Pages of the Publication
                    value_editor(instance.project, f'{BASE_URI}domain/publication/page', cit.page if cit.page else '', None, None, None, 0, instance.set_index)
                    # Add Publication Date
                    value_editor(instance.project, f'{BASE_URI}domain/publication/date', cit.date if cit.date else '', None, None, None, 0, instance.set_index)
                else:
                    value_editor(instance.project, f'{BASE_URI}domain/publication/id', 'not found', None, None, None, 0, instance.set_index)

            # Add relations for publications from MathModDB
            if getDetails == '0':
                Ids = []
                idx = 0
                for property in ['documents', 'invents', 'studies', 'surveys', 'uses']:
                    if results['mathmoddb'][0].get(property, {}).get('value'):
                        entities = results['mathmoddb'][0][property]['value'].split(' / ')
                        for entity in entities:
                            id, label, description = entity.split(' | ')
                            if id and label and description:
                                if id not in Ids:
                                    value_editor(instance.project, f'{BASE_URI}domain/publication/entity-relation', None, None, Option.objects.get(uri=mathmoddb[property]), None, idx, instance.set_index)
                                    value_editor(instance.project, f'{BASE_URI}domain/publication/entity-relatant', f"{label} ({description}) [mathmoddb]", f'{id}', None, None, idx, instance.set_index)    
                                    Ids.append(id)

        elif URL:
            return

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

            # Add Publication Information to Questionnaire
            add_entity(instance.project, results, 'publication')

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
                print(results)
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
    DOIs = []

    if kind == 'publication':

        path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
        with open(path, "r") as json_file:
            option = json.load(json_file)

        if results[0].get(kind,{}).get('value'):
            entities = results[0][kind]['value'].split(' / ')
            for entity in entities:
                DOIs.append(entity)

        for idx, DOI in enumerate(DOIs):
                # Set up Page
                value_editor(project, f'{BASE_URI}domain/{kind}', idx, None, None, None, idx)
                # Add DOI Values
                value_editor(project, f'{BASE_URI}domain/{kind}/doi', f"doi:{DOI}", None, None, None, idx)
                # Add MaRDMO for further Information
                value_editor(project, f'{BASE_URI}domain/{kind}/automatic-or-manual', None, None, Option.objects.get(uri=option['MaRDMO']), None, idx)
                # Add MathModDB as Source
                value_editor(project, f'{BASE_URI}domain/{kind}/get-details', 'MathModDB Knowledge Graph', '0', None, None, idx)

    else:
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
                # Set up Page
                value_editor(project, f'{BASE_URI}domain/{kind}', idx, None, None, None, idx)
                # Add ID Values
                value_editor(project, f'{BASE_URI}domain/{kind}/id', f'{Label} ({Description}) [mathmoddb]', f"mathmoddb:{Id}", None, None, idx)

    return

def get_crossref_data(doi):
    return requests.get(f'{crossref_api}{doi}')

def get_datacite_data(doi):
    return requests.get(f'{datacite_api}{doi}')

def get_doi_data(doi):
    return requests.get(f'{doi_api}{doi}', headers={"accept": "application/json"})

def get_zbmath_data(doi):
    return requests.get(f'https://api.zbmath.org/v1/document/_structured_search?page=0&results_per_page=100&external%20id={doi}')

def get_orcids(doi):
    return requests.get(f'https://pub.orcid.org/v3.0/search/?q=doi-self:{doi}', headers={'Accept': 'application/json'})

def get_author_by_orcid(orcid_id):
    return requests.get(f'https://pub.orcid.org/v3.0/{orcid_id}/personal-details', headers={'Accept': 'application/json'})

def assign_orcid(publication, source, id='orcid'):
    for author in publication[source].authors:
        if not author.orcid_id:
            for id_author in publication[id].values():
                if author.label == id_author.label:
                    author.orcid_id = id_author.orcid_id

def assign_id(entities, target, prefix):
    for entity in entities:
        if not entity.id:
            for id_entity in target.values():
                if entity.label == id_entity.label:
                    entity.id = f"{prefix}:{id_entity.id}"
                    entity.label = id_entity.label
                    entity.description = id_entity.description

def extract_authors(data):
    authors = {}
    if data:
        for idx, entry in enumerate(data[0].get('authorInfos', {}).get('value', '').split(" | ")):
            if entry:
                authors[idx] = Author.from_query(entry)
    return authors

def extract_journals(data):
    journals = {}
    if data:
        for idx, entry in enumerate(data[0].get('journalInfos', {}).get('value', '').split(" | ")):
            if entry:
                journals[idx] = Journal.from_query(entry)
    return journals

def additional_queries(publication, choice, key, mardi_parameter, wikidata_parameter, function):
    '''Additional MaRDI Portal and Wikidata SPARQL Queries instance like authors or journals'''
    mardi_query = queryPublication[key].format(*mardi_parameter)
    wikidata_query = queryPublication[key].format(*wikidata_parameter)
    # Get Journal Information from MaRDI Portal / Wikidata
    results = query_sparql_pool({'wikidata':(wikidata_query, wikidata_endpoint), 'mardi':(mardi_query, mardi_endpoint)})
    mardi_info = function(results['mardi'])
    wikidata_info = function(results['wikidata'])
    # Add (missing) MaRDI Portal / Wikidata IDs to authors
    assign_id(getattr(publication[choice],key), mardi_info, 'mardi')
    assign_id(getattr(publication[choice],key), wikidata_info, 'wikidata')

def index_check(instance,key,uri):
    '''Get value with similar index as instance value'''
    index_value = ''
    values = instance.project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=uri))
    for value in values:
        if value.set_index == instance.set_index:
            index_value = getattr(value,key)
            break
    return index_value
