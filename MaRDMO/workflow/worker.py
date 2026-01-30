from dataclasses import asdict

from .models import ModelProperties, Variables, Parameters
from .constants import REPRODUCIBILITY

from ..getters import get_items, get_options, get_properties, get_sparql_query, get_url
from ..helpers import unique_items
from ..queries import query_sparql
from ..payload import GeneratePayload

class prepareWorkflow:

    def __init__(self):
        self.items = get_items()
        self.properties = get_properties()

    def preview(self, data):
        '''Function to establish relations between Workflow Documentation Data'''
        # Update Model Properties via MathModDB
        if data.get('model',{}).get('ID'):
            _, identifier = data['model']['ID'].split(':')

            query = get_sparql_query(
                f'workflow/queries/preview_basic.sparql'
            ).format(
                identifier,
                **self.items,
                **self.properties
            )

            basic = query_sparql(query, get_url('mardi', 'sparql'))

            if basic:
                data.get('model', {}).update(asdict(ModelProperties.from_query(basic)))

        # Update Model Variables and Parameters via MathModDB
        if data.get('model', {}).get('task'):

            query = get_sparql_query(
                f'workflow/queries/preview_variable.sparql'
            ).format(
                ' '.join(f"wd:{value.get('ID', '').split(':')[1]}"
                for _, value in data['model']['task'].items()),
                **self.items,
                **self.properties
            )

            variables = query_sparql(query, get_url('mardi', 'sparql'))
            if variables:
                for idx, variable in enumerate(variables):
                    data.setdefault('variables', {}).update(
                        {
                            idx: asdict(Variables.from_query(variable))
                        }
                    )

            query = get_sparql_query(
                f'workflow/queries/preview_parameter.sparql'
            ).format(
                ' '.join(f"wd:{value.get('ID', '').split(':')[1]}"
                for _, value in data['model']['task'].items()),
                **self.items,
                **self.properties
            )

            parameters = query_sparql(query, get_url('mardi', 'sparql'))
            if parameters:
                for idx, parameter in enumerate(parameters):
                    data.setdefault('parameters', {}).update(
                        {
                            idx: asdict(Parameters.from_query(parameter))
                        }
                    )

        return data

    def export(self,data, title, url):
        """Function to create Payload for Workflow Export."""
        
        items, dependency = unique_items(data, title)

        payload = GeneratePayload(
            dependency = dependency,
            user_items = items,
            url = url,
            wikibase = {
                'items': get_items(),
                'properties': get_properties(),
            }
        )

        # Load Options
        options = get_options()

        # Add / Retrieve Components of Interdisciplinary Workflow Item
        payload.process_items()

        ### Add additional Algorithms / Methods Information
        for method in data.get('method', {}).values():

            # Continue if no ID exists
            if not method.get('ID'):
                continue

            # Get Item Key
            payload.get_item_key(method)

            # Add Class
            if 'mathalgodb' in method['ID']:
                payload.add_answer(
                    verb=self.properties['instance of'],
                    object_and_type=[
                        self.items['algorithm'],
                        'wikibase-item',
                    ]
                )
            else:
                payload.add_answer(
                    verb=self.properties['instance of'],
                    object_and_type=[
                        self.items['method'],
                        'wikibase-item',
                    ]
                )

        ### Add additional Software Information
        for software in data.get('software', {}).values():

            # Continue if no ID exists
            if not software.get('ID'):
                continue

            # Get Item Key
            payload.get_item_key(software)

            # Add Class
            payload.add_answer(
                    verb=self.properties['instance of'],
                    object_and_type=[
                        self.items['software'],
                        'wikibase-item',
                    ]
                )

            # Add References of the Software
            for reference in software.get('Reference', {}).values():
                if reference[0] == options['DOI']:
                    payload.add_answer(
                        verb=self.properties['DOI'],
                        object_and_type=[
                            reference[1],
                            'external-id',
                        ]
                    )
                elif reference[0] == options['SWMATH']:
                    payload.add_answer(
                        verb=self.properties['swMath work ID'],
                        object_and_type=[
                            reference[1],
                            'external-id',
                        ]
                    )
                elif reference[0] == options['URL']:
                    payload.add_answer(
                        verb=self.properties['URL'],
                        object_and_type=[
                            reference[1],
                            'url',
                        ]
                    )

            # Add Programming Languages
            payload.add_single_relation(
                statement = {
                    'relation': self.properties['programmed in'],
                    'relatant': 'programminglanguage'
                }
            )

            # Add Dependencies
            payload.add_single_relation(
                statement = {
                    'relation': self.properties['depends on software'],
                    'relatant': 'dependency'
                }
            )

            # Add Source Code Repository
            if software.get('Published', [''])[0] == options['YesText']:
                payload.add_answer(
                    verb=self.properties['source code repository URL'],
                    object_and_type=[
                        software['Published'][1],
                        'url',
                    ]
                )

            # Add Documentation / Manual
            if software.get('Documented', [''])[0] == options['YesText']:
                payload.add_answer(
                    verb=self.properties['user manual URL'],
                    object_and_type=[
                        software['Documented'][1],
                        'url',
                    ]
                )

        ### Add additional Hardware Information
        for hardware in data.get('hardware', {}).values():

            # Continue if no ID exists
            if not hardware.get('ID'):
                continue

            # Get Item Key
            payload.get_item_key(hardware)

            # Add Class
            payload.add_answer(
                verb=self.properties['instance of'],
                object_and_type=[
                    self.items['computer hardware'],
                    'wikibase-item',
                ]
            )

            # Add CPU
            payload.add_single_relation(
                statement = {
                    'relation': self.properties['CPU'],
                    'relatant': 'cpu'
                }
            )

            # Add Number of Computing Nodes
            if hardware['Nodes']:
                payload.add_answer(
                    verb=self.properties['has part(s)'],
                    object_and_type=[
                        self.items['compute node'],
                        'wikibase-item',
                    ],
                    qualifier = [
                                    {
                                        "property": {
                                            "id": self.properties['quantity_property'],
                                        },
                                        "value": {
                                            "type": "value",
                                            "content": {
                                                "amount": f"+{hardware['Nodes']}",
                                                "unit": "1",
                                            },
                                        },
                                    }
                                ]
                )

            # Add Number of Processor Cores
            if hardware['Cores']:
                payload.add_answer(
                    verb=self.properties['number of processor cores'],
                    object_and_type=[
                        {
                            "amount": f"+{hardware['Cores']}",
                            "unit":"1"
                        },
                        'quantity'
                    ]
                )

        ### Add additional Instrument Information
        for instrument in data.get('instrument', {}).values():

            # Continue if no ID exists
            if not instrument.get('ID'):
                continue

            # Get Item Key
            payload.get_item_key(instrument)

            # Add Class
            payload.add_answer(
                verb=self.properties['instance of'],
                object_and_type=[
                    self.items['research tool'],
                    'wikibase-item',
                ]
            )

            ### MORE INSTRUMENT INFORMATION TO ADD ###

        ### Add additional Dataset Information
        for dataset in data.get('dataset', {}).values():

            # Continue if no ID exists
            if not dataset.get('ID'):
                continue

            # Get Item Key
            payload.get_item_key(dataset)

            # Add Class
            payload.add_answer(
                verb=self.properties['instance of'],
                object_and_type=[
                    self.items['data set'],
                    'wikibase-item',
                ]
            )

            # Size of the data set
            if dataset.get('Size'):
                if dataset['Size'][0] == options['kilobyte']:
                    verb = self.properties['data size']
                    object = {
                        "amount": f"+{dataset['Size'][1]}",
                        "unit": f"{get_url('mardi', 'uri')}/entity/{self.items['kilobyte']}"
                    }
                elif dataset['Size'][0] == options['megabyte']:
                    verb = self.properties['data size']
                    object = {
                        "amount": f"+{dataset['Size'][1]}",
                        "unit": f"{get_url('mardi', 'uri')}/entity/{self.items['megabyte']}"
                    }
                elif dataset['Size'][0] == options['gigabyte']:
                    verb = self.properties['data size']
                    object = {
                        "amount": f"+{dataset['Size'][1]}",
                        "unit": f"{get_url('mardi', 'uri')}/entity/{self.items['gigabyte']}"
                    }
                elif dataset['Size'][0] == options['terabyte']:
                    verb = self.properties['data size']
                    object = {
                        "amount": f"+{dataset['Size'][1]}",
                        "unit": f"{get_url('mardi', 'uri')}/entity/{self.items['terabyte']}"
                    }
                elif dataset['Size'][0] == options['items']:
                    verb = self.properties['number of records']
                    object = {
                        "amount": f"+{dataset['Size'][1]}","unit":"1"
                    }

                payload.add_answer(
                    verb=verb,
                    object_and_type=[
                        object,
                        'quantity',
                    ]
                )

            # Add Data Type
            payload.add_single_relation(
                statement = {
                    'relation': self.properties['uses'], 
                    'relatant': 'datatype'
                },
                qualifier = payload.add_qualifier(
                    self.properties['object has role'],
                    'wikibase-item',
                    self.items['data type']
                )
            )

            # Add Representation Format
            payload.add_single_relation(
                statement = {
                    'relation': self.properties['uses'], 
                    'relatant': 'representationformat'
                },
                qualifier = payload.add_qualifier(
                    self.properties['object has role'],
                    'wikibase-item',
                    self.items['representation format']
                )
            )

            # Add File Format
            if dataset.get('FileFormat'):
                payload.add_answer(
                    verb=self.properties['file extension'],
                    object_and_type=[
                        dataset['FileFormat'],
                        'string',
                    ]
                )

            # Add binary or text data
            if dataset.get('BinaryText'):
                if dataset['BinaryText'] == options['binary']:
                    payload.add_answer(
                        verb=self.properties['instance of'],
                        object_and_type=[
                            self.items['binary data'],
                            'wikibase-item',
                        ]
                    )
                elif dataset['BinaryText'] == options['text']:
                    payload.add_answer(
                        verb=self.properties['instance of'],
                        object_and_type=[
                            self.items['text data'],
                            'wikibase-item',
                        ]
                    )

            # Data Set Proprietary
            if dataset.get('Proprietary'):
                if dataset['Proprietary'] == options['Yes']:
                    payload.add_answer(
                        verb=self.properties['instance of'],
                        object_and_type=[
                            self.items['proprietary information'],
                            'wikibase-item',
                        ]
                    )
                elif dataset['Proprietary'] == options['No']:
                    payload.add_answer(
                        verb=self.properties['instance of'],
                        object_and_type=[
                            self.items['open data'],
                            'wikibase-item',
                        ]
                    )

            # Data Set to Publish
            if dataset.get('ToPublish'):
                if dataset['ToPublish'].get(0, ['',''])[0] == options['Yes']:
                    payload.add_answer(
                        verb=self.properties['mandates'],
                        object_and_type=[
                            self.items['data publishing'],
                            'wikibase-item',
                        ]
                    )
                    if dataset['ToPublish'].get(1, ['',''])[0] == options['DOI']:
                        payload.add_answer(
                            verb=self.properties['DOI'],
                            object_and_type=[
                                dataset['ToPublish'][1][1],
                                'external-id',
                            ]
                        )
                    if dataset['ToPublish'].get(2, ['',''])[0] == options['URL']:
                        payload.add_answer(
                            verb=self.properties['URL'],
                            object_and_type=[
                                dataset['ToPublish'][2][2],
                                'url',
                            ]
                        )

            # Data Set To Archive
            if dataset.get('ToArchive'):
                if dataset['ToArchive'][0] == options['YesText']:
                    qualifier = []
                    if dataset['ToArchive'][1]:
                        qualifier = payload.add_qualifier(
                            self.properties['end time'],
                            'time',
                            {
                                "time": f"+{dataset['ToArchive'][1]}-00-00T00:00:00Z",
                                "precision": 9,
                                "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                            }
                        )
                    payload.add_answer(
                            verb=self.properties['mandates'],
                            object_and_type=[
                                self.items['research data archiving'],
                                'wikibase-item',
                            ],
                            qualifier=qualifier
                        )

        ### Add Process Step Information
        for processstep in data.get('processstep', {}).values():

            # Continue if no ID exists
            if not processstep.get('ID'):
                continue

            # Get Item Key
            payload.get_item_key(processstep)

            # Add Class
            payload.add_answer(
                verb=self.properties['instance of'],
                object_and_type=[
                    self.items['process step'],
                    'wikibase-item',
                ]
            )

            # Add Input Data Sets
            payload.add_single_relation(
                statement = {
                    'relation': self.properties['input data set'],
                    'relatant': 'input'
                }
            )

            # Add Output Data Sets
            payload.add_single_relation(
                statement = {
                    'relation': self.properties['output data set'],
                    'relatant': 'output'
                }
            )

            # Add applied Methods
            for method in processstep.get('method', {}).values():
                # Continue if no ID exists
                if not method.get('ID'):
                    continue
                # Get Entry Key
                method_item = payload.get_item_key(method, 'object')
                # Get Qualifier
                qualifier = []
                for parameter in method.get('Parameter', {}).values():
                    qualifier.extend(
                        payload.add_qualifier(
                            self.properties['comment'],
                            'string',
                            parameter
                        )
                    )
                # Add to Payload
                payload.add_answer(
                            verb=self.properties['uses'],
                            object_and_type=[
                                method_item,
                                'wikibase-item',
                            ],
                            qualifier=qualifier
                        )

            # Add Software Environment
            payload.add_single_relation(
                statement = {
                    'relation': self.properties['platform'], 
                    'relatant': 'environmentSoftware'
                },
                qualifier = payload.add_qualifier(
                    self.properties['object has role'],
                    'wikibase-item',
                    self.items['software']
                )
            )

            # Add Instrument Environment
            payload.add_single_relation(
                statement = {
                    'relation': self.properties['platform'], 
                    'relatant': 'environmentInstrument'
                },
                qualifier = payload.add_qualifier(
                    self.properties['object has role'],
                    'wikibase-item',
                    self.items['research tool']
                )
            )

            # Add Disciplines (math and non-math)
            for discipline in processstep.get('discipline', {}).values():
                # Check if new ID exists
                if 'msc:' in discipline.get('ID'):
                    _, id = discipline['ID'].split(':')
                    payload.add_answer(
                        verb=self.properties['MSC ID'],
                        object_and_type=[
                            id,
                            'external-id',
                        ]
                    )
                else:
                    # Get Discipline Key
                    discipline_item = payload.get_item_key(discipline, 'object')
                    # Add to Payload
                    payload.add_answer(
                        verb=self.properties['field of work'],
                        object_and_type=[
                            discipline_item,
                            'wikibase-item',
                        ]
                    )

        for publication in data.get('publication', {}).values():

            # Continue if no ID exists
            if not publication.get('ID'):
                continue

            # Get Item Key
            payload.get_item_key(publication)

            if 'mardi' not in publication['ID']:

                # Set and add the Class of the Publication
                if publication.get('entrytype') == 'scholarly article':
                    pclass = self.items['scholarly article']
                else:
                    pclass = self.items['publication']

                payload.add_answer(
                    verb=self.properties['instance of'],
                    object_and_type=[
                        pclass,
                        'wikibase-item',
                    ]
                )

                # Add Publication Profile
                payload.add_answer(
                        verb = self.properties["MaRDI profile type"],
                        object_and_type = [
                            self.items["MaRDI publication profile"],
                            "wikibase-item"
                        ],
                    )

                # Add the DOI of the Publication
                if publication.get('reference', {}).get(0):
                    payload.add_answer(
                        verb=self.properties['DOI'],
                        object_and_type=[
                            publication['reference'][0][1],
                            'external-id',
                        ]
                    )

                # Add the Title of the Publication
                if publication.get('title'):
                    payload.add_answer(
                        verb=self.properties['title'],
                        object_and_type=[
                            {"text": publication['title'], "language": "en"},
                            'monolingualtext',
                        ]
                    )

                # Add the Volume of the Publication
                if publication.get('volume'):
                    payload.add_answer(
                        verb=self.properties['volume'],
                        object_and_type=[
                            publication['volume'],
                            'string',
                        ]
                    )

                # Add the Issue of the Publication
                if publication.get('issue'):
                    payload.add_answer(
                        verb=self.properties['issue'],
                        object_and_type=[
                            publication['issue'],
                            'string',
                        ]
                    )

                # Add the Page(s) of the Publication
                if publication.get('page'):
                    payload.add_answer(
                        verb=self.properties['page(s)'],
                        object_and_type=[
                            publication['page'],
                            'string',
                        ]
                    )

                # Add the Date of the Publication
                if publication.get('date'):
                    payload.add_answer(
                        verb=self.properties['publication date'],
                        object_and_type=[
                            {
                                "time": f"+{publication['date']}T00:00:00Z",
                                "precision": 11,
                                "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                            },
                            'time',
                        ]
                    )

                # Add the Language of the Publication
                payload.add_single_relation(
                    statement = {
                        'relation': self.properties['language of work or name'],
                        'relatant': 'language'
                    }
                )

                # Add the Journal of the Publication
                payload.add_single_relation(
                    statement = {
                        'relation': self.properties['published in'],
                        'relatant': 'journal'
                    }
                )

                # Add the Authors of the Publication
                payload.add_single_relation(
                    statement = {
                        'relation': self.properties['author'],
                        'relatant': 'author'
                    },
                    alt_statement = {
                        'relation': self.properties['author name string'], 
                        'relatant': 'Name'
                    }
                )

        # Add Interdisciplinary Workflow Information
        workflow = {
            'ID': 'not found',
            'Name': title,
            'Description': data.get('general', {}).get('objective')
        }

        # Get Item Key
        payload.get_item_key(workflow)

        # Add Class
        payload.add_answer(
            verb=self.properties['instance of'],
            object_and_type=[
                self.items['research workflow'],
                'wikibase-item',
            ]
        )

        # Procedure Description to Workflow
        if data.get('general', {}).get('procedure'):
            payload.add_answer(
                verb=self.properties['description'],
                object_and_type=[
                    data['general']['procedure'],
                    'string',
                ]
            )

        # Add Reproducibility Aspects
        for key, value in REPRODUCIBILITY.items():
            if data.get('reproducibility', {}).get(key) == options['Yes']:
                qualifier = []
                if data['reproducibility'].get(f'{key}condition'):
                    qualifier.extend(
                        payload.add_qualifier(
                            self.properties['comment'],
                            'string',
                            data['reproducibility'][f'{key}condition']
                        )
                    )
                payload.add_answer(
                    verb=self.properties['instance of'],
                    object_and_type=[
                        self.items[value],
                        'wikibase-item',
                    ],
                    qualifier=qualifier
                )

        # Add Transferability Aspects
        if data.get('reproducibility', {}).get('transferability'):
            qualifier = []
            for value in data['reproducibility']['transferability'].values():
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['comment'],
                        'string',
                        value
                    )
                )
            payload.add_answer(
                verb=self.properties['instance of'],
                object_and_type=[
                    self.items['transferable research workflow'],
                    'wikibase-item',
                ],
                qualifier=qualifier
            )

        # Add Model and Task the Workflow Uses
        if data.get('model'):
            #Continue if ID exists
            if data['model'].get('ID'):
                # Get Item Key
                model_item = payload.get_item_key(data['model'], 'object')
                # Add Statement with Qualifier
                qualifier = []
                for task in data['model'].get('task', {}).values():
                    qualifier.extend(
                        payload.add_qualifier(
                            self.properties['used by'],
                            'wikibase-item',
                            payload.get_item_key(task, 'object')
                        )
                    )
                payload.add_answer(
                    verb=self.properties['uses'],
                    object_and_type=[
                        model_item,
                        'wikibase-item',
                    ],
                    qualifier=qualifier
                )

        # Add Methods the Workflow Uses
        for value in data.get('method', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            method_item = payload.get_item_key(value, 'object')
            # Add Statement with Qualifier
            qualifier = []
            for parameter in value.get('Parameter', {}).values():
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['comment'],
                        'string',
                        parameter
                    )
                )
            for software in value.get('software', {}).values():
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['implemented by'],
                        payload.get_item_key(software, 'object')
                    )
                )
            for instrument in value.get('instrument', {}).values():
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['implemented by'],
                        payload.get_item_key(instrument, 'object')
                    )
                )
            payload.add_answer(
                verb=self.properties['uses'],
                object_and_type=[
                    method_item,
                    'wikibase-item',
                ],
                qualifier=qualifier
            )

        # Add Software the Workflow uses
        for value in data.get('software', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            software_item = payload.get_item_key(value, 'object')
            # Add Statement with Qualifier
            qualifier = []
            for hardware in data.get('hardware', {}).values():
                for software in hardware.get('software', {}).values():
                    if (software.get('ID'), software.get('Name'), software.get('Description')) == (value['ID'], value['Name'], value['Description']):
                        hardware_item = payload.get_item_key(hardware, 'object')
                        qualifier.extend(payload.add_qualifier(self.properties['platform'], 'wikibase-item', hardware_item))
            if value.get('Version'):
                qualifier = payload.add_qualifier(
                    self.properties['software version identifier'],
                    'string',
                    value['Version']
                )
            payload.add_answer(
                verb=self.properties['uses'],
                object_and_type=[
                    software_item,
                    'wikibase-item',
                ],
                qualifier=qualifier
            )

        # Add Hardware the Workflow Uses
        for value in data.get('hardware', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            hardware_item = payload.get_item_key(value, 'object')
            # Add Satement with Qualifier
            qualifier = []
            for compiler in value.get('compiler', {}).values():
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['uses'],
                        'wikibase-item',
                        payload.get_item_key(compiler, 'object')
                    )
                )
            payload.add_answer(
                verb=self.properties['uses'],
                object_and_type=[
                    hardware_item,
                    'wikibase-item',
                ],
                qualifier=qualifier
            )

        # Add instruments the workflow Uses
        for value in data.get('instrument', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            instrument_item = payload.get_item_key(value, 'object')
            # Add Statement with Qualifer
            qualifier = []
            if value.get('Version'):
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['edition number'],
                        'string',
                        value['Version']
                    )
                )
            if value.get('SerialNumber'):
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['serial number'],
                        'string',
                        value['SerialNumber']
                    )
                )
            for location in value.get('location', {}).values():
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['location'],
                        'wikibase-item',
                        payload.get_item_key(location, 'object')
                    )
                )
            for software in value.get('software', {}).values():
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['uses'],
                        'wikibase-item',
                        payload.get_item_key(software, 'object')
                    )
                )
            payload.add_answer(
                verb=self.properties['uses'],
                object_and_type=[
                    instrument_item,
                    'wikibase-item',
                ],
                qualifier=qualifier
            )

        # Add Data Sets the Workflow Uses
        for value in data.get('dataset', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            dataset_item = payload.get_item_key(value, 'object')
            # Add Statement
            payload.add_answer(
                verb=self.properties['uses'],
                object_and_type=[
                    dataset_item,
                    'wikibase-item',
                ]
            )

        # Add Process Steps the Workflow Uses
        for value in data.get('processstep', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            processstep_item = payload.get_item_key(value, 'object')
            # Add Statement with Qualifier
            qualifier = []
            for parameter in value.get('parameter', {}).values():
                qualifier.extend(
                    payload.add_qualifier(
                        self.properties['comment'],
                        'string',
                        parameter
                    )
                )
            payload.add_answer(
                verb=self.properties['uses'],
                object_and_type=[
                    processstep_item,
                    'wikibase-item',
                ],
                qualifier=qualifier
            )

        # Add Publications related to the Workflow
        for value in data.get('publication', {}).values():
            # Continue if no ID exists
            if not value.get('ID'):
                continue
            # Get Item Key
            publication_item = payload.get_item_key(value, 'object')
            # Add Statement
            payload.add_answer(
                verb=self.properties['cites work'],
                object_and_type=[
                    publication_item,
                    'wikibase-item',
                ]
            )

        # Construct Item Payloads
        payload.add_item_payload()

        # If Relations are added, check if they exist
        if any(key.startswith('RELATION') for key in payload.get_dictionary()):

            # Generate SPARQL Check Query
            query = payload.build_relation_check_query()

            # Perform Check Query for Relations
            check = query_sparql(query, get_url('mardi', 'sparql'))

            # Add Check Results
            payload.add_check_results(check)

        return payload.get_dictionary()
