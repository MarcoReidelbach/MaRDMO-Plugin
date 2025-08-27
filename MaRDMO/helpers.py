'''General Helper Functions of MaRDMO'''

import re

from rdmo.projects.models import Value
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

def basic_dict(value):
    '''Basic Information from ID Question as Dict'''
    # Extract Label and Description from ID Question
    label, description, _ = extract_parts(value.text)
    # Return Basic Dict
    return {
        'ID': value.external_id, 
        'Name': label, 
        'Description': description
    }

def basic_list(value):
    '''Basic List with Option URI and Text'''
    # Return Basic List
    return [
        value.option_uri,
        value.text
    ]

def define_setup(query_attributes, creation=False, query_id='', sources=None):
    """Define the setup of particular queries."""
    return {
        'creation': creation,
        'query_attributes': query_attributes,
        'query_id': query_id,
        'sources': sources,
    }

def nested_set(data, path, entry):
    """Walk a sequence of keys, creating dicts as needed, and set the final value."""
    d = data
    for key in path[:-1]:
        d = d.setdefault(key, {})
    d[path[-1]] = entry

def extract_parts(string):
    '''Extract Label, Description and Source from ID Question'''
    # Step 1: Split the string at the last occurrence of ') [' to isolate source
    parts = string.rsplit(') [', 1)
    if len(parts) == 2:
        main_part, c = parts[0].strip(), parts[1].rstrip(']')
    else:
        main_part, c = parts[0].strip(), ""
    # Step 2: Find the last whitespace outside brackets to split
    depth = 0
    split_index = -1
    for i, char in enumerate(main_part):
        if char in ('(', '['):
            depth += 1
        elif char in (')', ']'):
            depth -= 1
        elif char == ' ' and depth == 0:
            split_index = i  # Update split_index to last whitespace outside brackets
    if split_index != -1:
        a = main_part[:split_index].strip()
        b = main_part[split_index+1:].strip().lstrip('(')  # Strip any leading '('
    else:
        a, b = main_part, ""
    return a, b, c

def value_editor(project, uri, info):
    '''Add values to the Questionnaire'''
    attribute_object = Attribute.objects.get(uri=uri)
    # Prepare the defaults dictionary
    defaults = {
        'project': project,
        'attribute': attribute_object,
    }

    if info.get('text') is not None:
        defaults['text'] = info['text']

    if info.get('external_id') is not None:
        defaults['external_id'] = info['external_id']

    if info.get('option') is not None:
        defaults['option'] = Option.objects.get(uri=info['option'])

    # Prepare the fields for update_or_create
    update_fields = {
        'project': project,
        'attribute': attribute_object,
        'defaults': defaults
    }

    if info.get('collection_index') is not None:
        update_fields['collection_index'] = info['collection_index']

    if info.get('set_index') is not None:
        update_fields['set_index'] = info['set_index']

    if info.get('set_prefix') is not None:
        update_fields['set_prefix'] = info['set_prefix']

    # Update or create the value
    obj, created = Value.objects.update_or_create(**update_fields)

    return obj, created

def merge_dicts_with_unique_keys(answers, keys):
    '''Merge Dicts with unique Keys.'''
    merged_dict = {}

    for key in keys:
        for inner_key, value in answers[key].items():
            new_inner_key = f"{inner_key}{key}"
            merged_dict[new_inner_key] = value

    return merged_dict

def check_list(list_var):
    '''Check if List is List'''
    if list_var is None:
        list_var = []
    elif not isinstance(list_var, list):
        list_var = [list_var]
    return list_var

def label_index_map(data, data_type):
    '''Map Label to Index'''
    label_to_index_maps = []
    for to_idx_entry in data_type:
        label_to_index_maps.append(
            {
                data[to_idx_entry][k].get('Name'): idx
                for idx, k in enumerate(data.get(to_idx_entry, {}))
            }
        )
    return label_to_index_maps

def resolve_target(name, id_, entity_enc, label_map):
    """Try to resolve name to index in label_map; fallback to id_."""
    if name in label_map:
        return f"{entity_enc}{label_map[name] + 1}"
    return id_


def build_new_value(from_entry, entity, key, resolved, order):
    """Build the new value depending on relation and order flags."""
    if not entity['relation']:
        return resolved

    relation_value = from_entry.get(entity['relation'], {}).get(
        key, "MISSING RELATION TYPE"
    )

    if order['formulation']:
        return [
            relation_value,
            resolved,
            from_entry.get('formulation_number', {}).get(key),
        ]
    if order['task']:
        return [
            relation_value,
            resolved,
            from_entry.get('task_number', {}).get(key),
        ]
    if not order['formulation'] and not order['task']:
        return [relation_value, resolved]

    return resolved


def entity_relations(data, idx, entity, order):
    """Process Entity Relations."""
    idx['to'] = check_list(idx.get('to'))
    entity['encryption'] = check_list(entity['encryption'])
    label_to_index_maps = label_index_map(data, idx['to'])

    for from_entry in data.get(idx.get('from'), {}).values():
        for key, value in from_entry.get(entity['old_name'], {}).items():
            entity_values = from_entry.setdefault(entity['new_name'], {})

            resolved = None
            for enc_entry, label_map in zip(entity['encryption'], label_to_index_maps):
                resolved = resolve_target(
                    name=value.get("Name"),
                    id_=value.get("ID"),
                    entity_enc=enc_entry,
                    label_map=label_map,
                )
                if resolved != value.get("ID"):
                    break  # match found

            new_value = build_new_value(from_entry, entity, key, resolved, order)

            if key not in entity_values.values() and entity_values.get(key) != new_value:
                entity_values[key] = new_value

def initialize_counter(counter):
    '''Function which initializes counter.'''
    return int(max(counter, default=-1)) + 1

def map_entity(data, idx, entity):
    '''Map Entities'''
    # Ensure idx['to'] and enc are lists
    idx['to'] = check_list(idx['to'])
    entity['encryption'] = check_list(entity['encryption'])

    # Create mappings for all idx['to'] lists
    label_to_index_maps = label_index_map(data, idx['to'])

    # Use Template or Ressource Label
    for from_entry in data.get(idx['from'], {}).values():
        for outer_key, relation in from_entry.get(entity['old_name'], {}).items():
            for inner_key, entity_item in relation.items():
                match_found = False
                # Create Dict Entry
                outer = from_entry.setdefault(entity['new_name'], {})
                inner = outer.setdefault(outer_key, {})
                for enc_entry, label_to_index in zip(entity['encryption'], label_to_index_maps):
                    if entity_item['Name'] in label_to_index:
                        label_idx = label_to_index[entity_item['Name']]
                        match_found = True
                        inner[inner_key] = f"{enc_entry}{label_idx+1}"
                        break

                if not match_found:
                    inner[inner_key] = entity_item['ID']

def process_qualifier(value):
    '''Process Qualifier'''
    # Create Value Dictionary
    value_dict = {}
    # Get splitted Values
    value_splitted = value.split(' <|> ')
    for value_idx, value_text in enumerate(value_splitted):
        # Extract Value ID, Label, and Description
        value_id, value_label, value_description = value_text.split(' | ')
        # Get Value Source
        value_source, _ = value_id.split(':')
        # Add to dict
        value_dict.update({value_idx: {'id': value_id,
                                       'label': value_label,
                                       'description': value_description,
                                       'source': value_source}})
    return value_dict


def reduce_prefix(prefix):
    '''Function that takes a prefix and reduces it if |-appended.'''
    if isinstance(prefix, int):
        prefix_reduced = prefix
    else:
        prefix_reduced = int(prefix.split('|')[0])
    return prefix_reduced

def relation_exists(value, set_prefix_red, info, relation_id=None):
    '''Checks if a value–set (–relation) combination already exists in info.
       If relation_id is provided, also checks relation existence.'''

    # Case: relation check required
    if relation_id and "rels" in info:
        return any(
            (
                (f"{value.label} ({value.description})" in text or vid == value.id)
                and int(sid) == set_prefix_red
                and rel == relation_id
            )
            for vid, sid, rel, text in zip(
                info['value_ids'],
                info['set_prefix_ids'],
                info['rels'],
                info['texts'],
            )
        )

    # Case: only value + set check
    return any(
        (
            (f"{value.label} ({value.description})" in text or vid == value.id)
            and int(sid) == set_prefix_red
        )
        for vid, sid, text in zip(
            info['value_ids'],
            info['set_prefix_ids'],
            info['texts']
        )
    )

def relevant_set_ids(info, set_prefix_red):
    ''''Get relevant Set IDs'''
    relevant_set_ids_list = []
    for set_index, set_prefix in zip(info['set_index_ids'], info['set_prefix_ids']):
        if set_prefix == set_prefix_red:
            relevant_set_ids_list.append(set_index)
    return relevant_set_ids_list

def replace_in_dict(d, target, replacement):
    '''Replace IDs in Dict'''
    if isinstance(d, dict):
        return {k: replace_in_dict(v, target, replacement) for k, v in d.items()}
    if isinstance(d, list):
        return [replace_in_dict(v, target, replacement) for v in d]
    if isinstance(d, str):
        return d.replace(target, replacement)
    return d

def unique_items(data, title = None):
    '''Search unique Items'''
    # Set up Item Dict and track seen Items
    items = {}
    seen_items = set()
    # Add Workflow Item
    if title:
        triple = (
            'not found',
            title,
            data.get('general', {}).get('objective', '')
        )
        items[f'Item{str(0).zfill(10)}'] = {
            'ID': 'not found',
            'Name': title,
            'Description': data.get('general', {}).get('objective', '')
        }
        seen_items.add(triple)
    # Add Workflow Component Items
    def search(subdict):
        '''Search unique Items'''
        if isinstance(subdict, dict) and 'ID' in subdict:
            triple = (
                subdict.get('ID', ''),
                subdict.get('Name', ''),
                subdict.get('Description', ''),
                subdict.get('orcid', ''),
                subdict.get('zbmath', ''),
                subdict.get('issn', '')
            )
            if triple not in seen_items:
                item_key = f'Item{str(len(items)).zfill(10)}'  # Create unique key
                items[item_key] = {
                    'ID': triple[0],
                    'Name': triple[1],
                    'Description': triple[2],
                    'orcid': triple[3],
                    'zbmath': triple[4],
                    'issn': triple[5]
                }
                seen_items.add(triple)
        if isinstance(subdict, dict):
            for value in subdict.values():
                if isinstance(value, dict):
                    search(value)
    search(data)
    return items

def inline_mathml(data):
    '''Process MathML to be inline'''
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                if '<math' in value:
                    data[key] = clean_mathml(value)
            elif isinstance(value, (dict, list)):
                inline_mathml(value)
    elif isinstance(data, list):
        for item in data:
            inline_mathml(item)

def clean_mathml(mathml_str):
    '''Clean MathL'''
    def clean_tag(match):
        '''Clean Tag'''
        tag = match.group(1)
        # Keep xmlns on <math> tag
        if tag.startswith('math'):
            xmlns_match = re.search(r'xmlns="[^"]+"', tag)
            if xmlns_match:
                return f"<math {xmlns_match.group(0)}>"
            return "<math>"
        else:
            # Just keep the tag name, strip attributes
            tagname_match = re.match(r'^/?\w+', tag)
            if tagname_match:
                return f"<{tagname_match.group(0)}>"
            return f"<{tag}>"

    # Apply substitution on all opening tags
    cleaned = re.sub(r'<([^>\s]+(?:\s[^>]*)?)>', clean_tag, mathml_str)
    return cleaned

def process_question_dict(project, questions, get_answer):
    """Iterate through nested questions dict and extract answers using provided answer function."""
    answers = {}

    for group in questions.values():
        for sub_key, config in group.items():
            if sub_key == "uri":
                continue  # Skip the group-level URI

            if not isinstance(config, dict) or "uri" not in config:
                continue  # Skip invalid or metadata-only entries

            # Fill in optional/default values
            config = {
                "key1": config.get("key1"),
                "key2": config.get("key2"),
                "key3": config.get("key3"),
                "uri": config["uri"],
                "set_prefix": config.get("set_prefix", False),
                "set_index": config.get("set_index", False),
                "collection_index": config.get("collection_index", False),
                "external_id": config.get("external_id", False),
                "option_text": config.get("option_text", False),
            }

            # Call the injected function
            answers = get_answer(
                project,
                answers,
                config
            )

    return answers
