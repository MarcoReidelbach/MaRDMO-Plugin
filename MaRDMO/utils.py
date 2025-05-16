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

from .config import BASE_URI, endpoint

from .algorithm.sparql import queryProviderAL

logger = logging.getLogger(__name__)  # Get Django's logger for the current module

def get_questionsWO():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questionsWO

def get_questionsAL():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questionsAL

def get_questionsMO():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questionsMO

def get_questionsPU():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questionsPU

def get_questionsSE():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questionsSE

def get_id(project, uri, keys):
    values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=uri))
    ids = []
    if len(keys) == 1:
        for value in values:
            id = getattr(value, keys[0])
            if isinstance(id, str) and '|' in id:
                id = id.split('|')[0]
            ids.append(id)
    else:
        for value in values:
            id = []
            for key in keys:
                id.append(getattr(value, key))
            ids.append(id)
    return ids 

def add_basics(project, text, url_name, url_description, collection_index = None, set_index = None, set_prefix = None):
    label, description, source = extract_parts(text)
    value_editor(project, url_name, label, None, None, collection_index, set_index, set_prefix)
    value_editor(project, url_description, description, None, None, collection_index, set_index, set_prefix)
    return label, description, source

def add_entities(project, question_set, question_id, datas, source, prefix):
    # Get Name and Description URL
    question_name = f'{question_id.rsplit("/", 1)[0]}/name'
    question_description = f'{question_id.rsplit("/", 1)[0]}/description'
    # Get Set Ids and IDs of Publications
    set_ids = get_id(project, question_set, ['set_index'])
    value_ids = get_id(project, question_id, ['external_id'])
    texts = get_id(project, question_id, ['text'])
    names = get_id(project, question_name, ['text'])
    descriptions = get_id(project, question_description, ['text'])
    # Add Publication to Questionnaire
    idx = max(set_ids, default = -1) + 1
    for data in datas:
        if data.id not in value_ids and not any(f'{data.label} ({data.description})' in text for text in texts) and not any(f'{data.label} ({data.description})' in f'{name} ({description})' for name, description in zip(names, descriptions)):
            # Set up Page
            value_editor(project, question_set, f"{prefix}{idx}", None, None, None, idx)
            # Add ID Values
            value_editor(project, question_id, f'{data.label} ({data.description}) [{source}]', f"{data.id}", None, None, idx)
            idx += 1
            value_ids.append(data.id)
    return

def add_new_entities(project, question_set, question_id, datas, source, prefix):
    # Get Name and Description URL
    question_name = f'{question_id.rsplit("/", 1)[0]}/name'
    question_description = f'{question_id.rsplit("/", 1)[0]}/description'
    # Get Set Ids and IDs of Publications
    set_ids = get_id(project, question_set, ['set_index'])
    names = get_id(project, question_name, ['text'])
    descriptions = get_id(project, question_description, ['text'])
    # Add Publication to Questionnaire
    idx = max(set_ids, default = -1) + 1
    for data in datas:
        if not any(f'{data.label} ({data.description})' in f'{name} ({description})' for name, description in zip(names, descriptions)):
            # Set up Page
            value_editor(project, question_set, f"{prefix}{idx}", None, None, None, idx)
            # Add ID Values
            value_editor(project, question_id, 'not found', 'not found', None, None, idx)
            # Add Name Values
            value_editor(project, question_name, data.label, None, None, None, None, idx)
            # Add Description Values
            value_editor(project, question_description, data.description, None, None, None, None, idx)
            idx += 1
    return

def add_relations(project, data, props, set_prefix, relatant, mapping=None, relation=None, suffix='', assumption=None):
    # Get Set Ids and IDs of Entities
    set_ids = get_id(project, relatant, ['set_prefix'])
    set_ids2 = get_id(project, relatant, ['set_index'])
    #set_ids2 = get_id(project, relatant, ['set_index'])
    collection_ids = get_id(project, relatant, ['collection_index'])
    value_ids = get_id(project, relatant, ['external_id'])
    texts = get_id(project, relatant, ['text'])
    if relation:
        rels = get_id(project, relation, ['option_uri'])
    
    # Reduce Set Prefix
    set_prefix_reduced = set_prefix if isinstance(set_prefix, int) else int(set_prefix.split('|')[0])
    ids = [set_id2 for set_id2, set_id in zip(set_ids2, set_ids) if set_id == set_prefix_reduced]

    # Set initial value of counter
    idx = int(max(ids if relation else collection_ids, default=-1)) + 1

    # Add Relations and Relatants
    for prop in props:
        for value in getattr(data, f"{prop}{suffix}"):
            if relation:
                if any(value.id == value_id and int(set_id) == set_prefix_reduced and rel == mapping[prop] for value_id, set_id, rel in zip(value_ids, set_ids, rels)):
                    continue  
            else:
                if any(value.id == value_id and int(set_id) == set_prefix_reduced for value_id, set_id in zip(value_ids, set_ids)):
                    continue  

            # Determine Indices and add relation
            if relation:
                collection_index, set_index = None, idx
                value_editor(project = project, 
                             uri = relation, 
                             option = Option.objects.get(uri=mapping[prop]), 
                             collection_index = collection_index, 
                             set_index = set_index, 
                             set_prefix = set_prefix)
            else:
                collection_index, set_index = idx, 0

            # Get source of Relatant
            source, _ = value.id.split(':')

            text_entry = f"{value.label} ({value.description})"
            existing_index = None
            if not relation:
                existing_index = next((IDX for IDX, (text, set_id) in enumerate(zip(texts, set_ids)) if set_id == set_prefix and text_entry in text), None)
                collection_index = existing_index if existing_index is not None else idx

            # Add Relatant
            value_editor(
                project=project, 
                uri=relatant, 
                text=f"{text_entry} [{source}]",
                external_id=value.id, 
                collection_index=collection_index,
                set_index=set_index, 
                set_prefix=set_prefix
                )
            
            # Add Assumption
            if assumption and hasattr(value, 'qualifier') and value.qualifier:
                for assumption_idx, ivalue in enumerate(value.qualifier.split(' <|> ')):
                    
                    assumption_id, assumption_label, assumption_description = ivalue.split(' | ')
                    
                    assumption_source, _ = assumption_id.split(':')
                    assumption_text = f"{assumption_label} ({assumption_description})"
                    
                    value_editor(
                        project=project, 
                        uri=assumption, 
                        text=f"{assumption_text} [{assumption_source}]",
                        external_id=assumption_id, 
                        collection_index=assumption_idx,
                        set_index=set_index, 
                        set_prefix=set_prefix
                        )
                    
            if existing_index is None:
                # Only increment if a new entry was added
                idx += 1  

            value_ids.append(value.id)
            set_ids.append(set_prefix_reduced)
            texts.append(f"{text_entry} [{source}]")
            if relation:
                rels.append(mapping[prop])
    return

def add_properties(project, data, uri, set_prefix):

    for key, value in data.properties.items():
        value_editor(project = project, 
                     uri  = uri, 
                     option = Option.objects.get(uri=value[0]), 
                     collection_index = key,
                     set_index = 0, 
                     set_prefix = set_prefix)
    return
        
def add_references(project, data, uri, set_index = 0, set_prefix = None):

    for key, value in data.reference.items():
        value_editor(project = project, 
                     uri  = uri, 
                     text = value[1],
                     option = Option.objects.get(uri=value[0]), 
                     collection_index = key,
                     set_index = set_index, 
                     set_prefix = set_prefix)
    return

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

def find_item(label, description, api = endpoint['mardi']['api']):
    '''API request returning an Item with matching label and description.'''
    # Check description
    description = description if description and description != 'No Description Provided!' else ''
    # Get Data
    data = query_api(api,label)
    # Filter results based on description
    matched_items = [item for item in data if item.get('description', '') == description]
    if matched_items:
        # Return the ID of the first matching item
        return matched_items[0]['id']
    else:
        # No matching item found
        return None

def query_api(api_url, search_term, timeout=5):
    """API requests returning all Items with matching label."""
    try:
        response = requests.get(
            api_url,
            params={
                'action': 'wbsearchentities',
                'format': 'json',
                'language': 'en',
                'type': 'item',
                'limit': 10,
                'search': search_term
            },
            headers={'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'},
            timeout=timeout
        )
        response.raise_for_status()  # Raise an error on bad HTTP status codes
        try:
            return response.json().get('search', [])
        except ValueError:
            # Malformed JSON
            logger.error("Failed to parse JSON.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed due to {e}")

    return []

def query_sparql(query, endpoint):
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
            'wikidata': lambda s: query_api(endpoint['wikidata']['api'], s),
            'mardi': lambda s: query_api(endpoint['mardi']['api'], s),
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
        
        if 'mathalgodb' in results_dict:
            options += results_dict['mathalgodb'][:15]

        if 'mardi' in results_dict:
            options += [process_result(result, 'mardi') for result in results_dict['mardi'][:15]]

        if 'wikidata' in results_dict:
            options += [process_result(result, 'wikidata') for result in results_dict['wikidata'][:15]]

        if notFound:
            options = [{'id': 'not found', 'text': 'not found'}] + options
        return options

def MathDBProvider(search, query, source):
    """
    Dynamic query of MathModDB and MathAlgoDB, results as options for Provider.
    """
    if not search:
        return []

    # Fetch results from the MathAlgoDB knowledge graph
    results = query_sparql(query, endpoint['mathalgodb']['sparql'] if source == 'mathalgodb' else endpoint['mathmoddb']['sparql'] if source == 'mathmoddb' else '')
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

def query_sources_with_user_additions(search, project, queryID, queryAttribute, sources = ['mathmoddb'], user = False):
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
                id = idx
                source = 'user'
            else:
                # ID Cases
                label, description, source = extract_parts(value1.text)
                _, id = value1.external_id.split(':')
        if source not in sources:
            if source == 'user':
                dic[f"{label} ({description}) [{source}]"] = {'id': f"not found"}
            else:
                dic[f"{label} ({description}) [{source}]"] = {'id': f"{source}:{id}"}
            
    # Add the user-defined options to the list, filtered by search
    options.extend([{'id': f"{dic[key]['id']}", 'text': key} for key in dic if search.lower() in key.lower()])
    
    if user:
        options = [{'id': 'not found', 'text': f"{search} [user]"}] + options

    # Return combined, sorted options
    return sorted(options, key=lambda option: option['text'])

def checkList(LIST):
    if not isinstance(LIST, list):
        LIST = [LIST]
    return LIST

def labelIndexMap(data, type):
    label_to_index_maps = []
    for toIDX_entry in type:
        label_to_index_maps.append({data[toIDX_entry][k].get('Name'): idx for idx, k in enumerate(data.get(toIDX_entry, {}))})
    return label_to_index_maps

def entityRelations(data, fromIDX='', toIDX=[], relationOld='', entityOld='', entityNew='', enc=[]):
    toIDX = checkList(toIDX)
    enc = checkList(enc)
    label_to_index_maps = labelIndexMap(data, toIDX)

    def resolve_target(name, id_, entity_enc, label_map):
        """Try to resolve name to index in label_map; fallback to id_."""
        if name in label_map:
            idx = label_map[name]
            return f"{entity_enc}{idx + 1}"
        return id_

    for from_entry in data.get(fromIDX, {}).values():
        entries = from_entry.get(entityOld, {})
        for key, value in entries.items():
            name = value.get("Name")
            id_ = value.get("ID")
            entity_values = from_entry.setdefault(entityNew, {})

            resolved = None
            for enc_entry, label_map in zip(enc, label_to_index_maps):
                resolved = resolve_target(name, id_, enc_entry, label_map)
                if resolved != id_:
                    break  # match found

            if relationOld:
                if from_entry.get(relationOld, {}).get(key):
                    relation_value = from_entry[relationOld][key]
                else:
                    relation_value = 'MISSING RELATION TYPE'
                new_value = [relation_value, resolved]
            else:
                new_value = resolved

            if key not in entity_values.values() and entity_values.get(key) != new_value:
                entity_values[key] = new_value

    return

def mapEntity(data, fromIDX, toIDX, entityOld, entityNew, enc):
    
    # Ensure toIDX and enc are lists
    toIDX = checkList(toIDX)
    enc = checkList(enc)
    
    # Create mappings for all toIDX lists
    label_to_index_maps = labelIndexMap(data, toIDX)
    
    # Use Template or Ressource Label
    for from_entry in data.get(fromIDX, {}).values():
        for outerKey, relation in from_entry.get(entityOld, {}).items():
            for innerKey, entity in relation.items():
                #Id, label = entity.split(' <|> ')[:2]
                match_found = False
                for enc_entry, label_to_index in zip(enc, label_to_index_maps):
                    if entity['Name'] in label_to_index:
                        idx = label_to_index[entity['Name']]
                        match_found = True
                        from_entry.setdefault(entityNew, {}).setdefault(outerKey, {}).update({innerKey: f'{enc_entry}{idx+1}'})
                        break

                if not match_found:
                    from_entry.setdefault(entityNew, {}).setdefault(outerKey, {}).update({innerKey: entity['ID']})
    return

def replace_in_dict(d, target, replacement):
    if isinstance(d, dict):
        return {k: replace_in_dict(v, target, replacement) for k, v in d.items()}
    elif isinstance(d, list):
        return [replace_in_dict(v, target, replacement) for v in d]
    elif isinstance(d, str):
        return d.replace(target, replacement)
    else:
        return d 
    
def unique_items(data, title = None):
    # Set up Item Dict and track seen Items
    items = {}
    seen_items = set() 
    # Add Workflow Item
    if title:
        triple = ('not found', title, data.get('general', {}).get('objective', ''))
        items[f'Item{str(0).zfill(10)}'] = {'ID': 'not found', 'Name': title, 'Description': data.get('general', {}).get('objective', '')}
        seen_items.add(triple)
    # Add Workflow Component Items
    def search(subdict):
        if isinstance(subdict, dict) and 'ID' in subdict:
            triple = (subdict.get('ID', ''), subdict.get('Name', ''), subdict.get('Description', ''))
            if triple not in seen_items:
                item_key = f'Item{str(len(items)).zfill(10)}'  # Create unique key
                items[item_key] = {'ID': triple[0], 'Name': triple[1], 'Description': triple[2]}
                seen_items.add(triple)
        if isinstance(subdict, dict):
            for value in subdict.values():
                if isinstance(value, dict):
                    search(value)
    search(data)
    return items
