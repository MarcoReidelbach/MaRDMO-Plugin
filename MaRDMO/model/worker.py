from ..utils import get_data
from ..publication.worker import PublicationRetriever


def model_relations(instance, answers,mathmoddb):
    '''Function queries MathModDB to gather further Model Information
       and connects them with Information provided by the User'''
     
    inversePropertyMapping = get_data('model/data/inversePropertyMapping.json')
    options = get_data('data/options.json')

    # Flag all Tasks as unwanted by User in Workflow Documentation
    for key in answers['task']:
        answers['task'][key].update({'Include':False})
 
    # Research Field to Research Field Relations
    entityRelations(answers,'field','field','IntraClassRelation','IntraClassElement','RelationRF1','RF')
    
    # Research Field to Research Problem Relations
    entityRelations(answers,'problem','field','RP2RF','RFRelatant','RelationRF1','RF')

    # Research Problem to Research Problem Relations
    entityRelations(answers,'problem','problem','IntraClassRelation','IntraClassElement','RelationRP1','RP')
    
    # Convert Research Problems in additional Models
    entityRelations(answers,'model','problem','MM2RP','RPRelatant','RelationRP1','RP')
    
    # Add Mathematical Model to Mathematical Model Relations
    entityRelations(answers,'model','model','IntraClassRelation','IntraClassElement','RelationMM1','MM')

    # Add Mathematical Formulation to Mathematical Formulation Relations 1
    entityRelations(answers,'formulation','formulation','MF2MF','MFRelatant','RelationMF1','MF')

    # Add Mathematical Formulation to Mathematical Formulation Relations 2
    entityRelations(answers,'formulation','formulation','IntraClassRelation','IntraClassElement','RelationMF2','MF')
    
    # Add Mathematical Model to Mathematical Formulation Relations 1
    entityRelations(answers,'formulation','model','MF2MM','MMRelatant','RelationMM1','MM', 3)

    for _, task in answers['task'].items():
        # Extract MFRelatant from the task
        mf_relations = task.get('T2MF', {})
        mf_relatants = task.get('MFRelatant', {})
        for mf_relation, mf_relatant in zip(mf_relations.values(),mf_relatants.values()):
            # Parse the ID and Name from the MFRelatant string
            mf_id, mf_name = mf_relatant.split(' <|> ')
            # Check if the ID already exists in the formulation dict
            existing_entry = next((key for key, value in answers['formulation'].items() if value.get('ID') == mf_id), None)
            if existing_entry is not None:
                # Update the existing entry with the task details
                new_key = max(answers['formulation'][existing_entry].get('MF2T',{}).keys(), default=-1) + 1
                answers['formulation'][existing_entry].setdefault('MF2T',{}).update({new_key:inversePropertyMapping[mf_relation]})
                answers['formulation'][existing_entry].setdefault('TRelatant',{}).update({new_key:f"{task['ID']} <|> {task['Name']}"})
            else:
                # Create a new entry for the formulation
                new_key = max(answers['formulation'].keys(), default=-1) + 1
                answers['formulation'][new_key] = {
                    'ID': mf_id,
                    'Name': mf_name,
                    'MF2T': {0: inversePropertyMapping[mf_relation]},
                    'TRelatant': {0: f"{task['ID']} <|> {task['Name']}"}
                }

    # Add Task to Mathematical Formulation Relations 1
    entityRelations(answers,'formulation','task','MF2T','TRelatant','RelationT1','T', 3)

    # Add Quantity to Quantity Relations
    entityRelations(answers,'quantity','quantity','Q2Q','QRelatant','RelationQQ','QQK')
    
    # Add QuantityKind to QuantityKind Relations
    entityRelations(answers,'quantity','quantity','QK2QK','QKRelatant','RelationQKQK','QQK')

    # Add Quantity to QuantityKind Relations
    entityRelations(answers,'quantity','quantity','Q2QK','QKRelatant','RelationQQK','QQK')

    # Add QuantityKind to Quantity Relations
    entityRelations(answers,'quantity','quantity','QK2Q','QRelatant','RelationQKQ','QQK')
    
    # Add Quantity to Elements
    for key in answers['formulation']:
        for key2 in answers['formulation'][key].get('element',{}):
            
            if len(answers['formulation'][key]['element'][key2]['quantity'].split(' <|> ')) == 1:
                label = answers['formulation'][key]['element'][key2]['quantity']
                Id = ''
            elif len(answers['formulation'][key]['element'][key2]['quantity'].split(' <|> ')) >= 2:
                Id,label = answers['formulation'][key]['element'][key2]['quantity'].split(' <|> ')[:2]
            for k in answers['quantity']:
                if label.lower() == answers['quantity'][k]['Name'].lower():
                    if answers['quantity'][k]['QorQK'] == mathmoddb['Quantity']:
                        relatants = answers['quantity'][k].get('QKRelatant', {}).values()
                        relatantIDs = []
                        relatantLabels = []
                        for relatant in relatants:
                            relatantID, relatantLabel = relatant.split(' <|> ')
                            if relatantID.startswith('mathmoddb:'):
                                relatantIDs.append(relatantID)
                            else:
                                relatantIDs.append('-')
                            relatantLabels.append(relatantLabel)
                        answers['quantity'][k].update({'QKName':', '.join(relatantLabels),
                                                       'QKID':', '.join(relatantIDs)})    
                        answers['formulation'][key]['element'][key2].update(
                            {'Info': 
                                {'Name':answers['quantity'][k].get('Name',''),
                                 'Description':answers['quantity'][k].get('Description',''),
                                 'QID':answers['quantity'][k].get('ID','') if answers['quantity'][k].get('ID','') and answers['quantity'][k].get('ID','') != 'not found' else answers['quantity'][k].get('Reference','') if answers['quantity'][k].get('Reference','') else '', 
                                 'QKName':answers['quantity'][k].get('QKName',''),
                                 'QKID':answers['quantity'][k].get('QKID','')}
                            })
                    elif answers['quantity'][k]['QorQK'] == mathmoddb['QuantityKind']:
                        answers['formulation'][key]['element'][key2].update(
                            {'Info':
                                {'QKName':answers['quantity'][k].get('Name',''),
                                 'Description':answers['quantity'][k].get('Description',''),
                                 'QKID':answers['quantity'][k].get('ID','') if answers['quantity'][k].get('ID','') and answers['quantity'][k].get('ID','') != 'not found' else ''}
                            })
    
    # Add Definition to Quantities
    for key in answers.get('quantity',[]):
        for key2 in answers['formulation']:
            if answers['formulation'][key2].get('DefinedQuantity'):
                Id,label = answers['formulation'][key2]['DefinedQuantity'].split(' <|> ')[:2]
                if label == answers['quantity'][key]['Name']:
                    answers['quantity'][key].update({'MDef':answers['formulation'][key2]})

    # Add Mathematical Model to Task Relations
    entityRelations(answers,'task','model','T2MM','MMRelatant','RelationMM','MM')
        
    # Add Quantity / Quantity Kind to Task Relations
    entityRelations(answers,'task','quantity','T2Q','QRelatant','RelationQQK','QQK')
    
    # Add Task to Task Relations
    entityRelations(answers,'task','task','IntraClassRelation','IntraClassElement','RelationT','T')
    
    return answers

def entityRelations(data, fromIDX, toIDX, relationOld, entityOld, relationNew, enc, no=2):
    # Add relations between model entities
    label_to_index = {data[toIDX][k].get('Name'): idx for idx, k in enumerate(data.get(toIDX,{}))}
    for key in data.get(fromIDX, []):
        for key2 in data[fromIDX][key].get(relationOld, {}):
            if data[fromIDX][key][entityOld].get(key2):
                Id, label = data[fromIDX][key][entityOld][key2].split(' <|> ')[:2]
                if label in label_to_index:
                    idx = label_to_index[label]
                    if no == 2:
                        if [data[fromIDX][key][relationOld][key2], f'{enc}{idx+1}'] not in data[fromIDX][key].get(relationNew,{}).values():
                            data[fromIDX][key].setdefault(relationNew, {}).update({key2: [data[fromIDX][key][relationOld][key2], f'{enc}{idx+1}']})
                    else:
                        if [data[fromIDX][key][relationOld][key2], idx+1, f'{enc}{idx+1}'] not in data[fromIDX][key].get(relationNew,{}).values():
                            data[fromIDX][key].setdefault(relationNew, {}).update({key2: [data[fromIDX][key][relationOld][key2], idx+1, f'{enc}{idx+1}']})
                else:
                    if no == 2:
                        if [data[fromIDX][key][relationOld][key2], Id] not in data[fromIDX][key].get(relationNew,{}).values():
                            data[fromIDX][key].setdefault(relationNew, {}).update({key2: [data[fromIDX][key][relationOld][key2], Id]})
                    else:
                        if [data[fromIDX][key][relationOld][key2], Id, Id] not in data[fromIDX][key].get(relationNew,{}).values():
                            data[fromIDX][key].setdefault(relationNew, {}).update({key2: [data[fromIDX][key][relationOld][key2], Id, Id]})
    return