from .utils import mapEntryQuantity, restructureIntracClass
from .constants import REVERSE, RELATION_MAP

from ..utils import entityRelations, get_data, find_item, mapEntity, unique_items
from ..id_testwiki import PROPERTIES, ITEMS

from ..workflow.utils import add_item_relation, add_static_or_non_item_relation, add_qualifier, find_key_by_values, get_item_key, items_url, items_payload

def prepareModelPreview(answers, mathmoddb):
    '''Function to establish relations between Model Documentation Data'''
     
    # Flag all Tasks as unwanted by User in Workflow Documentation
    for key in answers['task']:
        answers['task'][key].update({'Include':False})

    # Mathematical Model to Research Problem Relations
    entityRelations(data =answers,
                    fromIDX = 'model',
                    toIDX = 'problem',
                    entityOld = 'RPRelatant',
                    entityNew = 'RelationRP',
                    enc = 'RP')
    
    # Mathematical Model to Mathematical Formulation Relations
    entityRelations(answers,'model','formulation','MM2MF','MFRelatant','RelationMF1','MF')

    # Mathematical Model to Task Relations
    entityRelations(data =answers,
                    fromIDX = 'model',
                    toIDX = 'task',
                    entityOld = 'TRelatant',
                    entityNew = 'RelationT',
                    enc = 'T')
    #entityRelations(answers,'model','task','MM2T','TRelatant','RelationT','T')
    
    # Mathematical Model to Mathematical Model Relations
    entityRelations(answers,'model','model','IntraClassRelation','IntraClassElement','RelationMM1','MM')

    # Mathematical Model Assumptions for specializes / specialized by Relations
    mapEntity(answers, 'model', 'formulation', 'assumption', 'assumptionMapped', 'MF')

    # Task to Formulation Relations
    entityRelations(answers,'task','formulation','T2MF','MFRelatant','RelationMF','MF')

    # Task to Quantity / Quantity KInd Relations
    entityRelations(answers,'task','quantity','T2Q','QRelatant','RelationQQK','QQK')
    
    # Task to Task Relations
    entityRelations(answers,'task','task','IntraClassRelation','IntraClassElement','RelationT','T')

    # Task Assumptions for specializes / specialized by Relations
    mapEntity(answers, 'task', 'formulation', 'assumption', 'assumptionMapped', 'MF')

    # Add Quantity to Elements
    mapEntryQuantity(answers, 'formulation', mathmoddb)

    # Add Mathematical Formulation to Mathematical Formulation Relations 1
    entityRelations(answers,'formulation','formulation','MF2MF','MFRelatant','RelationMF1','MF')

    # Add Mathematical Formulation to Mathematical Formulation Relations 2
    entityRelations(answers,'formulation','formulation','IntraClassRelation','IntraClassElement','RelationMF2','MF')
    
    # Formulation Assumptions for specializes / specialized by Relations
    mapEntity(answers, 'formulation', 'formulation', 'assumption', 'assumptionMapped', 'MF')

    # Add Quantity to Quantity Relations
    entityRelations(answers,'quantity','quantity','Q2Q','QRelatant','RelationQQ','QQK')
    
    # Add QuantityKind to QuantityKind Relations
    entityRelations(answers,'quantity','quantity','QK2QK','QKRelatant','RelationQKQK','QQK')

    # Add Quantity to QuantityKind Relations
    entityRelations(answers,'quantity','quantity','Q2QK','QKRelatant','RelationQQK','QQK')

    # Add QuantityKind to Quantity Relations
    entityRelations(answers,'quantity','quantity','QK2Q','QRelatant','RelationQKQ','QQK')

    # Add Quantity to Elements
    mapEntryQuantity(answers, 'quantity', mathmoddb)
    
    # Research Field to Research Field Relations
    entityRelations(answers,'field','field','IntraClassRelation','IntraClassElement','RelationRF1','RF')
    
    # Research Field to Research Problem Relations
    entityRelations(data =answers,
                    fromIDX = 'problem',
                    toIDX = 'field',
                    entityOld = 'RFRelatant',
                    entityNew = 'RelationRF',
                    enc = 'RF')

    # Research Problem to Research Problem Relations
    entityRelations(answers,'problem','problem','IntraClassRelation','IntraClassElement','RelationRP1','RP')

    # Add Publication to Entity Relations
    entityRelations(answers,'publication',['field', 'problem', 'model', 'formulation', 'quantity', 'task'],'P2E','EntityRelatant','RelationP',['RF', 'RP', 'MM', 'MF', 'QQK', 'T'])
    
    return answers

def prepareModelExport(data, url):

    # Load MathModDB Ontology Mapping
    mathmoddb = get_data('model/data/mapping.json')

    # Create an empty Payload Dictionary
    payload = {}
    old_new = {}
    rel_idx = 0
     
    items = unique_items(data)

    # Add / Retrieve Components of Interdisciplinary Workflow Item

    for key, value in items.items():
        if value.get('ID'):
            # Item from MaRDI Portal
            if 'mardi:' in value['ID']:
                _, id = value['ID'].split(':')
                payload.update({key:{'id': id, 'url': items_url(url), 'payload': items_payload(value['Name'], value['Description'])}})
            # Item from Wikidata
            elif 'wikidata:' in value['ID']:
                _, id = value['ID'].split(':')
                mardiID = find_item(value['Name'], value['Description'])
                if mardiID:
                    old_new.update({(value['ID'], value['Name'], value['Description']): (f"mardi:{mardiID}", value['Name'], value['Description'])})
                    value['ID'] = f"mardi:{mardiID}"
                    payload.update({key:{'id': mardiID, 'url': items_url(url), 'payload': ''}})
                else:
                    payload.update({key:{'id': '', 'url': items_url(url), 'payload': items_payload(value['Name'], value['Description'])}})
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, key, rel_idx, PROPERTIES['Wikidata QID'], id, 'external-id')
            # Item from MathAlgoDB KG
            elif 'mathalgodb' in value['ID']:
                _, id = value['ID'].split(':')
                mardiID = find_item(value['Name'], value['Description'])
                if mardiID:
                    old_new.update({(value['ID'], value['Name'], value['Description']): (f"mardi:{mardiID}", value['Name'], value['Description'])})
                    value['ID'] = f"mardi:{mardiID}"
                    payload.update({key:{'id': mardiID, 'url': items_url(url), 'payload': ''}})
                else:
                    payload.update({key:{'id': '', 'url': items_url(url), 'payload': items_payload(value['Name'], value['Description'])}})
                    # No MathAlgoDB ID Property in Portal yet
            # Item defined by User (I)
            elif 'not found' in value['ID']:
                mardiID = find_item(value['Name'], value['Description'])
                if mardiID:
                    old_new.update({(value['ID'], value['Name'], value['Description']): (f"mardi:{mardiID}", value['Name'], value['Description'])})
                    value['ID'] = f"mardi:{mardiID}"
                    payload.update({key:{'id': mardiID, 'url': items_url(url), 'payload': items_payload(value['Name'], value['Description'])}}) #''}})
                else:
                    payload.update({key:{'id': '', 'url': items_url(url), 'payload': items_payload(value['Name'], value['Description'])}})
                    if value.get('ISSN'):
                        payload, rel_idx = add_static_or_non_item_relation(url, payload, key, rel_idx, PROPERTIES['ISSN'], value['ISSN'], 'external-id')
            # Item defined by User (II)
            elif 'no author found' in value['ID']:
                mardiID = find_item(value['Name'], value['Description'])
                if mardiID:
                    old_new.update({(value['ID'], value['Name'], value['Description']): (f"mardi:{mardiID}", value['Name'], value['Description'])})
                    value['ID'] = f"mardi:{mardiID}"
                    payload.update({key:{'id': mardiID, 'url': items_url(url), 'payload': ''}})
                else:
                    if value.get('orcid') or value.get('zbmath'):
                        payload.update({key:{'id': '', 'url': items_url(url), 'payload': items_payload(value['Name'], value['Description'])}})
                        if value.get('orcid'):
                            payload, rel_idx = add_static_or_non_item_relation(url, payload, key, rel_idx, PROPERTIES['ORCID iD'], value['orcid'], 'external-id')
                        if value.get('zbmath'):
                            payload, rel_idx = add_static_or_non_item_relation(url, payload, key, rel_idx, PROPERTIES['zbMATH author ID'], value['zbmath'], 'external-id')
    
    for field in data.get('field', {}).values():
        
        # Continue if no ID exists
        if not field.get('ID'):
            continue
        
        # Get Item Key
        field_item = get_item_key(field, items, old_new)
        
        # Add instance and MathModDB community to MAIN Academic Discipline
        payload, rel_idx = add_static_or_non_item_relation(url, payload, field_item, rel_idx, PROPERTIES['instance of'], ITEMS['academic discipline'])
        payload, rel_idx = add_static_or_non_item_relation(url, payload, field_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])
        
        # Add instance and MathModDB community to RELATED Academic Disciplines
        for rel_field in field.get('IntraClassElement', {}).values():
            rel_field_item = get_item_key(rel_field, items, old_new)
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_field_item, rel_idx, PROPERTIES['instance of'], ITEMS['academic discipline'])
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_field_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])

        # Add relations to Research Problems
        for problem in data.get('problem', {}).values():
            for con_field in problem.get('RFRelatant', {}).values():
                #if old_new.get((con_field['ID'], con_field['Name'], con_field['Description'])):
                con_field_id, con_field_name, con_field_description = old_new.get((con_field['ID'], con_field['Name'], con_field['Description'])) or (con_field['ID'], con_field['Name'], con_field['Description'])
                if con_field_id == field['ID'] and con_field_name == field['Name'] and con_field_description == field['Description']:
                    #if old_new.get((problem['ID'], problem['Name'], problem['Description'])):
                    problem_id, problem_name, problem_description = old_new.get((problem['ID'], problem['Name'], problem['Description'])) or (problem['ID'], problem['Name'], problem['Description'])
                    problem_item = find_key_by_values(items, problem_id, problem_name, problem_description)
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, field_item, rel_idx, PROPERTIES['contains'], problem_item)
                    
        # Restructure IntraClass
        restructureIntracClass(field)
        
        # Add Forward Relations to Item
        for relation in ['specialized by', 'similar to']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = field.get(relation, {}).values(), 
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = field_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[relation])
            
        ## Add Backward Relations to Item
        for relation in ['specializes']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = field.get(relation, {}).values(),
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = field_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[REVERSE[relation]],
                                                 reverse = True)
    
    for problem in data.get('problem', {}).values():
        
        # Continue if no ID exists
        if not problem.get('ID'):
            continue
        
        # Get Item Key
        problem_item = get_item_key(problem, items, old_new)

        # Add instance and MathModDB community to MAIN Research Problem
        payload, rel_idx = add_static_or_non_item_relation(url, payload, problem_item, rel_idx, PROPERTIES['instance of'], ITEMS['research problem'])
        payload, rel_idx = add_static_or_non_item_relation(url, payload, problem_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])
        
        # Add instance and MathModDB community to RELATED Research Problems
        for rel_problem in problem.get('IntraClassElement', {}).values():
            rel_problem_item = get_item_key(rel_problem, items, old_new)
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_problem_item, rel_idx, PROPERTIES['instance of'], ITEMS['research problem'])
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_problem_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])    

        # Add relations to Mathematical Models
        for model in data.get('model', {}).values():
            for mod_problem in model.get('RPRelatant', {}).values():
                #if old_new.get((mod_problem['ID'], mod_problem['Name'], mod_problem['Description'])):
                mod_problem_id, mod_problem_name, mod_problem_description = old_new.get((mod_problem['ID'], mod_problem['Name'], mod_problem['Description'])) or (mod_problem['ID'], mod_problem['Name'], mod_problem['Description'])
                if mod_problem_id == problem['ID'] and mod_problem_name == problem['Name'] and mod_problem_description == problem['Description']:
                    #if old_new.get((model['ID'], model['Name'], model['Description'])):
                    model_id, model_name, model_description = old_new.get((model['ID'], model['Name'], model['Description'])) or (model['ID'], model['Name'], model['Description'])
                    model_item = find_key_by_values(items, model_id, model_name, model_description)
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, problem_item, rel_idx, PROPERTIES['modelled by'], model_item)

        # Restructure IntraClass
        restructureIntracClass(problem)
        
        # Add Forward Relations to Item
        for relation in ['specialized by', 'similar to']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = problem.get(relation, {}).values(), 
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = problem_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[relation])
            
        ## Add Backward Relations to Item
        for relation in ['specializes']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = problem.get(relation, {}).values(),
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = problem_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[REVERSE[relation]],
                                                 reverse = True)

    for model in data.get('model', {}).values():
        
        # Continue if no ID exists
        if not model.get('ID'):
            continue
        
        # Get Item Key
        model_item = get_item_key(model, items, old_new)

        # Add instance and MathModDB community to MAIN Mathematical Model
        payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['mathematical model'])
        payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])

        # Add instance and MathModDB community to RELATED Mathematical Models
        for rel_model in model.get('IntraClassElement', {}).values():
            rel_model_item = get_item_key(rel_model, items, old_new)
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_model_item, rel_idx, PROPERTIES['instance of'], ITEMS['mathematical model'])
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_model_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])

        # Add Properties to Mathematical Model
        for prop in model.get('Properties', {}).values():
            if prop == mathmoddb['isDeterministic']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['deterministic model'])
            elif prop == mathmoddb['isStochastic']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['probabilistic model'])
            elif prop == mathmoddb['isDimensionless']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['dimensionless model'])
            elif prop == mathmoddb['isDimensional']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['dimensional model'])
            elif prop == mathmoddb['isDynamic']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['dynamic model'])
            elif prop == mathmoddb['isStatic']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['static model'])
            elif prop == mathmoddb['isLinear']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['linear model'])
            elif prop == mathmoddb['isNotLinear']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['nonlinear model'])
            elif prop == mathmoddb['isSpaceContinuous']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-space model'])
            elif prop == mathmoddb['isSpaceDiscrete']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-space model'])
            elif prop == mathmoddb['isTimeContinuous']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-time model'])
            elif prop == mathmoddb['isTimeDiscrete']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-time model'])

        # Add related Mathematical Formulations
        for key, prop in model.get('MM2MF', {}).items():
            formulation_id, formulation_name, formulation_description = old_new.get((model.get('MFRelatant',{}).get(key,{}).get('ID'), model.get('MFRelatant',{}).get(key,{}).get('Name'), model.get('MFRelatant',{}).get(key,{}).get('Description'))) or (model.get('MFRelatant',{}).get(key,{}).get('ID'), model.get('MFRelatant',{}).get(key,{}).get('Name'), model.get('MFRelatant',{}).get(key,{}).get('Description'))
            formulation_item = find_key_by_values(items, formulation_id, formulation_name, formulation_description)    
            qualifier = []
            if prop == mathmoddb['assumes']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['assumes'], formulation_item)
            elif prop == mathmoddb['contains']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['contains'], formulation_item)
            elif prop == mathmoddb['containsBoundaryCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['boundary condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsConstraintCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['constraint']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsCouplingCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['coupling condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsInitialCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['initial condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsFinalCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['final condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)

        # Add related Computational Tasks
        for task in model.get('TRelatant', {}).values():
            task_id, task_name, task_description = old_new.get((task.get('ID'),task.get('Name'),task.get('Description'))) or (task.get('ID'),task.get('Name'),task.get('Description'))
            task_item = find_key_by_values(items, task_id, task_name, task_description)
            payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['used by'], task_item)

        # Restructure IntraClass
        restructureIntracClass(model)
        
        # Add Forward Relations to Item (without specialized by)
        for relation in ['approximated by', 'contains', 'discretized by', 'linearized by', 'similar to']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = model.get(relation, {}).values(), 
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = model_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[relation])
            
        ## Add Backward Relations to Item (without specializes)
        for relation in ['approximates', 'contained in', 'discretizes', 'linearizes']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = model.get(relation, {}).values(),
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = model_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[REVERSE[relation]],
                                                 reverse = True)
            
        ### Add Forward Relations (specialized by)
        for key, value in model.get('IntraClassRelation', {}).items():
            if value == mathmoddb['specializedBy']:
                # Use new ID if present
                model['IntraClassElement'][key]['ID'] = old_new.get((model['IntraClassElement'][key]['ID'], model['IntraClassElement'][key]['Name'], model['IntraClassElement'][key]['Description']), [''])[0] or model['IntraClassElement'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, model['IntraClassElement'][key]['ID'], model['IntraClassElement'][key]['Name'], model['IntraClassElement'][key]['Description'])                
                qualifier = []
                if model.get('assumption', {}).get(key):
                    for assumption in model['assumption'][key].values():
                        # Use new ID if present
                        assumption['ID'] = old_new.get((assumption['ID'], assumption['Name'], assumption['Description']), [''])[0] or assumption['ID']
                        # Get Entry Key
                        assumption_entry = find_key_by_values(items, assumption['ID'], assumption['Name'], assumption['Description'])
                        # Add to qualifier
                        qualifier.extend(add_qualifier(PROPERTIES['assumes'], assumption_entry))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, model_item, rel_idx, PROPERTIES['specialized by'], entry, 'wikibase-item', qualifier)

        ### Add Forward Relations (specialized by)
        for key, value in model.get('IntraClassRelation', {}).items():
            if value == mathmoddb['specializes']:
                # Use new ID if present
                model['IntraClassElement'][key]['ID'] = old_new.get((model['IntraClassElement'][key]['ID'], model['IntraClassElement'][key]['Name'], model['IntraClassElement'][key]['Description']), [''])[0] or model['IntraClassElement'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, model['IntraClassElement'][key]['ID'], model['IntraClassElement'][key]['Name'], model['IntraClassElement'][key]['Description'])                
                qualifier = []
                if model.get('assumption', {}).get(key):
                    for assumption in model['assumption'][key].values():
                        # Use new ID if present
                        assumption['ID'] = old_new.get((assumption['ID'], assumption['Name'], assumption['Description']), [''])[0] or assumption['ID']
                        # Get Entry Key
                        assumption_entry = find_key_by_values(items, assumption['ID'], assumption['Name'], assumption['Description'])
                        # Add to qualifier
                        qualifier.extend(add_qualifier(PROPERTIES['assumes'], assumption_entry))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, entry, rel_idx, PROPERTIES['specialized by'], model_item, 'wikibase-item', qualifier)

    for task in data.get('task', {}).values():
        
        # Continue if no ID exists
        if not task.get('ID'):
            continue
        
        # Get Item Key
        task_item = get_item_key(task, items, old_new)

        # Add instance and MathModDB community to MAIN Computational Task
        payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['instance of'], ITEMS['computational task'])
        payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])

        # Add instance and MathModDB community to RELATED Mathematical Models
        for rel_task in model.get('IntraClassElement', {}).values():
            rel_task_item = get_item_key(rel_task, items, old_new)
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_task_item, rel_idx, PROPERTIES['instance of'], ITEMS['computational task'])
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_task_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])

        # Add Properties to Computational Task
        for prop in task.get('Properties', {}).values():
            if prop == mathmoddb['isLinear']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['instance of'], ITEMS['linear task'])
            elif prop == mathmoddb['isNotLinear']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['instance of'], ITEMS['nonlinear task'])
            elif prop == mathmoddb['isSpaceContinuous']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-space task'])
            elif prop == mathmoddb['isSpaceDiscrete']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-space task'])
            elif prop == mathmoddb['isTimeContinuous']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-time task'])
            elif prop == mathmoddb['isTimeDiscrete']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-time task'])

        # Add related Mathematical Formulations
        for key, prop in task.get('T2MF', {}).items():
            formulation_id, formulation_name, formulation_description = old_new.get((task.get('MFRelatant',{}).get(key,{}).get('ID'), task.get('MFRelatant',{}).get(key,{}).get('Name'), task.get('MFRelatant',{}).get(key,{}).get('Description'))) or (task.get('MFRelatant',{}).get(key,{}).get('ID'), task.get('MFRelatant',{}).get(key,{}).get('Name'), task.get('MFRelatant',{}).get(key,{}).get('Description'))
            formulation_item = find_key_by_values(items, formulation_id, formulation_name, formulation_description)    
            qualifier = []
            if prop == mathmoddb['assumes']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['assumes'], formulation_item)
            elif prop == mathmoddb['contains']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], formulation_item)
            elif prop == mathmoddb['containsBoundaryCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['boundary condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsConstraintCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['constraint']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsCouplingCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['coupling condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsInitialCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['initial condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsFinalCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['final condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], formulation_item, 'wikibase-item', qualifier)

        # Add related Quantities and Quantity Kinds
        for key, prop in task.get('T2Q', {}).items():
            quantity_id, quantity_name, quantity_description = old_new.get((task.get('QRelatant',{}).get(key,{}).get('ID'), task.get('QRelatant',{}).get(key,{}).get('Name'), task.get('QRelatant',{}).get(key,{}).get('Description'))) or (task.get('QRelatant',{}).get(key,{}).get('ID'), task.get('QRelatant',{}).get(key,{}).get('Name'), task.get('QRelatant',{}).get(key,{}).get('Description'))
            quantity_item = find_key_by_values(items, quantity_id, quantity_name, quantity_description)    
            qualifier = []
            if prop == mathmoddb['containsInput']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['input']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], quantity_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsConstant']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['constant']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], quantity_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsObjective']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['objective function']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], quantity_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsOutput']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['output']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], quantity_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsParameter']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['parameter']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['contains'], quantity_item, 'wikibase-item', qualifier)
        
        # Restructure IntraClass
        restructureIntracClass(task)
        
        # Add Forward Relations to Item (without specialized by)
        for relation in ['approximated by', 'contains', 'discretized by', 'linearized by', 'similar to']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = task.get(relation, {}).values(), 
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = task_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[relation])
            
        ## Add Backward Relations to Item (without specializes)
        for relation in ['approximates', 'contained in', 'discretizes', 'linearizes']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = task.get(relation, {}).values(),
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = task_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[REVERSE[relation]],
                                                 reverse = True)
            
        ### Add Forward Relations (specialized by)
        for key, value in task.get('IntraClassRelation', {}).items():
            if value == mathmoddb['specializedBy']:
                # Use new ID if present
                task['IntraClassElement'][key]['ID'] = old_new.get((task['IntraClassElement'][key]['ID'], task['IntraClassElement'][key]['Name'], task['IntraClassElement'][key]['Description']), [''])[0] or task['IntraClassElement'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, task['IntraClassElement'][key]['ID'], task['IntraClassElement'][key]['Name'], task['IntraClassElement'][key]['Description'])                
                qualifier = []
                if task.get('assumption', {}).get(key):
                    for assumption in task['assumption'][key].values():
                        # Use new ID if present
                        assumption['ID'] = old_new.get((assumption['ID'], assumption['Name'], assumption['Description']), [''])[0] or assumption['ID']
                        # Get Entry Key
                        assumption_entry = find_key_by_values(items, assumption['ID'], assumption['Name'], assumption['Description'])
                        # Add to qualifier
                        qualifier.extend(add_qualifier(PROPERTIES['assumes'], assumption_entry))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, task_item, rel_idx, PROPERTIES['specialized by'], entry, 'wikibase-item', qualifier)

        ### Add Forward Relations (specialized by)
        for key, value in task.get('IntraClassRelation', {}).items():
            if value == mathmoddb['specializes']:
                # Use new ID if present
                task['IntraClassElement'][key]['ID'] = old_new.get((task['IntraClassElement'][key]['ID'], task['IntraClassElement'][key]['Name'], task['IntraClassElement'][key]['Description']), [''])[0] or task['IntraClassElement'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, task['IntraClassElement'][key]['ID'], task['IntraClassElement'][key]['Name'], task['IntraClassElement'][key]['Description'])                
                qualifier = []
                if task.get('assumption', {}).get(key):
                    for assumption in task['assumption'][key].values():
                        # Use new ID if present
                        assumption['ID'] = old_new.get((assumption['ID'], assumption['Name'], assumption['Description']), [''])[0] or assumption['ID']
                        # Get Entry Key
                        assumption_entry = find_key_by_values(items, assumption['ID'], assumption['Name'], assumption['Description'])
                        # Add to qualifier
                        qualifier.extend(add_qualifier(PROPERTIES['assumes'], assumption_entry))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, entry, rel_idx, PROPERTIES['specialized by'], task_item, 'wikibase-item', qualifier)

    for formulation in data.get('formulation', {}).values():
        
        # Continue if no ID exists
        if not formulation.get('ID'):
            continue
        
        # Get Item Key
        formulation_item = get_item_key(formulation, items, old_new)

        # Add instance and MathModDB community to MAIN Mathematical Formulation
        payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['mathematical expression'])
        payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])

        # Add instance and MathModDB community to RELATED Mathematical Formulations
        for rel_formulation in formulation.get('IntraClassElement', {}).values():
            rel_formulation_item = get_item_key(rel_formulation, items, old_new)
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['mathematical expression'])
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_formulation_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])

        # Add Properties to Mathematical Formulation
        for prop in formulation.get('Properties', {}).values():
            if prop == mathmoddb['isDeterministic']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['deterministic equation'])
            elif prop == mathmoddb['isStochastic']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['probabilistic equation'])
            elif prop == mathmoddb['isDimensionless']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['dimensionless equation'])
            elif prop == mathmoddb['isDimensional']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['dimensional equation'])
            elif prop == mathmoddb['isDynamic']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['dynamic equation'])
            elif prop == mathmoddb['isStatic']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['static equation'])
            elif prop == mathmoddb['isLinear']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['linear equation'])
            elif prop == mathmoddb['isNotLinear']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['nonlinear equation'])
            elif prop == mathmoddb['isSpaceContinuous']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-space equation'])
            elif prop == mathmoddb['isSpaceDiscrete']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-space equation'])
            elif prop == mathmoddb['isTimeContinuous']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-time equation'])
            elif prop == mathmoddb['isTimeDiscrete']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-time equation'])

        # Add defining Formulas to Mathematical Formulation
        for formula in formulation.get('Formula', {}).values():
            payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['defining formula'], formula, 'string')

        # Add Symbols and Quantities to Mathematical Formulation
        for element in formulation.get('element', {}).values():
            quantity_id, quantity_name, quantity_description = old_new.get((element.get('quantity', {}).get('ID'),element.get('quantity', {}).get('Name'),element.get('quantity', {}).get('Description'))) or (element.get('quantity', {}).get('ID'),element.get('quantity', {}).get('Name'),element.get('quantity', {}).get('Description'))
            quantity_item = find_key_by_values(items, quantity_id, quantity_name, quantity_description)
            qualifier = add_qualifier(PROPERTIES['symbol represents'], quantity_item)
            payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['in defining formula'], element.get('symbol', ''), 'string', qualifier)
            
        # Add related Mathematical Formulations
        for key, prop in formulation.get('MF2MF', {}).items():
            formulation_id, formulation_name, formulation_description = old_new.get((formulation.get('MFRelatant',{}).get(key,{}).get('ID'), formulation.get('MFRelatant',{}).get(key,{}).get('Name'), formulation.get('MFRelatant',{}).get(key,{}).get('Description'))) or (formulation.get('MFRelatant',{}).get(key,{}).get('ID'), formulation.get('MFRelatant',{}).get(key,{}).get('Name'), formulation.get('MFRelatant',{}).get(key,{}).get('Description'))
            rel_formulation_item = find_key_by_values(items, formulation_id, formulation_name, formulation_description)    
            qualifier = []
            if prop == mathmoddb['assumes']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['assumes'], rel_formulation_item)
            elif prop == mathmoddb['contains']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['contains'], rel_formulation_item)
            elif prop == mathmoddb['containsBoundaryCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['boundary condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['contains'], rel_formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsConstraintCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['constraint']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['contains'], rel_formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsCouplingCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['coupling condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['contains'], rel_formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsInitialCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['initial condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['contains'], rel_formulation_item, 'wikibase-item', qualifier)
            elif prop == mathmoddb['containsFinalCondition']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['final condition']))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['contains'], rel_formulation_item, 'wikibase-item', qualifier)

        # Restructure IntraClass
        restructureIntracClass(formulation)
        
        # Add Forward Relations to Item (without specialized by)
        for relation in ['approximated by', 'discretized by', 'linearized by', 'nondimensionalized by', 'similar to']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = formulation.get(relation, {}).values(), 
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = formulation_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[relation])
            
        ## Add Backward Relations to Item (without specializes)
        for relation in ['approximates', 'discretizes', 'linearizes', 'nondimensionalizes']:
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = formulation.get(relation, {}).values(),
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = formulation_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES[REVERSE[relation]],
                                                 reverse = True)
            
        ### Add Forward Relations (specialized by)
        for key, value in formulation.get('IntraClassRelation', {}).items():
            if value == mathmoddb['specializedBy']:
                # Use new ID if present
                formulation['IntraClassElement'][key]['ID'] = old_new.get((formulation['IntraClassElement'][key]['ID'], formulation['IntraClassElement'][key]['Name'], formulation['IntraClassElement'][key]['Description']), [''])[0] or formulation['IntraClassElement'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, formulation['IntraClassElement'][key]['ID'], formulation['IntraClassElement'][key]['Name'], formulation['IntraClassElement'][key]['Description'])                
                qualifier = []
                if formulation.get('assumption', {}).get(key):
                    for assumption in formulation['assumption'][key].values():
                        # Use new ID if present
                        assumption['ID'] = old_new.get((assumption['ID'], assumption['Name'], assumption['Description']), [''])[0] or assumption['ID']
                        # Get Entry Key
                        assumption_entry = find_key_by_values(items, assumption['ID'], assumption['Name'], assumption['Description'])
                        # Add to qualifier
                        qualifier.extend(add_qualifier(PROPERTIES['assumes'], assumption_entry))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, formulation_item, rel_idx, PROPERTIES['specialized by'], entry, 'wikibase-item', qualifier)

        ### Add Forward Relations (specialized by)
        for key, value in formulation.get('IntraClassRelation', {}).items():
            if value == mathmoddb['specializes']:
                # Use new ID if present
                formulation['IntraClassElement'][key]['ID'] = old_new.get((formulation['IntraClassElement'][key]['ID'], formulation['IntraClassElement'][key]['Name'], formulation['IntraClassElement'][key]['Description']), [''])[0] or formulation['IntraClassElement'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, formulation['IntraClassElement'][key]['ID'], formulation['IntraClassElement'][key]['Name'], formulation['IntraClassElement'][key]['Description'])                
                qualifier = []
                if formulation.get('assumption', {}).get(key):
                    for assumption in formulation['assumption'][key].values():
                        # Use new ID if present
                        assumption['ID'] = old_new.get((assumption['ID'], assumption['Name'], assumption['Description']), [''])[0] or assumption['ID']
                        # Get Entry Key
                        assumption_entry = find_key_by_values(items, assumption['ID'], assumption['Name'], assumption['Description'])
                        # Add to qualifier
                        qualifier.extend(add_qualifier(PROPERTIES['assumes'], assumption_entry))
                payload, rel_idx = add_static_or_non_item_relation(url, payload, entry, rel_idx, PROPERTIES['specialized by'], formulation_item, 'wikibase-item', qualifier)

    for quantity in data.get('quantity', {}).values():
        
        # Continue if no ID exists
        if not quantity.get('ID'):
            continue
        
        # Get Item Key
        quantity_item = get_item_key(quantity, items, old_new)

        # Add instance and MathModDB community to MAIN Quantity / Quantity Kind
        if quantity.get('QorQK') == mathmoddb['Quantity']:
            payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['quantity'])
        elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
            payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['kind of quantity'])
        payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])

        # Add instance and MathModDB community to RELATED Mathematical Formulations
        for rel_quantity in quantity.get('IntraClassElement', {}).values():
            rel_quantity_item = get_item_key(rel_quantity, items, old_new)
            payload, rel_idx = add_static_or_non_item_relation(url, payload, rel_quantity_item, rel_idx, PROPERTIES['community'], ITEMS['MathModDB'])

        # Add Properties to Quantity / Quantity Kind
        for prop in quantity.get('Properties', {}).values():
            if prop == mathmoddb['isChemicalConstant']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['chemical constant'])
            elif prop == mathmoddb['isMathematicalConstant']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['mathematical constant'])
            elif prop == mathmoddb['isPhysicalConstant']:
                payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['physical constant'])
            elif prop == mathmoddb['isDeterministic']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['deterministic quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['deterministic quantity kind'])
            elif prop == mathmoddb['isStochastic']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['probabilistic quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['probabilistic quantity kind'])
            elif prop == mathmoddb['isDimensionless']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['dimensionless quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['dimensionless quantity kind'])
            elif prop == mathmoddb['isDimensional']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['dimensional quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['dimensional quantity kind'])
            elif prop == mathmoddb['isDynamic']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['dynamic quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['dynamic quantity kind'])
            elif prop == mathmoddb['isStatic']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['static quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['static quantity kind'])
            elif prop == mathmoddb['isSpaceContinuous']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-space quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-space quantity kind'])
            elif prop == mathmoddb['isSpaceDiscrete']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-space quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-space quantity kind'])
            elif prop == mathmoddb['isTimeContinuous']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-time quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['continuous-time quantity kind'])
            elif prop == mathmoddb['isTimeDiscrete']:
                if quantity.get('QorQK') == mathmoddb['Quantity']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-time quantity'])
                elif quantity.get('QorQK') == mathmoddb['QuantityKind']:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['instance of'], ITEMS['discrete-time quantity kind'])

        # Add QUDT ID for Quantity Kind
        if quantity.get('QorQK') == mathmoddb['QuantityKind'] and quantity.get('reference'):
            payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['QUDT quantity kind ID'], quantity['reference'][0][1])

        # Add defining Formulas to Quantity or Quantity Kind
        for formula in quantity.get('Formula', {}).values():
            payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['defining formula'], formula, 'string')

        # Add Symbols and Quantities to Mathematical Formulation
        for element in quantity.get('element', {}).values():
            quantity_id, quantity_name, quantity_description = old_new.get((element.get('quantity', {}).get('ID'),element.get('quantity', {}).get('Name'),element.get('quantity', {}).get('Description'))) or (element.get('quantity', {}).get('ID'),element.get('quantity', {}).get('Name'),element.get('quantity', {}).get('Description'))
            rel_quantity_item = find_key_by_values(items, quantity_id, quantity_name, quantity_description)
            qualifier = add_qualifier(PROPERTIES['symbol represents'], rel_quantity_item)
            payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES['in defining formula'], element.get('symbol', ''), 'string', qualifier)

        ### Add Forward Relations (Q2Q)
        for key, value in quantity.get('Q2Q', {}).items():
            if value == mathmoddb['approximatedBy'] or value == mathmoddb['discretizedBy'] or value == mathmoddb['nondimensionalizedBy'] or value == mathmoddb['similarTo'] or value == mathmoddb['specializedBy']:
                # Use new ID if present
                quantity['QRelatant'][key]['ID'] = old_new.get((quantity['QRelatant'][key]['ID'], quantity['QRelatant'][key]['Name'], quantity['QRelatant'][key]['Description']), [''])[0] or quantity['QRelatant'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, quantity['QRelatant'][key]['ID'], quantity['QRelatant'][key]['Name'], quantity['QRelatant'][key]['Description'])                
                payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES[RELATION_MAP[value]], entry, 'wikibase-item')

        ### Add Forward Relations (Q2Q)
        for key, value in quantity.get('Q2Q', {}).items():
            if value == mathmoddb['approximates'] or value == mathmoddb['discretizes'] or value == mathmoddb['nondimensionalizes'] or value == mathmoddb['specializes']:
                # Use new ID if present
                quantity['QRelatant'][key]['ID'] = old_new.get((quantity['QRelatant'][key]['ID'], quantity['QRelatant'][key]['Name'], quantity['QRelatant'][key]['Description']), [''])[0] or quantity['QRelatant'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, quantity['QRelatant'][key]['ID'], quantity['QRelatant'][key]['Name'], quantity['QRelatant'][key]['Description'])                
                payload, rel_idx = add_static_or_non_item_relation(url, payload, entry, rel_idx, PROPERTIES[REVERSE[RELATION_MAP[value]]], quantity_item, 'wikibase-item')

        ### Add Forward Relations (Q2QK)
        for key, value in quantity.get('Q2QK', {}).items():
            if value == mathmoddb['specializedBy']:
                # Use new ID if present
                quantity['QKRelatant'][key]['ID'] = old_new.get((quantity['QKRelatant'][key]['ID'], quantity['QKRelatant'][key]['Name'], quantity['QKRelatant'][key]['Description']), [''])[0] or quantity['QKRelatant'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, quantity['QKRelatant'][key]['ID'], quantity['QKRelatant'][key]['Name'], quantity['QKRelatant'][key]['Description'])                
                payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES[RELATION_MAP[value]], entry, 'wikibase-item')

        ### Add Forward Relations (Q2QK)
        for key, value in quantity.get('Q2QK', {}).items():
            if value == mathmoddb['specializes']:
                # Use new ID if present
                quantity['QKRelatant'][key]['ID'] = old_new.get((quantity['QKRelatant'][key]['ID'], quantity['QKRelatant'][key]['Name'], quantity['QKRelatant'][key]['Description']), [''])[0] or quantity['QKRelatant'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, quantity['QKRelatant'][key]['ID'], quantity['QKRelatant'][key]['Name'], quantity['QKRelatant'][key]['Description'])                
                payload, rel_idx = add_static_or_non_item_relation(url, payload, entry, rel_idx, PROPERTIES[REVERSE[RELATION_MAP[value]]], quantity_item, 'wikibase-item')

        ### Add Forward Relations (QK2QK)
        for key, value in quantity.get('QK2QK', {}).items():
            if value == mathmoddb['discretizedBy'] or value == mathmoddb['nondimensionalizedBy'] or value == mathmoddb['similarTo']:
                # Use new ID if present
                quantity['QKRelatant'][key]['ID'] = old_new.get((quantity['QKRelatant'][key]['ID'], quantity['QKRelatant'][key]['Name'], quantity['QKRelatant'][key]['Description']), [''])[0] or quantity['QKRelatant'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, quantity['QKRelatant'][key]['ID'], quantity['QKRelatant'][key]['Name'], quantity['QKRelatant'][key]['Description'])                
                payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES[RELATION_MAP[value]], entry, 'wikibase-item')

        ### Add Forward Relations (QK2QK)
        for key, value in quantity.get('QK2QK', {}).items():
            if value == mathmoddb['discretizes'] or value == mathmoddb['nondimensionalizes']:
                # Use new ID if present
                quantity['QKRelatant'][key]['ID'] = old_new.get((quantity['QKRelatant'][key]['ID'], quantity['QKRelatant'][key]['Name'], quantity['QKRelatant'][key]['Description']), [''])[0] or quantity['QKRelatant'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, quantity['QKRelatant'][key]['ID'], quantity['QKRelatant'][key]['Name'], quantity['QKRelatant'][key]['Description'])                
                payload, rel_idx = add_static_or_non_item_relation(url, payload, entry, rel_idx, PROPERTIES[REVERSE[RELATION_MAP[value]]], quantity_item, 'wikibase-item')

        ### Add Forward Relations (QK2Q)
        for key, value in quantity.get('QK2Q', {}).items():
            if value == mathmoddb['specializedBy']:
                # Use new ID if present
                quantity['QRelatant'][key]['ID'] = old_new.get((quantity['QRelatant'][key]['ID'], quantity['QRelatant'][key]['Name'], quantity['QRelatant'][key]['Description']), [''])[0] or quantity['QRelatant'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, quantity['QRelatant'][key]['ID'], quantity['QRelatant'][key]['Name'], quantity['QRelatant'][key]['Description'])                
                payload, rel_idx = add_static_or_non_item_relation(url, payload, quantity_item, rel_idx, PROPERTIES[RELATION_MAP[value]], entry, 'wikibase-item')

        ### Add Forward Relations (QK2Q)
        for key, value in quantity.get('QK2Q', {}).items():
            if value == mathmoddb['specializes']:
                # Use new ID if present
                quantity['QRelatant'][key]['ID'] = old_new.get((quantity['QRelatant'][key]['ID'], quantity['QRelatant'][key]['Name'], quantity['QRelatant'][key]['Description']), [''])[0] or quantity['QRelatant'][key]['ID']
                # Get Entry Key
                entry = find_key_by_values(items, quantity['QRelatant'][key]['ID'], quantity['QRelatant'][key]['Name'], quantity['QRelatant'][key]['Description'])                
                payload, rel_idx = add_static_or_non_item_relation(url, payload, entry, rel_idx, PROPERTIES[REVERSE[RELATION_MAP[value]]], quantity_item, 'wikibase-item')

    for publication in data.get('publication', {}).values():
        
        # Continue if no ID exists
        if not publication.get('ID'):
            continue

        # Get Item Key
        publication_item = get_item_key(publication, items, old_new)
        
        if 'mardi' not in publication['ID'] and 'wikidata' not in publication['ID']:
            # Add the class of the Publication
            if publication.get('entrytype'):
                payload, rel_idx = add_static_or_non_item_relation(url, payload, publication_item, rel_idx, PROPERTIES['instance of'], ITEMS['scholarly article'] if publication['entrytype'] == 'scholarly article' else ITEMS['publication'])
            # Add the Title of the Publication
            if publication.get('title'):
                payload, rel_idx = add_static_or_non_item_relation(url, payload, publication_item, rel_idx, PROPERTIES['title'], {"text": publication['title'], "language": "en"}, 'monolingualtext')
            # Add the Volume of the Publication
            if publication.get('volume'):
                payload, rel_idx = add_static_or_non_item_relation(url, payload, publication_item, rel_idx, PROPERTIES['volume'], publication['volume'], 'string')
            # Add the Issue of the Publication
            if publication.get('issue'):
                payload, rel_idx = add_static_or_non_item_relation(url, payload, publication_item, rel_idx, PROPERTIES['issue'], publication['issue'], 'string')
            # Add the Page(s) of the Publication
            if publication.get('page'):
                payload, rel_idx = add_static_or_non_item_relation(url, payload, publication_item, rel_idx, PROPERTIES['page(s)'], publication['page'], 'string')
            # Add the Date of the Publication
            if publication.get('date'):
                payload, rel_idx = add_static_or_non_item_relation(url, payload, publication_item, rel_idx, PROPERTIES['publication date'], {"time":f"+{publication['date']}T00:00:00Z","precision":11,"calendarmodel":"http://www.wikidata.org/entity/Q1985727"}, 'time')
            # Add the DOI of the Publication
            if publication.get('reference', {}).get(0):
                payload, rel_idx = add_static_or_non_item_relation(url, payload, publication_item, rel_idx, PROPERTIES['DOI'], publication['reference'][0][1], 'external-id')
            
            # Add the Language of the Publication
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = publication.get('language', {}).values(), 
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = publication_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES['language of work or name'])
            # Add the Journal of the Publication
            payload, rel_idx = add_item_relation(url = url,
                                                 payload = payload, 
                                                 values = publication.get('journal', {}).values(), 
                                                 lookup = old_new, 
                                                 items = items, 
                                                 item = publication_item, 
                                                 idx = rel_idx, 
                                                 property = PROPERTIES['published in'])
            # Add the Authors of the Publication
            for entry in publication.get('author', {}).values():
                # Continue if no ID exists
                if not entry.get('ID'):
                    continue
                # Get Item Key
                entry_item = get_item_key(entry, items, old_new)
                # Add to Payload
                if entry_item in payload.keys():
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, publication_item, rel_idx, PROPERTIES['author'], entry_item)
                else:
                    payload, rel_idx = add_static_or_non_item_relation(url, payload, publication_item, rel_idx, PROPERTIES['author name string'], entry['Name'], 'string')

        # Add relations to Entities of Mathematical Model
        for key, value in publication.get('P2E', {}).items():
            
            qualifier = []
            if value == mathmoddb['documents']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['documentation']))
            elif value == mathmoddb['invents']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['invention']))
            elif value == mathmoddb['studies']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['study']))
            elif value == mathmoddb['surveys']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['review']))
            elif value == mathmoddb['uses']:
                qualifier.extend(add_qualifier(PROPERTIES['object has role'], ITEMS['use']))

            # Use new ID if present
            publication['EntityRelatant'][key]['ID'] = old_new.get((publication['EntityRelatant'][key]['ID'], publication['EntityRelatant'][key]['Name'], publication['EntityRelatant'][key]['Description']), [''])[0] or publication['EntityRelatant'][key]['ID']
            # Get Entry Key
            entry = find_key_by_values(items, publication['EntityRelatant'][key]['ID'], publication['EntityRelatant'][key]['Name'], publication['EntityRelatant'][key]['Description'])                

            payload, rel_idx = add_static_or_non_item_relation(url, payload, entry, rel_idx, PROPERTIES['described by source'], publication_item, 'wikibase-item', qualifier)
        
    return payload
