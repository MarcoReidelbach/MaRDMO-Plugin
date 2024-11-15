import re
import requests
import os, json

from .sparql import queryModelDocumentation
from .config import mardi_api, mathmoddb_endpoint
from .utils import find_item, query_sparql

def ModelRetriever(answers,mathmoddb):
    '''Function queries MathModDB to gather further Model Information
       and connects them with Information provided by the User'''
     
    path = os.path.join(os.path.dirname(__file__), 'data', 'options.json')
    with open(path, "r") as json_file:
        option = json.load(json_file)
    
    path = os.path.join(os.path.dirname(__file__), 'data', 'inversePropertyMapping.json')
    with open(path, "r") as json_file:
        inversePropertyMapping = json.load(json_file)
    
    # Kinds of Objects, Relations and Properties
    formulationKinds = ['Formulation', 'Assumption', 'BoundaryCondition', 'ConstraintCondition', 'CouplingCondition', 'InitialCondition', 'FinalCondition']
    quantityKinds = ['Input', 'Output', 'Objective', 'Parameter', 'Constant']
    intraClassRelations = ['generalizedBy','generalizes','approximatedBy','approximates','discretizedBy','discretizes','linearizedBy','linearizes','nondimensionalizedBy','nondimensionalizes','similarTo']
    publicationRelations = ['documentedIn', 'inventedIn', 'studiedIn', 'surveyedIn', 'usedIn']
    dataProperties = ['isLinear','isNotLinear','isConvex','isNotConvex','isDynamic','isStatic','isDeterministic','isStochastic','isDimensionless',
                     'isDimensional','isTimeContinuous','isTimeDiscrete','isTimeIndependent','isSpaceContinuous','isSpaceDiscrete','isSpaceIndependent']
    
    # Flag all Tasks as unwanted by User in Workflow Documentation
    for key in answers['Task']:
        answers['Task'][key].update({'Include':False})

    # Get additional Task Information from MathModDB
    
    qClass = 'Task'
    
    search_string = searchGenerator(answers,[qClass])
    results = query_sparql(queryModelDocumentation[qClass].format(search_string))
    
    # Get MathModDB ID of all selected Tasks
    mathmodidToKey = {answers[qClass][key].get('MathModID'): key for key in answers[qClass]}

    for result in results:
        # Get MathModDB ID of queried Task
        mathmod_id = result.get(qClass, {}).get('value')
        # Queried Task in Selection?
        if mathmod_id in mathmodidToKey:    
            key = mathmodidToKey[mathmod_id]
            # Evaluate Comment of Task
            assignValue(qClass, ['quote'], 'Description',result ,key, answers)
            # Evaluate Data Properties of Task
            assignProperties(answers[qClass][key], result, mathmoddb, dataProperties)
            # Evaluate Subclass of Task
            assignValue(qClass, ['subclass'], 'TaskClass',result ,key, answers, mathmoddb)
            # Evaluate related Mathematical Models
            assignSimpleEntityRelation(qClass, 'appliesModel', ['T2MM','MMRelatant','appliesModel'], result, key, answers, mathmoddb)
            # Evaluate Tasks containend in Task
            assignSimpleEntityRelation(qClass, 'containsTask', ['IntraClassRelation','IntraClassElement','containsTask'], result, key, answers, mathmoddb)
            # Evaluate Task containing Task
            assignSimpleEntityRelation(qClass, 'containedInTask', ['IntraClassRelation','IntraClassElement','containedInTask'], result, key, answers, mathmoddb)
            # Evaluate different kinds of Mathematical Formulations of Task
            for kind in formulationKinds:
                assignComplexEntityRelations(qClass, 'MathematicalFormulation', f'contains{kind}', ['MF2T','TRelatant'], result, key, answers, mathmoddb, inversePropertyMapping)
            # Evaluate different kinds of Quantities of Task
            for kind in quantityKinds:
                assignSimpleEntityRelation(qClass, f'contains{kind}', ['T2Q','QRelatant',f'contains{kind}'], result, key, answers, mathmoddb)
    
    # Add Mathematical Formulations from Task to Formulation List
    name_to_key = {v['Name']: k for k, v in answers['MathematicalFormulation'].items()}
    # Iterate through Tasks
    for idx, key in enumerate(answers['Task']):
        task = answers['Task'][key]
        # Process each relation
        for key2, relation in task.get('T2MF', {}).items():
            Id, label = task['MFRelatant'][key2].split(' <|> ')[:2]
            # Check if the label already exists in Mathematical Formulation
            if label in name_to_key:
                k = name_to_key[label]
                math_form = answers['MathematicalFormulation'][k]
                relation4 = math_form.setdefault('MF2T', {})
                other4 = math_form.setdefault('TRelatant', {})
                relation4[f'TF{key}{idx}'] = inversePropertyMapping[relation]
                other4[f'TF{key}{idx}'] = f"{task.get('MathModID', idx)} <|> {task['Name']}"
            else:
                # Create a new entry for the Mathematical Formulation
                new_key = max(answers['MathematicalFormulation'].keys(), default=-1) + 1
                new_form = {
                    'MathModID': Id,
                    'Name': label,
                    'MF2T': {f'TF{key}{idx}': inversePropertyMapping[relation]},
                    'TRelatant': {f'TF{key}{idx}': f"{task.get('MathModID', idx)} <|> {task['Name']}"}
                }
                answers['MathematicalFormulation'][new_key] = new_form
                # Update the lookup dictionary
                name_to_key[label] = new_key

    # Get additional Mathematical Formulation Information from MathModDB

    qClass = 'MathematicalFormulation'

    search_string = searchGenerator(answers,[qClass])
    results = query_sparql(queryModelDocumentation[qClass].format(search_string))
     
    # Get MathModID of all selected Mathematical Formulations
    mathmodidToKey = {answers[qClass][key].get('MathModID'): key for key in answers[qClass]}

    for result in results:
        # Get MathModID of queried Mathematical Formulation
        mathmod_id = result.get(qClass, {}).get('value')
        # Queried Mathematical Formulation in Selection?
        if mathmod_id in mathmodidToKey:
            key = mathmodidToKey[mathmod_id]
            #Evaluate Comment of Mathematical Formulation
            assignValue(qClass, ['quote'], 'Description',result ,key, answers)
            #Evaluate Data Properties of Mathematical Formulation
            assignProperties(answers['MathematicalFormulation'][key], result, mathmoddb, dataProperties)   
            #Evaluate different kinds of Mathematical Formulations of Mathematical Formulations
            for kind in formulationKinds:
                assignSimpleEntityRelation(qClass, f'contains{kind}', ['MF2MF','MFRelatant',f'contains{kind}'], result, key, answers, mathmoddb)
            #Evaluate Formula of Mathematical Formulation    
            assignValues(qClass, 'formula', ['Formula'], result, key, answers)
            #Evaluate Elements of Mathematical Formulation
            assignValues(qClass, 'formula_elements', ['Element','Symbol','Quantity'], result, key, answers, splitVariableText)
            #Evaluate Quantities of Mathematical Formulation
            assignComplexEntityRelations(qClass, 'Quantity', 'ContainsQuantity', [], result, key, answers, mathmoddb)
                
    # Get additional Mathematical Formulation Information from MathModDB (Quantity Defintions)
    
    qClass = 'Quantity'
    tClass = 'MathematicalFormulation'

    search_string = searchGenerator(answers,[qClass])
    results = query_sparql(queryModelDocumentation[f'{qClass}Definition'].format(search_string))
    
    # Get MathModID of all selected Mathematical Formulations
    mathmodidToKey = {answers[tClass][key].get('MathModID'): key for key in answers[tClass]}

    for result in results:
        # Get MathModID of queried Mathematical Formulation
        mathmod_id = result.get(tClass, {}).get('value')
        # Queried Mathematical Formulation in Selection?
        if mathmod_id in mathmodidToKey:
            # If Mathematial Formulation selected add defined quantity statement
            key = mathmodidToKey[mathmod_id]
            # Evaluate defined Quantity of Mathematical Formulation
            assignValue(tClass, ['q','qlabel'], 'DefinedQuantity',result ,key, answers)
        else:
            # If Mathematical Formulation is not selected add it
            key = max(answers[tClass].keys(), default=-1) + 1
            #Evaluate ID, Name, Comment and defined Quantity of Mathematical Formulation
            assignValue(tClass, [tClass], 'MathModID',result ,key, answers)
            assignValue(tClass, ['label'], 'Name',result ,key, answers)
            assignValue(tClass, ['quote'], 'Description',result ,key, answers)
            assignValue(tClass, ['q','qlabel'], 'DefinedQuantity',result ,key, answers)
            #Evaluate Properties of Mathematical Formulation
            assignProperties(answers['MathematicalFormulation'][key], result, mathmoddb, dataProperties)
            #Evaluate Formula of Mathematical Formulation    
            assignValues(tClass, 'formula', ['Formula'], result, key, answers)
            #Evaluate Elements of Mathematical Formulation
            assignValues(tClass, 'formula_elements', ['Element','Symbol','Quantity'], result, key, answers, splitVariableText)
            #Evaluate Quantities of Mathematical Formulation
            assignComplexEntityRelations(tClass, 'Quantity', 'ContainsQuantity', [], result, key, answers, mathmoddb)

    # Get additional Quantity Information from MathModDB
    
    qClass = 'Quantity'
    
    search_string = searchGenerator(answers,[qClass])
    results = query_sparql(queryModelDocumentation[qClass].format(search_string))

    # Get MathModID of all selected Quantities
    mathmodidToKey = {answers[qClass][key].get('MathModID'): key for key in answers[qClass]}

    for result in results:
        # Get MathModID of queried Quantity
        mathmod_id = result.get(qClass, {}).get('value')
        # Queried Quantity in Selection?
        if mathmod_id in mathmodidToKey:
            key = mathmodidToKey[mathmod_id]
            #Evaluate Comment of Quantity
            assignValue(qClass, ['quote'], 'Description',result ,key, answers)
            #Evaluate Data Properties of Quantities
            assignProperties(answers['Quantity'][key], result, mathmoddb, dataProperties)
            # Evaluate Quantity Kind (ID, Name, Description) of Quantity
            assignValue(qClass, ['qk'], 'QKID',result ,key, answers)
            assignValue(qClass, ['qklabel'], 'QKName',result ,key, answers)
            assignValue(qClass, ['qkquote'], 'QKDescription',result ,key, answers)
    
    # Get additional Intra-Class Information for Model, Task, Formulation and Quantity Relations from MathModDB
    
    search_string = searchGenerator(answers,['Task', 'MathematicalFormulation', 'MathematicalModel', 'Quantity', 'ResearchField', 'ResearchProblem'])
    results = query_sparql(queryModelDocumentation['IntraClass'].format(search_string))
    
    mathmodidToKey = {}

    # Get MathModID of all selected Entities
    for className in ['ResearchField', 'ResearchProblem', 'Task', 'MathematicalFormulation', 'MathematicalModel', 'Quantity']:
        mathmodidToKey[className] = {answers[className][key].get('MathModID'): key for key in answers[className]}

    propAppendix = {'ResearchField': 'Field',
                    'ResearchProblem': 'Problem',
                    'Task': 'Task',
                    'MathematicalFormulation': 'Formulation',
                    'MathematicalModel': 'Model',
                    'Quantity': 'Quantity'}

    for result in results:
        # Get MathModID and Class of queried Entity
        math_mod_id, qClass = result['Item']['value'].split(' >|< ')
        # Queried Entity in Selection?
        if math_mod_id in mathmodidToKey[qClass]:
            key = mathmodidToKey[qClass][math_mod_id]
            # Evaluate Relations of Mathematical Models, Mathematical Formulations, Tasks and Quantities
            for relation in intraClassRelations:
                assignSimpleEntityRelation(qClass, relation, [f"{relation}{propAppendix[qClass]}"], result, key, answers, mathmoddb)

    # Get additional Publication Information from MathModDB

    tClass = 'PublicationModel'

    search_string = searchGenerator(answers,['ResearchField','ResearchProblem','MathematicalModel','Quantity','MathematicalFormulation','Task'])
    results = query_sparql(queryModelDocumentation[tClass].format(search_string))
    
    for result in results:
        # Get MathModID and Class of queries entity
        mathmodid, qClass = result['Item']['value'].split(' >|< ')
        # Queried entity in Selection?
        if mathmodid in mathmodidToKey[qClass]:
            key = mathmodidToKey[qClass][mathmodid]
            for relation in publicationRelations:
                assignComplexEntityRelations(qClass, tClass, relation, ['P2E','EntityRelatant'], result, key, answers, mathmoddb, inversePropertyMapping)

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
                    if answers['Quantity'][k]['QorQK'] == mathmoddb['QuantityClass']:
                        if not Id.startswith('https://mardi4nfdi.de/mathmoddb#'):
                            relatants = answers['Quantity'][k].get('QKRelatant', {}).values()
                            relatantIDs = []
                            relatantLabels = []
                            for relatant in relatants:
                                relatantID, relatantLabel = relatant.split(' <|> ')
                                if relatantID.startswith('https://mardi4nfdi.de/mathmoddb#') or relatantID.startswith('https://mardi4nfdi.de/mathmoddb#') or relatantID.startswith('https://mardi4nfdi.de/mathmoddb#'):
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
                                 'QID':answers['Quantity'][k].get('MathModID','') if answers['Quantity'][k].get('MathModID','') and answers['Quantity'][k].get('MathModID','') != 'not in MathModDB' else answers['Quantity'][k].get('ID','') if answers['Quantity'][k].get('ID','') else answers['Quantity'][k].get('Reference','') if answers['Quantity'][k].get('Reference','') else '', 
                                 'QKName':answers['Quantity'][k].get('QKName',''),
                                 'QKID':answers['Quantity'][k].get('QKID','')}
                            })
                    elif answers['Quantity'][k]['QorQK'] == mathmoddb['QuantityKindClass']:
                        answers['MathematicalFormulation'][key]['Element'][key2].update(
                            {'Info':
                                {'QKName':answers['Quantity'][k].get('Name',''),
                                 'Description':answers['Quantity'][k].get('Description',''),
                                 'QKID':answers['Quantity'][k].get('MathModID','') if answers['Quantity'][k].get('MathModID','') and answers['Quantity'][k].get('MathModID','') != 'not in MathModDB' else answers['Quantity'][k].get('ID','') if answers['Quantity'][k].get('ID','') else ''}
                            })

    # Add Definition to Quantities
    for key in answers.get('Quantity',[]):
        for key2 in answers['MathematicalFormulation']:
            if answers['MathematicalFormulation'][key2].get('DefinedQuantity'):
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

def assignProperties(data, queryData, mathmoddb, properties):
    # Add Data Property Information from Query to Data
    for idx,property in enumerate(properties):
        if queryData.get(property, {}).get('value') == 'true':
            data.setdefault('Properties',{}).update({idx:mathmoddb[property]})
    return

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
            math_mod_id = data[key][key2].get('MathModID')
            if math_mod_id and math_mod_id != 'not in MathModDB':
                search_string += f" :{math_mod_id.split('#')[1]}"
    
    return search_string

def splitVariableText(inputString):
    
    match = re.match(r'(\$.*?\$)\s*,\s*(.*)', inputString)
    
    if match:
        # Extract the groups: math part and text part
        math_part, text_part = match.groups()
        return math_part, text_part
    else:
        # Handle case where the pattern is not found
        return '', ''
    
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
        current = f"{answers[qClass][key]['MathModID']} <|> {answers[qClass][key]['Name']} <|> {qClass} <|> {''.join(filter(str.isupper, qClass))}"
    else:
        current = f"{answers[qClass][key]['MathModID']} <|> {answers[qClass][key]['Name']}"

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

def assignSimpleEntityRelation(qClass, qrel, trel, r, key, answers, mathmoddb=None):

    condition_map = {
                     ('ResearchField', 'ResearchField'): ('IntraClassRelation','IntraClassElement'),
                     ('ResearchProblem', 'ResearchProblem'): ('IntraClassRelation','IntraClassElement'),
                     ('MathematicalModel', 'MathematicalModel'): ('IntraClassRelation','IntraClassElement'),
                     ('MathematicalFormulation', 'MathematicalFormulation'): ('IntraClassRelation','IntraClassElement'),
                     ('ComputationalTask', 'ComputationalTask'): ('IntraClassRelation','IntraClassElement'),
                     ('Quantity', 'Quantity'): ('Q2Q', 'QRelatant'),
                     ('QuantityKind', 'QuantityKind'): ('QK2QK', 'QKRelatant'),
                     ('Quantity', 'QuantityKind'): ('Q2QK', 'QKRelatant'),
                     ('QuantityKind', 'Quantity'): ('QK2Q', 'QRelatant')
                    }

    values = r.get(qrel,{}).get('value')
                
    if values:
    
        # Split values into list of entities
        entities = values.split(' <|> ')

        for idx, entity in enumerate(entities):
        
            # Assign trelValues
            trelValues = trel

            # Get Id and label of entitiy
            entitySplit = entity.split(' >|< ')

            # trel's on-the-fly if needed
            if len(entitySplit) == 4:
                trelValues = condition_map[tuple(entitySplit[2:])] + tuple(trelValues)
            
            # Update answers with IntraClassRelation and IntraClassElement
            data = answers[qClass][key]
            data.setdefault(trelValues[0], {})[f'{qrel}{idx}'] = mathmoddb[trelValues[2]]
            data.setdefault(trelValues[1], {})[f'{qrel}{idx}'] = f'{entitySplit[0]} <|> {entitySplit[1]}'
    return

def assignValue(qClass,keyOld,keyNew,r,key,answers,mathmoddb=None):
    if len(keyOld) == 1:
        if mathmoddb:
            if r.get(keyOld[0], {}).get('value'):
                answers[qClass].setdefault(key, {}).update({keyNew:mathmoddb[r[keyOld[0]]['value']]})
        else:
            if r.get(keyOld[0], {}).get('value'):
                answers[qClass].setdefault(key, {}).update({keyNew:r[keyOld[0]]['value']})
    elif len(keyOld) == 2:
        if r.get(keyOld[0], {}).get('value') and r.get(keyOld[1], {}).get('value'):
            answers[qClass].setdefault(key, {}).update({keyNew:f'{r[keyOld[0]]["value"]} <|> {r[keyOld[1]]["value"]}'})
    return

def assignValues(qClass,keyOld,keyNew,r,key,answers,splitVariableText=None):
    if r.get(keyOld,{}).get('value'):
        entities = r[keyOld]['value'].split(' <|> ')
        for idx,entity in enumerate(entities):
            if splitVariableText:
                # Split Content
                var, text = splitVariableText(entity)
                answers[qClass][key].setdefault(keyNew[0],{}).update({idx:{keyNew[1]:f'${var}$',keyNew[2]:text}})
            else:
                # Keep Content as it is
                answers[qClass][key].setdefault(keyNew[0],{}).update({idx:f'${entity}$'})
    return
