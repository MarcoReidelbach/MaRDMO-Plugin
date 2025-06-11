import re

from rdmo.domain.models import Attribute

from ..config import BASE_URI
from ..utils import extract_parts

def get_answer_model(project, val, uri, key1 = None, key2 = None, key3 = None, set_prefix = None, set_index = None, collection_index = None, external_id = None, option_text = None):
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
            if not set_prefix and set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.option_uri})
            elif not set_prefix and set_index and not collection_index and not external_id and option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:[value.option_uri, value.text]})
            elif not set_prefix and set_index and collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
            elif set_prefix and not set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(int(value.set_prefix), {}).update({key2:value.option_uri})
            elif set_prefix and set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:value.option_uri})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                if key2 == 'reference':
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
                else:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.option_uri})      
        elif value.text:
            if not set_prefix and not set_index and not collection_index and not external_id and not option_text:
                val[key1].update({key2:value.text})
            elif not set_prefix and not set_index and collection_index and not external_id and not option_text:
                val[key1].setdefault(key2, {}).update({value.collection_index:value.text})
            elif not set_prefix and set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.text})
            elif not set_prefix and set_index and not collection_index and external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.external_id})
            elif set_prefix and not set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).update({key2:value.text})
            elif set_prefix and not set_index and not collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                if key2 == 'DefinedQuantity':
                    label, description,_ = extract_parts(value.text)
                    val[key1].setdefault(int(prefix[0]), {}).update({key2:{'ID': value.external_id, 'Name': label, 'Description': description}})
                else:
                    val[key1].setdefault(int(prefix[0]), {}).update({key2:value.external_id})    
            elif set_prefix and set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                if key3:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).setdefault(value.set_index, {}).update({key3:value.text})
                else:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:value.text})
            elif set_prefix and set_index and not collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label, description, _ = extract_parts(value.text)
                if key3:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).setdefault(value.set_index, {}).update({key3:{'ID': value.external_id, 'Name': label, 'Description': description}})
                else: 
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:{'ID': value.external_id, 'Name': label, 'Description': description}})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.text})    
            elif set_prefix and not set_index and collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label, description,_ = extract_parts(value.text)
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:{'ID': value.external_id, 'Name': label, 'Description': description}})
            elif set_prefix and set_index and collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label, description,_ = extract_parts(value.text)
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).setdefault(value.set_index, {}).update({value.collection_index:{'ID': value.external_id, 'Name': label, 'Description': description}})
            elif not set_prefix and set_index and collection_index and not external_id and not option_text:
                if key3:
                    val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).setdefault(value.collection_index, {}).update({key3:value.text})

    return val

def mathmlToLatex(mathml):
    # Get via annotation tag
    match = re.search(r'<annotation[^>]*encoding="application/x-tex"[^>]*>\s*(.*?)\s*</annotation>', mathml, re.DOTALL)
    if not match:
        # Fall back to alttext attribute
        match = re.search(r'alttext="(.*?)"', mathml)
        if not match:
            # Extract from error message
            match = re.search(r'<strong class="error texerror">.*?:\s*(\{\\displaystyle\s+.*?\})</strong>', mathml, re.DOTALL)
    if match:
        # Get Group
        latex = match.group(1).strip()
        # Remove \displaystyle and associated braces
        latex = re.sub(r'^\{?\\displaystyle\s*', '', latex)
        latex = re.sub(r'\}$', '', latex)
        return latex
    return None

def mapEntityQuantity(data, type, mapping):
    for key in data[type]:
        for key2 in data[type][key].get('element',{}):
            for k in data['quantity']:
                if data[type][key]['element'][key2].get('quantity', {}).get('Name', '').lower() == data['quantity'][k]['Name'].lower():
                    if data['quantity'][k].get('QorQK') == mapping['Quantity']:
                        data[type][key]['element'][key2].update(
                            {'Info': 
                                {'Type': mapping['Quantity'],
                                 'Name':data['quantity'][k].get('Name',''),
                                 'Description':data['quantity'][k].get('Description',''),
                                 'ID':data['quantity'][k].get('ID','') if data['quantity'][k].get('ID','') and data['quantity'][k].get('ID','') != 'not found' else data['quantity'][k].get('Reference','') if data['quantity'][k].get('Reference','') else '', 
                                 'QKName':data['quantity'][k].get('QKRelatant', {}).get(0, {}).get('Name', ''),
                                 'QKID':data['quantity'][k].get('QKRelatant', {}).get(0, {}).get('ID', '')}
                            })
                    elif data['quantity'][k].get('QorQK') == mapping['QuantityKind']:
                        data[type][key]['element'][key2].update(
                            {'Info':
                                {'Type': mapping['QuantityKind'],
                                 'Name':data['quantity'][k].get('Name',''),
                                 'Description':data['quantity'][k].get('Description',''),
                                 'ID':data['quantity'][k].get('ID','') if data['quantity'][k].get('ID','') and data['quantity'][k].get('ID','') != 'not found' else ''}
                            })
    return






                    
