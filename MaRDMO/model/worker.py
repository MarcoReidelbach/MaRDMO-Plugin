from .utils import mapEntityQuantity
from .constants import PREVIEW_RELATIONS, PREVIEW_MAP_GENERAL, PREVIEW_MAP_QUANTITY, get_Relations, get_DATA_PROPERTIES

from ..config import endpoint
from ..getters import get_items, get_mathmoddb, get_properties
from ..helpers import entityRelations, mapEntity, unique_items
from ..queries import query_sparql
from ..payload import GeneratePayload


class prepareModel:

    def __init__(self):

        self.mathmoddb = get_mathmoddb()
        self.ITEMS = get_items()
        self.PROPERTIES = get_properties()

    def preview(self, answers):
        '''Function to establish relations between Model Documentation Data'''
        
        # Prepare Relations for Preview
        for relation in PREVIEW_RELATIONS:
            entityRelations(
                data = answers,
                fromIDX = relation[0],
                toIDX = relation[1],
                relationOld = relation[2],
                entityOld = relation[3],
                entityNew = relation[4],
                enc = relation[5],
                forder = relation[6],
                torder = relation[7]
            )

        # Prepare General Mappings
        for mapping in PREVIEW_MAP_GENERAL:
            mapEntity(
                data = answers, 
                fromIDX = mapping[0], 
                toIDX = mapping[1], 
                entityOld = mapping[2], 
                entityNew = mapping[3], 
                enc = mapping[4]
            )
        
        # Prepare Quantity Mapping
        for mapping in PREVIEW_MAP_QUANTITY:
            mapEntityQuantity(
                data= answers, 
                type = mapping, 
                mapping = self.mathmoddb)
        
        return answers

    def export(self, data, url):

        items = unique_items(data)
        
        payload = GeneratePayload(url, items, get_Relations, get_DATA_PROPERTIES)
        
        # Add / Retrieve Components of Model Item
        payload.process_items()
        
        for field in data.get('field', {}).values():

            # Continue if no ID exists
            if not field.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(field)

            # Add Class
            payload.add_answer(
                verb=self.PROPERTIES['instance of'],
                object_and_type=[
                    self.ITEMS['academic discipline'],
                    'wikibase-item',
                ]
            )

            # Add Community
            payload.add_answer(
                verb=self.PROPERTIES['community'],
                object_and_type=[
                    self.ITEMS['MathModDB'],
                    'wikibase-item',
                ]
            )
            
            # Add MaRDI Research Field Profile
            payload.add_answer(
                verb=self.PROPERTIES['MaRDI profile type'],
                object_and_type=[
                    self.ITEMS['MaRDI research field profile'],
                    'wikibase-item',
                ]
            )
            
            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')
                    
            # Add Problem Relations (Backward)
            payload.add_backward_relation(data      = data.get('problem', {}).values(),
                                          relation  = self.PROPERTIES['contains'], 
                                          relatants = 'RFRelatant')
                            
            # Add Intraclass Relations (For-/Backward)
            payload.add_intra_class_relation(relation = 'IntraClassRelation',
                                             relatant = 'IntraClassElement')

        for problem in data.get('problem', {}).values():

            # Continue if no ID exists
            if not problem.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(problem)

            # Add Class
            payload.add_answer(
                verb=self.PROPERTIES['instance of'],
                object_and_type=[
                    self.ITEMS['research problem'],
                    'wikibase-item',
                ]
            )

            # Add Community
            payload.add_answer(
                verb=self.PROPERTIES['community'],
                object_and_type=[
                    self.ITEMS['MathModDB'],
                    'wikibase-item',
                ]
            )
            
            # Add MaRDI Research Field Profile
            payload.add_answer(
                verb=self.PROPERTIES['MaRDI profile type'],
                object_and_type=[
                    self.ITEMS['MaRDI research problem profile'],
                    'wikibase-item',
                ]
            )

            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')

            # Add Model Relations (Backward)
            payload.add_backward_relation(data      = data.get('model', {}).values(), 
                                          relation  = self.PROPERTIES['modelled by'], 
                                          relatants = 'RPRelatant')

            # Add Intraclass Relations (For-/Backward)
            payload.add_intra_class_relation(relation = 'IntraClassRelation',
                                             relatant = 'IntraClassElement')

        for model in data.get('model', {}).values():

            # Continue if no ID exists
            if not model.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(model)

            # Add Class
            payload.add_answer(
                verb=self.PROPERTIES['instance of'],
                object_and_type=[
                    self.ITEMS['mathematical model'],
                    'wikibase-item',
                ]
            )

            # Add Community
            payload.add_answer(
                verb=self.PROPERTIES['community'],
                object_and_type=[
                    self.ITEMS['MathModDB'],
                    'wikibase-item',
                ]
            )
            
            # Add MaRDI Research Field Profile
            payload.add_answer(
                verb=self.PROPERTIES['MaRDI profile type'],
                object_and_type=[
                    self.ITEMS['MaRDI model profile'],
                    'wikibase-item',
                ]
            )
            
            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')

            # Add Data Properties
            payload.add_data_properties('model')
            
            # Add Mathematical Formulations
            payload.add_forward_relation_multiple('MM2MF', 'MFRelatant')
    
            # Add related Computational Tasks
            payload.add_forward_relation_single(self.PROPERTIES['used by'], 'TRelatant')
            
            # Add Intraclass Relations (For-/Backward)
            payload.add_intra_class_relation(relation = 'IntraClassRelation',
                                             relatant = 'IntraClassElement')
            
        for task in data.get('task', {}).values():

            # Continue if no ID exists
            if not task.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(task)

            # Add Class
            payload.add_answer(
                verb=self.PROPERTIES['instance of'],
                object_and_type=[
                    self.ITEMS['computational task'],
                    'wikibase-item',
                ]
            )

            # Add Community
            payload.add_answer(
                verb=self.PROPERTIES['community'],
                object_and_type=[
                    self.ITEMS['MathModDB'],
                    'wikibase-item',
                ]
            )
            
            # Add MaRDI Research Field Profile
            payload.add_answer(
                verb=self.PROPERTIES['MaRDI profile type'],
                object_and_type=[
                    self.ITEMS['MaRDI task profile'],
                    'wikibase-item',
                ]
            )
            
            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')

            # Add Data Properties
            payload.add_data_properties('task')

            # Add Mathematical Formulations
            payload.add_forward_relation_multiple('T2MF', 'MFRelatant')

            # Add Quantities / Quantity Kinds
            payload.add_forward_relation_multiple('T2Q', 'QRelatant')

            # Add Intraclass Relations (For-/Backward)
            payload.add_intra_class_relation(relation = 'IntraClassRelation',
                                             relatant = 'IntraClassElement')

        for formulation in data.get('formulation', {}).values():

            # Continue if no ID exists
            if not formulation.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(formulation)

            # Add Class
            payload.add_answer(
                verb=self.PROPERTIES['instance of'],
                object_and_type=[
                    self.ITEMS['mathematical expression'],
                    'wikibase-item',
                ]
            )

            # Add Community
            payload.add_answer(
                verb=self.PROPERTIES['community'],
                object_and_type=[
                    self.ITEMS['MathModDB'],
                    'wikibase-item',
                ]
            )
            
            # Add MaRDI Research Field Profile
            payload.add_answer(
                verb=self.PROPERTIES['MaRDI profile type'],
                object_and_type=[
                    self.ITEMS['MaRDI formula profile'],
                    'wikibase-item',
                ]
            )

            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')

            # Add Data Properties
            payload.add_data_properties('equation')

            # Add defining Formulas to Mathematical Formulation
            payload.add_answers('Formula', 'defining formula', 'math')
            
            # Add Symbols and Quantities to Mathematical Formulation
            payload.add_in_defining_formula()
            
            # Add Quantities / Quantity Kinds
            payload.add_forward_relation_multiple('MF2MF', 'MFRelatant')

            # Add Intraclass Relations (For-/Backward)
            payload.add_intra_class_relation(relation = 'IntraClassRelation',
                                             relatant = 'IntraClassElement')
            
        for quantity in data.get('quantity', {}).values():

            # Continue if no ID exists
            if not quantity.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(quantity)
            
            # Get Class of Quantity
            if quantity.get('QorQK') == self.mathmoddb['Quantity']:
                qclass = self.ITEMS['quantity']
                qtype = 'quantity'
            elif quantity.get('QorQK') == self.mathmoddb['QuantityKind']:
                qclass = self.ITEMS['kind of quantity']
                qtype = 'quantity kind'

            # Add Class
            payload.add_answer(
                verb=self.PROPERTIES['instance of'],
                object_and_type=[
                    qclass,
                    'wikibase-item',
                ]
            )

            # Add Community
            payload.add_answer(
                verb=self.PROPERTIES['community'],
                object_and_type=[
                    self.ITEMS['MathModDB'],
                    'wikibase-item',
                ]
            )
            
            # Add MaRDI Research Field Profile
            payload.add_answer(
                verb=self.PROPERTIES['MaRDI profile type'],
                object_and_type=[
                    self.ITEMS['MaRDI quantity profile'],
                    'wikibase-item',
                ]
            )

            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')

            # Add Data Properties
            payload.add_data_properties(qtype)

            # Add QUDT ID for Quantity Kind
            if quantity.get('reference') and qtype == 'quantity kind':
                payload.add_answer(
                    verb=self.PROPERTIES['QUDT quantity kind ID'],
                    object_and_type=[
                        quantity['reference'][0][1],
                        'external-id',
                    ]
                )
            
            # Add defining Formulas to Mathematical Formulation
            payload.add_answers('Formula', 'defining formula', 'math')
            
            # Add Symbols and Quantities to Mathematical Formulation
            payload.add_in_defining_formula()

            # Add Intraclass Relations
            if qtype == 'quantity':
                # Quantity to Quantity
                payload.add_intra_class_relation(relation = 'Q2Q',
                                                 relatant = 'QRelatant')
                # Quantity to Quantity Kind
                payload.add_intra_class_relation(relation = 'Q2QK',
                                                 relatant = 'QKRelatant')
            elif qtype == 'quantity kind':
                # Quantity to Quantity
                payload.add_intra_class_relation(relation = 'QK2QK',
                                                 relatant = 'QKRelatant')
                # Quantity to Quantity Kind
                payload.add_intra_class_relation(relation = 'QK2Q',
                                                 relatant = 'QRelatant')

        for publication in data.get('publication', {}).values():

            # Continue if no ID exists
            if not publication.get('ID'):
                continue

            # Get Item Key
            payload.get_item_key(publication)

            if 'mardi' not in publication['ID'] and 'wikidata' not in publication['ID']:
                
                # Add the class of the Publication
                if publication.get('entrytype'):

                    if publication['entrytype'] == 'scholarly article':
                        pclass = self.ITEMS['scholarly article']
                    else:
                        pclass = self.ITEMS['publication']

                    payload.add_answer(
                        verb=self.PROPERTIES['instance of'],
                        object_and_type=[
                            pclass,
                            'wikibase-item',
                        ]
                    )
               
                # Add the Title of the Publication
                if publication.get('title'):

                    payload.add_answer(
                        verb=self.PROPERTIES['title'],
                        object_and_type=[
                            {"text": publication['title'], "language": "en"},
                            'monolingualtext',
                        ]
                    )

                # Add the Volume of the Publication
                if publication.get('volume'):

                    payload.add_answer(
                        verb=self.PROPERTIES['volume'],
                        object_and_type=[
                            publication['volume'],
                            'string',
                        ]
                    )

                # Add the Issue of the Publication
                if publication.get('issue'):

                    payload.add_answer(
                        verb=self.PROPERTIES['issue'],
                        object_and_type=[
                            publication['issue'],
                            'string',
                        ]
                    )

                # Add the Page(s) of the Publication
                if publication.get('page'):

                    payload.add_answer(
                        verb=self.PROPERTIES['page(s)'],
                        object_and_type=[
                            publication['page'],
                            'string',
                        ]
                    )

                # Add the Date of the Publication
                if publication.get('date'):

                    payload.add_answer(
                        verb=self.PROPERTIES['publication date'],
                        object_and_type=[
                            {"time":f"+{publication['date']}T00:00:00Z","precision":11,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"},
                            'time',
                        ]
                    )

                # Add the DOI of the Publication
                if publication.get('reference', {}).get(0):

                    payload.add_answer(
                        verb=self.PROPERTIES['DOI'],
                        object_and_type=[
                            publication['reference'][0][1],
                            'external-id',
                        ]
                    )
                
                # Add the Language of the Publication
                payload.add_forward_relation_single(self.PROPERTIES['language of work or name'], 'language')
                # Add the Journal of the Publication
                payload.add_forward_relation_single(self.PROPERTIES['published in'], 'journal')
                # Add the Authors of the Publication
                payload.add_forward_relation_single(self.PROPERTIES['author'], 'author', self.PROPERTIES['author name string'], 'Name')

                # Add the Profile Type
                payload.add_answer(
                        verb=self.PROPERTIES['MaRDI profile type'],
                        object_and_type=[
                            self.ITEMS['MaRDI publication profile'],
                            'wikibase-item',
                        ]
                    )
                
            # Add relations to Entities of Mathematical Model
            payload.add_forward_relation_multiple('P2E', 'EntityRelatant', True)

        # Construct Item Payloads
        payload.add_item_payload()  
        
        # If Relations are added, check if they exist
        if any(key.startswith('RELATION') for key in payload.get_dictionary('dictionary')):

            # Generate SPARQL Check Query
            query = payload.build_relation_check_query()
            
            # Perform Check Query for Relations
            check = query_sparql(query, endpoint['mardi']['sparql'])

            # Add Check Results
            payload.add_check_results(check)
            
        return payload.get_dictionary('dictionary')
