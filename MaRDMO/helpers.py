import re

from rdmo.projects.models import Value
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

def extract_parts(string):
    # Step 1: Split the string at the last occurrence of ') [' to isolate `c` (source)
    parts = string.rsplit(') [', 1)
    if len(parts) == 2:
        main_part, c = parts[0].strip(), parts[1].rstrip(']')
    else:
        main_part, c = parts[0].strip(), ""
    # Step 2: Find the last whitespace outside brackets to split `a` and `b`
    depth = 0
    split_index = -1
    for i, char in enumerate(main_part):
        if char == '(' or char == '[':
            depth += 1
        elif char == ')' or char == ']':
            depth -= 1
        elif char == ' ' and depth == 0:
            split_index = i  # Update split_index to last whitespace outside brackets
    if split_index != -1:
        a = main_part[:split_index].strip()
        b = main_part[split_index+1:].strip().lstrip('(')  # Strip any leading '(' from b
    else:
        a, b = main_part, ""
    return a, b, c

def value_editor(project, uri, text=None, external_id=None, option=None, collection_index=None, set_index=None, set_prefix=None):
    '''Add values to the Questionnaire'''
    attribute_object = Attribute.objects.get(uri=uri)
    # Prepare the defaults dictionary
    defaults = {
        'project': project,
        'attribute': attribute_object,
    }

    if text is not None:
        defaults['text'] = text

    if external_id is not None:
        defaults['external_id'] = external_id

    if option is not None:
        defaults['option'] = Option.objects.get(uri=option)

    # Prepare the fields for update_or_create
    update_fields = {
        'project': project,
        'attribute': attribute_object,
        'defaults': defaults
    }

    if collection_index is not None:
        update_fields['collection_index'] = collection_index

    if set_index is not None:
        update_fields['set_index'] = set_index

    if set_prefix is not None:
        update_fields['set_prefix'] = set_prefix

    # Update or create the value
    obj, created = Value.objects.update_or_create(**update_fields)

    return obj, created

def merge_dicts_with_unique_keys(answers, keys):
    
    merged_dict = {}
    
    for key in keys:
        for inner_key, value in answers[key].items():
            new_inner_key = f"{inner_key}{key}"
            merged_dict[new_inner_key] = value    
    
    return merged_dict

def checkList(LIST):
    if not isinstance(LIST, list):
        LIST = [LIST]
    return LIST

def labelIndexMap(data, type):
    label_to_index_maps = []
    for toIDX_entry in type:
        label_to_index_maps.append({data[toIDX_entry][k].get('Name'): idx for idx, k in enumerate(data.get(toIDX_entry, {}))})
    return label_to_index_maps

def entityRelations(data, fromIDX='', toIDX=[], relationOld='', entityOld='', entityNew='', enc=[], forder=False, torder=False):
    toIDX = checkList(toIDX)
    enc = checkList(enc)
    label_to_index_maps = labelIndexMap(data, toIDX)

    def resolve_target(name, id_, entity_enc, label_map):
        """Try to resolve name to index in label_map; fallback to id_."""
        if name in label_map:
            idx = label_map[name]
            return f"{entity_enc}{idx + 1}"
        return id_

    for from_entry in data.get(fromIDX, {}).values():
        entries = from_entry.get(entityOld, {})
        for key, value in entries.items():
            name = value.get("Name")
            id_ = value.get("ID")
            entity_values = from_entry.setdefault(entityNew, {})

            resolved = None
            for enc_entry, label_map in zip(enc, label_to_index_maps):
                resolved = resolve_target(name, id_, enc_entry, label_map)
                if resolved != id_:
                    break  # match found

            if relationOld:
                if from_entry.get(relationOld, {}).get(key):
                    relation_value = from_entry[relationOld][key]
                else:
                    relation_value = 'MISSING RELATION TYPE'
                if forder == False and torder == False:
                    new_value = [relation_value, resolved]
                elif forder == True:
                    new_value = [relation_value, resolved, from_entry.get('formulation_number',{}).get(key)]
                elif torder == True:
                    new_value = [relation_value, resolved, from_entry.get('task_number',{}).get(key)]
                else:
                    new_value = resolved
            else:
                new_value = resolved

            if key not in entity_values.values() and entity_values.get(key) != new_value:
                entity_values[key] = new_value

    return

def mapEntity(data, fromIDX, toIDX, entityOld, entityNew, enc):
    
    # Ensure toIDX and enc are lists
    toIDX = checkList(toIDX)
    enc = checkList(enc)
    
    # Create mappings for all toIDX lists
    label_to_index_maps = labelIndexMap(data, toIDX)
    
    # Use Template or Ressource Label
    for from_entry in data.get(fromIDX, {}).values():
        for outerKey, relation in from_entry.get(entityOld, {}).items():
            for innerKey, entity in relation.items():
                match_found = False
                for enc_entry, label_to_index in zip(enc, label_to_index_maps):
                    if entity['Name'] in label_to_index:
                        idx = label_to_index[entity['Name']]
                        match_found = True
                        from_entry.setdefault(entityNew, {}).setdefault(outerKey, {}).update({innerKey: f'{enc_entry}{idx+1}'})
                        break

                if not match_found:
                    from_entry.setdefault(entityNew, {}).setdefault(outerKey, {}).update({innerKey: entity['ID']})
    return

def replace_in_dict(d, target, replacement):
    if isinstance(d, dict):
        return {k: replace_in_dict(v, target, replacement) for k, v in d.items()}
    elif isinstance(d, list):
        return [replace_in_dict(v, target, replacement) for v in d]
    elif isinstance(d, str):
        return d.replace(target, replacement)
    else:
        return d 
        
def unique_items(data, title = None):
    # Set up Item Dict and track seen Items
    items = {}
    seen_items = set() 
    # Add Workflow Item
    if title:
        triple = ('not found', title, data.get('general', {}).get('objective', ''))
        items[f'Item{str(0).zfill(10)}'] = {'ID': 'not found', 'Name': title, 'Description': data.get('general', {}).get('objective', '')}
        seen_items.add(triple)
    # Add Workflow Component Items
    def search(subdict):
        if isinstance(subdict, dict) and 'ID' in subdict:
            triple = (subdict.get('ID', ''), subdict.get('Name', ''), subdict.get('Description', ''))
            if triple not in seen_items:
                item_key = f'Item{str(len(items)).zfill(10)}'  # Create unique key
                items[item_key] = {'ID': triple[0], 'Name': triple[1], 'Description': triple[2]}
                seen_items.add(triple)
        if isinstance(subdict, dict):
            for value in subdict.values():
                if isinstance(value, dict):
                    search(value)
    search(data)
    return items

def inline_mathml(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                if '<math' in value:
                    data[key] = clean_mathml(value)
            elif isinstance(value, dict) or isinstance(value, list):
                inline_mathml(value)
    elif isinstance(data, list):
        for item in data:
            inline_mathml(item)

def clean_mathml(mathml_str):
    def clean_tag(match):
        tag = match.group(1)
        # Keep xmlns on <math> tag
        if tag.startswith('math'):
            xmlns_match = re.search(r'xmlns="[^"]+"', tag)
            if xmlns_match:
                return f"<math {xmlns_match.group(0)}>"
            else:
                return "<math>"
        else:
            # Just keep the tag name, strip attributes
            tagname_match = re.match(r'^/?\w+', tag)
            if tagname_match:
                return f"<{tagname_match.group(0)}>"
            else:
                return f"<{tag}>"

    # Apply substitution on all opening tags
    cleaned = re.sub(r'<([^>\s]+(?:\s[^>]*)?)>', clean_tag, mathml_str)
    return cleaned