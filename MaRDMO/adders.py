'''Functions to add Information to the Questionaire.'''

from rdmo.options.models import Option

from .config import BASE_URI
from .getters import get_id, get_options
from .helpers import extract_parts, value_editor


def add_basics(project, text, questions, item_type, index = (None, None)):
    '''Function extracts Label, Description and Source of Items selected or defined
       in the ID Question on each Page. Label and Description are added to the Name
       and Description Questions on the individual Pages.
       
       Input: Selected/Defined Item as String 'Label (Description) [source]'
       Output: Label, Description and Source'''

    # Extract Label, Description, Source from ID Question
    label, description, source = extract_parts(text)

    # Add Label to Questionnaire
    value_editor(project = project,
                 uri = f'{BASE_URI}{questions[item_type]["Name"]["uri"]}',
                 text = label,
                 set_index = index[0],
                 set_prefix = index[1])

    # Add Description to Questionnaire
    value_editor(project = project,
                 uri = f'{BASE_URI}{questions[item_type]["Description"]["uri"]}',
                 text = description,
                 set_index = index[0],
                 set_prefix = index[1])

    return label, description, source

def add_entities(project, question_set, datas, source, prefix):
    '''Function checks if an Item selected in one Section of the Questionnaire is 
       defined in another Section of the Questionnaire. If the Item is not yet in
       the Questionnaire a new Page is created and the ID Question is answered.

       Input: Item Information
       Output: -'''

    # Generate ID, Name and Description URL from Set URL
    question = {'id': f'{question_set}/id',
                'name': f'{question_set}/name',
                'description': f'{question_set}/description'}

    # Get existing Set and Item Information
    info = {'set_ids': get_id(project, question_set, ['set_index']),
            'value_ids': get_id(project, question['id'], ['external_id']),
            'texts': get_id(project, question['id'], ['text']),
            'names': get_id(project, question['name'], ['text']),
            'descs': get_id(project, question['description'], ['text'])}

    # Add Item to Questionnaire
    idx = max(info['set_ids'], default = -1) + 1

    for data in datas:
        # Label Description String
        name_desc = f'{data.label} ({data.description})'
        # Check if Item already in Questionnaire via ID Question
        check_id = any(
            name_desc in text
            for text in info['texts']
            )
        # Check if Item already in Questionnaire via Name/Description Question
        check_name_desc = any(
            name_desc in f'{name} ({desc})'
            for name, desc in zip(info['names'], info['descs'])
            )
        # If Item not already in Questionnaire
        if data.id not in info['value_ids'] and not check_id and not check_name_desc:
            # Set up Page in Questionnaire
            value_editor(project = project,
                         uri = question_set,
                         text = f"{prefix}{idx}",
                         set_index = idx)
            # Add ID Values
            value_editor(project = project,
                         uri = question['id'],
                         text = f'{data.label} ({data.description}) [{source}]',
                         external_id = f"{data.id}",
                         set_index = idx)

            # Update Index and existing Items
            idx += 1
            info['value_ids'].append(data.id)

def add_new_entities(project, question_set, datas, prefix):
    '''Function checks if an Item defined in one Section of the Questionnaire is 
       defined in another Section of the Questionnaire. If the Item is not yet in
       the Questionnaire a new Page is created and the ID Question is answered.

       Input: Item Information
       Output: -'''

    # Generate ID, Name and Description URL from Set URL
    question = {'id': f'{question_set}/id',
                'name': f'{question_set}/name',
                'description': f'{question_set}/description'}

    # Get existing Set and Item Information
    info = {'set_ids': get_id(project, question_set, ['set_index']),
            'names': get_id(project, question['name'], ['text']),
            'descs': get_id(project, question['description'], ['text'])}

    # Add Publication to Questionnaire
    idx = max(info['set_ids'], default = -1) + 1
    for data in datas:
        # Label Description String
        name_desc = f'{data.label} ({data.description})'
        # Check if Item already in Questionnaire via Name/Description Question
        check_name_desc = any(
            name_desc in f'{name} ({desc})'
            for name, desc in zip(info['names'], info['descs'])
            )
        # If Item not already in Questionnaire
        if not check_name_desc:
            # Set up Page
            value_editor(project = project,
                         uri = question_set,
                         text = f"{prefix}{idx}",
                         set_index = idx)
            # Add ID Values
            value_editor(project = project,
                         uri = question['id'],
                         text = 'not found',
                         external_id = 'not found',
                         set_index = idx)
            # Add Name Values
            value_editor(project = project,
                         uri = question['name'],
                         text = data.label,
                         set_prefix = idx)
            # Add Description Values
            value_editor(project = project,
                         uri = question['description'],
                         text = data.description,
                         set_prefix = idx)

            # Update Index
            idx += 1

def add_relations(project, data, props, set_prefix, relatant,
                  mapping=None, relation=None, assumption=None, order=None):
    '''Function checks if an Item and a Relation (fixed/flexible) are part of the 
       Questionnaire. If the Item / Relation Pair is not yet in the Questionnaire 
       it is added to the Questionnaire. Qualifiers are likewise checked and added.

       Input: Item Information + Relation (if flexible)
       Output: -'''

    # Get existing Set, Item and Relation Information
    info = {'set_ids': get_id(project, relatant, ['set_prefix']),
            'set_ids2': get_id(project, relatant, ['set_index']),
            'collection_ids': get_id(project, relatant, ['collection_index']),
            'value_ids': get_id(project, relatant, ['external_id']),
            'texts': get_id(project, relatant, ['text'])}
    if relation:
        info['rels'] = get_id(project, relation, ['option_uri'])

    # Get IDs by reduced set_prefixes
    set_prefix_red = set_prefix if isinstance(set_prefix, int) else int(set_prefix.split('|')[0])
    ids = [set_id2
           for set_id2, set_id in zip(info['set_ids2'], info['set_ids'])
           if set_id == set_prefix_red]

    # Set initial value of counter
    idx = int(max(ids if relation else info['collection_ids'], default=-1)) + 1

    # Add Relations and Relatants
    for prop in props:
        for value in getattr(data, prop):

            # Get Source and Label Description String
            source, _ = value.id.split(':')
            name_desc = f"{value.label} ({value.description})"

            if relation:
                # Check if Relation / Relatant Combination exists (flexible relation)
                matches = any(
                    value.id == vid and int(sid) == set_prefix_red and rel == mapping[prop]
                    for vid, sid, rel in zip(info['value_ids'], info['set_ids'], info['rels'])
                    )

                if matches:
                    # Continue if existing
                    continue

                # Define Indices for Relation / Relatant Entry
                existing_index = None
                collection_index = None
                set_index = idx

                # Add Relation to Questionnaire
                value_editor(project = project,
                             uri = relation,
                             option = Option.objects.get(uri=mapping[prop]),
                             collection_index = collection_index,
                             set_index = set_index,
                             set_prefix = set_prefix)
            else:
                # Check if Relation / Relatant Combination exists (fixed relation)
                matches = any(
                    value.id == vid and int(sid) == set_prefix_red
                    for vid, sid in zip(info['value_ids'], info['set_ids'])
                    )

                if matches:
                    # Continue if existing
                    continue

                # Define Indices for Relatant Entry
                existing_index = next(
                    (i for i, (text, sid) in enumerate(zip(info['texts'], info['set_ids']))
                    if sid == set_prefix and name_desc in text), None
                    )
                collection_index = existing_index if existing_index is not None else idx
                set_index = 0

            # Add Relatant to Questionnaire
            value_editor(
                project = project,
                uri = relatant,
                text = f"{name_desc} [{source}]",
                external_id = value.id,
                collection_index = collection_index,
                set_index = set_index,
                set_prefix = set_prefix
                )

            # Add Assumption
            if assumption and hasattr(value, 'qualifier') and value.qualifier:
                # Get Assumptions
                assumptions = value.qualifier.split(' <|> ')
                for a_idx, a_value in enumerate(assumptions):
                    # Extract Assumption ID, Label, and Description
                    a_id, a_label, a_description = a_value.split(' | ')
                    # Get Assumption Source and Name Description String
                    a_source, _ = a_id.split(':')
                    a_name_desc = f"{a_label} ({a_description})"
                    # Add Assumption to Questionnaire
                    value_editor(
                        project = project,
                        uri = assumption,
                        text = f"{a_name_desc} [{a_source}]",
                        external_id = a_id,
                        collection_index = a_idx,
                        set_index = set_index,
                        set_prefix = set_prefix
                        )

            # Add Order Number
            if order and hasattr(value, 'order') and value.order:
                # Add Order Number to Questionnaire
                value_editor(
                    project = project,
                    uri = order,
                    text = value.order,
                    set_index = set_index,
                    set_prefix = set_prefix
                    )

            if existing_index is None:
                # Only increment if a new entry was added
                idx += 1

            # Update existing IDs, Texts, and Relations
            info['value_ids'].append(value.id)
            info['set_ids'].append(set_prefix_red)
            info['texts'].append(f"{name_desc} [{source}]")
            if relation:
                info['rels'].append(mapping[prop])

def add_properties(project, data, uri, set_prefix):
    '''Function which adds Data Properties to the Questionnaire.
       
       Input: Data Properties
       Output: -'''

    for key, value in data.properties.items():
        value_editor(project = project,
                     uri  = uri,
                     option = Option.objects.get(uri=value[0]),
                     collection_index = key,
                     set_index = 0,
                     set_prefix = set_prefix)

def add_references(project, data, uri, set_index = 0, set_prefix = None):
    '''Function which adds References to the Questionnaire.
       
       Input: References
       Output: -'''

    for key, value in data.reference.items():
        value_editor(project = project,
                     uri  = uri,
                     text = value[1],
                     option = Option.objects.get(uri=value[0]),
                     collection_index = key,
                     set_index = set_index,
                     set_prefix = set_prefix)

def add_reference_order(entity):
    '''Function which defines the reference order according to the Item type
    
       Input: Item Information
       Output: -'''
    options = get_options()
    # Define Flexible Key and Value
    flex_key = 'morwiki' if entity == 'benchmark' else 'swmath'
    flex_value = options['MORWIKI' if entity == 'benchmark' else 'SWMATH']
    # Define Reference Order
    order = {
        'doi': (0, options['DOI']),
        flex_key: (1, flex_value),
        'url': (2, options['URL']),
        }
    return order
