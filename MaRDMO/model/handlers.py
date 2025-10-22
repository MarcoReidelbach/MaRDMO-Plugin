'''Module containing Handlers for the Model Documentation'''

from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value
from rdmo.options.models import Option

from . import models

from .constants import props, relatant_uris, relation_uris, index_counters, get_uri_prefix_map

from ..config import BASE_URI, endpoint
from ..getters import get_items, get_mathmoddb, get_properties, get_questions, get_sparql_query
from ..helpers import extract_parts, value_editor
from ..queries import query_sparql
from ..adders import (
    add_basics,
    add_entities,
    add_new_entities,
    add_properties,
    add_relations_static,
    add_relations_flexible,
    add_references
)

@receiver(post_save, sender=Value)
def field_information(sender, **kwargs):
    '''Research Field Handler, checking if an existing Field is chosen,
       querying the external Source, and integrating the related Meta-
       data into the Questionnaire.'''
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-model-catalog'):
        # Get Questions of Model Catalog...
        questions = get_questions('model') | get_questions('publication')
        #... and Research Field specific Questions.
        field = questions["Research Field"]
        if instance.attribute.uri == f'{BASE_URI}{field["ID"]["uri"]}':
            if instance.text and instance.text != 'not found':

                # Add basic Informatiom
                add_basics(
                    project = instance.project,
                    text = instance.text,
                    questions = questions,
                    item_type = 'Research Field',
                    index = (0, instance.set_index)
                )

                # Get source and ID of Item
                source, identifier = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return

                # If Item from MathModDB, set up Query...
                query = get_sparql_query('model/queries/field.sparql').format(
                    identifier,
                    **get_items(),
                    **get_properties()
                )
                
                # ...get Results...
                results = query_sparql(query, endpoint[source]['sparql'])
                
                # ... and load MathModDB Vocabulary.
                mathmoddb = get_mathmoddb()

                if not results:
                    return

                # Structure Results
                data = models.ResearchField.from_query(results)

                # Add long Descriptions (optional)
                for idx, description_long in enumerate(data.description_long):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{field["Long Description"]["uri"]}',
                        info = {
                            'text': description_long, 
                            'collection_index': idx,
                            'set_index': 0, 
                            'set_prefix': instance.set_index
                        }
                    )

                # Add Research Field Relations (flexible)
                add_relations_flexible(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['Field'],
                        'mapping': mathmoddb,
                    },
                    index = {
                        'set_prefix': instance.set_index
                    },
                    statement = {
                        'relation': f'{BASE_URI}{field["IntraClassRelation"]["uri"]}',
                        'relatant': f'{BASE_URI}{field["IntraClassElement"]["uri"]}',
                    },
                )

                # Add Publications
                add_entities(
                    project = instance.project,
                    question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                    datas = data.publications,
                    source = source,
                    prefix = 'P'
                )

@receiver(post_save, sender=Value)
def problem_information(sender, **kwargs):
    '''Research Problem Handler, checking if an existing Problem is chosen,
       querying the external Source, and integrating the related Meta-
       data into the Questionnaire.'''
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-model-catalog'):
        # Get Questions of Model Catalog...
        questions = get_questions('model') | get_questions('publication')
        #... Research Problem specific Questions.
        problem = questions["Research Problem"]
        if instance.attribute.uri == f'{BASE_URI}{problem["ID"]["uri"]}':
            if instance.text and instance.text != 'not found':

                # Add basic Information
                add_basics(
                    project = instance.project,
                    text = instance.text,
                    questions = questions,
                    item_type = 'Research Problem',
                    index = (0, instance.set_index)
                )

                # Get source and ID of Item
                source, identifier = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return

                # If Item from MathModDB, set up Query...
                query = get_sparql_query('model/queries/problem.sparql').format(
                    identifier,
                    **get_items(),
                    **get_properties()
                )

                # ...get Results...
                results = query_sparql(query, endpoint[source]['sparql'])

                # ...and load MathModDB Vocabulary.
                mathmoddb = get_mathmoddb()

                if not results:
                    return

                # Structure Results
                data = models.ResearchProblem.from_query(results)

                # Add long Description (optional)
                for idx, description_long in enumerate(data.description_long):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{problem["Long Description"]["uri"]}',
                        info = {
                            'text': description_long,
                            'collection_index': idx, 
                            'set_index': 0, 
                            'set_prefix': instance.set_index
                        }
                    )

                # Add Research Field Relations (static)
                add_relations_static(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['RP2RF']
                    },
                    index = {
                        'set_prefix': instance.set_index
                    },
                    statement = {
                        'relatant': f'{BASE_URI}{problem["RFRelatant"]["uri"]}'
                    }
                )

                # Add Research Problem Relations (flexible)
                add_relations_flexible(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['Problem'],
                        'mapping': mathmoddb,
                    },
                    index = {
                        'set_prefix': instance.set_index
                    },
                    statement = {
                        'relation': f'{BASE_URI}{problem["IntraClassRelation"]["uri"]}',
                        'relatant': f'{BASE_URI}{problem["IntraClassElement"]["uri"]}',
                    },
                )

                # Add Publications
                add_entities(
                    project = instance.project,
                    question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                    datas = data.publications,
                    source = source,
                    prefix = 'P'
                )

@receiver(post_save, sender=Value)
def quantity_information(sender, **kwargs):
    '''Quantity [Kind] Handler, checking if an existing Quantity is chosen,
       querying the external Source, and integrating the related Meta-
       data into the Questionnaire.'''
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-model-catalog'):
        # Get Questions of Model Catalog...
        questions = get_questions('model') | get_questions('publication')
        #... and quantity specific Questions.
        quantity = questions["Quantity"]
        if instance.attribute.uri == f'{BASE_URI}{quantity["ID"]["uri"]}':
            if instance.text and instance.text != 'not found':

                # Add basic Information
                add_basics(
                    project = instance.project,
                    text = instance.text,
                    questions = questions,
                    item_type = 'Quantity',
                    index = (0, instance.set_index)
                )

                # Get source and ID of Item
                source, identifier = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return

                # If Item from MathModDB, set up Query...
                query = get_sparql_query('model/queries/quantity.sparql').format(
                    identifier,
                    **get_items(),
                    **get_properties()
                )

                # ...get Results...
                results = query_sparql(query, endpoint[source]['sparql'])

                # ...and load MathModDB Vocabulary.
                mathmoddb = get_mathmoddb()

                if not results:
                    return

                # Structure Results
                data = models.QuantityOrQuantityKind.from_query(results)

                # Add long Description (optional)
                for idx, description_long in enumerate(data.description_long):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{quantity["Long Description"]["uri"]}',
                        info = {
                            'text': description_long,
                            'collection_index': idx, 
                            'set_index': 0, 
                            'set_prefix': instance.set_index
                        }
                    )

                # Add Type
                if data.qclass:
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{quantity["QorQK"]["uri"]}',
                        info = {
                            'option': Option.objects.get(
                                uri=mathmoddb[results[0]['class']['value']]
                            ),
                            'set_index': instance.set_index
                        }
                    )

                # Add Properties
                add_properties(
                    project = instance.project,
                    data = data,
                    uri = f'{BASE_URI}{quantity["Properties"]["uri"]}',
                    set_prefix = instance.set_index
                )

                # Add References
                add_references(
                    project = instance.project,
                    data = data,
                    uri = f'{BASE_URI}{quantity["Reference"]["uri"]}',
                    set_prefix = instance.set_index
                )

                # Add defining Formula(s)
                for idx, formula in enumerate(data.formulas):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{quantity["Formula"]["uri"]}',
                        info = {
                            'text': formula, 
                            'collection_index': idx, 
                            'set_index': 0, 
                            'set_prefix': f"{instance.set_index}|0"
                        }
                    )

                # Add Symbol(s)
                for idx, symbol in enumerate(data.symbols):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{quantity["Element Symbol"]["uri"]}',
                        info = {
                            'text': symbol,
                            'set_index': idx, 
                            'set_prefix': f"{instance.set_index}|0|0"
                        }
                    )

                # Add Quantities
                for idx, encoded_quantity in enumerate(data.contains_quantity):
                    source, _ = encoded_quantity.id.split(':')
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{quantity["Element Quantity"]["uri"]}',
                        info = {
                            'text': f"{encoded_quantity.label} ({encoded_quantity.description}) [{source}]",
                            'external_id': encoded_quantity.id,
                            'set_index': idx,
                            'set_prefix': f"{instance.set_index}|0|0"
                        }
                    )

                # Add Quantity [Kind] Relations (flexible)
                for prop in props['Quantity']:
                    for value in getattr(data, prop):
                        qclass_pair = (data.qclass, value.qclass)
                        value_editor(
                            project=instance.project,
                            uri=f"{BASE_URI}{quantity[relation_uris[qclass_pair]]['uri']}",
                            info = {
                                'option': Option.objects.get(uri=mathmoddb[prop]),
                                'set_index': index_counters[qclass_pair],
                                'set_prefix': f"{instance.set_index}"
                            }
                        )
                        value_editor(
                            project=instance.project,
                            uri=f"{BASE_URI}{quantity[relatant_uris[qclass_pair]]['uri']}",
                            info = {
                                'text': f"{value.label} ({value.description}) [{source}]",
                                'external_id': value.id,
                                'set_index': index_counters[qclass_pair],
                                'set_prefix': f"{instance.set_index}"
                            }
                        )
                        index_counters[qclass_pair] += 1

                # Add Publications
                add_entities(
                    project = instance.project,
                    question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                    datas = data.publications,
                    source = source,
                    prefix = 'P'
                )

@receiver(post_save, sender=Value)
def formulation_information(sender, **kwargs):
    '''Mathematical Formulation Handler, checking if an existing Formulation is chosen,
       querying the external Source, and integrating the related Meta-
       data into the Questionnaire.'''
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-model-catalog'):
        # Get Questions of Model Catalog...
        questions = get_questions('model') | get_questions('publication')
        # ... and Formulation specific Questions.
        formulation = questions["Mathematical Formulation"]
        if instance.attribute.uri == f'{BASE_URI}{formulation["ID"]["uri"]}':
            if instance.text and instance.text != 'not found':

                # Add basic Information
                add_basics(
                    project = instance.project,
                    text = instance.text,
                    questions = questions,
                    item_type = 'Mathematical Formulation',
                    index = (0, instance.set_index)
                )

                # Get source and ID of Item
                source, identifier = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return

                # If Item from MathModDB, set up Query...
                query = get_sparql_query('model/queries/formulation.sparql').format(
                    identifier,
                    **get_items(),
                    **get_properties()
                )

                # ...get Results...
                results = query_sparql(query, endpoint[source]['sparql'])

                # ...and load MaRDMO Vocabulary.
                mathmoddb = get_mathmoddb()

                if not results:
                    return

                # Structure Results
                data = models.MathematicalFormulation.from_query(results)

                # Add long Description (optional)
                for idx, description_long in enumerate(data.description_long):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{formulation["Long Description"]["uri"]}',
                        info = {
                            'text': description_long,
                            'collection_index': idx,
                            'set_index': 0,
                            'set_prefix': instance.set_index
                        }
                    )

                # Add Properties
                add_properties(
                    project = instance.project,
                    data = data,
                    uri = f'{BASE_URI}{formulation["Properties"]["uri"]}',
                    set_prefix = instance.set_index
                )

                # Add Formula(s)
                for idx, formula in enumerate(data.formulas):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{formulation["Formula"]["uri"]}',
                        info = {
                            'text': formula, 
                            'collection_index': idx, 
                            'set_index': 0, 
                            'set_prefix': f"{instance.set_index}|0"
                        }
                    )

                # Add Symbol(s)
                for idx, symbol in enumerate(data.symbols):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{formulation["Element Symbol"]["uri"]}',
                        info = {
                            'text': symbol, 
                            'set_index': idx, 
                            'set_prefix': f"{instance.set_index}|0|0"
                        }
                    )

                # Add Quantities
                for idx, quantity in enumerate(data.contains_quantity):
                    source, _ = quantity.id.split(':')
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{formulation["Element Quantity"]["uri"]}',
                        info = {
                            'text': f"{quantity.label} ({quantity.description}) [{source}]", 
                            'external_id': quantity.id, 
                            'set_index': idx, 
                            'set_prefix': f"{instance.set_index}|0|0"
                        }
                    )

                # Add Formulation Relations I (flexible)
                add_relations_flexible(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['MF2MF'],
                        'mapping': mathmoddb,
                    },
                    index = {
                        'set_prefix': f"{instance.set_index}|0"
                    },
                    statement = {
                        'relation': f'{BASE_URI}{formulation["MF2MF"]["uri"]}',
                        'relatant': f'{BASE_URI}{formulation["MFRelatant"]["uri"]}',
                    },
                )

                # Add Formulation Relations II (flexible)
                add_relations_flexible(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['Formulation'],
                        'mapping': mathmoddb,
                    },
                    index = {
                        'set_prefix': instance.set_index
                    },
                    statement = {
                        'relation': f'{BASE_URI}{formulation["IntraClassRelation"]["uri"]}',
                        'relatant': f'{BASE_URI}{formulation["IntraClassElement"]["uri"]}',
                        'assumption': f'{BASE_URI}{formulation["Assumption"]["uri"]}',
                    },
                )

                # Add Publications
                add_entities(
                    project = instance.project,
                    question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                    datas = data.publications,
                    source = source,
                    prefix = 'P'
                )

@receiver(post_save, sender=Value)
def task_information(sender, **kwargs):
    '''Task Handler, checking if an existing Task is chosen,
       querying the external Source, and integrating the related Meta-
       data into the Questionnaire.'''
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-model-catalog'):
        # Get Questions of Model Catalog...
        questions = get_questions('model') | get_questions('publication')
        # ... and Task specific Questions.
        task = questions["Task"]
        if instance.attribute.uri == f'{BASE_URI}{task["ID"]["uri"]}':
            if instance.text and instance.text != 'not found':

                # Add basic Information
                add_basics(
                    project = instance.project,
                    text = instance.text,
                    questions = questions,
                    item_type = 'Task',
                    index = (0, instance.set_index)
                )

                # Get source and ID of Item
                source, identifier = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return

                # If Item from MathModDB, set up Query...
                query = get_sparql_query('model/queries/task.sparql').format(
                    identifier,
                    **get_items(),
                    **get_properties()
                )

                # ...get Results...
                results = query_sparql(query, endpoint[source]['sparql'])

                # ...and load MazjModDB Vocabulary.
                mathmoddb = get_mathmoddb()

                if not results:
                    return

                #Structure Results
                data = models.Task.from_query(results)

                # Add long Description (optional)
                for idx, description_long in enumerate(data.description_long):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{task["Long Description"]["uri"]}',
                        info = {
                            'text': description_long,
                            'collection_index': idx,
                            'set_index': 0,
                            'set_prefix': instance.set_index
                        }
                    )

                # Add Properties
                add_properties(
                    project = instance.project,
                    data = data,
                    uri = f'{BASE_URI}{task["Properties"]["uri"]}',
                    set_prefix = instance.set_index
                )

                # Add Formulations Relations (flexible)
                add_relations_flexible(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['T2MF'],
                        'mapping': mathmoddb,
                    },
                    index = {
                        'set_prefix': f"{instance.set_index}|0"
                    },
                    statement = {
                        'relation': f'{BASE_URI}{task["T2MF"]["uri"]}',
                        'relatant': f'{BASE_URI}{task["MFRelatant"]["uri"]}',
                    },
                )

                # Add Quantity Relations (flexible)
                add_relations_flexible(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['T2Q'],
                        'mapping': mathmoddb,
                    },
                    index = {
                        'set_prefix': f"{instance.set_index}|0"
                    },
                    statement = {
                        'relation': f'{BASE_URI}{task["T2Q"]["uri"]}',
                        'relatant': f'{BASE_URI}{task["QRelatant"]["uri"]}',
                    },
                )

                # Add Task Relations (flexible)
                add_relations_flexible(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['Task'],
                        'mapping': mathmoddb,
                    },
                    index = {
                        'set_prefix': instance.set_index
                    },
                    statement = {
                        'relation': f'{BASE_URI}{task["IntraClassRelation"]["uri"]}',
                        'relatant': f'{BASE_URI}{task["IntraClassElement"]["uri"]}',
                        'assumption': f'{BASE_URI}{task["Assumption"]["uri"]}',
                        'order': f'{BASE_URI}{task["Order Number"]["uri"]}',
                    },
                )

                # Add Publications
                add_entities(
                    project = instance.project,
                    question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                    datas = data.publications,
                    source = source,
                    prefix = 'P'
                )

@receiver(post_save, sender=Value)
def model_information(sender, **kwargs):
    '''Mathematical Model Handler, checking if an existing Model is chosen,
       querying the external Source, and integrating the related Meta-
       data into the Questionnaire.'''
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-model-catalog'):
        # Get Questions of Model Catalog...
        questions = get_questions('model') | get_questions('publication')
        # ... and Model specific Questions.
        model = questions["Mathematical Model"]
        if instance.attribute.uri == f'{BASE_URI}{model["ID"]["uri"]}':
            if instance.text and instance.text != 'not found':

                # Add basic Information
                add_basics(
                    project = instance.project,
                    text = instance.text,
                    questions = questions,
                    item_type = 'Mathematical Model',
                    index = (0, instance.set_index)
                )

                # Get source and ID of Item
                source, identifier = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return

                # If Item from MathModDB, set up Query...
                query = get_sparql_query('model/queries/model.sparql').format(
                    identifier,
                    **get_items(),
                    **get_properties()
                )

                # ...get Results...
                results = query_sparql(query, endpoint[source]['sparql'])

                # ...and load MathModDB Vocabulary.
                mathmoddb = get_mathmoddb()

                if not results:
                    return

                # Structure Results
                data = models.MathematicalModel.from_query(results)

                # Add long Description (optional)
                for idx, description_long in enumerate(data.description_long):
                    value_editor(
                        project = instance.project,
                        uri = f'{BASE_URI}{model["Long Description"]["uri"]}',
                        info = {
                            'text': description_long,
                            'collection_index': idx, 
                            'set_index': 0,
                            'set_prefix': instance.set_index
                        }
                    )

                # Add Properties
                add_properties(
                    project = instance.project,
                    data = data,
                    uri = f'{BASE_URI}{model["Properties"]["uri"]}',
                    set_prefix = instance.set_index
                )

                # Add Research Problems Relations (static)
                add_relations_static(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['MM2RP']
                    },
                    index = {
                        'set_prefix': instance.set_index
                    },
                    statement = {
                        'relatant': f'{BASE_URI}{model["RPRelatant"]["uri"]}'
                    }
                )

                # Add Formulations contained in Mathematical Model
                add_relations_flexible(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['MM2MF'],
                        'mapping': mathmoddb,
                    },
                    index = {
                        'set_prefix': f"{instance.set_index}|0"
                    },
                    statement = {
                        'relation': f'{BASE_URI}{model["MM2MF"]["uri"]}',
                        'relatant': f'{BASE_URI}{model["MFRelatant"]["uri"]}',
                        'order': f'{BASE_URI}{model["Order Number"]["uri"]}',
                    },
                )

                # Add Relations between Mathematical Models and Tasks to Questionnaire
                add_relations_static(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['MM2T']
                    },
                    index = {
                        'set_prefix': instance.set_index
                    },
                    statement = {
                        'relatant': f'{BASE_URI}{model["TRelatant"]["uri"]}'
                    }
                )

                # Add related Models to questionnaire
                add_relations_flexible(
                    project = instance.project,
                    data = data,
                    props = {
                        'keys': props['Model'],
                        'mapping': mathmoddb,
                    },
                    index = {
                        'set_prefix': instance.set_index
                    },
                    statement = {
                        'relation': f'{BASE_URI}{model["IntraClassRelation"]["uri"]}',
                        'relatant': f'{BASE_URI}{model["IntraClassElement"]["uri"]}',
                        'assumption': f'{BASE_URI}{model["Assumption"]["uri"]}',
                    },
                )

                # Add Publications to Questionnaire
                add_entities(
                    project = instance.project,
                    question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                    datas = data.publications,
                    source = source,
                    prefix = 'P'
                )

@receiver(post_save, sender=Value)
def relation_handler(sender, **kwargs):
    '''Handler integrating related Entities into the Questionnaire.'''
    #Get Instance
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).endswith('mardmo-model-catalog'):
        # Get config map
        config_map = get_uri_prefix_map()
        if instance.attribute.uri in config_map and instance.text:
            # Get item, config and data information
            label, description, source = extract_parts(instance.text)
            config = config_map[instance.attribute.uri]
            datas = [models.Relatant.from_relation(instance.external_id, label, description)]
            # Add items from specific source
            if source in ('mardi', 'wikidata'):
                add_entities(
                    project=instance.project,
                    question_set=config["question_set"],
                    datas=datas,
                    source=source,
                    prefix=config["prefix"]
                )
            # Add items from user
            elif source == 'user':
                add_new_entities(
                    project=instance.project,
                    question_set=config["question_set"],
                    datas=datas,
                    prefix=config["prefix"]
                )
