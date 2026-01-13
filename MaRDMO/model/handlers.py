'''Module containing Handlers for the Model Documentation'''

from rdmo.options.models import Option

from . import models

from .constants import props, relatant_uris, relation_uris, index_counters

from ..constants import BASE_URI
from ..getters import (
    get_items,
    get_mathmoddb,
    get_properties,
    get_questions,
    get_sparql_query,
    get_url
)
from ..helpers import value_editor
from ..queries import query_sparql
from ..adders import (
    add_basics,
    add_entities,
    add_properties,
    add_relations_static,
    add_relations_flexible,
    add_references
)

class Information:
    '''Class containing functions, querying external sources for specific
       entities and integrating the related metadata into the questionnaire.'''

    def __init__(self):
        # Load shared data once
        self.questions = get_questions("model") | get_questions('publication')
        self.mathmoddb = get_mathmoddb()
        self.base = BASE_URI

    def field(self, instance):
        '''Research Field Information'''

        # Research Field specific Questions.
        field = self.questions["Research Field"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Informatiom
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Research Field',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # Only consider MaRDI (so far)
        if source != 'mardi':
            return

        # If Item from MathModDB, set up Query and...
        query = get_sparql_query('model/queries/field.sparql').format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...get Results.
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        # Structure Results
        data = models.ResearchField.from_query(results)

        # Add Aliases (optional)
        for idx, alias in enumerate(data.aliases):
            value_editor(
                project = instance.project,
                uri = f'{BASE_URI}{field["Alias"]["uri"]}',
                info = {
                    'text': alias,
                    'collection_index': idx,
                    'set_index': 0,
                    'set_prefix': instance.set_index
                }
            )

        # Add long Descriptions (optional)
        for idx, description_long in enumerate(data.description_long):
            value_editor(
                project = instance.project,
                uri = f'{self.base}{field["Long Description"]["uri"]}',
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
                'mapping': self.mathmoddb,
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relation': f'{self.base}{field["IntraClassRelation"]["uri"]}',
                'relatant': f'{self.base}{field["IntraClassElement"]["uri"]}',
            },
        )

        # Add Publications
        add_entities(
            project = instance.project,
            question_set = f'{self.base}{self.questions["Publication"]["uri"]}',
            datas = data.publications,
            source = source,
            prefix = 'P'
        )

    def problem(self, instance):
        '''Research Problem Information'''

        # Research Problem specific Questions.
        problem = self.questions["Research Problem"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Research Problem',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # Only consider MaRDI (so far)
        if source != 'mardi':
            return

        # If Item from MathModDB, set up Query and...
        catalog = getattr(instance.project, "catalog", None)
        if 'basics' in str(catalog):
            sparql_file = 'model/queries/problem-basics.sparql'
        else:
            sparql_file = 'model/queries/problem.sparql'

        query = get_sparql_query(sparql_file).format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...get Results.
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        # Structure Results
        data = models.ResearchProblem.from_query(results)

        # Add Aliases (optional)
        for idx, alias in enumerate(data.aliases):
            value_editor(
                project = instance.project,
                uri = f'{BASE_URI}{problem["Alias"]["uri"]}',
                info = {
                    'text': alias,
                    'collection_index': idx,
                    'set_index': 0,
                    'set_prefix': instance.set_index
                }
            )

        # Add long Description (optional)
        for idx, description_long in enumerate(data.description_long):
            value_editor(
                project = instance.project,
                uri = f'{self.base}{problem["Long Description"]["uri"]}',
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
                'relatant': f'{self.base}{problem["RFRelatant"]["uri"]}'
            }
        )

        # Add Research Problem Relations (flexible)
        add_relations_flexible(
            project = instance.project,
            data = data,
            props = {
                'keys': props['Problem'],
                'mapping': self.mathmoddb,
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relation': f'{self.base}{problem["IntraClassRelation"]["uri"]}',
                'relatant': f'{self.base}{problem["IntraClassElement"]["uri"]}',
            },
        )

        # Add Publications
        add_entities(
            project = instance.project,
            question_set = f'{self.base}{self.questions["Publication"]["uri"]}',
            datas = data.publications,
            source = source,
            prefix = 'P'
        )

    def quantity(self, instance):
        '''Quantity [Kind] Information'''

        # Quantity specific Questions.
        quantity = self.questions["Quantity"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Quantity',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # Only consider MaRDI (so far)
        if source != 'mardi':
            return

        # If Item from MathModDB, set up Query and...
        query = get_sparql_query('model/queries/quantity.sparql').format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...get Results.
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        # Structure Results
        data = models.QuantityOrQuantityKind.from_query(results)

        # Add Aliases (optional)
        for idx, alias in enumerate(data.aliases):
            value_editor(
                project = instance.project,
                uri = f'{BASE_URI}{quantity["Alias"]["uri"]}',
                info = {
                    'text': alias,
                    'collection_index': idx,
                    'set_index': 0,
                    'set_prefix': instance.set_index
                }
            )

        # Add long Description (optional)
        for idx, description_long in enumerate(data.description_long):
            value_editor(
                project = instance.project,
                uri = f'{self.base}{quantity["Long Description"]["uri"]}',
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
                uri = f'{self.base}{quantity["QorQK"]["uri"]}',
                info = {
                    'option': Option.objects.get(
                        uri = self.mathmoddb[results[0]['class']['value']]
                    ),
                    'set_index': instance.set_index
                }
            )

        # Add Properties
        add_properties(
            project = instance.project,
            data = data,
            uri = f'{self.base}{quantity["Properties"]["uri"]}',
            set_prefix = instance.set_index
        )

        # Add References
        add_references(
            project = instance.project,
            data = data,
            uri = f'{self.base}{quantity["Reference"]["uri"]}',
            set_prefix = instance.set_index
        )

        # Add defining Formula(s)
        for idx, formula in enumerate(data.formulas):
            value_editor(
                project = instance.project,
                uri = f'{self.base}{quantity["Formula"]["uri"]}',
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
                uri = f'{self.base}{quantity["Element Symbol"]["uri"]}',
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
                uri = f'{self.base}{quantity["Element Quantity"]["uri"]}',
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
                qclass_pair = (data.qclass, value.item_class)
                value_editor(
                    project=instance.project,
                    uri=f"{self.base}{quantity[relation_uris[qclass_pair]]['uri']}",
                    info = {
                        'option': Option.objects.get(uri = self.mathmoddb[prop]),
                        'set_index': index_counters[qclass_pair],
                        'set_prefix': f"{instance.set_index}"
                    }
                )
                value_editor(
                    project=instance.project,
                    uri=f"{self.base}{quantity[relatant_uris[qclass_pair]]['uri']}",
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
            question_set = f'{self.base}{self.questions["Publication"]["uri"]}',
            datas = data.publications,
            source = source,
            prefix = 'P'
        )

    def formulation(self, instance):
        '''Mathematical Formulation Information'''

        # Formulation specific Questions.
        formulation = self.questions["Mathematical Formulation"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Mathematical Formulation',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # Only consider MaRDI (so far)
        if source != 'mardi':
            return

        # If Item from MathModDB, set up Query and...
        catalog = getattr(instance.project, "catalog", None)
        if 'basics' in str(catalog):
            sparql_file = 'model/queries/formulation-basics.sparql'
        else:
            sparql_file = 'model/queries/formulation.sparql'

        # If Item from MathModDB, set up Query and...
        query = get_sparql_query(sparql_file).format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...get Results.
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        # Structure Results
        data = models.MathematicalFormulation.from_query(results)

        # Add Aliases (optional)
        for idx, alias in enumerate(data.aliases):
            value_editor(
                project = instance.project,
                uri = f'{BASE_URI}{formulation["Alias"]["uri"]}',
                info = {
                    'text': alias,
                    'collection_index': idx,
                    'set_index': 0,
                    'set_prefix': instance.set_index
                }
            )

        # Add long Description (optional)
        for idx, description_long in enumerate(data.description_long):
            value_editor(
                project = instance.project,
                uri = f'{self.base}{formulation["Long Description"]["uri"]}',
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
            uri = f'{self.base}{formulation["Properties"]["uri"]}',
            set_prefix = instance.set_index
        )

        # Add Formula(s)
        for idx, formula in enumerate(data.formulas):
            value_editor(
                project = instance.project,
                uri = f'{self.base}{formulation["Formula"]["uri"]}',
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
                uri = f'{self.base}{formulation["Element Symbol"]["uri"]}',
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
                uri = f'{self.base}{formulation["Element Quantity"]["uri"]}',
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
                'mapping': self.mathmoddb,
            },
            index = {
                'set_prefix': f"{instance.set_index}|0"
            },
            statement = {
                'relation': f'{self.base}{formulation["MF2MF"]["uri"]}',
                'relatant': f'{self.base}{formulation["MFRelatant"]["uri"]}',
            },
        )

        # Add Formulation Relations II (flexible)
        add_relations_flexible(
            project = instance.project,
            data = data,
            props = {
                'keys': props['Formulation'],
                'mapping': self.mathmoddb,
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relation': f'{self.base}{formulation["IntraClassRelation"]["uri"]}',
                'relatant': f'{self.base}{formulation["IntraClassElement"]["uri"]}',
                'assumption': f'{self.base}{formulation["Assumption"]["uri"]}',
            },
        )

        # Add Publications
        add_entities(
            project = instance.project,
            question_set = f'{self.base}{self.questions["Publication"]["uri"]}',
            datas = data.publications,
            source = source,
            prefix = 'P'
        )

    def task(self, instance):
        '''Task Information'''

        # Task specific Questions.
        task = self.questions["Task"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Task',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # Only consider MaRDI (so far)
        if source != 'mardi':
            return

        # If Item from MathModDB, set up Query and...
        catalog = getattr(instance.project, "catalog", None)
        if 'basics' in str(catalog):
            sparql_file = 'model/queries/task-basics.sparql'
        else:
            sparql_file = 'model/queries/task.sparql'

        query = get_sparql_query(sparql_file).format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...get Results.
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        #Structure Results
        data = models.Task.from_query(results)

        # Add Aliases (optional)
        for idx, alias in enumerate(data.aliases):
            value_editor(
                project = instance.project,
                uri = f'{BASE_URI}{task["Alias"]["uri"]}',
                info = {
                    'text': alias,
                    'collection_index': idx,
                    'set_index': 0,
                    'set_prefix': instance.set_index
                }
            )

        # Add long Description (optional)
        for idx, description_long in enumerate(data.description_long):
            value_editor(
                project = instance.project,
                uri = f'{self.base}{task["Long Description"]["uri"]}',
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
            uri = f'{self.base}{task["Properties"]["uri"]}',
            set_prefix = instance.set_index
        )

        # Add Formulations Relations (flexible)
        add_relations_flexible(
            project = instance.project,
            data = data,
            props = {
                'keys': props['T2MF'],
                'mapping': self.mathmoddb,
            },
            index = {
                'set_prefix': f"{instance.set_index}|0"
            },
            statement = {
                'relation': f'{self.base}{task["T2MF"]["uri"]}',
                'relatant': f'{self.base}{task["MFRelatant"]["uri"]}',
            },
        )

        # Add Quantity Relations (flexible)
        add_relations_flexible(
            project = instance.project,
            data = data,
            props = {
                'keys': props['T2Q'],
                'mapping': self.mathmoddb,
            },
            index = {
                'set_prefix': f"{instance.set_index}|0"
            },
            statement = {
                'relation': f'{self.base}{task["T2Q"]["uri"]}',
                'relatant': f'{self.base}{task["QRelatant"]["uri"]}',
            },
        )

        # Add Task Relations (flexible)
        add_relations_flexible(
            project = instance.project,
            data = data,
            props = {
                'keys': props['Task'],
                'mapping': self.mathmoddb,
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relation': f'{self.base}{task["IntraClassRelation"]["uri"]}',
                'relatant': f'{self.base}{task["IntraClassElement"]["uri"]}',
                'assumption': f'{self.base}{task["Assumption"]["uri"]}',
                'order': f'{self.base}{task["Order Number"]["uri"]}',
            },
        )

        # Add Publications
        add_entities(
            project = instance.project,
            question_set = f'{self.base}{self.questions["Publication"]["uri"]}',
            datas = data.publications,
            source = source,
            prefix = 'P'
        )

    def model(self, instance):
        '''Mathematical Model Information'''

        # Model specific Questions.
        model = self.questions["Mathematical Model"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Mathematical Model',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # Only consider MaRDI (so far)
        if source != 'mardi':
            return

        # If Item from MathModDB, set up Query and...
        catalog = getattr(instance.project, "catalog", None)
        if 'basics' in str(catalog):
            sparql_file = 'model/queries/model-basics.sparql'
        else:
            sparql_file = 'model/queries/model.sparql'

        query = get_sparql_query(sparql_file).format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...get Results.
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        # Stop if no Results retrieved from external source
        if not results:
            return

        # Structure Results
        data = models.MathematicalModel.from_query(results)

        # Add Aliases (optional)
        for idx, alias in enumerate(data.aliases):
            value_editor(
                project = instance.project,
                uri = f'{BASE_URI}{model["Alias"]["uri"]}',
                info = {
                    'text': alias,
                    'collection_index': idx,
                    'set_index': 0,
                    'set_prefix': instance.set_index
                }
            )

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
                'mapping': self.mathmoddb,
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
                'mapping': self.mathmoddb,
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
            question_set = f'{BASE_URI}{self.questions["Publication"]["uri"]}',
            datas = data.publications,
            source = source,
            prefix = 'P'
        )
