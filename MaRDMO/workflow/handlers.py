'''Module containing Handlers for the Workflow Documentation'''

from ..constants import BASE_URI
from ..getters import (
    get_items,
    get_options,
    get_properties,
    get_questions,
    get_sparql_query,
    get_url
)
from ..helpers import value_editor
from ..queries import query_sparql
from ..adders import add_basics, add_references, add_relations_static

from .constants import PROPS
from .models import Method, ProcessStep, Software, Hardware, DataSet

class Information:
    '''Class containing functions, querying external sources for specific
       entities and integrating the related metadata into the questionnaire.'''

    def __init__(self):
        # Load shared data once
        self.questions = get_questions("workflow")
        self.base = BASE_URI
        self.options = get_options()

    def software(self, instance):
        '''Software Information'''

        # Software specific Questions.
        software = self.questions["Software"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add Basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Software',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # If Item from MaRDI Portal, Wikidata, or MathAlgoDB, set up Query and...
        query = get_sparql_query(f'workflow/queries/software_{source}.sparql').format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...Query source for further Information
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        if not results:
            return

        # Structure Results and load options
        data = Software.from_query(results)

        # Add References to Questionnaire
        add_references(
            project = instance.project,
            data = data,
            uri = f'{self.base}{software["Reference"]["uri"]}',
            set_prefix = instance.set_index
        )

        # Add Relations between Programming Language and Method to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['S2PL']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{software["Programming Language"]["uri"]}'
            }
        )

        # Add Relations between Programming Language and Method to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['S2DP']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{software["Dependency"]["uri"]}'
            }
        )

        # Software Source Code Published?
        if data.sourceCodeRepository:
            value_editor(
                project = instance.project,
                uri = f'{self.base}{software["Published"]["uri"]}',
                info = {
                    'text': data.sourceCodeRepository, 
                    'option': self.options['YesText'], 
                    'set_prefix': instance.set_index
                }
            )

        # Software User Manual Documented?
        if data.userManualURL:
            value_editor(
                project = instance.project,
                uri = f'{self.base}{software["Documented"]["uri"]}',
                info = {
                    'text': data.userManualURL,
                    'option': self.options['YesText'],
                    'set_prefix': instance.set_index
                }
            )

    def hardware(self, instance):
        '''Hardware Information'''

        # Hardwre specific Questions.
        hardware = self.questions["Hardware"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add Basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Hardware',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # If Item from MaRDI Portal or Wikidata set up Query and...
        query = get_sparql_query(f'workflow/queries/hardware_{source}.sparql').format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...Query source for further Information
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        if not results:
            return

        # Structure Results
        data = Hardware.from_query(results)

        # Add Relations between CPU and Hardware to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['H2CPU']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{hardware["CPU"]["uri"]}'
            }
        )

        # Number of Nodes
        if data.nodes:
            value_editor(
                project = instance.project,
                uri = f'{self.base}{hardware["Nodes"]["uri"]}',
                info = {
                    'text': data.nodes, 
                    'set_prefix': instance.set_index
                }
            )

        # Number of Cores
        if data.cores:
            value_editor(
                project = instance.project,
                uri = f'{self.base}{hardware["Cores"]["uri"]}',
                info = {
                    'text': data.cores, 
                    'set_prefix': instance.set_index
                }
            )

    def instrument(self, instance):
        '''Instrument Information'''

        # Instrument specific Questions.
        instrument = self.questions["Instrument"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add Basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Instrument',
            index = (0, instance.set_index)
        )

    def data_set(self, instance):
        '''Data Set Information'''

        # Data Set specific Questions.
        data_set = self.questions["Data Set"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add Basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Data Set',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # If Item from MaRDI Portal or Wikidata set up Query and...
        query = get_sparql_query(f'workflow/queries/data_set_{source}.sparql').format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...Query source for further Information
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        if not results:
            return

        # Structure Results and load Pptions
        data = DataSet.from_query(results)

        # Data Set Size
        if data.size:
            value_editor(
                project = instance.project,
                uri = f'{self.base}{data_set["Size"]["uri"]}',
                info = {
                    'text': data.size[1],
                    'option': data.size[0],
                    'set_prefix': instance.set_index
                }
            )

        # Add Relations between Data Type and Data Set to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['DS2DT']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{data_set["Data Type"]["uri"]}'
            }
        )

        # Add Relations between Representation Format and Data Set to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['DS2RF']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{data_set["Representation Format"]["uri"]}'
            }
        )

        # File Format
        if data.fileFormat:
            value_editor(
                project = instance.project,
                uri = f'{self.base}{data_set["File Format"]["uri"]}',
                info = {
                    'text': data.fileFormat, 
                    'set_prefix': instance.set_index
                }
            )

        # Binary or Text
        if data.binaryOrText:
            value_editor(
                project = instance.project,
                uri = f'{self.base}{data_set["Binary or Text"]["uri"]}',
                info = {
                    'option': data.binaryOrText, 
                    'set_prefix': instance.set_index
                }
            )

        # Proprietary
        if data.proprietary:
            value_editor(
                project = instance.project,
                uri = f'{self.base}{data_set["Proprietary"]["uri"]}',
                info = {
                    'option': data.proprietary, 
                    'set_prefix':  instance.set_index
                }
            )

        # References To Publish
        add_references(
            project = instance.project,
            data = data,
            uri = f'{self.base}{data_set["To Publish"]["uri"]}',
            set_prefix = instance.set_index
        )

        # Archiving
        if data.toArchive:
            value_editor(
                project = instance.project,
                uri = f'{self.base}{data_set["To Archive"]["uri"]}',
                info = {
                    'text': data.toArchive[1],
                    'option': data.toArchive[0], 
                    'set_prefix': instance.set_index
                }
            )

    def method(self, instance):
        '''Method Information'''

        # Method specific Questions.
        method = self.questions["Method"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Method',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # If Item from MaRDI Portal, Wikidata, or MathAlgoDB, set up Query and...
        query = get_sparql_query(f'workflow/queries/method_{source}.sparql').format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...Query source for further Information
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        if not results:
            return

        # Structure Results
        data = Method.from_query(results)

        # Add Relations between Software and Method to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['M2S']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{method["Software"]["uri"]}'
            }
        )

        # Add Relations between Instrument and Method to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['M2I']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{method["Instrument"]["uri"]}'
            }
        )

        return

    def process_step(self, instance):
        '''Process Step Information'''

        # Process Step specific Questions.
        process_step = self.questions["Process Step"]

        # Stop if no Text or 'not found' in ID Field
        if not instance.text or instance.text == 'not found':
            return

        # Add basic Information
        add_basics(
            project = instance.project,
            text = instance.text,
            questions = self.questions,
            item_type = 'Process Step',
            index = (0, instance.set_index)
        )

        # Get source and ID of Item
        source, identifier = instance.external_id.split(':')

        # If Item from MaRDI Portal or Wikidata set up Query and...
        query = get_sparql_query(f'workflow/queries/process_step_{source}.sparql').format(
            identifier,
            **get_items(),
            **get_properties()
        )

        # ...Query source for further Information
        results = query_sparql(
            query,
            get_url(
                source,
                'sparql'
            )
        )

        if not results:
            return

        # Structure Results
        data = ProcessStep.from_query(results)

        # Add Relations between Input Data Set and Process Step to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['PS2IDS']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{process_step["Input"]["uri"]}'
            }
        )

        # Add Relations between Output Data Set and Process Step to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['PS2ODS']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{process_step["Output"]["uri"]}'
            }
        )

        # Add Relations between Method and Process Step to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['PS2M']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{process_step["Method"]["uri"]}'
            }
        )

        # Add Relations between Software Platform and Process Step to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['PS2PLS']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{process_step["Environment-Software"]["uri"]}'
            }
        )

        # Add Relations between Instrument Platform and Process Step to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['PS2PLI']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{process_step["Environment-Instrument"]["uri"]}'
            }
        )

        # Add Relations between Fields and Process Step to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['PS2F']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{process_step["Discipline"]["uri"]}'
            }
        )

        # Add Relations between Math Areas and Process Step to Questionnaire
        add_relations_static(
            project = instance.project,
            data = data,
            props = {
                'keys': PROPS['PS2MA']
            },
            index = {
                'set_prefix': instance.set_index
            },
            statement = {
                'relatant': f'{self.base}{process_step["Discipline"]["uri"]}'
            }
        )
