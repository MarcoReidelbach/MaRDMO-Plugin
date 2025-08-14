'''Functions to add Information to the Questionaire.'''

import json
import os

from django.apps import apps
from rdmo.domain.models import Attribute

from .config import BASE_URI, endpoint
from .constants import flag_dict
from .helpers import nested_set


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
    """Get Data from JSON File"""
    path = os.path.join(os.path.dirname(__file__), file_name)
    with open(path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

def get_id(project, uri, keys):
    """Get Set of User requested Identifiers for specific URI"""
    values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=uri))
    identifiers = []
    if len(keys) == 1:
        for value in values:
            identifier = getattr(value, keys[0])
            if isinstance(identifier, str) and '|' in identifier:
                identifier = identifier.split('|')[0]
            identifiers.append(identifier)
    else:
        for value in values:
            identifier = []
            for key in keys:
                identifier.append(getattr(value, key))
            identifiers.append(identifier)
    return identifiers

def get_answers(project, val, config):

    """Unified function to get user answers into dictionary."""
    
    val.setdefault(config["key1"], {})

    try:
        values = project.values.filter(
            snapshot=None,
            attribute=Attribute.objects.get(uri = f"{BASE_URI}{config['uri']}")
            )
    except Attribute.DoesNotExist:
        values = []

    if not (config["key1"] or config["key2"]):
        return val
    
    for value in values:
        
        # Set Prefix IDX
        prefix_idx = None
        if value.set_prefix:
            prefix_idx = int(value.set_prefix.split('|')[0])

        # Set Flags
        flags = (
                 bool(config["set_prefix"]),
                 bool(config["set_index"]),
                 bool(config["collection_index"]),
                 bool(config["external_id"]),
                 bool(config["option_text"]),
                )
        
        # Set Attribute
        attribute = 'option_uri' if value.option else 'text' if value.text else None

        if not attribute:
            # Ignore if not Attribute Set
            continue

        # Get Flag Combo Handler
        handler = flag_dict[flags]

        # Get Entry and Path
        entry, path = handler(value, attribute, config, prefix_idx)

        # Generate nested Dict Entry
        nested_set(data=val,
                   path=path,
                   entry=entry)

    return val
