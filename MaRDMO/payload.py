'''Functions to create Payload for Export'''

from dataclasses import dataclass, field
from typing import Optional

import re

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

    def __init__(
        self,
        url: str,
        user_items: dict | None = None,
        wikibase: dict | None = None,
        dependency: dict | None = None
    ):
        '''Instantiate Class Attributes'''
        # Input Attributes
        self.url: str = url
        self.user_items: dict = user_items
        self.wikibase: dict =  wikibase
        self.dependency: dict= dependency
        # Working Attributes
        self.state: PayloadState = PayloadState()

    def _items_url(self):
        '''Get Item URL'''
        return f'{self.url}/w/rest.php/wikibase/v1/entities/items'

    def _statement_url(self, item):
        '''Get Statement URL'''
        return f'{self.url}/w/rest.php/wikibase/v1/entities/items/{item}/statements'

    def _alias_url(self, item):
        '''Get Alias URL'''
        return f'{self.url}/w/rest.php/wikibase/v1/entities/items/{item}/aliases/en'

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

    def _build_alias(self, alias):
        '''Build Alias Dictionary'''
        aliases_dict = {
          "aliases": alias
        }
        return aliases_dict

    def _normalize_aliases(self, aliases_dict: dict) -> list[str]:
        '''Convert Alias Dict to List'''
        return [
            a for _, a in sorted(aliases_dict.items())
            if isinstance(a, str) and a.strip()
        ]

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
            escaped_value = value.replace("'", "\\'")
            formatted_value = f"'{escaped_value}'"
        elif data_type == 'quantity':
            formatted_value = f"'{value}'^^<http://www.w3.org/2001/XMLSchema#decimal>"
        elif data_type == 'time':
            formatted_value = f"'{value}'^^<http://www.w3.org/2001/XMLSchema#dateTime>"
        elif data_type == 'monolingualtext':
            escaped_value = value.replace("'", "\\'")
            formatted_value = f"'{escaped_value}'@en"
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
        if not value:
            raise ValueError("Missing Item in Statement!")
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
        data_properties = self.wikibase['data_properties'](item_class)
        for prop in self.state.subject.get('Properties', {}).values():
            self.add_answer(
                verb=self.wikibase['properties']['instance of'],
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

    def add_aliases(self, aliases_dict):
        '''Add Aliases to Payload'''
        if not aliases_dict:
            return
        aliases_list = self._normalize_aliases(aliases_dict)
        # Add Aliases
        if (
            self.state.dictionary[self.state.subject_item]['id']
        ):
            self._add_alias(
                item = self.state.subject_item,
                aliases = aliases_list
            )
        else:
            self._add_to_item_alias(
                item = self.state.subject_item,
                aliases = aliases_list
            )

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
        ):
            self._add_relation(
                item=subject,
                statement=statement,
                qualifier=qualifier
            )
        else:
            if (isinstance(statement['value'], str) and pattern.match(statement['value'])):
                self.dependency[subject].add(statement['value'])
            self._add_to_item_statement(
                item=subject,
                statement=statement,
                qualifier=qualifier
            )

    def add_answers(self, mardmo_property, wikibase_property, datatype = 'string'):
        '''Add answer to Payload.'''
        for entry in self.state.subject.get(mardmo_property, {}).values():
            if not re.search(r"<math.*?</math>", entry, re.DOTALL): #IGNORE MATHML EXPORT UNTIL HANDLERS RE-WRITTEN FOR LATEX
                self.add_answer(
                    verb=self.wikibase['properties'][wikibase_property],
                    object_and_type=[
                        entry,
                        datatype,
                    ]
                )

    def add_single_relation(
        self,
        statement,
        alt_statement = None,
        qualifier = None,
        reverse = False
    ):
        '''Add single relation to payload.'''
        # Empty Qualifiers if none provided
        if qualifier is None:
            qualifier = []
        for entry in self.state.subject.get(statement['relatant'], {}).values():
            # Get Item Key
            entry_item = self.get_item_key(entry, 'object')
            if entry_item in self.state.dictionary:
                # Assign Object and Subject
                if reverse:
                    subject_item, object_item = entry_item, self.state.subject_item
                else:
                    subject_item, object_item = self.state.subject_item, entry_item
                # Add to Payload
                self.add_answer(
                    verb = statement['relation'],
                    object_and_type = [
                        object_item,
                        'wikibase-item',
                    ],
                    qualifier = qualifier,
                    subject = subject_item
                )
            else:
                # Add to Payload
                self.add_answer(
                    verb = alt_statement['relation'],
                    object_and_type = [
                        entry.get(alt_statement['relatant']),
                        'string',
                    ],
                    qualifier = qualifier
                )

    def add_multiple_relation(self, statement, optional_qualifier = None, reverse = False):
        '''Add multiple relations to payload.'''

        if optional_qualifier is None:
            optional_qualifier = []

        for key, prop in self.state.subject.get(statement['relation'], {}).items():
            for key2 in self.state.subject.get(statement['relatant'], {}).get(key, {}):
                # Get Item Key
                relatant_item = self.get_item_key(
                    self.state.subject.get(statement['relatant'], {}).get(key, {}).get(key2, {}),
                    'object'
                )

                # Set Up Qualifier
                qualifier = []

                # Add Formulation and Task Order Numbers to Qualifier
                if 'series ordinal' in optional_qualifier:
                    for number in ('formulation_number', 'task_number'):
                        if self.state.subject.get(number, {}).get(key, {}):
                            qualifier = self.add_qualifier(
                                self.wikibase['properties']['series ordinal'],
                                'string', 
                                self.state.subject[number][key]
                            )

                # Add Assumptions to Qualifier
                if 'assumes' in optional_qualifier:
                    if self.state.subject.get('assumption', {}).get(key, {}):
                        for assumption in self.state.subject['assumption'][key].values():
                            assumption_item = self.get_item_key(
                                assumption,
                                'object'
                            )
                            qualifier.extend(
                                self.add_qualifier(
                                    self.wikibase['properties']['assumes'],
                                    'wikibase-item',
                                    assumption_item
                                )
                            )

                # Add Roles to Qualifier
                if len(self.wikibase['relations'][prop]) == 2:
                    if self.wikibase['relations'][prop][1] not in ('forward', 'backward'):
                        qualifier.extend(
                            self.add_qualifier(
                                self.wikibase['properties']['object has role'],
                                'wikibase-item',
                                self.wikibase['relations'][prop][1]
                            )
                        )

                # Assign Object and Subject
                if reverse or self.wikibase['relations'][prop][-1] == 'backward':
                    subject_item, object_item = relatant_item, self.state.subject_item
                else:
                    subject_item, object_item = self.state.subject_item, relatant_item

                # Add to Payload
                self.add_answer(
                    verb = self.wikibase['relations'][prop][0],
                    object_and_type = [
                        object_item,
                        'wikibase-item',
                    ],
                    qualifier = qualifier,
                    subject = subject_item
                )

    def add_in_defining_formula(self):
        '''Add in defining formula Statement'''
        for element in self.state.subject.get('element', {}).values():
            if not re.search(r"<math.*?</math>", element.get('symbol', ''), re.DOTALL): #IGNORE MATHML EXPORT UNTIL HANDLERS RE-WRITTEN FOR LATEX
                # Get Item Key
                quantity_item = self.get_item_key(
                    element.get('quantity', {}),
                    'object'
                )
                # Add Quantity Qualifier
                qualifier = self.add_qualifier(
                    self.wikibase['properties']['symbol represents'],
                    'wikibase-item',
                    quantity_item
                )
                # Pattern of New Item
                pattern = re.compile(r"^Item\d{10}$")
                # Add Symbol to Payload
                if (
                    self.state.dictionary[self.state.subject_item]['id']
                    or self.state.subject_item == quantity_item
                ):
                    self._add_relation(
                        item = self.state.subject_item,
                        statement = {
                            'property_id': self.wikibase['properties']['in defining formula'],
                            'value': element.get('symbol', ''),
                            'datatype': 'math'
                        },
                        qualifier = qualifier
                    )
                else:
                    if (isinstance(quantity_item, str) and pattern.match(quantity_item)):
                        self.dependency[self.state.subject_item].add(quantity_item)
                    self.add_answer(
                        verb=self.wikibase['properties']['in defining formula'],
                        object_and_type=[
                            element.get('symbol', ''),
                            'math',
                        ],
                        qualifier=qualifier
                    )

    def _add_entry(self, key, value):
        '''Add Entry to Payload'''
        self.state.dictionary[key] = value

    def _add_to_item_alias(self, item, aliases):
        self.state.dictionary[item]['aliases'] = aliases

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

    def _add_alias(self, item, aliases):
        '''Add Alias to Item'''
        for alias in aliases:
            key = f"ALIAS{self.state.counter}"
            self.state.dictionary[key] = {
                'id': '',
                'url': self._alias_url(item),
                'payload': self._build_alias(
                    alias = [alias]
                )
            }
            self.state.counter += 1

    def add_item_payload(self):
        '''Add Payload String to Item'''
        for item_id, item_data in self.state.dictionary.items():
            # Check if Item in Payload
            if not item_id.startswith('Item'):
                continue
            # Extract Information
            label = item_data.get("label", "")
            description = item_data.get("description", "")
            aliases = item_data.get("aliases", "")
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
            if aliases:
                payload["item"]["aliases"] = {"en": aliases}
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
                    self.wikibase['properties']['Wikidata QID'],
                    'external-id',
                    value['ID'].split(':')[1]
                ]
            )
        if id_type == 'no author found':
            # Add ORCID ID Statement
            if value.get('orcid'):
                statements.append(
                    [
                        self.wikibase['properties']['ORCID iD'],
                        'external-id',
                        value['orcid']
                    ]
                )
            # Add zbMath ID Statement
            if value.get('zbmath'):
                statements.append(
                    [
                        self.wikibase['properties']['zbMATH author ID'],
                        'external-id',
                        value['zbmath']
                    ]
                )
            # If Authors has ID, add further Statements
            if statements:
                statements.append(
                    [
                        self.wikibase['properties']['instance of'],
                        'wikibase-item',
                        self.wikibase['items']['human']
                    ]
                )
                statements.append(
                    [
                        self.wikibase['properties']['MaRDI profile type'],
                        'wikibase-item',
                        self.wikibase['items']['Person']
                    ]
                )
        if id_type == 'no journal found':
            # Add ISSN ID Statement
            if value.get('issn'):
                statements.append(
                    [
                        self.wikibase['properties']['ISSN'],
                        'external-id',
                        value['issn']
                    ]
                )
            # Add further Statements
            statements.append(
                [
                    self.wikibase['properties']['instance of'],
                    'wikibase-item',
                    self.wikibase['items']['scientific journal']
                ]
            )
        return statements

    def process_items(self):
        """Process Items"""
        handlers = {
            'mardi': lambda key, value: 
                self._add_entry(
                    key,
                    self._build_item(
                        value['ID'].split(':')[1],
                        value['Name'],
                        value['Description'],
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
                        value['Description'],
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
