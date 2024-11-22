import os, json

from .utils import find_item

def ModelRetriever(answers,mathmoddb):
    '''Function queries MathModDB to gather further Model Information
       and connects them with Information provided by the User'''
     
    path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
    with open(path, "r") as json_file:
        option = json.load(json_file)
    
    path = os.path.join(os.path.dirname(__file__), 'data', 'inversePropertyMapping.json')
    with open(path, "r") as json_file:
        inversePropertyMapping = json.load(json_file)
    
    # Flag all Tasks as unwanted by User in Workflow Documentation
    for key in answers['Task']:
        answers['Task'][key].update({'Include':False})
 
    # Get MathModID of all selected Entities
    #for className in ['ResearchField', 'ResearchProblem', 'Task', 'MathematicalFormulation', 'MathematicalModel', 'Quantity']:
    #    mathmodidToKey[className] = {answers[className][key].get('ID').split(':')[1]: key for key in answers[className]}

    # Get additional Publication Information from MathModDB

    #tClass = 'PublicationModel'
    #
    #search_string = searchGenerator(answers,['ResearchField','ResearchProblem','MathematicalModel','Quantity','Task'])
    #results = query_sparql(queryModelDocumentation[tClass].format(search_string))
    #
    #for result in results:
    #    # Get MathModID and Class of queries entity
    #    mathmodid, qClass = result['Item']['value'].split(' >|< ')
    #
    #    t = mathmodid.split('#')
    #    if len(t) == 2:
    #        mathmodid = t[1]
#
    #    # Queried entity in Selection?
    #    if mathmodid in mathmodidToKey[qClass]:
    #        key = mathmodidToKey[qClass][mathmodid]
    #        for relation in publicationRelations:
    #            assignComplexEntityRelations(qClass, tClass, relation, ['P2E','EntityRelatant'], result, key, answers, mathmoddb, inversePropertyMapping)

    # Research Field to Research Field Relations
    entityRelations(answers,'ResearchField','ResearchField','IntraClassRelation','IntraClassElement','RelationRF1','RF')
    
    # Research Field to Research Problem Relations
    entityRelations(answers,'ResearchProblem','ResearchField','RP2RF','RFRelatant','RelationRF1','RF')

    # Research Problem to Research Problem Relations
    entityRelations(answers,'ResearchProblem','ResearchProblem','IntraClassRelation','IntraClassElement','RelationRP1','RP')
    
    # Convert Research Problems in additional Models
    entityRelations(answers,'MathematicalModel','ResearchProblem','MM2RP','RPRelatant','RelationRP1','RP')
    
    # Add Information to main Mathematical Model
    for key2 in answers['Models']:
        if answers['Models'][key2].get('MathModID') and answers['Models'][key2]['MathModID'] != 'not in MathModDB':
            for key in answers['MathematicalModel']:
                if answers['Models'][key2]['MathModID'] == answers['MathematicalModel'][key].get('MathModID'):
                    Name = answers['MathematicalModel'][key]['Name']
                    Description = answers['MathematicalModel'][key]['Description']
                    Properties = answers['MathematicalModel'][key]['Properties']
                    mardiID = find_item(Name,Description)
                    if mardiID:
                        answers['Models'][key2].update({'ID':f"mardi:{mardiID}", 'Name':Name, 'Description':Description, 'Properties':Properties})
                    else:
                        answers['Models'][key2].update({'ID':None, 'Name':Name, 'Description':Description, 'Properties':Properties})
        else:
            for key in answers['MathematicalModel']:
                if answers['MathematicalModel'][key].get('Main') == option['Yes']:
                    Name = answers['MathematicalModel'][key]['Name']
                    Description = answers['MathematicalModel'][key]['Description']
                    Properties = answers['MathematicalModel'][key].get('Properties')
                    mardiID = find_item(Name,Description)
                    if mardiID:
                        answers['Models'][key2].update({'ID':f"mardi:{mardiID}", 'Name':Name, 'Description':Description, 'Properties':Properties})
                    else:
                        answers['Models'][key2].update({'ID':None, 'Name':Name, 'Description':Description, 'Properties':Properties})
    
    # Add Mathematical Model to Mathematical Model Relations
    entityRelations(answers,'MathematicalModel','MathematicalModel','IntraClassRelation','IntraClassElement','RelationMM1','MM')

    # Add Mathematical Formulation to Mathematical Formulation Relations 1
    entityRelations(answers,'MathematicalFormulation','MathematicalFormulation','MF2MF','MFRelatant','RelationMF1','MF')

    # Add Mathematical Formulation to Mathematical Formulation Relations 2
    entityRelations(answers,'MathematicalFormulation','MathematicalFormulation','IntraClassRelation','IntraClassElement','RelationMF2','MF')
    
    # Add Mathematical Model to Mathematical Formulation Relations 1
    entityRelations(answers,'MathematicalFormulation','MathematicalModel','MF2MM','MMRelatant','RelationMM1','MM', 3)

    for _, task in answers['Task'].items():
        # Extract MFRelatant from the task
        mf_relations = task.get('T2MF', {})
        mf_relatants = task.get('MFRelatant', {})
        for mf_relation, mf_relatant in zip(mf_relations.values(),mf_relatants.values()):
            # Parse the ID and Name from the MFRelatant string
            mf_id, mf_name = mf_relatant.split(' <|> ')
            # Check if the ID already exists in the formulation dict
            existing_entry = next((key for key, value in answers['MathematicalFormulation'].items() if value.get('ID') == mf_id), None)
            if existing_entry is not None:
                # Update the existing entry with the task details
                new_key = max(answers['MathematicalFormulation'][existing_entry].get('MF2T',{}).keys(), default=-1) + 1
                answers['MathematicalFormulation'][existing_entry].setdefault('MF2T',{}).update({new_key:inversePropertyMapping[mf_relation]})
                answers['MathematicalFormulation'][existing_entry].setdefault('TRelatant',{}).update({new_key:f"{task['ID']} <|> {task['Name']}"})
            else:
                # Create a new entry for the formulation
                new_key = max(answers['MathematicalFormulation'].keys(), default=-1) + 1
                answers['MathematicalFormulation'][new_key] = {
                    'ID': mf_id,
                    'Name': mf_name,
                    'MF2T': {0: inversePropertyMapping[mf_relation]},
                    'TRelatant': {0: f"{task['ID']} <|> {task['Name']}"}
                }

    # Add Task to Mathematical Formulation Relations 1
    entityRelations(answers,'MathematicalFormulation','Task','MF2T','TRelatant','RelationT1','T', 3)

    # Add Quantity to Quantity Relations
    entityRelations(answers,'Quantity','Quantity','Q2Q','QRelatant','RelationQQ','QQK')
    
    # Add QuantityKind to QuantityKind Relations
    entityRelations(answers,'Quantity','Quantity','QK2QK','QKRelatant','RelationQKQK','QQK')

    # Add Quantity to QuantityKind Relations
    entityRelations(answers,'Quantity','Quantity','Q2QK','QKRelatant','RelationQQK','QQK')

    # Add QuantityKind to Quantity Relations
    entityRelations(answers,'Quantity','Quantity','QK2Q','QRelatant','RelationQKQ','QQK')
    
    # Add Quantity to Elements
    for key in answers['MathematicalFormulation']:
        for key2 in answers['MathematicalFormulation'][key].get('Element',{}):
            
            if len(answers['MathematicalFormulation'][key]['Element'][key2]['Quantity'].split(' <|> ')) == 1:
                label = answers['MathematicalFormulation'][key]['Element'][key2]['Quantity']
                Id = ''
            elif len(answers['MathematicalFormulation'][key]['Element'][key2]['Quantity'].split(' <|> ')) >= 2:
                Id,label = answers['MathematicalFormulation'][key]['Element'][key2]['Quantity'].split(' <|> ')[:2]
            for k in answers['Quantity']:
                if label.lower() == answers['Quantity'][k]['Name'].lower():
                    if answers['Quantity'][k]['QorQK'] == mathmoddb['Quantity']:
                        relatants = answers['Quantity'][k].get('QKRelatant', {}).values()
                        relatantIDs = []
                        relatantLabels = []
                        for relatant in relatants:
                            relatantID, relatantLabel = relatant.split(' <|> ')
                            if relatantID.startswith('mathmoddb:'):
                                relatantIDs.append(relatantID)
                            else:
                                relatantIDs.append('-')
                            relatantLabels.append(relatantLabel)
                        answers['Quantity'][k].update({'QKName':', '.join(relatantLabels),
                                                       'QKID':', '.join(relatantIDs)})    
                        answers['MathematicalFormulation'][key]['Element'][key2].update(
                            {'Info': 
                                {'Name':answers['Quantity'][k].get('Name',''),
                                 'Description':answers['Quantity'][k].get('Description',''),
                                 'QID':answers['Quantity'][k].get('ID','') if answers['Quantity'][k].get('ID','') and answers['Quantity'][k].get('ID','') != 'not found' else answers['Quantity'][k].get('Reference','') if answers['Quantity'][k].get('Reference','') else '', 
                                 'QKName':answers['Quantity'][k].get('QKName',''),
                                 'QKID':answers['Quantity'][k].get('QKID','')}
                            })
                    elif answers['Quantity'][k]['QorQK'] == mathmoddb['QuantityKind']:
                        answers['MathematicalFormulation'][key]['Element'][key2].update(
                            {'Info':
                                {'QKName':answers['Quantity'][k].get('Name',''),
                                 'Description':answers['Quantity'][k].get('Description',''),
                                 'QKID':answers['Quantity'][k].get('ID','') if answers['Quantity'][k].get('ID','') and answers['Quantity'][k].get('ID','') != 'not found' else ''}
                            })

    # Add Definition to Quantities
    for key in answers.get('Quantity',[]):
        for key2 in answers['MathematicalFormulation']:
            if answers['MathematicalFormulation'][key2].get('DefinedQuantity'):
                print(answers['MathematicalFormulation'][key2].get('DefinedQuantity'))
                Id,label = answers['MathematicalFormulation'][key2]['DefinedQuantity'].split(' <|> ')[:2]
                if label == answers['Quantity'][key]['Name']:
                    answers['Quantity'][key].update({'MDef':answers['MathematicalFormulation'][key2]})

    # Add Mathematical Model to Task Relations
    entityRelations(answers,'Task','MathematicalModel','T2MM','MMRelatant','RelationMM','MM')
        
    # Add Quantity / Quantity Kind to Task Relations
    entityRelations(answers,'Task','Quantity','T2Q','QRelatant','RelationQQK','QQK')
    
    # Add Task to Task Relations
    entityRelations(answers,'Task','Task','IntraClassRelation','IntraClassElement','RelationT','T')

    # Add Entities to Publication Relations
    for key in answers['PublicationModel']:
        for key2 in answers['PublicationModel'][key].get('P2E',{}):
            Id,label,kind,abbr = answers['PublicationModel'][key]['EntityRelatant'][key2].split(' <|> ')
            for idx, k in enumerate(answers[kind]):
                if label == answers[kind][k]['Name']:
                    answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['P2E'][key2],f"{abbr}{str(idx+1)}"]})
            if not answers['PublicationModel'][key].get('RelationP',{}).get(key2):
                answers['PublicationModel'][key].setdefault('RelationP',{}).update({key2:[answers['PublicationModel'][key]['P2E'][key2],Id]})
    
    return answers

def entityRelations(data, fromIDX, toIDX, relationOld, entityOld, relationNew, enc, no=2):
    # Add relations between model entities
    label_to_index = {data[toIDX][k]['Name']: idx for idx, k in enumerate(data.get(toIDX,{}))}
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

def searchGenerator(data, class_list):
    """
    Generates a search string for SPARQL queries.

    Parameters:
        data (dict): The data structure containing relevant information.
        class_list (list): The list of keys to look up in the data.

    Returns:
        str: The generated search string.
    """
    search_string = ""

    for key in class_list:
        for key2 in data[key]:
            math_mod_id = data[key][key2].get('ID')
            if math_mod_id and math_mod_id != 'not found':
                search_string += f" :{math_mod_id.split(':')[1]}"
    
    return search_string

def assignComplexEntityRelations(qClass, tClass, qrel, trel_values, r, key, answers, mathmoddb=None, inversePropertyMapping=None):

    # Retrieve values for the current kind of class
    values1 = r.get(qrel, {}).get('value')

    if not values1:
        return  # Exit if values are missing

    # Split values into a list of entities
    entities = values1.split(' <|> ')

    # Existing entries in the target class
    existing_entries = {v.get('MathModID'): k for k, v in answers[tClass].items()}

    if tClass == 'PublicationModel':
        current = f"{answers[qClass][key]['ID']} <|> {answers[qClass][key]['Name']} <|> {qClass} <|> {''.join(filter(str.isupper, qClass))}"
    else:
        current = f"{answers[qClass][key]['ID']} <|> {answers[qClass][key]['Name']}"

    # Track the next available key in the target class
    next_available_key = max(answers[tClass].keys(), default=-1) + 1

    for idx, entity in enumerate(entities):

        # Get Id and label of the entity
        entitySplit = entity.split(' >|< ')

        # Update qrel in source entity if not present
        if f"{entitySplit[0]} <|> {entitySplit[1]}" not in answers[qClass][key].setdefault(qrel, {}).values():
            answers[qClass][key][qrel].update({f"{qrel}{idx}": f"{entitySplit[0]} <|> {entitySplit[1]}"})

        if entitySplit[0] in existing_entries:
            tkey = existing_entries[entitySplit[0]]

            if len(trel_values) == 2:
                # Check if New relation pair is not already present
                newPair = (inversePropertyMapping[mathmoddb[qrel]], current)
                existingPairs = set(zip(answers[tClass][tkey].setdefault(trel_values[0], {}).values(), answers[tClass][tkey].setdefault(trel_values[1], {}).values()))

            if len(trel_values) != 2 or newPair not in existingPairs:
                # Update relations in target class entity
                for i, trel in enumerate(trel_values):
                    if i == len(trel_values) - 1: 
                        # Related Element
                        new_inner_key = max(answers[tClass][tkey].setdefault(trel, {}).keys(), default=-1) + 1
                        answers[tClass][tkey][trel][new_inner_key] = current
                    else:
                        # Relation Kind
                        if mathmoddb and inversePropertyMapping:
                            new_inner_key = max(answers[tClass][tkey].setdefault(trel, {}).keys(), default=-1) + 1
                            answers[tClass][tkey][trel].update({
                                new_inner_key: inversePropertyMapping[mathmoddb[qrel]]
                            })
        else:
            # Add a new entity entry if it does not exist
            if tClass == 'Quantity':
                answers[tClass][next_available_key] = {'MathModID': entitySplit[0], 'Name': entitySplit[1], 'QorQK': mathmoddb[f'{entitySplit[2]}Class']}
            elif tClass == 'ResearchField':
                answers[tClass][next_available_key] = {'MathModID': entitySplit[0], 'Name': entitySplit[1], 'Description': entitySplit[2]}
            else:
                answers[tClass][next_available_key] = {'MathModID': entitySplit[0], 'Name': entitySplit[1]}
            for i, trel in enumerate(trel_values):
                if i == len(trel_values) - 1:  # Check if it's the last trel value
                    answers[tClass][next_available_key].setdefault(trel, {}).update({0: current})
                else:
                    if mathmoddb and inversePropertyMapping:
                        answers[tClass][next_available_key].setdefault(trel, {}).update({
                            0: inversePropertyMapping[mathmoddb[qrel]]
                        })

            # Update existing entries map with the new entity
            existing_entries[entitySplit[0]] = next_available_key
            next_available_key += 1  # Increment the next available key

    return