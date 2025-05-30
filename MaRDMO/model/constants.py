from ..config import BASE_URI
from ..utils import get_mathmoddb, get_questionsMO

# Dictionary for internal / external section names
SECTION_MAP = {
    'model': 'Mathematical Model',
    'task': 'Computational Task',
    'formulation': 'Mathematical Expression',
    'quantity': 'Quantity / Quantity Kind',
    'problem': 'Research Problem',
    'field': 'Academic Discipline',
    'publication': 'Publication'
}

# Dictionary with list of property names
PROPS = {
    'T2MF': ['assumes','containsFormulation','containsBoundaryCondition','containsConstraintCondition','containsCouplingCondition','containsInitialCondition','containsFinalCondition'],
    'T2Q': ['containsInput','containsOutput','containsObjective','containsParameter','containsConstant'],
    'Q2MF': ['defines'],
    'RP2RF': ['containedInField'],
    'MM2RP': ['models'],
    'MM2T': ['usedBy'],
    'MM2MF': ['assumes', 'containsFormulation', 'containsBoundaryCondition', 'containsConstraintCondition', 'containsCouplingCondition', 'containsInitialCondition', 'containsFinalCondition'],
    'MF2MF': ['assumes', 'containsFormulation', 'containsBoundaryCondition', 'containsConstraintCondition', 'containsCouplingCondition', 'containsInitialCondition', 'containsFinalCondition'],
    'Field': ["specializedBy", "specializes", "similarTo"],
    'Problem': ["specializedBy", "specializes", "similarTo"],
    'Model': ['specializedBy','specializes','discretizedBy','discretizes','containedInModel','containsModel','approximatedBy','approximates','linearizedBy','linearizes','similarTo'],
    'Task': ['specializedBy','specializes','discretizedBy','discretizes','containedInTask','containsTask','approximatedBy','approximates','linearizedBy','linearizes','similarTo'],
    'Formulation': ['specializedBy','specializes','discretizedBy','discretizes','approximatedBy','approximates','linearizedBy','linearizes','nondimensionalizedBy','nondimensionalizes','similarTo'],
    'Quantity': ["specializedBy", "specializes", "approximatedBy", "approximates", "linearizedBy", "linearizes", "nondimensionalizedBy", "nondimensionalizes", "similarTo"],
}

# Index counters for different qclass combinations
INDEX_COUNTERS = {
    ("Quantity", "Quantity"): 0,
    ("QuantityKind", "QuantityKind"): 0,
    ("Quantity", "QuantityKind"): 0,
    ("QuantityKind", "Quantity"): 0,
}

# URI mappings for quantity relations
RELATION_URIS = {
    ("Quantity", "Quantity"): "Quantity Q2Q",
    ("QuantityKind", "QuantityKind"): "QuantityKind QK2QK",
    ("Quantity", "QuantityKind"): "Quantity Q2QK",
    ("QuantityKind", "Quantity"): "QuantityKind QK2Q",
}

# URI mappings for quantity relatants
RELATANT_URIS = {
    ("Quantity", "Quantity"): "Quantity QRelatant",
    ("QuantityKind", "QuantityKind"): "QuantityKind QKRelatant",
    ("Quantity", "QuantityKind"): "Quantity QKRelatant",
    ("QuantityKind", "Quantity"): "QuantityKind QRelatant",
}

# Reverse Properties
REVERSE = {
    "specializes": "specialized by",
    "approximates": "approximated by",
    "discretizes": "discretized by",
    "linearizes": "linearized by",
    "nondimensionalizes": "nondimensionalized by",
    "contained in": "contains"
}

# Relation Map
def get_RELATION_MAP():
    mathmoddb = get_mathmoddb()
    RELATION_MAP = {
            mathmoddb['specializedBy']:         'specialized by',
            mathmoddb['specializes']:           'specializes',
            mathmoddb['approximatedBy']:        'approximated by',
            mathmoddb['approximates']:          'approximates',
            mathmoddb['discretizedBy']:         'discretized by',
            mathmoddb['discretizes']:           'discretizes',
            mathmoddb['linearizedBy']:          'linearized by',
            mathmoddb['linearizes']:            'linearizes',
            mathmoddb['nondimensionalizedBy']:  'nondimensionalized by',
            mathmoddb['nondimensionalizes']:    'nondimensionalizes',
            mathmoddb['contains']:              'contains',
            mathmoddb['containedIn']:           'contained in',
            mathmoddb['similarTo']:             'similar to'
        }
    return RELATION_MAP

# Parameter for Entity relations
PREVIEW_RELATIONS = [
    # fromIDX, toIDX, relationOld, entityOld, entityNew, enc
    ('model', 'problem', None, 'RPRelatant', 'RelationRP', 'RP', False),
    ('model', 'formulation', 'MM2MF', 'MFRelatant', 'RelationMF', 'ME', True),
    ('model', 'task', None, 'TRelatant', 'RelationT', 'T', False),
    ('model', 'model', 'IntraClassRelation', 'IntraClassElement', 'RelationMM', 'MM', False),
    ('task', 'formulation', 'T2MF', 'MFRelatant', 'RelationMF', 'ME', False),
    ('task', 'quantity', 'T2Q', 'QRelatant', 'RelationQQK', 'QQK', False),
    ('task', 'task', 'IntraClassRelation', 'IntraClassElement', 'RelationT', 'T', False),
    ('formulation', 'formulation', 'MF2MF', 'MFRelatant', 'RelationMF1', 'ME', False),
    ('formulation', 'formulation', 'IntraClassRelation', 'IntraClassElement', 'RelationMF2', 'ME', False),
    ('quantity', 'quantity', 'Q2Q', 'QRelatant', 'RelationQQ', 'QQK', False),
    ('quantity', 'quantity', 'QK2QK', 'QKRelatant', 'RelationQKQK', 'QQK', False),
    ('quantity', 'quantity', 'Q2QK', 'QKRelatant', 'RelationQQK', 'QQK', False),
    ('quantity', 'quantity', 'QK2Q', 'QRelatant', 'RelationQKQ', 'QQK', False),
    ('field', 'field', 'IntraClassRelation', 'IntraClassElement', 'RelationRF', 'RF', False),
    ('problem', 'field', None, 'RFRelatant', 'RelationRF', 'RF', False),
    ('problem', 'problem', 'IntraClassRelation', 'IntraClassElement', 'RelationRP', 'RP', False),
    ('publication', ['field', 'problem', 'model', 'formulation', 'quantity', 'task'],
     'P2E', 'EntityRelatant', 'RelationP', ['RF', 'RP', 'MM', 'ME', 'QQK', 'T'], False),
]

PREVIEW_MAP_GENERAL = [
    # fromIDX, toIDX, entityOld, entityNew, enc
    ('model', 'formulation', 'assumption', 'assumptionMapped', 'ME'),
    ('task', 'formulation', 'assumption', 'assumptionMapped', 'ME'),
    ('formulation', 'formulation', 'assumption', 'assumptionMapped', 'ME'),
]

PREVIEW_MAP_QUANTITY = [
    # type
    ('formulation'),
    ('quantity'),
]

# URI PREFIX Map (I)
def get_URI_PREFIX_MAP():
    questions = get_questionsMO()
    URI_PREFIX_MAP = {
        f'{BASE_URI}{questions["Task QRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Quantity"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Quantity ID"]["uri"]}',
            "prefix": "QQK"
        },
        f'{BASE_URI}{questions["Task MFRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Mathematical Formulation Element Quantity"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Quantity"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Quantity ID"]["uri"]}',
            "prefix": "QQK"
        },
        f'{BASE_URI}{questions["Quantity Element Quantity"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Quantity"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Quantity ID"]["uri"]}',
            "prefix": "QQK"
        },
        f'{BASE_URI}{questions["Mathematical Model MFRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Mathematical Model Assumption"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Task Assumption"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Mathematical Formulation Assumption"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Mathematical Formulation MFRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Research Problem RFRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Research Field"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Research Field ID"]["uri"]}',
            "prefix": "AD"
        },
        f'{BASE_URI}{questions["Mathematical Model RPRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Research Problem"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Research Problem ID"]["uri"]}',
            "prefix": "RP"
        },
        f'{BASE_URI}{questions["Mathematical Model TRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Task"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Task ID"]["uri"]}',
            "prefix": "T"
        }
    }
    return URI_PREFIX_MAP

