from rdmo.domain.models import Attribute

from ..config import BASE_URI
from ..utils import extract_parts, value_editor

from ..model.utils import get_id

def add_publication(instance, publications, source):
    # Get Set Ids and IDs of Publications
    set_ids = get_id(instance, f'{BASE_URI}domain/publication', ['set_index'])
    value_ids = get_id(instance, f'{BASE_URI}domain/publication/id', ['external_id'])
    # Add Publication to Questionnaire
    idx = max(set_ids, default = -1) + 1
    for publication in publications:
        if publication.id not in value_ids:
            # Set up Page
            value_editor(instance.project, f'{BASE_URI}domain/publication', f"P{idx}", None, None, None, idx)
            # Add ID Values
            value_editor(instance.project, f'{BASE_URI}domain/publication/id', f'{publication.label} ({publication.description}) [{source}]', f"{publication.id}", None, None, idx)
            idx += 1
            value_ids.append(publication.id)
    return

def get_answer_algorithm(project, val, uri, key1 = None, key2 = None, key3 = None, set_prefix = None, set_index = None, collection_index = None, external_id = None, option_text = None):
    '''Function to get user answers into dictionary.'''
    val.setdefault(key1, {})
    
    try:
        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f"{BASE_URI}{uri}"))
    except:
        values = []

    if not (key1 or key2):
        values =[]

    for value in values:
        if value.option:
            if set_prefix and set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:value.option_uri})
            elif not set_prefix and set_index and collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
        elif value.text:
            if not set_prefix and set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.text})
            elif not set_prefix and set_index and not collection_index and external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.external_id})
            elif set_prefix and not set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                print(value.text, prefix)
                val[key1].setdefault(int(prefix[0]), {}).update({key2:value.text})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.text})    
            elif set_prefix and not set_index and collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label,_,_ = extract_parts(value.text)
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:f"{value.external_id} <|> {label}"})
            elif set_prefix and set_index and not collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label,_,_ = extract_parts(value.text)
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:f"{value.external_id} <|> {label}"})    
    return val