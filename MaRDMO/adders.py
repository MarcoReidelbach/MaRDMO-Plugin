from rdmo.options.models import Option

from .getters import get_id, get_options
from .helpers import extract_parts, value_editor


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

def add_relations(project, data, props, set_prefix, relatant, mapping=None, relation=None, suffix='', assumption=None, order=None):
    # Get Set Ids and IDs of Entities
    set_ids = get_id(project, relatant, ['set_prefix'])
    set_ids2 = get_id(project, relatant, ['set_index'])
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
                    
            # Add Assumption
            if order and hasattr(value, 'order') and value.order:
                
                    value_editor(
                        project=project, 
                        uri=order, 
                        text=value.order,
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

def add_reference_order(entity):
    options = get_options()
    order = {
            'doi': (0, options['DOI']),
            'morwiki' if entity == 'benchmark' else 'swmath': (1, options['MORWIKI' if entity == 'benchmark' else 'SWMATH']),
            'url': (2, options['URL']),
            }
    return order