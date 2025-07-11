from .getters import get_properties

class GeneratePayload:
    
    def __init__(self, url, items, RELATIONS = None, DATA_PROPERTIES = None):
        self.counter = 0
        self.dictionary = {}
        self.lookup = {}
        self.url = url
        self.items = items
        self.subject = None
        self.subject_item = None
        self.RELATIONS = RELATIONS
        self.DATA_PROPERTIES = DATA_PROPERTIES
        self.PROPERTIES = get_properties()

    def items_url(self):
        return f'{self.url}/w/rest.php/wikibase/v1/entities/items'

    def statement_url(self, item):
        return f'{self.url}/w/rest.php/wikibase/v1/entities/items/{item}/statements'
    
    def build_item(self, id, label, description, statements = None):
        if statements is None:
            statements = []
        return {'id': id, 'url': self.items_url(), 'label': label, 'description':  description, 'statements': statements}
        
    def build_statement(self, id, content, data_type = "wikibase-item", qualifiers = []):
        return {"statement": {"property": {"id": id, "data_type": data_type}, "value": {"type": "value", "content": content}, "qualifiers": qualifiers}}
    
    def build_relation_check_query(self):
        relation_keys = [k for k in self.dictionary.keys() if k.startswith('RELATION')]
        optional_blocks = []
        bind_blocks = []
        for idx, key in enumerate(relation_keys):
            entry = self.dictionary[key]
            url = entry['url']
            target_item_key = url.split('/')[-2]
            target_item_data = self.dictionary.get(target_item_key)
            if not target_item_data:
                continue
            target_item_id = target_item_data['id']
            statement = entry['payload']['statement']
            prop_id = statement['property']['id']
            value = statement['value']['content']
            data_type = statement['property']['data_type']
            if value in self.dictionary and 'id' in self.dictionary[value]:
                value = self.dictionary[value]['id']
            subject = f'wd:{target_item_id}'
            if data_type == 'wikibase-item':
                value_str = f'wd:{value}'
            elif data_type == 'string':
                value_str = f"'{value}'"
            elif data_type == 'quantity':
                value_str = f"'{value}'^^<http://www.w3.org/2001/XMLSchema#decimal>"
            elif data_type == 'time':
                value_str = f"'{value}'^^<http://www.w3.org/2001/XMLSchema#dateTime>"
            elif data_type == 'monolingualtext':
                value_str = f"'{value}'@en"
            elif data_type == 'math':
                escaped_value = value.replace('\"', '\\\"')
                value_str = f"'{escaped_value}'^^<http://www.w3.org/1998/Math/MathML>"
            else:
                value_str = f"'{value}'"
            qualifiers = statement.get('qualifiers', [])
            qual_triples = ''
            for q in qualifiers:
                q_prop = q['property']['id']
                q_value = q['value']['content']
                q_data_type = q['property']['data_type']
                if q_value in self.dictionary and 'id' in self.dictionary[q_value]:
                    q_value = self.dictionary[q_value]['id']
                if q_data_type == 'wikibase-item':
                    q_value_str = f'wd:{q_value}'
                elif q_data_type == 'string':
                    q_value_str = f"'{q_value}'"
                elif q_data_type == 'quantity':
                    q_value_str = f"'{q_value}'^^<http://www.w3.org/2001/XMLSchema#decimal>"
                elif q_data_type == 'time':
                    q_value_str = f"'{q_value}'^^<http://www.w3.org/2001/XMLSchema#dateTime>"
                elif q_data_type == 'monolingualtext':
                    q_value_str = f"'{q_value}'@en"
                elif q_data_type == 'math':
                    escaped_q_value = q_value.replace('\"', '\\\"')
                    q_value_str = f"'{escaped_q_value}'^^<http://www.w3.org/1998/Math/MathML>"
                else:
                    q_value_str = f"'{q_value}'"
                qual_triples += f'    ?statement{idx} pq:{q_prop} {q_value_str} .\n'
            optional_block = f'OPTIONAL {{\n  {subject} p:{prop_id} ?statement{idx} .\n  ?statement{idx} ps:{prop_id} {value_str} .\n{qual_triples if qualifiers else ""}}}'
            bind_block = f'BIND(BOUND(?statement{idx}) AS ?RELATION{idx})'
            optional_blocks.append(optional_block)
            bind_blocks.append(bind_block)
        query_body = '\n'.join(optional_blocks + bind_blocks)
        query = f'\nSELECT {" ".join([f"?RELATION{idx}" for idx in range(len(relation_keys))])} WHERE {{\n{query_body}\n}}'
        return query
    
    def update_items(self, key, value):
        self.items[key]['ID'] = value 

    def find_key_by_values(self, id_value, name_value, description_value):
        for key, values in self.items.items():
            if (values['ID'] == id_value and 
                values['Name'] == name_value and 
                values['Description'] == description_value):
                return key
        return None

    def get_dictionary(self, dictionary):
        # Get Target Dictionary
        target_dictionary = getattr(self, dictionary, None)
        return target_dictionary
    
    def get_item_key(self, value, role = 'subject'):
        # Check if Item has Name and Description
        if not value.get('Name') or not value.get('Description'):
            raise ValueError('All Items need to have a \'Name\' and \'Description\'!')
        # Check if Item has new ID
        value['ID'] = self.lookup.get((value['ID'], value['Name'], value['Description']), [''])[0] or value['ID']
        # Get Item Key
        if role == 'subject':
            self.subject = value
            self.subject_item = self.find_key_by_values(value['ID'], value['Name'], value['Description'])
        else:
            return self.find_key_by_values(value['ID'], value['Name'], value['Description'])

    def add_qualifier(self, id, data_type, content):
        return [{"property": {"id": id, "data_type": data_type},"value": {"type": "value","content": content}}]

    def add_data_properties(self, subDict_item_class):
        DATA_PROPERTIES = self.DATA_PROPERTIES(subDict_item_class)
        for prop in self.subject.get('Properties', {}).values():
            self.add_answer(self.PROPERTIES['instance of'], DATA_PROPERTIES[prop])

    def add_check_results(self, check):
        relation_keys = [k for k in self.dictionary.keys() if k.startswith('RELATION')]
        for idx, key in enumerate(relation_keys):
            exists_key = f'RELATION{idx}'
            exists_value = check[0].get(exists_key, {}).get('value', 'false')
            self.dictionary[key]['exists'] = exists_value

    def add_answer(self, predicate, object, object_type = 'wikibase-item', qualifier = None, subject = None):
        if subject is None:
            subject = self.subject_item
        if qualifier is None:
            qualifier = []
        if self.dictionary[self.subject_item]['id']:
            self.add_relation(subject, predicate, object, object_type, qualifier)
        else:
            self.add_to_item_statement(subject, predicate, object_type, object, qualifier)

    def add_answers(self, mardmo_property, wikibase_property, datatype = 'string'):
        for entry in self.subject.get(mardmo_property, {}).values():
            self.add_answer(self.PROPERTIES[wikibase_property], entry, datatype)

    def add_backward_relation(self, data, relation, relatants):
        for entry in data:
            for relatant in entry.get(relatants, {}).values():
                relatant_item = self.get_item_key(relatant, 'object')
                if self.subject_item == relatant_item:
                    entry_item = self.get_item_key(entry, 'object')
                    self.add_answer(relation, entry_item)

    def add_forward_relation_single(self, relation, relatant, alt_relation = None, prop = None, qualifier = []):
        for entry in self.subject.get(relatant, {}).values():
            # Get Item Key
            entry_item = self.get_item_key(entry, 'object')
            if entry_item in self.dictionary.keys():
                # Add Payload
                self.add_answer(relation, entry_item, 'wikibase-item', qualifier)
            else:
                # Add Payload
                self.add_answer(alt_relation, entry.get(prop), 'string', qualifier)
                
    def add_forward_relation_multiple(self, relation, relatant, reverse = False):
        for key, prop in self.subject.get(relation, {}).items():
            # Get Item Key
            relatant_item = self.get_item_key(self.subject.get(relatant,{}).get(key,{}), 'object')  
            # Get (optional) Order Number
            qualifier = []
            if self.subject.get('formulation_number'):
                qualifier = self.add_qualifier(self.PROPERTIES['series ordinal'], 'string', self.subject['formulation_number'][key])
            # Get potential Qualifier
            if len(self.RELATIONS()[prop]) == 2 and self.RELATIONS()[prop][1] != 'forward' and self.RELATIONS()[prop][1] != 'backward':
                qualifier.extend(self.add_qualifier(self.PROPERTIES['object has role'], 'wikibase-item', self.RELATIONS()[prop][1]))
            # Add Payload
            if not reverse:
                self.add_answer(self.RELATIONS()[prop][0], relatant_item, 'wikibase-item', qualifier)
            else:
                self.add_answer(self.RELATIONS()[prop][0], self.subject_item, 'wikibase-item', qualifier, relatant_item)
            
    def add_in_defining_formula(self):
        for element in self.subject.get('element', {}).values():
            # Get Item Key
            quantity_item = self.get_item_key(element.get('quantity', {}), 'object') 
            # Add Quantity Qualifier
            qualifier = self.add_qualifier(self.PROPERTIES['symbol represents'], 'wikibase-item', quantity_item)
            # Add Symbol to Payload
            if self.subject_item == quantity_item:
                self.add_relation(self.subject_item, self.PROPERTIES['in defining formula'], element.get('symbol', ''), 'math', qualifier)
            else:
                self.add_answer(self.PROPERTIES['in defining formula'], element.get('symbol', ''), 'math', qualifier)
            
    def add_entry(self, dictionary, key, value):
        target_dictionary = getattr(self, dictionary, None)
        target_dictionary[key] = value
        
    def add_to_item_statement(self, item_key, property_id, datatype, value, qualifier=None):
        if qualifier is None:
            qualifier = []
        self.dictionary[item_key]['statements'].append([property_id, datatype, value, qualifier])

    def add_relation(self, item, property, content, datatype='wikibase-item', qualifier=None):
        if qualifier is None:
            qualifier = []
        key = f"RELATION{self.counter}"
        self.dictionary[key] = {
            'id': '',
            'url': self.statement_url(item),
            'payload': self.build_statement(property, content, datatype, qualifier)
        }
        self.counter += 1

    def add_intra_class_relation(self, relation, relatant):
        for key, prop in self.subject.get(relation, {}).items():
            # Get Item Key
            subDict_relatant_item = self.get_item_key(self.subject.get(relatant, {}).get(key), 'object')
            # Add potential Qualifier
            qualifier = []
            if self.subject.get('assumption', {}).get(key):
                for assumption in self.subject['assumption'][key].values():
                    assumption_item = self.get_item_key(assumption, 'object')
                    qualifier.extend(self.add_qualifier(self.PROPERTIES['assumes'], 'wikibase-item', assumption_item))
            if self.subject.get('task_number', {}).get(key):
                qualifier.extend(self.add_qualifier(self.PROPERTIES['series ordinal'], self.subject['task_number'][key], 'string'))
            # Add Forward or Backward Relation
            if self.RELATIONS()[prop][1] == 'forward':
                self.add_answer(self.RELATIONS()[prop][0], subDict_relatant_item, 'wikibase-item', qualifier)
            elif self.RELATIONS()[prop][1] == 'backward':
                self.add_answer(self.RELATIONS()[prop][0], self.subject_item, 'wikibase-item', qualifier, subDict_relatant_item)

    def add_item_payload(self):
        for item_id, item_data in self.dictionary.items():
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
                PID, dtype, obj = s[0], s[1], s[2]
                qualifier = None
                if len(s) == 4:
                    qualifier = s[3]
                statement = {
                    "property": {"id": PID, "data_type": dtype},
                    "value": {"type": "value", "content": obj}
                }
                if qualifier:
                    statement["qualifiers"] = qualifier

                statements.setdefault(PID, []).append(statement)
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
        


