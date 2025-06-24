from .utils import mapEntityQuantity
from .constants import PREVIEW_RELATIONS, PREVIEW_MAP_GENERAL, PREVIEW_MAP_QUANTITY, get_Relations, get_DATA_PROPERTIES

from ..utils import GeneratePayload, entityRelations, get_mathmoddb, find_item, mapEntity, unique_items
from ..id import PROPERTIES, ITEMS


class prepareModel:

    mathmoddb = get_mathmoddb()

    def preview(answers):
        '''Function to establish relations between Model Documentation Data'''
        
        # Flag all Tasks as unwanted by User in Workflow Documentation
        for key in answers['task']:
            answers['task'][key].update({'Include':False})

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
                mapping = prepareModel.mathmoddb)

        return answers

    def export(data, url):

        items = unique_items(data)
        
        payload = GeneratePayload(url, items, get_Relations, get_DATA_PROPERTIES)

        # Add / Retrieve Components of Model Item
        for key, value in items.items():
            if value.get('ID'):
                # Item from MaRDI Portal
                if 'mardi:' in value['ID']:
                    _, id = value['ID'].split(':')
                    payload.add_entry('dictionary', key, payload.build_item(id, value['Name'], value['Description']))
                # Item from Wikidata
                elif 'wikidata:' in value['ID']:
                    _, id = value['ID'].split(':')
                    mardiID = find_item(value['Name'], value['Description'])
                    if mardiID:
                        payload.add_entry('lookup', (value['ID'], value['Name'], value['Description']), (f"mardi:{mardiID}", value['Name'], value['Description']))
                        payload.add_entry('dictionary', key, payload.build_item(mardiID, value['Name'], value['Description']))
                        payload.update_items(key, f"mardi:{mardiID}")
                    else:
                        payload.add_entry('dictionary', key, payload.build_item('', value['Name'], value['Description'], [[PROPERTIES['Wikidata QID'], 'external-id', id]]))
                # Item from MathAlgoDB KG
                elif 'mathalgodb' in value['ID']:
                    _, id = value['ID'].split(':')
                    mardiID = find_item(value['Name'], value['Description'])
                    if mardiID:
                        payload.add_entry('lookup', (value['ID'], value['Name'], value['Description']), (f"mardi:{mardiID}", value['Name'], value['Description']))
                        payload.add_entry('dictionary', key, payload.build_item(mardiID, value['Name'], value['Description']))
                        payload.update_items(key, f"mardi:{mardiID}")
                    else:
                        payload.add_entry('dictionary', key, payload.build_item('', value['Name'], value['Description']))
                        # No MathAlgoDB ID Property in Portal yet
                # Item defined by User (I)
                elif 'not found' in value['ID']:
                    mardiID = find_item(value['Name'], value['Description'])
                    if mardiID:
                        payload.add_entry('lookup', (value['ID'], value['Name'], value['Description']), (f"mardi:{mardiID}", value['Name'], value['Description']))
                        payload.add_entry('dictionary', key, payload.build_item(mardiID, value['Name'], value['Description']))
                        payload.update_items(key, f"mardi:{mardiID}")
                    else:
                        statement = []
                        if value.get('ISSN'):
                            statement = statement.extend([[PROPERTIES['ISSN'], 'external-id', value['ISSN']]])
                        payload.add_entry('dictionary', key, payload.build_item('', value['Name'], value['Description'], statement))
                # Item defined by User (II)
                elif 'no author found' in value['ID']:
                    mardiID = find_item(value['Name'], value['Description'])
                    if mardiID:
                        payload.add_entry('lookup', (value['ID'], value['Name'], value['Description']), (f"mardi:{mardiID}", value['Name'], value['Description']))
                        payload.add_entry('dictionary', key, payload.build_item(mardiID, value['Name'], value['Description']))
                        payload.update_items(key, f"mardi:{mardiID}")
                    else:
                        statement = []
                        if value.get('orcid'):
                            statement = statement.extend([[PROPERTIES['ORCID iD'], 'external-id', value['orcid']]])
                        if value.get('zbmath'):
                            statement = statement.extend([[PROPERTIES['zbMATH author ID'], 'external-id', value['zbmath']]])
                        if statement:
                            payload.add_entry('dictionary', key, payload.build_item('', value['Name'], value['Description'], statement))
                              
        for field in data.get('field', {}).values():

            # Continue if no ID exists
            if not field.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(field)

            # Add Class and Community
            payload.add_answer(PROPERTIES['instance of'], ITEMS['academic discipline'])
            payload.add_answer(PROPERTIES['community'], ITEMS['MathModDB'])
            
            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')
                    
            # Add Problem Relations (Backward)
            payload.add_backward_relation(data      = data.get('problem', {}).values(),
                                          relation  = PROPERTIES['contains'], 
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

            # Add Class and Community
            payload.add_answer(PROPERTIES['instance of'], ITEMS['research problem'])
            payload.add_answer(PROPERTIES['community'], ITEMS['MathModDB']) 

            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')

            # Add Model Relations (Backward)
            payload.add_backward_relation(data      = data.get('model', {}).values(), 
                                          relation  = PROPERTIES['modelled by'], 
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
            
            # Add Class and Community
            payload.add_answer(PROPERTIES['instance of'], ITEMS['mathematical model'])
            payload.add_answer(PROPERTIES['community'], ITEMS['MathModDB']) 

            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')

            # Add Data Properties
            payload.add_data_properties('model')
            
            # Add Mathematical Formulations
            payload.add_forward_relation_multiple('MM2MF', 'MFRelatant')
    
            # Add related Computational Tasks
            payload.add_forward_relation_single(PROPERTIES['used by'], 'TRelatant')
            
            # Add Intraclass Relations (For-/Backward)
            payload.add_intra_class_relation(relation = 'IntraClassRelation',
                                             relatant = 'IntraClassElement')
            
        for task in data.get('task', {}).values():

            # Continue if no ID exists
            if not task.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(task)
            
            # Add Class and Community
            payload.add_answer(PROPERTIES['instance of'], ITEMS['computational task'])
            payload.add_answer(PROPERTIES['community'], ITEMS['MathModDB'])

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
            
            # Add Class and Community
            payload.add_answer(PROPERTIES['instance of'], ITEMS['mathematical expression'])
            payload.add_answer(PROPERTIES['community'], ITEMS['MathModDB']) 

            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')

            # Add Data Properties
            payload.add_data_properties('equation')

            # Add defining Formulas to Mathematical Formulation
            payload.add_answers('Formula', 'defining formula')
            
            # Add Symbols and Quantities to Mathematical Formulation
            payload.add_in_defining_formula()
            
            # Add Quantities / Quantity Kinds
            payload.add_forward_relation_multiple('MF2MF', 'MFRelatant')

            # Add Intraclass Relations (For-/Backward)
            payload.add_intra_class_relation(relation = 'IntraClassRelation',
                                             relatant = 'IntraClassElement')
            
        for quantity in data.get('quantityxyz', {}).values():

            # Continue if no ID exists
            if not quantity.get('ID'):
                continue
            
            # Get Item Key
            payload.get_item_key(quantity)
            
            # Get Class of Quantity
            if quantity.get('QorQK') == prepareModel.mathmoddb['Quantity']:
                qclass = ITEMS['quantity']
                qtype = 'quantity'
            elif quantity.get('QorQK') == prepareModel.mathmoddb['QuantityKind']:
                qclass = ITEMS['kind of quantity']
                qtype = 'quantity kind'

            # Add Class and Community
            payload.add_answer(PROPERTIES['instance of'], qclass)
            payload.add_answer(PROPERTIES['community'], ITEMS['MathModDB'])

            # Add Detailed Description
            payload.add_answers('descriptionLong', 'description')

            # Add Data Properties
            payload.add_data_properties(qtype)

            # Add QUDT ID for Quantity Kind
            if quantity.get('reference') and qtype == 'quantity kind':
                payload.add_answer(PROPERTIES['QUDT quantity kind ID'], quantity['reference'][0][1], 'external-id')
           
            # Add defining Formulas to Mathematical Formulation
            payload.add_answers('Formula', 'defining formula')
            
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
                    payload.add_answer(PROPERTIES['instance of'], ITEMS['scholarly article'] if publication['entrytype'] == 'scholarly article' else ITEMS['publication'])
                # Add the Title of the Publication
                if publication.get('title'):
                    payload.add_answer(PROPERTIES['title'], {"text": publication['title'], "language": "en"}, 'monolingualtext')
                # Add the Volume of the Publication
                if publication.get('volume'):
                    payload.add_answer(PROPERTIES['volume'], publication['volume'], 'string')
                # Add the Issue of the Publication
                if publication.get('issue'):
                    payload.add_answer(PROPERTIES['issue'], publication['issue'], 'string')
                # Add the Page(s) of the Publication
                if publication.get('page'):
                    payload.add_answer(PROPERTIES['page(s)'], publication['page'], 'string')
                # Add the Date of the Publication
                if publication.get('date'):
                    payload.add_answer(PROPERTIES['publication date'], {"time":f"+{publication['date']}T00:00:00Z","precision":11,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"}, 'time')
                # Add the DOI of the Publication
                if publication.get('reference', {}).get(0):
                    payload.add_answer(PROPERTIES['DOI'], publication['reference'][0][1], 'external-id')
                
                # Add the Language of the Publication
                payload.add_forward_relation_single(PROPERTIES['language of work or name'], 'language')
                # Add the Journal of the Publication
                payload.add_forward_relation_single(PROPERTIES['published in'], 'journal')
                # Add the Authors of the Publication
                payload.add_forward_relation_single(PROPERTIES['author'], 'author', PROPERTIES['author name string'], 'Name')
                
            # Add relations to Entities of Mathematical Model
            payload.add_forward_relation_multiple('P2E', 'EntityRelatant', True)

        # Construct Item Payloads
        payload.add_item_payload()            
            
        return payload.get_dictionary('dictionary')
