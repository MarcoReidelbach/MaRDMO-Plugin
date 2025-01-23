from rdmo.options.models import Option
from rdmo.domain.models import Attribute

from ..config import BASE_URI
from ..utils import extract_parts, get_data, value_editor, query_sparql

from .sparql import queryHandler

def add_basics(instance, url_name, url_description):
    label, description, _ = extract_parts(instance.text)
    value_editor(instance.project, url_name, label, None, None, None, 0, instance.set_index)
    value_editor(instance.project, url_description, description, None, None, None, 0, instance.set_index)
    return

def add_entity(instance, results, url_set, url_id, prop, prefix):
    set_ids = get_id(instance, url_set, ['set_index'])
    value_ids = get_id(instance, url_id, ['external_id'])
    # Add Research Field entry to questionnaire
    idx = max(set_ids, default = -1) + 1
    if results[0].get(prop, {}).get('value'):
        IDs = results[0][prop]['value'].split(' / ')
        Labels = results[0][f'{prop}Label']['value'].split(' / ')
        Descriptions = results[0][f'{prop}Description']['value'].split(' / ')
        for ID, Label, Description in zip(IDs, Labels, Descriptions):
            if f"mathmoddb:{ID}" not in value_ids:
                # Set up Page
                value_editor(instance.project, url_set, f"{prefix}{idx}", None, None, None, idx)
                # Add ID Values
                value_editor(instance.project, url_id, f'{Label} ({Description}) [mathmoddb]', f"mathmoddb:{ID}", None, None, idx)
                idx += 1
                value_ids.append(f"mathmoddb:{ID}")

def add_properties(instance, results, mathmoddb, url_properties):
    for idx, prop in enumerate(['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless','isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']):
        if results[0].get(prop, {}).get('value') == 'true':
            value_editor(instance.project, url_properties, None, None, Option.objects.get(uri=mathmoddb[prop]), idx, 0, instance.set_index)
    return

def add_publications(instance, results, options):
    # Gather DOIs for Query
    Id = ''
    if results[0].get('publication',{}).get('value'):
        entities = results[0]['publication']['value'].split(' / ')
        for entity in entities:
            Id = Id + f' :{entity}'
    # Query MathModDB for Publications
    results = query_sparql(queryHandler['publicationInformation'].format(f":{Id}"))
    # Get set and value ids of Publications in Questionnaire
    set_ids = get_id(instance, f'{BASE_URI}domain/publication', ['set_index'])
    value_ids = get_id(instance, f'{BASE_URI}domain/publication/reference', ['option_uri', 'text'])
    # Load MathModDB Mapping
    mathmoddb = get_data('model/data/mapping.json')
    # Add Publication entry to questionnaire
    idx = max(set_ids, default = -1) + 1
    for result in results:
        if all([options[src], result.get(src, {}).get('value')] not in value_ids for src in ['DOI', 'URL', 'MaRDIPortalID',  'MathAlgoDBID', 'MathModDBID', 'WikidataID']):
            # Set up Page
            value_editor(instance.project, f'{BASE_URI}domain/publication', f"P{idx}", None, None, None, idx)
            # Add Values
            for src_idx, src in enumerate(['DOI', 'URL', 'MaRDIPortalID',  'MathAlgoDBID', 'MathModDBID', 'WikidataID']):
                if result.get(src, {}).get('value'):
                    value_editor(instance.project, f'{BASE_URI}domain/publication/reference', result[src]['value'], None, Option.objects.get(uri=options[src]), src_idx, idx)
                    # Add ID to ID List
                    value_ids.append([options[src],result[src]['value']])
            # Add Relations
            prop_idx = 0
            for property in ['documents', 'invents', 'studies', 'surveys', 'uses']:
                if result.get(property, {}).get('value'):
                    entities = result[property]['value'].split(' / ')
                    for entity in entities:
                        id, label, description = entity.split(' | ')
                        if id and label and description:
                            value_editor(instance.project, f'{BASE_URI}domain/publication/entity-relation', None, None, Option.objects.get(uri=mathmoddb[property]), None, prop_idx, idx)
                            value_editor(instance.project, f'{BASE_URI}domain/publication/entity-relatant', f"{label} ({description}) [mathmoddb]", f'{id}', None, None, prop_idx, idx)
                            prop_idx =+ 1
        idx =+ 1
                
    return

def add_relations(instance, results, mathmoddb, url_relation, url_relatant, props, relation = True, appendix = '', set_prefix = None, collection_index = False):
    if set_prefix == None:
        set_prefix = instance.set_index
    idx = 0
    for prop in props:
        if results[0].get(f'{prop}{appendix}', {}).get('value'):
            IDs = results[0][f'{prop}{appendix}']['value'].split(' / ')
            Labels = results[0][f'{prop}{appendix}Label']['value'].split(' / ')
            Descriptions = results[0][f'{prop}{appendix}Description']['value'].split(' / ')
            for ID, Label, Description in zip(IDs, Labels, Descriptions):
                if relation:
                    if collection_index:
                        value_editor(instance.project, url_relation, None, None, Option.objects.get(uri=mathmoddb[prop]), idx, 0, set_prefix)
                    else:
                        value_editor(instance.project, url_relation, None, None, Option.objects.get(uri=mathmoddb[prop]), None, idx, set_prefix)
                if collection_index:
                    value_editor(instance.project, url_relatant, f"{Label} ({Description}) [mathmoddb]", f'mathmoddb:{ID}', None, idx, 0, set_prefix)
                else:
                    value_editor(instance.project, url_relatant, f"{Label} ({Description}) [mathmoddb]", f'mathmoddb:{ID}', None, None, idx, set_prefix)
                idx += 1
    return

def get_id(instance, uri, keys):
    values = instance.project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=uri))
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

def get_answer_model(project, val, uri, key1, key2, key3 = None, set_prefix = None, set_index = None, collection_index = None, external_id = None, option_text = None):
    '''Function to get user answers into dictionary.'''
    val.setdefault(key1, {})
    
    try:
        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f"{BASE_URI}{uri}"))
    except:
        values = []

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
                val[key1].setdefault(int(prefix[0]), {}).update({key2:value.external_id})    
            elif set_prefix and set_index and not collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                if key3:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).setdefault(value.set_index, {}).update({key3:value.text})
                else:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:value.text})
            elif set_prefix and set_index and not collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label,_,_ = extract_parts(value.text)
                if key3:
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).setdefault(value.set_index, {}).update({key3:f"{value.external_id} <|> {label}"})
                else: 
                    val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.set_index:f"{value.external_id} <|> {label}"})
            elif set_prefix and not set_index and collection_index and not external_id and not option_text:
                prefix = value.set_prefix.split('|')
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:value.text})    
            elif set_prefix and not set_index and collection_index and external_id and not option_text:
                prefix = value.set_prefix.split('|')
                label,_,_ = extract_parts(value.text)
                val[key1].setdefault(int(prefix[0]), {}).setdefault(key2, {}).update({value.collection_index:f"{value.external_id} <|> {label}"})
                
    return val


                    