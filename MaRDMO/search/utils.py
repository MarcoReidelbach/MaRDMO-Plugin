from rdmo.domain.models import Attribute

from ..config import BASE_URI
from ..utils import extract_parts

def get_answer_search(project, val, uri, key1 = None, key2 = None, key3 = None, set_prefix = None, set_index = None, collection_index = None, external_id = None, option_text = None):
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
            if not set_prefix and not set_index and not collection_index and not external_id and not option_text:
                val[key1].update({key2:value.option_uri})
        elif value.text:
            if not set_prefix and not set_index and collection_index and not external_id and not option_text:
                val[key1].setdefault(key2, {}).update({value.collection_index:value.text})
            elif not set_prefix and not set_index and collection_index and external_id and not option_text:
                label,_,_ = extract_parts(value.text)
                val[key1].setdefault(key2, {}).update({value.collection_index:{'selection':f"{value.external_id} <|> {label}"}})
    return val