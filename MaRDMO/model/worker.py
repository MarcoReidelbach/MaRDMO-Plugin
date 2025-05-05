from .utils import mapEntryQuantity

from ..utils import entityRelations, get_data, mapEntity

def model_relations(instance, answers, mathmoddb):
    '''Function to establish relations between Model Documentation Data'''
     
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
    entityRelations(answers,'problem','field','RP2RF','RFRelatant','RelationRF1','RF')

    # Research Problem to Research Problem Relations
    entityRelations(answers,'problem','problem','IntraClassRelation','IntraClassElement','RelationRP1','RP')

    
    
    # Add Publication to Entity Relations
    entityRelations(answers,'publication',['field', 'problem', 'model', 'formulation', 'quantity', 'task'],'P2E','EntityRelatant','RelationP',['RF', 'RP', 'MM', 'MF', 'QQK', 'T'])
    
    
    return answers