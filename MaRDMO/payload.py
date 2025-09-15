'''Functions to create Payload for Export'''

from dataclasses import dataclass, field
from typing import Optional, Callable

import re

from .getters import get_items, get_properties
from .queries import query_item

@dataclass
class PayloadState:
    '''Data Class to store the current state of the Payload.'''
    counter: int = 0
    dictionary: dict = field(default_factory=dict)
    subject: dict = field(default_factory=dict)
    subject_item: Optional[str] = None

class GeneratePayload:
    '''Class to build the Payload for an Export to a Wikibase
       with Items, Statements, Qualifiers, and Checks.'''

    def __init__(self, url: str, items: dict,
                 relations: dict | None = None,
                 data_properties: Callable[[str], dict] | None = None):
        '''Instantiate Class Attributes'''
        # Input Attributes
        self.url: str = url
        self.user_items: dict = items
        self.relations: dict = relations
        self.data_properties: Callable[[str], dict] | None = data_properties
        self.properties: dict = get_properties()
        self.items: dict = get_items()
        # Working Attributes
        self.state: PayloadState = PayloadState()

    def _items_url(self):
        '''Get Item URL'''
        return f'{self.url}/w/rest.php/wikibase/v1/entities/items'

    def _statement_url(self, item):
        '''Get Statement URL'''
        return f'{self.url}/w/rest.php/wikibase/v1/entities/items/{item}/statements'

    def _build_item(self, identifier, label, description, statements = None):
        '''Build Item with ID, URL, Label, Description and optional Statement.'''
        # Empty Statements if none provided
        if statements is None:
            statements = []
        # Build Item
        item = {'id': identifier,
                'url': self._items_url(),
                'label': label,
                'description':  description,
                'statements': statements}
        return item

    def _build_statement(self, identifier, content, data_type = "wikibase-item", qualifiers = None):
        '''Build Statement with ID, Datatype, Content and optional Qualifiers.'''
        # Empty Qualifiers if none provided
        if qualifiers is None:
            qualifiers = []
        # Build Statement
        statement = {"statement":
                        {"property":
                            {"id": identifier,
                             "data_type": data_type},
                             "value":
                                {"type": "value",
                                 "content": content},
                             "qualifiers": qualifiers
                        }
                    }
        return statement

    def build_relation_check_query(self):
        '''Build SPARQL Check Query for Statement'''
        relation_keys = [k for k in self.state.dictionary if k.startswith('RELATION')]
        optional_blocks, bind_blocks = [], []

        for idx, key in enumerate(relation_keys):
            entry = self.state.dictionary[key]
            optional_block, bind_block = self._build_relation_block(idx, entry)
            if optional_block is None:
                continue
            optional_blocks.append(optional_block)
            bind_blocks.append(bind_block)

        query_body = '\n'.join(optional_blocks + bind_blocks)
        selectors = " ".join(f"?RELATION{idx}" for idx in range(len(relation_keys)))
        return f'\nSELECT {selectors} WHERE {{\n{query_body}\n}}'

    def _sparql_value(self, value, data_type):
        '''Format Value according to Data Type'''
        if data_type == 'wikibase-item':
            formatted_value = f'wd:{value}'
        elif data_type == 'string':
            formatted_value = f"'{value}'"
        elif data_type == 'quantity':
            formatted_value = f"'{value}'^^<http://www.w3.org/2001/XMLSchema#decimal>"
        elif data_type == 'time':
            formatted_value = f"'{value}'^^<http://www.w3.org/2001/XMLSchema#dateTime>"
        elif data_type == 'monolingualtext':
            formatted_value = f"'{value}'@en"
        elif data_type == 'math':
            escaped_value = value.replace("\\", "\\\\").replace("\"", "\\\"")
            formatted_value = f"'{escaped_value}'^^<http://www.w3.org/1998/Math/MathML>"
        else:
            formatted_value = f"'{value}'"
        return formatted_value

    def _build_qualifier_triples(self, qualifiers, idx):
        '''Build Qualifier Triples'''
        triples = ''
        for q in qualifiers:
            q_prop = q['property']['id']
            q_value = q['value']['content']
            q_data_type = q['property']['data_type']
            if q_value in self.state.dictionary and 'id' in self.state.dictionary[q_value]:
                q_value = self.state.dictionary[q_value]['id']
            triples += (
                f'    ?statement{idx} pq:{q_prop} '
                f'{self._sparql_value(q_value, q_data_type)} .\n'
            )
        return triples

    def _build_relation_block(self, idx, entry):
        '''Build Relation Blocks'''
        target_item_key = entry['url'].split('/')[-2]
        target_item_data = self.state.dictionary.get(target_item_key)
        if not target_item_data:
            return None, None

        target_item_id = target_item_data['id']
        statement = entry['payload']['statement']
        prop_id = statement['property']['id']
        value = statement['value']['content']
        data_type = statement['property']['data_type']

        if value in self.state.dictionary and 'id' in self.state.dictionary[value]:
            value = self.state.dictionary[value]['id']

        subject = f'wd:{target_item_id}'
        value_str = self._sparql_value(value, data_type)
        qualifiers = statement.get('qualifiers', [])
        qual_triples = self._build_qualifier_triples(qualifiers, idx)

        block = {
            'optional': (
                f'OPTIONAL {{\n'
                f'  {subject} p:{prop_id} ?statement{idx} .\n'
                f'  ?statement{idx} ps:{prop_id} {value_str} .\n'
                f'{qual_triples if qualifiers else ""}}}'
            ),
            'bind': f'BIND(BOUND(?statement{idx}) AS ?RELATION{idx})'
        }

        return block['optional'], block['bind']

    def _find_key_by_values(self, id_value, name_value, description_value):
        '''Find Key of Item by its Value'''
        for key, values in self.user_items.items():
            if (values['ID'] == id_value and
                values['Name'] == name_value and
                values['Description'] == description_value):
                return key
        return None

    def get_dictionary(self):
        '''Get a Dictionary'''
        # Get Target Dictionary
        target_dictionary = self.state.dictionary
        return target_dictionary

    def get_item_key(self, value, role='subject'):
        """Get the Key of an Item (Subject/Object)"""
        if not value.get('Name') or not value.get('Description'):
            raise ValueError("All Items need to have a 'Name' and 'Description'!")

        item_key = self._find_key_by_values(
            value['ID'],
            value['Name'],
            value['Description'],
        )

        if role == 'subject':
            self.state.subject = value
            self.state.subject_item = item_key

        return item_key

    def add_qualifier(self, identifier, data_type, content):
        '''Build Qualifier to used in Statement.'''
        # Build Qualifer
        qualifier = [{"property":
                        {"id": identifier,
                         "data_type": data_type},
                         "value": 
                            {"type": "value",
                             "content": content}
                    }]
        return qualifier

    def add_data_properties(self, item_class):
        '''Build Data Property Statements'''
        data_properties = self.data_properties(item_class)
        for prop in self.state.subject.get('Properties', {}).values():
            self.add_answer(
                verb=self.properties['instance of'],
                object_and_type=[
                    data_properties[prop],
                    'wikibase-item',
                ]
            )

    def add_check_results(self, check):
        '''Add Check Status to Statements'''
        relation_keys = [k for k in self.state.dictionary if k.startswith('RELATION')]
        for idx, key in enumerate(relation_keys):
            exists_key = f'RELATION{idx}'
            exists_value = check[0].get(exists_key, {}).get('value', 'false')
            self.state.dictionary[key]['exists'] = exists_value

    def add_answer(self, verb, object_and_type,
                   qualifier = None, subject = None):
        '''Add answer to Payload'''
        if subject is None:
            subject = self.state.subject_item
        if qualifier is None:
            qualifier = []
        # Gather Statement
        statement = {
            'property_id': verb,
            'datatype': object_and_type[1],
            'value': object_and_type[0]
        }
        # Pattern of New Item
        pattern = re.compile(r"^Item\d{10}$")
        # Add Relation
        if (
            self.state.dictionary[subject]['id']
            or (isinstance(statement['value'], str) and pattern.match(statement['value']))
        ):
            self._add_relation(
                item=subject,
                statement=statement,
                qualifier=qualifier
            )
        else:
            self._add_to_item_statement(
                item=subject,
                statement=statement,
                qualifier=qualifier
            )


    def add_answers(self, mardmo_property, wikibase_property, datatype = 'string'):
        '''Add answer to Payload.'''
        for entry in self.state.subject.get(mardmo_property, {}).values():
            self.add_answer(
                verb=self.properties[wikibase_property],
                object_and_type=[
                    entry,
                    datatype,
                ]
            )

    def add_backward_relation(self, data, relation, relatants):
        '''Add backward relations to payload.'''
        for entry in data:
            for relatant in entry.get(relatants, {}).values():
                relatant_item = self.get_item_key(relatant, 'object')
                if self.state.subject_item == relatant_item:
                    entry_item = self.get_item_key(entry, 'object')
                    self.add_answer(
                        verb=relation,
                        object_and_type=[
                            entry_item,
                            'wikibase-item',
                        ]
                    )

    def add_forward_relation_single(self, relation, relatant,
                                    alternative = None, qualifier = None):
        '''Add single forward relation to payload.'''
        # Empty Qualifiers if none provided
        if qualifier is None:
            qualifier = []
        for entry in self.state.subject.get(relatant, {}).values():
            # Get Item Key
            entry_item = self.get_item_key(entry, 'object')
            if entry_item in self.state.dictionary:
                # Add Payload
                self.add_answer(
                    verb=relation,
                    object_and_type=[
                        entry_item,
                        'wikibase-item',
                    ],
                    qualifier=qualifier
                )
            else:
                # Add Payload
                self.add_answer(
                    verb=alternative['relation'],
                    object_and_type=[
                        entry.get(alternative['relatant']),
                        'string',
                    ],
                    qualifier=qualifier
                )

    def add_forward_relation_multiple(self, relation, relatant, reverse = False):
        '''Add multiple forward relations to payload.'''
        for key, prop in self.state.subject.get(relation, {}).items():
            # Get Item Key
            relatant_item = self.get_item_key(
                self.state.subject.get(relatant,{}).get(key,{}),
                'object'
            )
            # Get (optional) Order Number
            qualifier = []
            if self.state.subject.get('formulation_number'):
                qualifier = self.add_qualifier(
                    self.properties['series ordinal'],
                    'string', 
                    self.state.subject['formulation_number'][key]
                )
            # Get potential Qualifier
            if len(self.relations[prop]) == 2:
                if self.relations[prop][1] not in ('forward', 'backward'):
                    qualifier.extend(
                        self.add_qualifier(
                            self.properties['object has role'],
                            'wikibase-item',
                            self.relations[prop][1]
                        )
                    )
            # Add Payload
            if not reverse:
                self.add_answer(
                    verb=self.relations[prop][0],
                    object_and_type=[
                        relatant_item,
                        'wikibase-item',
                    ],
                    qualifier=qualifier
                )
            else:
                self.add_answer(
                    verb=self.relations[prop][0],
                    object_and_type=[
                        self.state.subject_item,
                        'wikibase-item',
                    ],
                    qualifier=qualifier,
                    subject=relatant_item
                )

    def add_in_defining_formula(self):
        '''Add in defining formula Statement'''
        for element in self.state.subject.get('element', {}).values():
            # Get Item Key
            quantity_item = self.get_item_key(
                element.get('quantity', {}),
                'object'
            )
            # Add Quantity Qualifier
            qualifier = self.add_qualifier(
                self.properties['symbol represents'],
                'wikibase-item',
                quantity_item
            )
            # Add Symbol to Payload
            if self.state.subject_item == quantity_item:
                self._add_relation(
                    item = self.state.subject_item,
                    statement = {
                        'property_id': self.properties['in defining formula'],
                        'value': element.get('symbol', ''),
                        'datatype': 'math'
                    },
                    qualifier = qualifier
                )
            else:
                self.add_answer(
                    verb=self.properties['in defining formula'],
                    object_and_type=[
                        element.get('symbol', ''),
                        'math',
                    ],
                    qualifier=qualifier
                )

    def _add_entry(self, key, value):
        '''Add Entry to Payload'''
        self.state.dictionary[key] = value

    def _add_to_item_statement(self, item, statement, qualifier=None):
        '''Add to Statement of Item'''
        if qualifier is None:
            qualifier = []
        self.state.dictionary[item]['statements'].append(
            [
                statement['property_id'],
                statement['datatype'],
                statement['value'],
                qualifier
            ]
        )

    def _add_relation(self, item, statement, qualifier=None):
        '''Add Statement to Item'''
        if qualifier is None:
            qualifier = []
        key = f"RELATION{self.state.counter}"
        self.state.dictionary[key] = {
            'id': '',
            'url': self._statement_url(item),
            'payload': self._build_statement(
                statement['property_id'],
                statement['value'],
                statement['datatype'],
                qualifier
            )
        }
        self.state.counter += 1

    def add_intra_class_relation(self, relation, relatant):
        '''Add forward/backward relations to Items of same Class'''
        for key, prop in self.state.subject.get(relation, {}).items():
            # Get Item Key
            relatant_item = self.get_item_key(
                self.state.subject.get(relatant, {}).get(key),
                'object'
            )
            # Add potential Qualifier
            qualifier = []
            if self.state.subject.get('assumption', {}).get(key):
                for assumption in self.state.subject['assumption'][key].values():
                    assumption_item = self.get_item_key(
                        assumption,
                        'object'
                    )
                    qualifier.extend(
                        self.add_qualifier(
                            self.properties['assumes'],
                            'wikibase-item',
                            assumption_item
                        )
                    )
            if self.state.subject.get('task_number', {}).get(key):
                qualifier.extend(
                    self.add_qualifier(
                        self.properties['series ordinal'],
                        'string',
                        self.state.subject['task_number'][key]
                    )
                )
            # Add Forward or Backward Relation
            if self.relations[prop][1] == 'forward':
                self.add_answer(
                    verb=self.relations[prop][0],
                    object_and_type=[
                        relatant_item,
                        'wikibase-item',
                    ],
                    qualifier=qualifier
                )
            elif self.relations[prop][1] == 'backward':
                self.add_answer(
                    verb=self.relations[prop][0],
                    object_and_type=[
                        self.state.subject_item,
                        'wikibase-item',
                    ],
                    qualifier=qualifier,
                    subject=relatant_item
                )

    def add_item_payload(self):
        '''Add Payload String to Item'''
        for item_id, item_data in self.state.dictionary.items():
            # Check if Item in Payload
            if not item_id.startswith('Item'):
                continue
            # Extract Information
            label = item_data.get("label", "")
            description = item_data.get("description", "")
            statements_input = item_data.get("statements", [])
            # Grouped statements by PID
            statements = {}
            for s in statements_input:
                pid, dtype, obj = s[0], s[1], s[2]
                qualifier = None
                if len(s) == 4:
                    qualifier = s[3]
                statement = {
                    "property": {"id": pid, "data_type": dtype},
                    "value": {"type": "value", "content": obj}
                }
                if qualifier:
                    statement["qualifiers"] = qualifier

                statements.setdefault(pid, []).append(statement)
            # Build payload
            payload = {
                "item": {
                    "labels": {"en": label},
                    "statements": statements
                }
            }
            if description:
                payload["item"]["descriptions"] = {"en": description}
            # Attach to original dict
            item_data["payload"] = payload

    def _check_mardi_and_raise(self, name: str, description: str):
        """Check if item exists in MaRDI Portal and raise error if it does."""
        mardi_identifier = query_item(name, description)
        if mardi_identifier:
            raise ValueError(
                f"An item ({mardi_identifier}) with the label '{name}' "
                f"and description '{description}' already exists on the MaRDI Portal. "
                "If you intend to use this item, please select it in the questionnaire. "
                "Otherwise, redefine it."
            )
        return mardi_identifier

    def _statement_by_id_type(self, value: dict, id_type: str):
        """Return statements for a user-defined item based on ID type."""
        statements = []
        if id_type == 'wikidata':
            # Add Wikidata ID
            statements.append(
                [
                    self.properties['Wikidata QID'],
                    'external-id',
                    value['ID'].split(':')[1]
                ]
            )
        if id_type == 'no author found':
            # Add ORCID ID Statement
            if value.get('orcid'):
                statements.append(
                    [
                        self.properties['ORCID iD'],
                        'external-id',
                        value['orcid']
                    ]
                )
            # Add zbMath ID Statement
            if value.get('zbmath'):
                statements.append(
                    [
                        self.properties['zbMATH author ID'],
                        'external-id',
                        value['zbmath']
                    ]
                )
            # If Authors has ID, add further Statements
            if statements:
                statements.append(
                    [
                        self.properties['instance of'],
                        'wikibase-item',
                        self.items['human']
                    ]
                )
        if id_type == 'no journal found':
            # Add ISSN ID Statement
            if value.get('issn'):
                statements.append(
                    [
                        self.properties['ISSN'],
                        'external-id',
                        value['issn']
                    ]
                )
            # Add further Statements
            statements.append(
                [
                    self.properties['instance of'],
                    'wikibase-item',
                    self.items['scientific journal']
                ]
            )
        return statements

    def process_items(self):
        """Process Items"""
        handlers = {
            'mardi': lambda key, value: 
                self._add_entry(
                    key,
                    self._build_item(value['ID'].split(':')[1],
                    value['Name'],
                    value['Description']
                )
            ),
            'wikidata': lambda key, value: (
                self._check_mardi_and_raise(
                    value['Name'],
                    value['Description']
                ),
                self._add_entry(
                    key,
                    self._build_item(
                        '',
                        value['Name'],
                        value['Description'],
                        self._statement_by_id_type(
                            value,
                            'wikidata'))
                )
            ),
            'mathalgodb': lambda key, value: (
                self._check_mardi_and_raise(
                    value['Name'],
                    value['Description']
                ),
                self._add_entry(
                    key,
                    self._build_item(
                        '',
                        value['Name'],
                        value['Description']
                    )
                )
            ),
            'not found': lambda key, value: (
                self._check_mardi_and_raise(
                    value['Name'],
                    value['Description']
                ),
                self._add_entry(
                    key,
                    self._build_item(
                        '',
                        value['Name'],
                        value['Description'],
                        self._statement_by_id_type(
                            value,
                            'not found'
                        )
                    )
                )
            ),
            'no author found': lambda key, value: (
                self._check_mardi_and_raise(
                    value['Name'],
                    value['Description']
                ),
                self._add_entry(
                    key,
                    self._build_item(
                        '',
                        value['Name'],
                        value['Description'],
                        self._statement_by_id_type(
                            value,
                            'no author found'
                        )
                    )
                )
            ),
            'no journal found': lambda key, value: (
                self._check_mardi_and_raise(
                    value['Name'],
                    value['Description']
                ),
                self._add_entry(
                    key,
                    self._build_item(
                        '',
                        value['Name'],
                        value['Description'],
                        self._statement_by_id_type(
                            value,
                            'no journal found'
                        )
                    )
                )
            ),
        }

        for key, value in self.user_items.items():
            if not value.get('ID'):
                continue
            for id_type, handler in handlers.items():
                if id_type in value['ID']:
                    if id_type == 'no author found':
                        if value['zbmath'] or value['orcid']:
                            handler(key, value)
                    else:
                        handler(key, value)
                    break
