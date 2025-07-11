import json, os, re

from django.apps import apps
from rdmo.domain.models import Attribute

from .config import BASE_URI, endpoint
from .queries import query_sparql
from .helpers import value_editor


def get_mathmoddb():
    """Retrieve the mathmoddb ontology from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").mathmoddb

def get_mathalgodb():
    """Retrieve the mathmoddb ontology from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").mathalgodb

def get_options():
    """Retrieve the rdmo options from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").options

def get_items():
    """Retrieve the rdmo options from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").ITEMS

def get_properties():
    """Retrieve the rdmo options from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").PROPERTIES

def get_questions_workflow():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questions_workflow

def get_questions_algorithm():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questions_algorithm

def get_questions_model():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questions_model

def get_questions_publication():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questions_publication

def get_questions_search():
    """Retrieve the questions dictionary from MaRDMOConfig."""
    return apps.get_app_config("MaRDMO").questions_search

def get_general_item_url():
    """Get general Wikibase Item URL from Wikibase URL"""
    return f"{endpoint['mardi']['uri']}/wiki/Item:"

def get_data(file_name):
    '''Get Data from JSON File'''
    path = os.path.join(os.path.dirname(__file__), file_name)
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data

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

def get_new_ids(project, ids, query, endpoint, source):
    '''Request IDs for new MathAlgoDB Items and add them to the Questionnaire'''
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
                set_index, set_name = match.groups()
                # Generate Entry
                value_editor(project = project, 
                             uri = f"{BASE_URI}domain/{set_name}/id", 
                             text = f"{key} ({results[0]['quote']['value']}) [{source}]", 
                             external_id = f"{source}:{results[0]['ID']['value']}", 
                             set_index = set_index)
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
