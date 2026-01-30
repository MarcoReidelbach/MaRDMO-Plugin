'''Functions to add Information to the Questionaire.'''

from rdmo.options.models import Option

from .constants import BASE_URI
from .getters import get_id, get_options
from .helpers import (
    extract_parts,
    initialize_counter,
    process_qualifier,
    reduce_prefix,
    relation_exists,
    relevant_set_ids,
    value_editor,
)


def add_basics(project, text, questions, item_type, index = (None, None)):
    '''Function extracts Label, Description and Source of Items selected or defined
       in the ID Question on each Page. Label and Description are added to the Name
       and Description Questions on the individual Pages.
       
       Input: Selected/Defined Item as String 'Label (Description) [source]'
       Output: Label, Description and Source'''

    # Extract Label, Description, Source from ID Question
    label, description, source = extract_parts(text)

    # Add Label to Questionnaire
    value_editor(
        project = project,
        uri = f'{BASE_URI}{questions[item_type]["Name"]["uri"]}',
        info = {
            'text': label,
            'set_index': index[0],
            'set_prefix': index[1]
        }
    )

    # Add Description to Questionnaire
    value_editor(
        project = project,
        uri = f'{BASE_URI}{questions[item_type]["Description"]["uri"]}',
        info = {
            'text': description,
            'set_index': index[0],
            'set_prefix': index[1]
        }
    )

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
            value_editor(
                project = project,
                uri = question_set,
                info = {
                    'text': f"{prefix}{int(idx)+1}",
                    'set_index': idx
                }
            )
            # Add ID Values
            value_editor(
                project = project,
                uri = question['id'],
                info = {
                    'text': f'{data.label} ({data.description}) [{source}]',
                    'external_id': f"{data.id}",
                    'set_index': idx
                }
            )

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
            name_desc == f'{name} ({desc})'
            for name, desc in zip(info['names'], info['descs'])
            )
        # If Item not already in Questionnaire
        if not check_name_desc:
            # Set up Page
            value_editor(
                project = project,
                uri = question_set,
                info = {
                    'text': f"{prefix}{int(idx)+1}",
                    'set_index': idx
                }
            )
            # Add ID Values
            value_editor(
                project = project,
                uri = question['id'],
                info = {
                    'text': 'not found',
                    'external_id': 'not found',
                    'set_index': idx
                }
            )
            # Add Name Values
            value_editor(
                project = project,
                uri = question['name'],
                info = {
                    'text': data.label,
                    'set_prefix': idx
                }
            )
            # Add Description Values
            value_editor(
                project = project,
                uri = question['description'],
                info = {
                    'text': data.description,
                    'set_prefix': idx
                }
            )

            # Update Index
            idx += 1

def add_relations_static(project, data, props, index, statement):
    '''Function checks if a related pair (relation and relatant) are part of the 
       Questionnaire (fixed relation). If the pair is not yet in the Questionnaire 
       it is added to the Questionnaire. Qualifiers are likewise checked and added.

       Input: Item Information + Relation (if flexible)
       Output: -'''

    # Get existing Set and Item Information
    info = {'set_prefix_ids': get_id(project, statement['relatant'], ['set_prefix']),
            'set_index_ids': get_id(project, statement['relatant'], ['set_index']),
            'collection_ids': get_id(project, statement['relatant'], ['collection_index']),
            'value_ids': get_id(project, statement['relatant'], ['external_id']),
            'texts': get_id(project, statement['relatant'], ['text'])}

    # Get reduced set_prefixes
    index.update({'set_prefix_reduced': reduce_prefix(index['set_prefix'])})

    # Set initial value of counter
    index.update({'idx': initialize_counter(info['collection_ids'])})

    # Add Relations and Relatants
    for prop in props['keys']:
        for value in getattr(data, prop):

            # Get Source and Label Description String
            source, _ = value.id.split(':')

            # Check if Relatant exists
            matches = relation_exists(
                value = value,
                set_prefix_red = index['set_prefix_reduced'],
                info = info)

            if matches:
                # Continue if existing
                continue

            # Add Relatant to Questionnaire
            value_editor(
                project = project,
                uri = statement['relatant'],
                info = {
                    'text': f"{value.label} ({value.description}) [{source}]",
                    'external_id': value.id,
                    'collection_index': index['idx'],
                    'set_index': 0,
                    'set_prefix': index['set_prefix']
                }
            )

            #Update Index
            index['idx'] += 1

            # Update existing IDs, Texts, and Relations
            info['value_ids'].append(value.id)
            info['set_prefix_ids'].append(index['set_prefix_reduced'])
            info['texts'].append(f"{value.label} ({value.description}) [{source}]")

def add_relations_flexible(project, data, props, index, statement):
    '''Function checks if an Item and a Relation (fixed/flexible) are part of the 
       Questionnaire. If the Item / Relation Pair is not yet in the Questionnaire 
       it is added to the Questionnaire. Qualifiers are likewise checked and added.

       Input: Item Information + Relation (if flexible)
       Output: -'''

    # Get existing Set, Item and Relation Information
    info = {'set_prefix_ids': get_id(project, statement['relatant'], ['set_prefix']),
            'set_index_ids': get_id(project, statement['relatant'], ['set_index']),
            'collection_ids': get_id(project, statement['relatant'], ['collection_index']),
            'value_ids': get_id(project, statement['relatant'], ['external_id']),
            'texts': get_id(project, statement['relatant'], ['text']),
            'rels': get_id(project, statement['relation'], ['option_uri'])}

    # Get reduced set prefix ids
    index.update({'set_prefix_reduced': reduce_prefix(index['set_prefix'])})

    # Get relevant set index ids
    ids = relevant_set_ids(info, index['set_prefix_reduced'])

    # Set initial value of counter
    index.update({'idx': initialize_counter(ids)})

    # Add Relations and Relatants
    for prop in props['keys']:
        inner_idx = 0
        assumption_store = {}
        order_number_store = {}
        for value in getattr(data, prop):
            assumption_index = None
            order_number_index = None
            # Get Source and Label Description String
            source, _ = value.id.split(':')

            # Check if Relation / Relatant Combination exists (flexible relation)
            matches = relation_exists(
                value = value,
                set_prefix_red = index['set_prefix_reduced'],
                info = info,
                relation_id = props['mapping'][prop]
            )

            if matches:
                # Continue if existing
                continue

            # Add Order Number
            if statement.get('order') and hasattr(value, 'order') and value.order:
                if value.order not in order_number_store:
                    index['idx'] +=1
                    inner_idx = 0
                    order_number_store.update({value.order: index['idx']})
                order_number_index = order_number_store.get(value.order)
                # Add Order Number to Questionnaire
                value_editor(
                    project = project,
                    uri = statement['order'],
                    info = {
                        'text': value.order,
                        'set_index': order_number_index,
                        'set_prefix': index['set_prefix']
                    }
                )

            # Add Assumption
            if statement.get('assumption') and hasattr(value, 'qualifier') and value.qualifier:
                if value.qualifier not in assumption_store:
                    index['idx'] +=1
                    inner_idx = 0
                    assumption_store.update({value.qualifier: index['idx']})
                assumption_index = assumption_store.get(value.qualifier)
                # Get Assumptions
                assumption_dict = process_qualifier(value.qualifier)
                # Add Assumptions
                for assumption_key, assumption_value in assumption_dict.items():
                    value_editor(
                        project = project,
                        uri = statement['assumption'],
                        info = {
                            'text': "{label} ({description}) [{source}]".format_map(
                                assumption_value
                            ),
                            'external_id': assumption_value['id'],
                            'collection_index': assumption_key,
                            'set_index': assumption_index,
                            'set_prefix': index['set_prefix']
                        }
                    )

            # Add Relation to Questionnaire
            value_editor(
                project = project,
                uri = statement['relation'],
                info = {
                    'option': Option.objects.get(uri=props['mapping'][prop]),
                    'collection_index': None,
                    'set_index': order_number_index or assumption_index or index['idx'],
                    'set_prefix': index['set_prefix']
                }
            )

            # Add Relatant to Questionnaire
            value_editor(
                project = project,
                uri = statement['relatant'],
                info = {
                    'text': f"{value.label} ({value.description}) [{source}]",
                    'external_id': value.id,
                    'collection_index': inner_idx,
                    'set_index': order_number_index or assumption_index or index['idx'],
                    'set_prefix': index['set_prefix']
                }
            )

            # Update existing IDs, Texts, and Relations
            info['value_ids'].append(value.id)
            info['set_prefix_ids'].append(index['set_prefix_reduced'])
            info['texts'].append(f"{value.label} ({value.description}) [{source}]")
            info['rels'].append(props['mapping'][prop])

            inner_idx += 1

        # Update index
        index['idx'] += 1

def add_properties(project, data, uri, set_prefix):
    '''Function which adds Data Properties to the Questionnaire.
       
       Input: Data Properties
       Output: -'''

    for key, value in data.properties.items():
        value_editor(
            project = project,
            uri  = uri,
            info = {
                'option': Option.objects.get(uri=value[0]),
                'collection_index': key,
                'set_index': 0,
                'set_prefix': set_prefix
            }
        )

def add_references(project, data, uri, set_index = 0, set_prefix = None):
    '''Function which adds References to the Questionnaire.
       
       Input: References
       Output: -'''

    for key, value in data.reference.items():
        value_editor(
            project = project,
            uri  = uri,
            info = {
                'text': value[1],
                'option': Option.objects.get(uri=value[0]),
                'collection_index': key,
                'set_index': set_index,
                'set_prefix': set_prefix
            }
        )

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
