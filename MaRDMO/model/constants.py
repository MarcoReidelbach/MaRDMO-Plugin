from ..config import BASE_URI
from ..getters import get_items, get_mathmoddb, get_properties, get_questions_model

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
    ("Quantity", "Quantity"): "Q2Q",
    ("QuantityKind", "QuantityKind"): "QK2QK",
    ("Quantity", "QuantityKind"): "Q2QK",
    ("QuantityKind", "Quantity"): "QK2Q",
}

# URI mappings for quantity relatants
RELATANT_URIS = {
    ("Quantity", "Quantity"): "QQRelatant",
    ("QuantityKind", "QuantityKind"): "QKQKRelatant",
    ("Quantity", "QuantityKind"): "QQKRelatant",
    ("QuantityKind", "Quantity"): "QKQRelatant",
}

# DATA Properties
def get_DATA_PROPERTIES(type):
    mathmoddb = get_mathmoddb()
    ITEMS = get_items()
    DATA_PROPERTIES = {
            mathmoddb['isChemicalConstant']:        ITEMS.get('chemical constant'),
            mathmoddb['isMathematicalConstant']:    ITEMS.get('mathematical constant'),
            mathmoddb['isPhysicalConstant']:        ITEMS.get('physical constant'),
            mathmoddb['isDeterministic']:           ITEMS.get(f'deterministic {type}'),
            mathmoddb['isStochastic']:              ITEMS.get(f'probabilistic {type}'),
            mathmoddb['isDimensional']:             ITEMS.get(f'dimensional {type}'),
            mathmoddb['isDimensionless']:           ITEMS.get(f'dimensionless {type}'),
            mathmoddb['isDynamic']:                 ITEMS.get(f'dynamic {type}'),
            mathmoddb['isStatic']:                  ITEMS.get(f'static {type}'),
            mathmoddb['isLinear']:                  ITEMS.get(f'linear {type}'),
            mathmoddb['isNotLinear']:               ITEMS.get(f'nonlinear {type}'),
            mathmoddb['isSpaceContinuous']:         ITEMS.get(f'continuous-space {type}'),
            mathmoddb['isSpaceDiscrete']:           ITEMS.get(f'discrete-space {type}'),
            mathmoddb['isTimeContinuous']:          ITEMS.get(f'continuous-time {type}'),
            mathmoddb['isTimeDiscrete']:            ITEMS.get(f'discrete-time {type}')
        }
    return DATA_PROPERTIES

# MF Relations
def get_Relations():
    mathmoddb = get_mathmoddb()
    ITEMS = get_items()
    PROPERTIES = get_properties()
    RELATIONS = {
            # Map MathModDB Relation on Wikibase Property + Qualifier Item
            mathmoddb['assumes']:                       [PROPERTIES['assumes']],
            mathmoddb['containsBoundaryCondition']:     [PROPERTIES['contains'], ITEMS['boundary condition']],
            mathmoddb['containsConstraintCondition']:   [PROPERTIES['contains'], ITEMS['constraint']],
            mathmoddb['containsCouplingCondition']:     [PROPERTIES['contains'], ITEMS['coupling condition']],
            mathmoddb['containsInitialCondition']:      [PROPERTIES['contains'], ITEMS['initial condition']],
            mathmoddb['containsFinalCondition']:        [PROPERTIES['contains'], ITEMS['final condition']],
            mathmoddb['containsInput']:                 [PROPERTIES['contains'], ITEMS['input']],
            mathmoddb['containsConstant']:              [PROPERTIES['contains'], ITEMS['constant']],
            mathmoddb['containsObjective']:             [PROPERTIES['contains'], ITEMS['objective function']],
            mathmoddb['containsOutput']:                [PROPERTIES['contains'], ITEMS['output']],
            mathmoddb['containsParameter']:             [PROPERTIES['contains'], ITEMS['parameter']],
            mathmoddb['documents']:                     [PROPERTIES['described by source'], ITEMS['documentation']],
            mathmoddb['invents']:                       [PROPERTIES['described by source'], ITEMS['invention']],
            mathmoddb['studies']:                       [PROPERTIES['described by source'], ITEMS['study']],
            mathmoddb['surveys']:                       [PROPERTIES['described by source'], ITEMS['review']],
            mathmoddb['uses']:                          [PROPERTIES['described by source'], ITEMS['use']],
            # Map MathModDB Relation on Wikibase Property + Direction
            mathmoddb['specializedBy']:                 [PROPERTIES['specialized by'],         'forward'],
            mathmoddb['specializes']:                   [PROPERTIES['specialized by'],         'backward'],
            mathmoddb['approximatedBy']:                [PROPERTIES['approximated by'],        'forward'],
            mathmoddb['approximates']:                  [PROPERTIES['approximated by'],        'backward'],
            mathmoddb['discretizedBy']:                 [PROPERTIES['discretized by'],         'forward'],
            mathmoddb['discretizes']:                   [PROPERTIES['discretized by'],         'backward'],
            mathmoddb['linearizedBy']:                  [PROPERTIES['linearized by'],          'forward'],
            mathmoddb['linearizes']:                    [PROPERTIES['linearized by'],          'backward'],
            mathmoddb['nondimensionalizedBy']:          [PROPERTIES['nondimensionalized by'],  'forward'],
            mathmoddb['nondimensionalizes']:            [PROPERTIES['nondimensionalized by'],  'backward'],
            mathmoddb['contains']:                      [PROPERTIES['contains'],               'forward'],
            mathmoddb['containedIn']:                   [PROPERTIES['contains'],               'backward'],
            mathmoddb['similarTo']:                     [PROPERTIES['similar to'],             'forward']
        }
    return RELATIONS

# Relation Map
def get_INTRACLASS_RELATION():
    mathmoddb = get_mathmoddb()
    PROPERTIES = get_properties()
    INTRACLASS_RELATION = {
            mathmoddb['specializedBy']:         [PROPERTIES['specialized by'],         'forward'],
            mathmoddb['specializes']:           [PROPERTIES['specialized by'],         'backward'],
            mathmoddb['approximatedBy']:        [PROPERTIES['approximated by'],        'forward'],
            mathmoddb['approximates']:          [PROPERTIES['approximated by'],        'backward'],
            mathmoddb['discretizedBy']:         [PROPERTIES['discretized by'],         'forward'],
            mathmoddb['discretizes']:           [PROPERTIES['discretized by'],         'backward'],
            mathmoddb['linearizedBy']:          [PROPERTIES['linearized by'],          'forward'],
            mathmoddb['linearizes']:            [PROPERTIES['linearized by'],          'backward'],
            mathmoddb['nondimensionalizedBy']:  [PROPERTIES['nondimensionalized by'],  'forward'],
            mathmoddb['nondimensionalizes']:    [PROPERTIES['nondimensionalized by'],  'backward'],
            mathmoddb['contains']:              [PROPERTIES['contains'],               'forward'],
            mathmoddb['containedIn']:           [PROPERTIES['contains'],               'backward'],
            mathmoddb['similarTo']:             [PROPERTIES['similar to'],             'forward']
        }
    return INTRACLASS_RELATION

# Parameter for Entity relations
PREVIEW_RELATIONS = [
    # fromIDX, toIDX, relationOld, entityOld, entityNew, enc
    ('model', 'problem', None, 'RPRelatant', 'RelationRP', 'RP', False, False),
    ('model', 'formulation', 'MM2MF', 'MFRelatant', 'RelationMF', 'ME', True, False),
    ('model', 'task', None, 'TRelatant', 'RelationT', 'T', False, False),
    ('model', 'model', 'IntraClassRelation', 'IntraClassElement', 'RelationMM', 'MM', False, False),
    ('task', 'formulation', 'T2MF', 'MFRelatant', 'RelationMF', 'ME', False, False),
    ('task', 'quantity', 'T2Q', 'QRelatant', 'RelationQQK', 'QQK', False, False),
    ('task', 'task', 'IntraClassRelation', 'IntraClassElement', 'RelationT', 'T', False, True),
    ('formulation', 'formulation', 'MF2MF', 'MFRelatant', 'RelationMF1', 'ME', False, False),
    ('formulation', 'formulation', 'IntraClassRelation', 'IntraClassElement', 'RelationMF2', 'ME', False, False),
    ('quantity', 'quantity', 'Q2Q', 'QRelatant', 'RelationQQ', 'QQK', False, False),
    ('quantity', 'quantity', 'QK2QK', 'QKRelatant', 'RelationQKQK', 'QQK', False, False),
    ('quantity', 'quantity', 'Q2QK', 'QKRelatant', 'RelationQQK', 'QQK', False, False),
    ('quantity', 'quantity', 'QK2Q', 'QRelatant', 'RelationQKQ', 'QQK', False, False),
    ('field', 'field', 'IntraClassRelation', 'IntraClassElement', 'RelationRF', 'AD', False, False),
    ('problem', 'field', None, 'RFRelatant', 'RelationRF', 'AD', False, False),
    ('problem', 'problem', 'IntraClassRelation', 'IntraClassElement', 'RelationRP', 'RP', False, False),
    ('publication', ['field', 'problem', 'model', 'formulation', 'quantity', 'task'],
     'P2E', 'EntityRelatant', 'RelationP', ['RF', 'RP', 'MM', 'ME', 'QQK', 'T'], False, False),
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
    questions = get_questions_model()
    URI_PREFIX_MAP = {
        f'{BASE_URI}{questions["Task"]["QRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Quantity"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Quantity"]["ID"]["uri"]}',
            "prefix": "QQK"
        },
        f'{BASE_URI}{questions["Task"]["MFRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation"]["ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Mathematical Formulation"]["Element Quantity"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Quantity"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Quantity"]["ID"]["uri"]}',
            "prefix": "QQK"
        },
        f'{BASE_URI}{questions["Quantity"]["Element Quantity"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Quantity"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Quantity"]["ID"]["uri"]}',
            "prefix": "QQK"
        },
        f'{BASE_URI}{questions["Mathematical Model"]["MFRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation"]["ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Mathematical Model"]["Assumption"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation"]["ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Task"]["Assumption"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation"]["ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Mathematical Formulation"]["Assumption"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation"]["ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Mathematical Formulation"]["MFRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Mathematical Formulation"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Mathematical Formulation"]["ID"]["uri"]}',
            "prefix": "ME"
        },
        f'{BASE_URI}{questions["Research Problem"]["RFRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Research Field"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Research Field"]["ID"]["uri"]}',
            "prefix": "AD"
        },
        f'{BASE_URI}{questions["Mathematical Model"]["RPRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Research Problem"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Research Problem"]["ID"]["uri"]}',
            "prefix": "RP"
        },
        f'{BASE_URI}{questions["Mathematical Model"]["TRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Task"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Task"]["ID"]["uri"]}',
            "prefix": "T"
        }
    }
    return URI_PREFIX_MAP

