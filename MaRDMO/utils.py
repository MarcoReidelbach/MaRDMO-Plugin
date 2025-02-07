import re
import requests
import os
import json
import logging

from django.apps import apps

from rdmo.projects.models import Value
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from multiprocessing.pool import ThreadPool

from .config import BASE_URI, mardi_api, wikidata_api, mathalgodb_endpoint, mathmoddb_endpoint
from .id import *

from .model.sparql import queryProviderMM
from .algorithm.sparql import queryProviderAL

logger = logging.getLogger(__name__)  # Get Django's logger for the current module

def get_questionsAL():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questionsAL

def get_questionsMO():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questionsMO

def get_questionsPU():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questionsPU

def get_id(project, uri, keys):
    values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=uri))
    ids = []
    if len(keys) == 1:
        for value in values:
            ids.append(getattr(value, keys[0]))
    else:
        for value in values:
            id = []
            for key in keys:
                id.append(getattr(value, key))
            ids.append(id)
    return ids 

def add_basics(instance, url_name, url_description):
    label, description, _ = extract_parts(instance.text)
    value_editor(instance.project, url_name, label, None, None, None, 0, instance.set_index)
    value_editor(instance.project, url_description, description, None, None, None, 0, instance.set_index)
    return

def add_entities(project, question_set, question_id, datas, source, prefix):
    # Get Set Ids and IDs of Publications
    set_ids = get_id(project, question_set, ['set_index'])
    value_ids = get_id(project, question_id, ['external_id'])
    # Add Publication to Questionnaire
    idx = max(set_ids, default = -1) + 1
    for data in datas:
        if data.id not in value_ids:
            # Set up Page
            value_editor(project, question_set, f"{prefix}{idx}", None, None, None, idx)
            # Add ID Values
            value_editor(project, question_id, f'{data.label} ({data.description}) [{source}]', f"{data.id}", None, None, idx)
            idx += 1
            value_ids.append(data.id)
    return

def add_relations(project, data, props, mapping, source, set_prefix, relatant, relation = None, suffix = ''):

    idx = 0
    for prop in props:
        for value in getattr(data, f"{prop}{suffix}"):
            if relation:
                collection_index = None
                set_index = idx
                value_editor(project = project, 
                             uri = relation, 
                             option = Option.objects.get(uri=mapping[prop]), 
                             collection_index = collection_index,
                             set_index = set_index, 
                             set_prefix = set_prefix)
            else:
                collection_index = idx
                set_index = 0
            value_editor(project = project, 
                         uri = relatant, 
                         text = f"{value.label} ({value.description}) [{source}]", 
                         external_id = value.id, 
                         collection_index = collection_index,
                         set_index = set_index, 
                         set_prefix = set_prefix)
            idx +=1
    return

def add_properties(project, data, uri, set_prefix):

    for key, value in data.properties.items():
        value_editor(project = project, 
                     uri  = uri, 
                     option = Option.objects.get(uri=value[0]), 
                     collection_index = key,
                     set_index = 0, 
                     set_prefix = set_prefix)
        
def add_references(project, data, uri, set_prefix):

    for key, value in data.reference.items():
        value_editor(project = project, 
                     uri  = uri, 
                     text = value[1],
                     option = Option.objects.get(uri=value[0]), 
                     collection_index = key,
                     set_index = 0, 
                     set_prefix = set_prefix)

def merge_dicts_with_unique_keys(answers, keys):
    
    merged_dict = {}
    
    for key in keys:
        for inner_key, value in answers[key].items():
            new_inner_key = f"{inner_key}{key}"
            merged_dict[new_inner_key] = value    
    
    return merged_dict

def get_new_ids(project, ids, query, endpoint, source):
    '''Request IDs for new MathModDB Items and add them to the Questionnaire'''
    new_ids ={}
    for key, id_value in ids.items():
        # Identify Items missing a MathModDB ID
        if not id_value.startswith(('mathmoddb:','bm:','pr:','so:','al:','pb')):
            # Get MathModDB or MathAlgoDB ID
            results = query_sparql(query.format(f'"{key}"'), endpoint)
            if results and results[0].get('ID', {}).get('value'):
                match = re.match(r"(\d+)(\D+)", id_value)
                if not match:
                    continue
                setID, setName = match.groups()
                # Generate Entry
                value_editor(project, f"{BASE_URI}domain/{setName}/id", f"{key} ({results[0]['quote']['value']}) [{source}]", f"{source}:{results[0]['ID']['value']}", None, None, setID)
                # Store new IDs
                if source == 'mathmoddb':
                    new_ids.update({key: results[0]['ID']['value']})
                elif source == 'mathalgodb':
                    if results[0].get('class', {}).get('value'):
                        if results[0]['class']['value'] == 'algorithm':
                            new_ids.update({key: f"al:{results[0]['ID']['value']}"})
                        elif results[0]['class']['value'] == 'problem':
                            new_ids.update({key: f"pr:{results[0]['ID']['value']}"})
                        elif results[0]['class']['value'] == 'benchmark':
                            new_ids.update({key: f"bm:{results[0]['ID']['value']}"})
                        elif results[0]['class']['value'] == 'software':
                            new_ids.update({key: f"sw:{results[0]['ID']['value']}"})
                        elif results[0]['class']['value'] == 'publication':
                            new_ids.update({key: f"pb:{results[0]['ID']['value']}"})
                        
    return new_ids

def extract_parts(string):
    # Step 1: Split the string at the last occurrence of ') [' to isolate `c` (source)
    parts = string.rsplit(') [', 1)
    if len(parts) == 2:
        main_part, c = parts[0].strip(), parts[1].rstrip(']')
    else:
        main_part, c = parts[0].strip(), ""
    # Step 2: Find the last whitespace outside brackets to split `a` and `b`
    depth = 0
    split_index = -1
    for i, char in enumerate(main_part):
        if char == '(' or char == '[':
            depth += 1
        elif char == ')' or char == ']':
            depth -= 1
        elif char == ' ' and depth == 0:
            split_index = i  # Update split_index to last whitespace outside brackets
    if split_index != -1:
        a = main_part[:split_index].strip()
        b = main_part[split_index+1:].strip().lstrip('(')  # Strip any leading '(' from b
    else:
        a, b = main_part, ""
    return a, b, c

def find_item(label, description, api=mardi_api, language="en"):
    '''API request returning an Item with matching label and description.'''
    data = query_api(api,label)
    # Filter results based on description
    matched_items = [item for item in data if item.get('description') == description]
    if matched_items:
        # Return the ID of the first matching item
        return matched_items[0]['id']
    else:
        # No matching item found
        return None
    
def query_api(api_url, search_term):
    '''API requests returning all Items with matching label'''
    response = requests.get(api_url, params={
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'en',
        'type': 'item',
        'limit': 10,
        'search': search_term
    }, headers={'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'})
    
    if response.status_code == 200:
        try:
            result = response.json().get('search', [])
        except:
            result = []

    return result

def query_sparql(query, endpoint=mathmoddb_endpoint):
    '''SPARQL request returning all Items with matching properties.'''
    if not endpoint:
        logger.warning("SPARQL query attempted without a valid endpoint.")
        return []
    
    try:
        response = requests.post(
            endpoint,
            data=query,
            headers={
                "Content-Type": "application/sparql-query",
                "Accept": "application/sparql-results+json"
            }
        )
        # Check if request was successful
        if response.status_code == 200:
            return response.json().get('results', {}).get('bindings', [])
        else:
            logger.error(f"SPARQL request failed with status {response.status_code}: {response.text}")
            return []

    except requests.exceptions.ConnectionError:
        logger.error(f"SPARQL query failed: Unable to connect to the {endpoint}.")
        return []
    except requests.exceptions.RequestException as e:
        logger.exception(f"SPARQL request failed: {e}")
        return []

def query_sparql_pool(input):
    '''Pooled SPARQL request returning all items with matching properties from different endpoints'''
    pool = ThreadPool(processes=len(input))
    # Map each endpoint's query and store results in a dictionary
    data = {key: result for key, result in zip(input.keys(), pool.map(lambda args: query_sparql(*args), input.values()))}
    return data

def value_editor(project, uri, text=None, external_id=None, option=None, collection_index=None, set_index=None, set_prefix=None):
    '''Add values to the Questionnaire'''
    attribute_object = Attribute.objects.get(uri=uri)
    # Prepare the defaults dictionary
    defaults = {
        'project': project,
        'attribute': attribute_object,
    }

    if text is not None:
        defaults['text'] = text

    if external_id is not None:
        defaults['external_id'] = external_id

    if option is not None:
        defaults['option'] = Option.objects.get(uri=option)

    # Prepare the fields for update_or_create
    update_fields = {
        'project': project,
        'attribute': attribute_object,
        'defaults': defaults
    }

    if collection_index is not None:
        update_fields['collection_index'] = collection_index

    if set_index is not None:
        update_fields['set_index'] = set_index

    if set_prefix is not None:
        update_fields['set_prefix'] = set_prefix

    # Update or create the value
    obj, created = Value.objects.update_or_create(**update_fields)

    return obj, created

def splitVariableText(inputString):
    '''Split inDefiningStatements in Variable and Text'''
    match = re.match(r'(\$.*?\$)\s*,\s*(.*)', inputString)
    if match:
        # Extract the groups: math part and text part
        math_part, text_part = match.groups()
        return math_part, text_part
    else:
        # Handle case where the pattern is not found
        return '', ''
    
def get_data(file_name):
    '''Get Data from JSON File'''
    path = os.path.join(os.path.dirname(__file__), file_name)
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data

def query_sources(search, queryID, sources, notFound=True):
        '''Helper function to query specified sources and process results.'''
        
        source_functions = {
            'wikidata': lambda s: query_api(wikidata_api, s),
            'mardi': lambda s: query_api(mardi_api, s),
            'mathmoddb': lambda s: MathDBProvider(s, queryProviderMM[queryID], 'mathmoddb'),
            'mathalgodb': lambda s: MathDBProvider(s, queryProviderAL[queryID], 'mathalgodb')
        }

        # Filter only specified sources
        queries = [source_functions[source] for source in sources if source in source_functions]

        # Use ThreadPool to make concurrent API requests
        pool = ThreadPool(processes=len(queries))

        results = pool.map(lambda func: func(search), queries)

        # Unpack results based on available sources
        results_dict = dict(zip(sources, results))

        # Process results to fit RDMO Provider Output Requirements
        options = []
        
        if 'mathmoddb' in results_dict:
            options += results_dict['mathmoddb'][:10]

        if 'mathalgodb' in results_dict:
            options += results_dict['mathalgodb'][:10]

        if 'mardi' in results_dict:
            options += [process_result(result, 'mardi') for result in results_dict['mardi'][:10]]

        if 'wikidata' in results_dict:
            options += [process_result(result, 'wikidata') for result in results_dict['wikidata'][:10]]

        if notFound:
            options = [{'id': 'not found', 'text': 'not found'}] + options

        return options

def MathDBProvider(search, query, source):
    """
    Dynamic query of MathAlgoDB, results as options for Provider.
    """
    if not search:
        return []

    # Fetch results from the MathAlgoDB knowledge graph
    results = query_sparql(query, mathalgodb_endpoint if source == 'mathalgodb' else mathmoddb_endpoint if source == 'mathmoddb' else '')
    dic = {}
    options = []
    
    # Store results in dict
    for result in results:
        dic.update({result['label']['value']:{'id':result['id']['value'], 'quote':result['quote']['value']}})

    # Filter results by user-defined search
    options.extend([{'id': f"{source}:{dic[key]['id']}", 'text': f'{key} ({dic[key]["quote"]}) [{source}]'} for key in dic if search.lower() in key.lower()])

    return options

def process_result(result, location):
    '''Function to process the result and return a dictionary with id, text, and description.'''
    return {
         'id': f"{location}:{result['id']}",
         'text': f"{result['display']['label']['value']} ({result['display'].get('description', {}).get('value', 'No Description Provided!')}) [{location}]"
    }

def query_sources_with_user_additions(search, project, queryID, queryAttribute, sources = ['mathmoddb']):
    '''Fetch options from MathModDB, user-defined fields, and other sources.'''

    # Query sources and get the results directly in options
    try:
        options = query_sources(search, queryID, sources, False)
    except:
        options = []

    # Fetch user-defined research fields from the project
    values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{queryAttribute}/id'))
    values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{queryAttribute}/name'))
    values3 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{queryAttribute}/description'))
    
    # Process user-defined research fields
    dic = {}
    for idx, (value1, value2, value3) in enumerate(zip(values1, values2, values3)):
        source = label = description = None
        if value1.text:
            if value1.text == 'not found':
                # User-Defined Cases
                label = value2.text or "No Label Provided!"
                description = value3.text or "No Description Provided!"
                source = 'user'
            elif 'mathmoddb' not in value1.text:
                # ID Cases
                label, description, source = extract_parts(value1.text)
        if source not in sources:
            dic[f"{label} ({description}) [{source}]"] = {'id': f"{source}:{idx}"}
            
    # Add the user-defined options to the list, filtered by search
    options.extend([{'id': f"{dic[key]['id']}", 'text': key} for key in dic if search.lower() in key.lower()])

    # Return combined, sorted options
    return sorted(options, key=lambda option: option['text'])

def entityRelations(data, fromIDX, toIDX, relationOld, entityOld, relationNew, enc, no=2):

    # Ensure toIDX and enc are lists
    if not isinstance(toIDX, list):
        toIDX = [toIDX]
    if not isinstance(enc, list):
        enc = [enc]

    # Create mappings for all toIDX lists
    label_to_index_maps = []
    for toIDX_entry in toIDX:
        label_to_index_maps.append({data[toIDX_entry][k].get('Name'): idx for idx, k in enumerate(data.get(toIDX_entry, {}))})

    # Use Template or Ressource Label
    for from_entry in data.get(fromIDX, {}).values():
        for key in from_entry.get(relationOld, {}):
            if from_entry[entityOld].get(key):
                Id, label = from_entry[entityOld][key].split(' <|> ')[:2]
                
                match_found = False
                for enc_entry, label_to_index in zip(enc, label_to_index_maps):
                    if label in label_to_index:
                        idx = label_to_index[label]
                        match_found = True
                        if no == 2:
                            if [from_entry[relationOld][key], f'{enc_entry}{idx+1}'] not in from_entry.get(relationNew, {}).values():
                                from_entry.setdefault(relationNew, {}).update({key: [from_entry[relationOld][key], f'{enc_entry}{idx+1}']})
                        else:
                            if [from_entry[relationOld][key], idx+1, f'{enc_entry}{idx+1}'] not in from_entry.get(relationNew, {}).values():
                                from_entry.setdefault(relationNew, {}).update({key: [from_entry[relationOld][key], idx+1, f'{enc_entry}{idx+1}']})
                        break
                
                if not match_found:
                    if no == 2:
                        if [from_entry[relationOld][key], Id] not in from_entry.get(relationNew, {}).values():
                            from_entry.setdefault(relationNew, {}).update({key: [from_entry[relationOld][key], Id]})
                    else:
                        if [from_entry[relationOld][key], Id, Id] not in from_entry.get(relationNew, {}).values():
                            from_entry.setdefault(relationNew, {}).update({key: [from_entry[relationOld][key], Id, Id]})
    return
