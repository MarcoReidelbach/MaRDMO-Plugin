from rdmo.domain.models import Attribute

from ..config import BASE_URI

def compare_items(old, new):
    ids = {}
    for key, value in old.items():
        if key.startswith('Item') and not value['id']:
            ids.update({new[key]['payload']['item']['labels']['en']: new[key]['id']})
    return ids

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
                val[key1].setdefault(key2, {}).update({value.collection_index:value.text})
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

