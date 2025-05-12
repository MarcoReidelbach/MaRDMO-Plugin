from rdmo.domain.models import Attribute

from ..config import BASE_URI

def add_item_relation(payload, values, lookup, items, item, idx, property, qualifier = [], datatype = 'wikibase-item', reverse = False):
    for value in values:
        # Continue if no ID exists
        if not value.get('ID'):
            continue
        # Use new ID if present
        value['ID'] = lookup.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Entry Key
        entry = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
        # Add to Payload
        if reverse:
            payload.update({f"RELATION{idx}":{'id': '', 'url': statements_uri(entry), 'payload': statements_payload(property, item, datatype, qualifier)}})
        else:
            payload.update({f"RELATION{idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload(property, entry, datatype, qualifier)}}) 
        idx += 1
    return payload, idx

def add_static_or_non_item_relation(payload, item, idx, property, content, datatype = 'wikibase-item', qualifier = []):
    payload.update({f"RELATION{idx}":{'id': '', 'url': statements_uri(item), 'payload': statements_payload(property, content, datatype, qualifier)}}) 
    idx += 1
    return payload, idx

def add_qualifier(id, content, data_type = 'wikibase-item'):
    return [{"property": {"id": id, "data_type": data_type},"value": {"type": "value","content": content}}]

def compare_items(old, new):
    ids = {}
    for key, value in old.items():
        if key.startswith('Item') and not value['id']:
            ids.update({new[key]['payload']['item']['labels']['en']: new[key]['id']})
    return ids

def find_key_by_values(extracted_dict, id_value, name_value, description_value):
    for key, values in extracted_dict.items():
        if (values['ID'] == id_value and 
            values['Name'] == name_value and 
            values['Description'] == description_value):
            return key
    return None

def get_answer_workflow(project, val, uri, key1 = None, key2 = None, key3 = None, set_prefix = None, set_index = None, collection_index = None, external_id = None, option_text = None):
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
            elif set_prefix and not set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).update({key2:value.option_uri})
            elif not set_prefix and set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.option_uri})
            elif set_prefix and not set_index and not collection_index and not external_id and option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).update({key2:[value.option_uri, value.text]})
            elif not set_prefix and set_index and collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:[value.option_uri,value.text]})
        elif value.text:
            if not set_prefix and not set_index and not collection_index and not external_id and not option_text:
                val[key1].update({key2:value.text})
            elif not set_prefix and not set_index and collection_index and not external_id and not option_text:
                val[key1].setdefault(value.collection_index, {}).update({key2:value.text})
            elif not set_prefix and not set_index and not collection_index and external_id and not option_text:
                val[key1].update({key2:value.external_id})
            elif not set_prefix and not set_index and collection_index and external_id and not option_text:
                val[key1].setdefault(value.collection_index, {}).update({key2:value.external_id})
            elif not set_prefix and set_index and not collection_index and not external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.text})
            elif not set_prefix and set_index and not collection_index and external_id and not option_text:
                val[key1].setdefault(value.set_index, {}).update({key2:value.external_id})
            elif not set_prefix and set_index and collection_index and not external_id and not option_text:
                if key3:
                    val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).setdefault(value.collection_index, {}).update({key3:value.text})
                else:
                    val[key1].setdefault(value.set_index, {}).setdefault(key2, {}).update({value.collection_index:value.text})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                if key3:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).setdefault(value.collection_index, {}).update({key3:value.text})
                else:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.text})
            elif set_prefix and not set_index and collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                if key3:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).setdefault(value.collection_index, {}).update({key3:value.external_id})
                else:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.external_id})    
            elif set_prefix and not set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).update({key2:value.text})
    return val

def get_discipline(answers):
    ids = []
    md = 0
    nmd = 0
    for key in answers.get('processstep', []):
        for key2 in answers['processstep'][key].get('discipline', []):
            if answers['processstep'][key]['discipline'][key2].get('ID') and answers['processstep'][key]['discipline'][key2]['ID'] not in ids:
                if 'mardi' in answers['processstep'][key]['discipline'][key2]['ID'] or 'wikidata' in answers['processstep'][key]['discipline'][key2]['ID']:
                    answers.setdefault('nonmathdiscipline', {}).update({nmd: {'ID': answers['processstep'][key]['discipline'][key2]['ID'],
                                                                              'Name': answers['processstep'][key]['discipline'][key2]['Name']}})
                    nmd += 1
                    ids.append(answers['processstep'][key]['discipline'][key2]['ID'])
                elif 'msc' in answers['processstep'][key]['discipline'][key2]['ID']:
                    answers.setdefault('mathsubject', {}).update({md: {'ID': answers['processstep'][key]['discipline'][key2]['ID'],
                                                                       'Name': answers['processstep'][key]['discipline'][key2]['Name']}})
                    md += 1
                    ids.append(answers['processstep'][key]['discipline'][key2]['ID'])
    return answers

def get_item_key(value, items, lookup):
    # Check if Item has Name and Description
    if not value.get('Name'):
        raise ValueError('All Items need to have a Name!')
    if not value.get('Description'):
        raise ValueError('All Items need to have a Description!')
    # Check if Item has new ID
    value['ID'] = lookup.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
    # Get Item Key
    item = find_key_by_values(items, value['ID'], value['Name'], value['Description'])
    return item

def items_payload(name, description):
    if description and description != 'No Description Provided!':
        return {"item": {"labels": {"en": name}, "descriptions": {"en": description}}} 
    else:
        return {"item": {"labels": {"en": name}}}
    
def items_uri():
    return 'https://test.wikidata.org/w/rest.php/wikibase/v1/entities/items'
    #return 'https://staging.mardi4nfdi.org/w/rest.php/wikibase/v1/entities/items'
    
def statements_payload(id, content, data_type = "wikibase-item", qualifiers = []):
    return {"statement": {"property": {"id": id, "data_type": data_type}, "value": {"type": "value", "content": content}, "qualifiers": qualifiers}}

def statements_uri(item):
    return f'https://test.wikidata.org/w/rest.php/wikibase/v1/entities/items/{item}/statements'
    #return f'https://staging.mardi4nfdi.org/w/rest.php/wikibase/v1/entities/items/{item}/statements'
    


