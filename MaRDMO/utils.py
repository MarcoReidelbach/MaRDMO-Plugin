import re
import requests
import os
import json

from rdmo.projects.models import Value
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from multiprocessing.pool import ThreadPool

from .config import BASE_URI, mardi_api, wikidata_api, mathalgodb_endpoint, mathmoddb_endpoint
from .id import *

from .model.sparql import queryProviderMM
from .algorithm.sparql import queryProviderAL

def get_new_ids(project, ids, query):
    '''Request IDs for new MathModDB Items and add them to the Questionnaire'''
    new_ids ={}
    for key, id_value in ids.items():
        # Identify Items missing a MathModDB ID
        if not id_value.startswith('https://mardi4nfdi.de/mathmoddb#'):
            # Get MathModDB ID
            results = query_sparql(query.format(f"'{key}'"))
            if results and results[0].get('ID', {}).get('value'):
                match = re.match(r"(\d+)(\D+)", id_value)
                if not match:
                    continue
                setID, setName = match.groups()
                # Generate Entry
                value_editor(project, f"{BASE_URI}domain/{setName}/id", f"{key} ({results[0]['quote']['value']}) [mathmoddb]", f"mathmoddb:{results[0]['ID']['value']}", None, None, setID)
                # Stor new IDs
                new_ids.update({key: results[0]['ID']['value']})
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

def query_sparql(query,endpoint=mathmoddb_endpoint):
    '''SPARQL request returning all Items with matching properties.'''
    response = requests.post(endpoint,
                             data=query,
                             headers={"Content-Type": "application/sparql-query","Accept": "application/sparql-results+json"}
                            )
    # Check if request was successfull
    if response.status_code == 200:
        req = response.json().get('results',{}).get('bindings',[])
    else:
        req = []
        
    return req

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

def get_answer(project, val, uri, key1, key2, key3=None, set_prefix=False, set_index=False, collection_index=False, option_text=False, external_id=False):
        '''Function that retrieves individual User answers'''
        val.setdefault(key1, {})
        try:
            values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f"{BASE_URI}{uri}"))
        except:
            values = []
        for value in values:
            if value.option:
                if option_text:
                    if set_prefix:
                        if set_index:
                            if collection_index:
                                if external_id:
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri, value.external_id]})
                                else:
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri, value.text]})
                            else:
                                if external_id:
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).update({key2:[value.option_uri, value.external_id]})
                                else:
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).update({key2:[value.option_uri, value.text]})
                        else:
                            if collection_index:
                                if external_id:
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri, value.external_id]})
                                else:
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri, value.text]})
                            else:
                                if external_id:
                                    val[key1].setdefault(int(value.set_prefix), {}).update({key2:[value.option_uri, value.external_id]})
                                else:
                                    val[key1].setdefault(int(value.set_prefix), {}).update({key2:[value.option_uri, value.text]})
                    else:
                        if set_index:
                            if collection_index:
                                if external_id:
                                    val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri, value.external_id]})
                                else:
                                    val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri, value.text]})
                            else:
                                if external_id:
                                    val[key1].setdefault(value.set_index, {}).update({key2:[value.option_uri, value.external_id]})
                                else:
                                    val[key1].setdefault(value.set_index, {}).update({key2:[value.option_uri, value.text]})
                        else:
                            if collection_index:
                                if external_id:
                                    val[key1].setdefault(key2, {}).update({value.collection_index:[value.option_uri, value.external_id]})
                                else:
                                    val[key1].setdefault(key2, {}).update({value.collection_index:[value.option_uri, value.text]})
                            else:
                                if external_id:
                                    val[key1].update({key2:[value.option_uri, value.external_id]})
                                else:
                                    val[key1].update({key2:[value.option_uri, value.text]})
                else:
                    if set_prefix:
                        if set_index:
                            if collection_index:
                                if len(value.set_prefix.split('|')) == 1:
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:value.option_uri})
                                elif len(value.set_prefix.split('|')) > 1:
                                    prefix = value.set_prefix.split('|')
                                    val[key1].setdefault(int(prefix[0]), {}).setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:value.option_uri})
                            else:
                                if len(value.set_prefix.split('|')) == 1:
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(key2, {}).update({value.set_index:value.option_uri})
                                elif len(value.set_prefix.split('|')) > 1:
                                    prefix = value.set_prefix.split('|')
                                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:value.option_uri})
                        else:
                            if collection_index:
                                val[key1].setdefault(int(value.set_prefix), {}).setdefault(key2, {}).update({value.collection_index:value.option_uri})
                            else:
                                val[key1].setdefault(int(value.set_prefix), {}).update({key2:value.option_uri})
                    else:
                        if set_index:
                            if collection_index:
                                val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:value.option_uri})
                            else:
                                val[key1].setdefault(value.set_index, {}).update({key2:value.option_uri})
                        else:
                            if collection_index:
                                val[key1].setdefault(key2, {}).update({value.collection_index:value.option_uri})
                            else:
                                val[key1].update({key2:value.option_uri})
            elif value.text and value.text != 'NONE':
                if set_prefix:
                    if set_index:
                        if collection_index:
                            if external_id:
                                val[key1].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:value.external_id})
                            else:
                                val[key1].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:value.text})
                        else:
                            if external_id:
                                if len(value.set_prefix.split('|')) == 1:
                                    label,_,_ = extract_parts(value.text)
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(key2, {}).update({value.set_index:f"{value.external_id} <|> {label}"})
                                elif len(value.set_prefix.split('|')) > 1:
                                    prefix = value.set_prefix.split('|')
                                    if 'element ' in key2:
                                        label,_,_ = extract_parts(value.text)
                                        val[key1].setdefault(int(prefix[0]), {}).setdefault(key2.split(' ')[0], {}).setdefault(value.set_index, {}).update({key2.split(' ')[1]:f"{value.external_id} <|> {label}"})
                                    else: 
                                        label,_,_ = extract_parts(value.text)
                                        val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:f"{value.external_id} <|> {label}"})
                            else:
                                if len(value.set_prefix.split('|')) == 1: 
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(key2, {}).update({value.set_index:value.text})
                                elif len(value.set_prefix.split('|')) > 1:
                                    prefix = value.set_prefix.split('|')
                                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2.split(' ')[0], {}).setdefault(value.set_index, {}).update({key2.split(' ')[1]:value.text})
                    else:
                        if collection_index:
                            if external_id:
                                if len(value.set_prefix.split('|')) == 1:
                                    label,_,_ = extract_parts(value.text)
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(key2, {}).update({value.collection_index:f"{value.external_id} <|> {label}"})
                                elif len(value.set_prefix.split('|')) > 1:
                                    prefix = value.set_prefix.split('|')
                                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.external_id})
                            else:
                                if len(value.set_prefix.split('|')) == 1:
                                    val[key1].setdefault(int(value.set_prefix), {}).setdefault(key2, {}).update({value.collection_index:value.text})
                                elif len(value.set_prefix.split('|')) > 1:
                                    prefix = value.set_prefix.split('|')
                                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.text})
                        else:
                            if external_id:
                                if len(value.set_prefix.split('|')) == 1:
                                    if key1 == 'publication':
                                        val[key1].setdefault(int(value.set_prefix), {}).update({key2:value.external_id})
                                    else:
                                        label,_,_ = extract_parts(value.text)
                                        val[key1].setdefault(int(value.set_prefix), {}).update({key2:f"{value.external_id} <|> {label}"})
                                elif len(value.set_prefix.split('|')) > 1:
                                    prefix = value.set_prefix.split('|')
                                    val[key1].setdefault(int(prefix[0]), {}).update({key2:value.external_id})
                            else:
                                if len(value.set_prefix.split('|')) == 1:
                                    val[key1].setdefault(int(value.set_prefix), {}).update({key2:value.text})
                                elif len(value.set_prefix.split('|')) > 1:
                                    prefix = value.set_prefix.split('|')
                                    val[key1].setdefault(int(prefix[0]), {}).update({key2:value.text})    
                else:
                    if set_index:
                        if collection_index:
                            if external_id:
                                if key3:
                                    val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).setdefault(value.collection_index, {}).update({key3:value.external_id})
                                else:
                                    val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:value.external_id})
                            else:
                                if key3:
                                    val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).setdefault(value.collection_index, {}).update({key3:value.text})
                                else:
                                    val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:value.text})
                        else:
                            if external_id:
                                val[key1].setdefault(value.set_index, {}).update({key2:value.external_id})
                            else:
                                val[key1].setdefault(value.set_index, {}).update({key2:value.text})
                    else:
                        if collection_index:
                            if external_id:
                                if key1 == 'search':
                                    label,_,_ = extract_parts(value.text)
                                    val[key1].setdefault(key2, {}).update({value.collection_index:{'selection':f"{value.external_id} <|> {label}"}})
                                else:
                                    val[key1].setdefault(value.collection_index, {}).update({key2:value.external_id})
                            else:
                                if key2 == 'transferability':
                                    val[key1].setdefault(key2, {}).update({value.collection_index:value.text})
                                else:
                                    val[key1].setdefault(value.collection_index, {}).update({key2:value.text})       
                        else:
                            if external_id:
                                val[key1].update({key2:value.external_id})
                            else:
                                val[key1].update({key2:value.text})
            elif value.set_index:
                if set_prefix:
                    if set_index:
                        if collection_index:
                            val[key1].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:None})
                        else:
                            val[key1].setdefault(int(value.set_prefix), {}).setdefault(value.set_index, {}).update({key2:None})
                    else:
                        if collection_index:
                            val[key1].setdefault(int(value.set_prefix), {}).setdefault(key2, {}).update({value.collection_index:None})
                        else:
                            val[key1].setdefault(int(value.set_prefix), {}).update({key2:None})
                else:
                    if set_index:
                        if collection_index:
                            val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:None})
                        else:
                            val[key1].setdefault(value.set_index, {}).update({key2:None})
                    else:
                        if collection_index:
                            val[key1].setdefault(key2, {}).update({value.collection_index:None})
                        else:
                            val[key1].update({key2:None})
        return val

def refine(answers, entities):
    '''This function takes user answers and performs SPARQL queries to MaRDI portal.'''
    
    #entities = ['NonMathematicalDiscipline','Software','DataSet','Method','Hardware','ExperimentalDevice','publication']

    for entity in entities:
        for key in answers[entity]:
            # Refining IDs, Names and Descriptions of entities
            if answers[entity][key].get('ID') == 'not found':
                if answers[entity][key].get('Name') and answers[entity][key].get('Description'):
                    mardiID = find_item(answers[entity][key]['Name'],answers[entity][key]['Description'])
                    if mardiID:
                        answers[entity][key].update({'ID':f"mardi:{mardiID}"})
                    else:
                        answers[entity][key].update({'ID':f"user:{str(key)}"})
                else:
                    answers[entity][key].update({'ID':f"user:{str(key)}"})
            # Refining Subproperties of entities
            if answers[entity][key].get('SubProperty'):
                for ikey in answers[entity][key]['SubProperty']:
                    ID, Name, Description = answers[entity][key]['SubProperty'][ikey].split(' <|> ')
                    if re.match(r"mardi:Q[0-9]+", ID):
                        answers[entity][key]['SubProperty'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
                    else:
                        mardiID = find_item(Name,Description)
                        if mardiID:
                            answers[entity][key]['SubProperty'].update({ikey:{'ID':f"mardi:{mardiID}", 'Name':Name, 'Description':Description}})
                        else:
                            answers[entity][key]['SubProperty'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
            if answers[entity][key].get('SubProperty2'):
                for ikey in answers[entity][key]['SubProperty2']:
                    ID, Name, Description = answers[entity][key]['SubProperty2'][ikey].split(' <|> ')
                    if re.match(r"mardi:Q[0-9]+", ID):
                        answers[entity][key]['SubProperty2'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
                    else:
                        mardiID = find_item(Name,Description)
                        if mardiID:
                            answers[entity][key]['SubProperty2'].update({ikey:{'ID':f"mardi:{mardiID}", 'Name':Name, 'Description':Description}})
                        else:
                            answers[entity][key]['SubProperty2'].update({ikey:{'ID':ID, 'Name':Name, 'Description':Description}})
    
    return answers

def merge_dicts_with_unique_keys(answers):
    
    keys = ['field','problem','model','formulation','quantity','task','publication']
    
    merged_dict = {}
    
    for key in keys:
        for inner_key, value in answers[key].items():
            new_inner_key = f"{inner_key}{key}"
            merged_dict[new_inner_key] = value    
    
    return merged_dict

def dict_to_triples(data):

    inversePropertyMapping = get_data('model/data/inversePropertyMapping.json')
    options = get_data('data/options.json')

    relations = ['IntraClassRelation','RP2RF','MM2RP','MF2MM','MF2MF','Q2Q','Q2QK','QK2Q','QK2QK','T2MF','T2Q','T2MM','P2E']
    relatants = ['IntraClassElement','RFRelatant','RPRelatant','MMRelatant','MFRelatant','QRelatant','QKRelatant','QRelatant','QKRelatant','MFRelatant','QRelatant','MMRelatant','EntityRelatant']
    
    triples = []
    ids = {} 
    
    # Get ID Dict
    for idx, item in data.items():
        if item['ID'] and item['ID'].startswith('mathmoddb:'):
            ids[item['Name']] = item['ID']
        else:
            ids[item['Name']] = idx
    
    # Go through all individuals
    for idx, item in data.items():

        # Get ID of Individual
        subject = ids[item['Name']]
        
        if not subject.startswith('mathmoddb:'):
        
            # Assign Individual Label 
            triples.append((subject, "rdfs:label", f'"{item["Name"]}"@en'))
        
            # Assign Individual Description
            if item.get('Description'):
                triples.append((subject, "rdfs:comment", f'"{item["Description"]}"@en'))
        
            # Assign Individual Class
            if 'field' in idx:
                triples.append((subject, "a", 'mathmoddb:ResearchField'))
            elif 'problem' in idx:
                triples.append((subject, "a", 'mathmoddb:ResearchProblem'))
            elif 'model' in idx:
                triples.append((subject, "a", 'mathmoddb:MathematicalModel'))
            elif 'quantity' in idx:
                if item['QorQK'] == 'https://rdmo.mardi4nfdi.de/terms/options/MathModDB/Quantity':
                    triples.append((subject, "a", 'mathmoddb:Quantity'))
                else:
                    triples.append((subject, "a", 'mathmoddb:QuantityKind'))
            elif 'formulation' in idx:
                triples.append((subject, "a", 'mathmoddb:MathematicalFormulation'))
            elif 'task' in idx:
                if item.get('TaskClass') == 'https://rdmo.mardi4nfdi.de/terms/options/MathModDB/ComputationalTask':
                    triples.append((subject, "a", 'mathmoddb:ComputationalTask'))
            elif 'publication' in idx:
                triples.append((subject, "a", 'mathmoddb:Publication'))
        
            # Assign Individual MaRDI/Wikidata ID
            if item.get('ID'):
                if item['ID'].startswith('wikidata:'):
                    q_number = item['ID'].split(':')[-1]
                    triples.append((subject, "mathmoddb:wikidataID", f'"{q_number}"'))
                elif item['ID'].startswith('mardi:'):
                    q_number = item['ID'].split(':')[-1]
                    triples.append((subject, "mathmoddb:mardiID", f'"{q_number}"'))

            # Assign Individual DOI/QUDT ID
            if item.get('reference'):
                print(item.get('reference'))
                if item['reference'].get(0):
                    if item['reference'][0][0] == options['DOI']:
                        doi_value = item['reference'][0][1]
                        triples.append((subject, "mathmoddb:doiID", f'<https://doi.org/{doi_value}>'))
                    if item['reference'][0][0] == options['QUDT']:
                        qudt_value = item['reference'][0][1]
                        triples.append((subject, "mathmoddb:qudtID", f'"{qudt_value}"'))
        
            # Assign Quantity definey by Individual
            if item.get('DefinedQuantity'):
                defined_quantity = item['DefinedQuantity'].split(' <|> ')
                if defined_quantity[0].startswith('mathmoddb:'):
                    object_value = defined_quantity[0]
                else:
                    #referred_name = defined_quantity[1]
                    object_value = ids.get(referred_name)
                triples.append((subject, 'mathmoddb:defines', object_value))
                triples.append((object_value, 'mathmoddb:definedBy', subject))
        
            # Assign Individual Formula
            if item.get('Formula'):
                formulas = item['Formula'].values()
                for formula in formulas:
                    formula = formula.replace('\\', '\\\\')
                    triples.append((subject, 'mathmoddb:definingFormulation', f'"{formula[1:-1]}"^^<https://mardi4nfdi.de/mathmoddb#LaTeX>'))
                if item.get('Element'):
                    elements = item['Element'].values()
                    for element in elements:
                        symbol = element['Symbol'].replace('\\', '\\\\')
                        quantity = element['quantity'].split(' <|> ')
                        if len(quantity) == 1:
                            referred_name = quantity[0]
                            object_value = ids.get(referred_name)
                        else:
                            if quantity[0].startswith('mathmoddb:'):
                                referred_name = quantity[1]
                                object_value = quantity[0]
                            else:
                                referred_name = quantity[1]
                                object_value = ids.get(referred_name)
                        if object_value:
                            triples.append((subject, 'mathmoddb:inDefiningFormulation', f'"{symbol[1:-1]}, {referred_name}"^^<https://mardi4nfdi.de/mathmoddb#LaTeX>'))
                            triples.append((subject, 'mathmoddb:containsQuantity', object_value))
                            triples.append((object_value, 'mathmoddb:containedInFormulation', subject))
        
            # Assign Individual Properties
            if item.get('Properties'):
                prefix = 'https://rdmo.mardi4nfdi.de/terms/options/MathModDB/'
                values = item['Properties'].values()
                if prefix + 'isLinear' in values:
                    triples.append((subject, "mathmoddb:isLinear", '"true"^^xsd:boolean'))
                elif prefix + 'isNotLinear' in values:
                    triples.append((subject, "mathmoddb:isLinear", '"false"^^xsd:boolean'))
                if prefix + 'isConvex' in values:
                    triples.append((subject, "mathmoddb:isConvex", '"true"^^xsd:boolean'))
                elif prefix + 'isNotConvex' in values:
                    triples.append((subject, "mathmoddb:isConvex", '"false"^^xsd:boolean'))
                if prefix + 'isDeterministic' in values:
                    triples.append((subject, "mathmoddb:isDeterministic", '"true"^^xsd:boolean'))
                elif prefix + 'isStochastic' in values:
                    triples.append((subject, "mathmoddb:isDeterministic", '"false"^^xsd:boolean'))
                if prefix + 'isDimensionless' in values:
                    triples.append((subject, "mathmoddb:isDimensionless", '"true"^^xsd:boolean'))
                elif prefix + 'isDimensional' in values:
                    triples.append((subject, "mathmoddb:isDimensionless", '"false"^^xsd:boolean'))
                if prefix + 'isDynamic' in values:
                    triples.append((subject, "mathmoddb:isDynamic", '"true"^^xsd:boolean'))
                elif prefix + 'isStatic' in values:
                    triples.append((subject, "mathmoddb:isDynamic", '"false"^^xsd:boolean'))
                if prefix + 'isSpaceContinuous' in values:
                    triples.append((subject, "mathmoddb:isSpaceContinuous", '"true"^^xsd:boolean'))
                elif prefix + 'isSpaceDiscrete' in values:
                    triples.append((subject, "mathmoddb:isSpaceContinuous", '"false"^^xsd:boolean'))
                if prefix + 'isTimeContinuous' in values:
                    triples.append((subject, "mathmoddb:isTimeContinuous", '"true"^^xsd:boolean'))
                elif prefix + 'isTimeDiscrete' in values:
                    triples.append((subject, "mathmoddb:isTimeContinuous", '"false"^^xsd:boolean'))	

        # Assign Individual Properties
        for relation, relatant in zip(relations,relatants):
            relation_dict = item.get(relation, {})
            relatant_dict = item.get(relatant, {})
            for key in relation_dict:
                if relatant_dict.get(key):
                    relation_uri = relation_dict[key]
                    relatant_value = relatant_dict[key].split(' <|> ')
                    if relatant_value[0].startswith('mathmoddb:'):
                        object_value = relatant_value[0]
                    else:
                        referred_name = relatant_value[1]
                        object_value = ids.get(referred_name)
                    triples.append((subject, f"mathmoddb:{relation_uri.split('/')[-1]}", object_value))
                    triples.append((object_value, f"mathmoddb:{inversePropertyMapping[relation_uri].split('/')[-1]}", subject))
    
    return triples, ids

def generate_sparql_insert_with_new_ids(triples):
    # Step 1: Identify new items that need mardmo IDs
    new_items = {}
    counter = 0
    for triple in triples:
        subject = triple[0]
        if not subject.startswith("mathmoddb:"):
            # Assign temporary placeholders for new IDs
            new_items[subject] = f"newItem{counter}"
            counter += 1

    # Step 2: Generate SPARQL query with BIND for new mardmo IDs
    insert_query = """
    PREFIX mathmoddb: <https://mardi4nfdi.de/mathmoddb#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    INSERT{
    """
    # Construct the insert part
    for triple in triples:
        subject = triple[0]
        predicate = triple[1]
        obj = triple[2]

        # Replace new subjects with placeholders
        if subject in new_items:
            subject = f"?{new_items[subject]}"
        else:
            subject = f"{subject}"

        # Format object based on whether it's a literal or a URI
        if re.match(r'^https?://', obj):
            obj_formatted = f"<{obj}>"
        else:
            if obj.startswith('mathmoddb:') or obj.startswith('"') or obj.startswith(':') or obj.startswith('<'):
                obj_formatted = f'{obj}'
            else:
                obj_formatted = f"?{new_items[obj]}"

        # Construct the triple in the query
        insert_query += f"  {subject} {predicate} {obj_formatted} .\n"

    insert_query += "}\nWHERE {\n"

    # Step 3: Add logic to get the next free mardmo ID
    insert_query += """
    {
      SELECT (MAX(?num) AS ?maxID) WHERE {
        ?id a ?type .
        FILTER (STRSTARTS(STR(?id), "https://mardi4nfdi.de/mathmoddb#mardmo"))
        BIND (xsd:integer(SUBSTR(STR(?id), STRLEN("https://mardi4nfdi.de/mathmoddb#mardmo") + 1)) AS ?num)
      }
    }
    BIND (IF(BOUND(?maxID), ?maxID + 1, 0) AS ?nextID)
    """
    id_counter = 0
    for new_item in new_items:
        insert_query += f"BIND(IRI(CONCAT('https://mardi4nfdi.de/mathmoddb#mardmo', STR(?nextID+{id_counter}))) AS ?{new_items[new_item]})\n"
        id_counter += 1

    insert_query += "}"

    return insert_query

def query_sources(search, queryID, sources, notFound=True):
        '''Helper function to query specified sources and process results.'''
        
        source_functions = {
            'wikidata': lambda s: query_api(wikidata_api, s),
            'mardi': lambda s: query_api(mardi_api, s),
            'mathmoddb': lambda s: MathModDBProvider(s, queryProviderMM[queryID]),
            'mathalgodb': lambda s: MathAlgoDBProvider(s, queryProviderAL[queryID])
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

def MathModDBProvider(search, query):
    """
    Dynamic query of MathModDB, results as options for Provider.
    """
    if not search:
        return []

    # Fetch results from the MathModDB knowledge graph
    results = query_sparql(query)
    dic = {}
    options = []
    
    # Store results in dict
    for result in results:
        dic.update({result['label']['value']:{'id':result['id']['value'], 'quote':result['quote']['value']}})

    # Filter results by user-defined search
    options.extend([{'id': f"mathmoddb:{dic[key]['id']}", 'text': f'{key} ({dic[key]["quote"]}) [mathmoddb]'} for key in dic if search.lower() in key.lower()])

    return options

def MathAlgoDBProvider(search, query):
    """
    Dynamic query of MathAlgoDB, results as options for Provider.
    """
    if not search:
        return []

    # Fetch results from the MathAlgoDB knowledge graph
    results = query_sparql(query, mathalgodb_endpoint)
    dic = {}
    options = []
    
    # Store results in dict
    for result in results:
        dic.update({result['label']['value']:{'id':result['id']['value'], 'quote':result['quote']['value']}})

    # Filter results by user-defined search
    options.extend([{'id': f"mathalgodb:{dic[key]['id']}", 'text': f'{key} ({dic[key]["quote"]}) [mathalgodb]'} for key in dic if search.lower() in key.lower()])

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

def index_check(instance,key,uri):
    '''Get value with similar index as instance value'''
    index_value = ''
    values = instance.project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=uri))
    for value in values:
        if value.set_index == instance.set_index:
            index_value = getattr(value,key)
            break
    return index_value

def information_exists(project, domain_type, set_index):
    """
    Checks if a matching name and description with the same set index exist in the project.
    """
    names = project.values.filter(snapshot = None, attribute = Attribute.objects.get(uri=f'{BASE_URI}domain/{domain_type}/name'))
    descriptions = project.values.filter(snapshot = None, attribute = Attribute.objects.get(uri=f'{BASE_URI}domain/{domain_type}/description'))
    
    return any(
        name.text and description.text and
        name.set_prefix == str(set_index) and
        description.set_prefix == str(set_index)
        for name, description in zip(names, descriptions)
    )
