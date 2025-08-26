from django.dispatch import receiver
from django.db.models.signals import post_save
from rdmo.projects.models import Value
from rdmo.options.models import Option

from .constants import PROPS, RELATANT_URIS, RELATION_URIS, INDEX_COUNTERS, get_URI_PREFIX_MAP
from .sparql import queryHandler
from .models import ResearchField, ResearchProblem, MathematicalModel, QuantityOrQuantityKind, MathematicalFormulation, Task, Relatant

from ..config import BASE_URI, endpoint
from ..getters import get_items, get_mathmoddb, get_properties, get_questions
from ..helpers import extract_parts, value_editor
from ..queries import query_sparql
from ..adders import add_basics, add_entities, add_new_entities, add_properties, add_relations_static, add_relations_flexible, add_references

@receiver(post_save, sender=Value)
def RFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questions('model') | get_questions('publication')
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Research Field"]["ID"]["uri"]}':
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
                source, Id = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return
                
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['researchFieldInformation'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                
                if results:
                    
                    # Structure Results
                    data = ResearchField.from_query(results)

                    # Add long Descriptions (optional)
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Research Field"]["Long Description"]["uri"]}',
                            info = { 
                                'text': descriptionLong, 
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
                            'keys': PROPS['Field'],
                            'mapping': mathmoddb,
                        },
                        index = {
                            'set_prefix': instance.set_index
                        },
                        statement = {
                            'relation': f'{BASE_URI}{questions["Research Field"]["IntraClassRelation"]["uri"]}',
                            'relatant': f'{BASE_URI}{questions["Research Field"]["IntraClassElement"]["uri"]}',
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
    return

@receiver(post_save, sender=Value)
def RPInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questions('model') | get_questions('publication')
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Research Problem"]["ID"]["uri"]}':
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
                source, Id = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return

                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['researchProblemInformation'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                
                if results:
                    
                    # Structure Results
                    data = ResearchProblem.from_query(results)
                    
                    # Add long Description (optional)
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Research Problem"]["Long Description"]["uri"]}', 
                            info = {
                                'text': descriptionLong,
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
                            'keys': PROPS['RP2RF']
                        }, 
                        index = {
                            'set_prefix': instance.set_index
                        }, 
                        statement = {
                            'relatant': f'{BASE_URI}{questions["Research Problem"]["RFRelatant"]["uri"]}'
                        }
                    )
                    
                    # Add Research Problem Relations (flexible)
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['Problem'],
                            'mapping': mathmoddb,
                        },
                        index = {
                            'set_prefix': instance.set_index
                        },
                        statement = {
                            'relation': f'{BASE_URI}{questions["Research Problem"]["IntraClassRelation"]["uri"]}',
                            'relatant': f'{BASE_URI}{questions["Research Problem"]["IntraClassElement"]["uri"]}',
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
    return

@receiver(post_save, sender=Value)
def QQKInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questions('model') | get_questions('publication')
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Quantity"]["ID"]["uri"]}':
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
                source, Id = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return
                
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['quantityOrQuantityKindInformation'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                
                if results:
                
                    # Structure Results
                    data = QuantityOrQuantityKind.from_query(results)
                    
                    # Add long Description (optional)
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Quantity"]["Long Description"]["uri"]}', 
                            info = {
                                'text': descriptionLong,
                                'collection_index': idx, 
                                'set_index': 0, 
                                'set_prefix': instance.set_index
                            }
                        )
                    
                    # Add Type
                    if data.qclass:
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Quantity"]["QorQK"]["uri"]}', 
                            info = {
                                'option': Option.objects.get(uri=mathmoddb[results[0]['class']['value']]),
                                'set_index': 0, 
                                'set_prefix': instance.set_index
                            }
                        )

                    # Add Properties
                    add_properties(
                        project = instance.project,
                        data = data,
                        uri = f'{BASE_URI}{questions["Quantity"]["Properties"]["uri"]}',
                        set_prefix = instance.set_index
                    )
                    
                    # Add References
                    add_references(
                        project = instance.project,
                        data = data,
                        uri = f'{BASE_URI}{questions["Quantity"]["Reference"]["uri"]}',
                        set_prefix = instance.set_index
                    )

                    # Add defining Formula(s)
                    for idx, formula in enumerate(data.formulas):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Quantity"]["Formula"]["uri"]}', 
                            info = {
                                'text': formula, 
                                'collection_index': idx, 
                                'set_index': 0, 
                                'set_prefix': instance.set_index
                            }
                        )

                    # Add Symbol(s)
                    for idx, symbol in enumerate(data.symbols):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Quantity"]["Element Symbol"]["uri"]}', 
                            text = symbol, 
                            set_index = idx, 
                            set_prefix = f"{instance.set_index}|0"
                        )

                    # Add Quantities
                    for idx, quantity in enumerate(data.containsQuantity):
                        source, _ = quantity.id.split(':')
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Quantity"]["Element Quantity"]["uri"]}', 
                            info = {
                                'text': f"{quantity.label} ({quantity.description}) [{source}]", 
                                'external_id': quantity.id, 
                                'set_index': idx, 
                                'set_prefix': f"{instance.set_index}|0"
                            }
                        )

                    # Add Quantity [Kind] Relations (flexible)
                    for prop in PROPS['Quantity']:
                        for value in getattr(data, prop):
                            qclass_pair = (data.qclass, value.qclass)
                            value_editor(
                                project=instance.project,
                                uri=f"{BASE_URI}{questions['Quantity'][RELATION_URIS[qclass_pair]]['uri']}",
                                info = {
                                    'option': Option.objects.get(uri=mathmoddb[prop]),
                                    'set_index': INDEX_COUNTERS[qclass_pair],
                                    'set_prefix': f"{instance.set_index}"
                                }
                            )
                            value_editor(
                                project=instance.project,
                                uri=f"{BASE_URI}{questions['Quantity'][RELATANT_URIS[qclass_pair]]['uri']}",
                                info = {
                                    'text': f"{value.label} ({value.description}) [{source}]",
                                    'external_id': value.id,
                                    'set_index': INDEX_COUNTERS[qclass_pair],
                                    'set_prefix': f"{instance.set_index}"
                                }
                            )
                            INDEX_COUNTERS[qclass_pair] += 1
                    
                    # Add Publications
                    add_entities(
                        project = instance.project, 
                        question_set = f'{BASE_URI}{questions["Publication"]["uri"]}',
                        datas = data.publications, 
                        source = source,
                        prefix = 'P'
                    )   
    return

@receiver(post_save, sender=Value)
def MFInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questions('model') | get_questions('publication')
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Formulation"]["ID"]["uri"]}':
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
                source, Id = instance.external_id.split(':')
                
                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return
                
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['mathematicalFormulationInformation'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                
                if results:
                    
                    # Structure Results
                    data = MathematicalFormulation.from_query(results)

                    # Add long Description (optional)
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Mathematical Formulation"]["Long Description"]["uri"]}', 
                            info = {
                                'text': descriptionLong,
                                'collection_index': idx, 
                                'set_index': 0, 
                                'set_prefix': instance.set_index
                            }
                        )

                    # Add Properties
                    add_properties(
                        project = instance.project,
                        data = data,
                        uri = f'{BASE_URI}{questions["Mathematical Formulation"]["Properties"]["uri"]}',
                        set_prefix = instance.set_index
                    )

                    # Add Formula(s)
                    for idx, formula in enumerate(data.formulas):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Mathematical Formulation"]["Formula"]["uri"]}', 
                            info = {
                                'text': formula, 
                                'collection_index': idx, 
                                'set_index': 0, 
                                'set_prefix': instance.set_index
                            }
                        )

                    # Add Symbol(s)
                    for idx, symbol in enumerate(data.symbols):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Mathematical Formulation"]["Element Symbol"]["uri"]}', 
                            info = {
                                'text': symbol, 
                                'set_index': idx, 
                                'set_prefix': f"{instance.set_index}|0"
                            }
                        )

                    # Add Quantities
                    for idx, quantity in enumerate(data.containsQuantity):
                        source, _ = quantity.id.split(':')
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Mathematical Formulation"]["Element Quantity"]["uri"]}', 
                            info = {
                                'text': f"{quantity.label} ({quantity.description}) [{source}]", 
                                'external_id': quantity.id, 
                                'set_index': idx, 
                                'set_prefix': f"{instance.set_index}|0"
                            }
                        )

                    # Add Formulation Relations I (flexible)
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['MF2MF'],
                            'mapping': mathmoddb,
                        },
                        index = {
                            'set_prefix': f"{instance.set_index}|0"
                        },
                        statement = {
                            'relation': f'{BASE_URI}{questions["Mathematical Formulation"]["MF2MF"]["uri"]}',
                            'relatant': f'{BASE_URI}{questions["Mathematical Formulation"]["MFRelatant"]["uri"]}',
                        },
                    )

                    # Add Formulation Relations II (flexible)
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['Formulation'],
                            'mapping': mathmoddb,
                        },
                        index = {
                            'set_prefix': instance.set_index
                        },
                        statement = {
                            'relation': f'{BASE_URI}{questions["Mathematical Formulation"]["IntraClassRelation"]["uri"]}',
                            'relatant': f'{BASE_URI}{questions["Mathematical Formulation"]["IntraClassElement"]["uri"]}',
                            'assumption': f'{BASE_URI}{questions["Mathematical Formulation"]["Assumption"]["uri"]}',
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
    return

@receiver(post_save, sender=Value)
def TInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questions('model') | get_questions('publication')
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Task"]["ID"]["uri"]}':
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
                source, Id = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return
                
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['taskInformation'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()
                
                if results:
                    
                    #Structure Results
                    data = Task.from_query(results)
                    
                    # Add long Description (optional)
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Task"]["Long Description"]["uri"]}', 
                            info = {
                                'text': descriptionLong, 
                                'collection_index': idx,
                                'set_index': 0, 
                                'set_prefix': instance.set_index
                            }
                        )
                        
                    # Add Properties
                    add_properties(
                        project = instance.project,
                        data = data,
                        uri = f'{BASE_URI}{questions["Task"]["Properties"]["uri"]}',
                        set_prefix = instance.set_index
                    )

                    # Add Formulations Relations (flexible)
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['T2MF'],
                            'mapping': mathmoddb,
                        },
                        index = {
                            'set_prefix': f"{instance.set_index}|0"
                        },
                        statement = {
                            'relation': f'{BASE_URI}{questions["Task"]["T2MF"]["uri"]}',
                            'relatant': f'{BASE_URI}{questions["Task"]["MFRelatant"]["uri"]}',
                        },
                    )
                    
                    # Add Quantity Relations (flexible)
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['T2Q'],
                            'mapping': mathmoddb,
                        },
                        index = {
                            'set_prefix': f"{instance.set_index}|0"
                        },
                        statement = {
                            'relation': f'{BASE_URI}{questions["Task"]["T2Q"]["uri"]}',
                            'relatant': f'{BASE_URI}{questions["Task"]["QRelatant"]["uri"]}',
                        },
                    )
                    
                    # Add Task Relations (flexible)
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['Task'],
                            'mapping': mathmoddb,
                        },
                        index = {
                            'set_prefix': instance.set_index
                        },
                        statement = {
                            'relation': f'{BASE_URI}{questions["Task"]["IntraClassRelation"]["uri"]}',
                            'relatant': f'{BASE_URI}{questions["Task"]["IntraClassElement"]["uri"]}',
                            'assumption': f'{BASE_URI}{questions["Task"]["Assumption"]["uri"]}',
                            'order': f'{BASE_URI}{questions["Task"]["Order Number"]["uri"]}',
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
    return                    

@receiver(post_save, sender=Value)
def MMInformation(sender, **kwargs):
    instance = kwargs.get("instance", None)
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
        # Get Questions of Model Catalog
        questions = get_questions('model') | get_questions('publication')
        if instance and instance.attribute.uri == f'{BASE_URI}{questions["Mathematical Model"]["ID"]["uri"]}':
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
                source, Id = instance.external_id.split(':')

                # Only consider MaRDI (so far)
                if source != 'mardi':
                    return
                
                # If Item from MathModDB, query relations and load MathModDB Vocabulary
                query = queryHandler['mathematicalModelInformation'].format(Id, **get_items(), **get_properties())
                results = query_sparql(query, endpoint[source]['sparql'])
                mathmoddb = get_mathmoddb()

                if results:
                    
                    # Structure Results
                    data = MathematicalModel.from_query(results)
                    
                    # Add long Description (optional)
                    for idx, descriptionLong in enumerate(data.descriptionLong):
                        value_editor(
                            project = instance.project, 
                            uri = f'{BASE_URI}{questions["Mathematical Model"]["Long Description"]["uri"]}', 
                            info = {
                                'text': descriptionLong,
                                'collection_index': idx, 
                                'set_index': 0, 
                                'set_prefix': instance.set_index
                            }
                        )
                        
                    # Add Properties
                    add_properties(
                        project = instance.project,
                        data = data,
                        uri = f'{BASE_URI}{questions["Mathematical Model"]["Properties"]["uri"]}',
                        set_prefix = instance.set_index
                    )
                    
                    # Add Research Problems Relations (static)
                    add_relations_static(
                        project = instance.project, 
                        data = data, 
                        props = {
                            'keys': PROPS['MM2RP']
                        }, 
                        index = {
                            'set_prefix': instance.set_index
                        }, 
                        statement = {
                            'relatant': f'{BASE_URI}{questions["Mathematical Model"]["RPRelatant"]["uri"]}'
                        }
                    )

                    # Add Formulations contained in Mathematical Model
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['MM2MF'],
                            'mapping': mathmoddb,
                        },
                        index = {
                            'set_prefix': f"{instance.set_index}|0"
                        },
                        statement = {
                            'relation': f'{BASE_URI}{questions["Mathematical Model"]["MM2MF"]["uri"]}',
                            'relatant': f'{BASE_URI}{questions["Mathematical Model"]["MFRelatant"]["uri"]}',
                            'order': f'{BASE_URI}{questions["Mathematical Model"]["Order Number"]["uri"]}',
                        },
                    )

                    # Add Relations between Mathematical Models and Tasks to Questionnaire
                    add_relations_static(
                        project = instance.project, 
                        data = data, 
                        props = {
                            'keys': PROPS['MM2T']
                        }, 
                        index = {
                            'set_prefix': instance.set_index
                        }, 
                        statement = {
                            'relatant': f'{BASE_URI}{questions["Mathematical Model"]["TRelatant"]["uri"]}'
                        }
                    )

                    # Add related Models to questionnaire
                    add_relations_flexible(
                        project = instance.project,
                        data = data,
                        props = {
                            'keys': PROPS['Model'],
                            'mapping': mathmoddb,
                        },
                        index = {
                            'set_prefix': instance.set_index
                        },
                        statement = {
                            'relation': f'{BASE_URI}{questions["Mathematical Model"]["IntraClassRelation"]["uri"]}',
                            'relatant': f'{BASE_URI}{questions["Mathematical Model"]["IntraClassElement"]["uri"]}',
                            'assumption': f'{BASE_URI}{questions["Mathematical Model"]["Assumption"]["uri"]}',
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
    return

@receiver(post_save, sender=Value)
def RelationHandler(sender, **kwargs):
    
    #Get Instance
    instance = kwargs.get("instance", None)
    
    # Check if Model Catalog is used
    if instance and str(instance.project.catalog).split('/')[-1] == 'mardmo-model-catalog':

        # Get config map
        config_map = get_URI_PREFIX_MAP()

        if instance.attribute.uri in config_map and instance.text:

            # Get item, config and data information
            label, description, source = extract_parts(instance.text)
            config = config_map[instance.attribute.uri]
            datas = [Relatant.from_relation(instance.external_id, label, description)]

            # Add items from specific source
            if source != 'user':
                add_entities(
                    project=instance.project,
                    question_set=config["question_set"],
                    datas=datas,
                    source=source,
                    prefix=config["prefix"]
                )
            
            # Add items from user
            elif instance.external_id == 'not found':
                add_new_entities(
                    project=instance.project,
                    question_set=config["question_set"],
                    datas=datas,
                    prefix=config["prefix"]
                )

    return
