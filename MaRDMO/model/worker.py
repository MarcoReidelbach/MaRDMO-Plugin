from ..utils import entityRelations, get_data, mapEntity

def model_relations(instance, answers,mathmoddb):
    '''Function to establish relations between Model Documentation Data'''
     
    inversePropertyMapping = get_data('model/data/inversePropertyMapping.json')

    # Flag all Tasks as unwanted by User in Workflow Documentation
    for key in answers['task']:
        answers['task'][key].update({'Include':False})

    # Mathematical Model to Research Problem Relations
    entityRelations(answers,'model','problem','MM2RP','RPRelatant','RelationRP1','RP')
    
    # Mathematical Model to Mathematical Formulation Relations
    entityRelations(answers,'model','formulation','MM2MF','MFRelatant','RelationMF1','MF')

    # Mathematical Model to Task Relations
    entityRelations(answers,'model','task','MM2T','TRelatant','RelationT','T')
    
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
    for key in answers['formulation']:
        for key2 in answers['formulation'][key].get('element',{}):
            
            #if len(answers['formulation'][key]['element'][key2]['quantity'].split(' <|> ')) == 1:
            #    label = answers['formulation'][key]['element'][key2]['quantity']
            #    Id = ''
            #elif len(answers['formulation'][key]['element'][key2]['quantity'].split(' <|> ')) >= 2:
            
            _, label = answers['formulation'][key]['element'][key2]['quantity'].split(' <|> ')#[:2]
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

    # Add Mathematical Formulation to Mathematical Formulation Relations 1
    entityRelations(answers,'formulation','formulation','MF2MF','MFRelatant','RelationMF1','MF')

    # Add Mathematical Formulation to Mathematical Formulation Relations 2
    entityRelations(answers,'formulation','formulation','IntraClassRelation','IntraClassElement','RelationMF2','MF')
    
    # Formulation Assumptions for specializes / specialized by Relations
    mapEntity(answers, 'formulation', 'formulation', 'assumption', 'assumptionMapped', 'MF')



 
    # Research Field to Research Field Relations
    entityRelations(answers,'field','field','IntraClassRelation','IntraClassElement','RelationRF1','RF')
    
    # Research Field to Research Problem Relations
    entityRelations(answers,'problem','field','RP2RF','RFRelatant','RelationRF1','RF')

    # Research Problem to Research Problem Relations
    entityRelations(answers,'problem','problem','IntraClassRelation','IntraClassElement','RelationRP1','RP')
    
    

    
    
    

    # Add Quantity to Quantity Relations
    entityRelations(answers,'quantity','quantity','Q2Q','QRelatant','RelationQQ','QQK')
    
    # Add QuantityKind to QuantityKind Relations
    entityRelations(answers,'quantity','quantity','QK2QK','QKRelatant','RelationQKQK','QQK')

    # Add Quantity to QuantityKind Relations
    entityRelations(answers,'quantity','quantity','Q2QK','QKRelatant','RelationQQK','QQK')

    # Add QuantityKind to Quantity Relations
    entityRelations(answers,'quantity','quantity','QK2Q','QRelatant','RelationQKQ','QQK')
    
    
    
    # Add Definition to Quantities
    for key in answers.get('quantity',[]):
        for key2 in answers['formulation']:
            if answers['formulation'][key2].get('DefinedQuantity'):
                Id,label = answers['formulation'][key2]['DefinedQuantity'].split(' <|> ')[:2]
                if label == answers['quantity'][key]['Name']:
                    answers['quantity'][key].update({'MDef':answers['formulation'][key2]})

    
    
    # Add Publication to Entity Relations
    entityRelations(answers,'publication',['field', 'problem', 'model', 'formulation', 'quantity', 'task'],'P2E','EntityRelatant','RelationP',['RF', 'RP', 'MM', 'MF', 'QQK', 'T'])
    
    
    return answers