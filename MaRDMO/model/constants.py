'''Module containing Constants for the Model Documentation'''

from ..constants import BASE_URI
from ..getters import get_items, get_mathmoddb, get_properties, get_questions

# Data Properties Check
data_properties_check = {
    ('is_deterministic', 'is_stochastic'): '(Deterministic and Stochastic)',
    ('is_dimensionless', 'is_dimensional'): '(Dimensionless and Dimensional)',
    ('is_dynamic', 'is_static'): '(Dynamic and Static)',
    ('is_linear', 'is_not_linear'): '(Linear and Not Linear)',
    ('is_space_continuous', 'is_space_discrete'): '(Space-Continuous and Space-Discrete)',
    ('is_time_continuous', 'is_time_discrete'): '(Time-Continuous and Time-Discrete)',
    ('is_mathematical_constant', 'is_physical_constant'): '(Mathematical and Physical Constant)',
    ('is_mathematical_constant', 'is_physical_constant'): '(Mathematical and Chemical Constant)'
}

# Data Properties per Class
data_properties_per_class = {
    'model': [
        'is_linear', 'is_not_linear', 'is_dynamic', 'is_static',
        'is_deterministic', 'is_stochastic', 'is_dimensionless', 'is_dimensional',
        'is_time_continuous', 'is_time_discrete', 'is_space_continuous', 'is_space_discrete',
    ],
    'quantity': [
        'is_chemical_constant', 'is_mathematical_constant', 'is_physical_constant',
        'is_dynamic', 'is_static', 'is_deterministic', 'is_stochastic', 'is_dimensionless',
        'is_dimensional', 'is_time_continuous', 'is_time_discrete', 'is_space_continuous',
        'is_space_discrete'
    ],
    'formulation': [
        'is_linear', 'is_not_linear', 'is_dynamic', 'is_static', 'is_deterministic',
        'is_stochastic', 'is_dimensionless', 'is_dimensional', 'is_time_continuous',
        'is_time_discrete', 'is_space_continuous', 'is_space_discrete'
    ],
    'task': ['is_linear', 'is_not_linear', 'is_time_continuous', 'is_time_discrete',
             'is_space_continuous', 'is_space_discrete'
    ]
}

# QUDT Reference IDs
qudt_reference_ids = [
    'qudt_quantitykind_id',
    'qudt_constant_id'
]

# Dictionary for internal / external section names
section_map = {
    'model': 'Mathematical Model',
    'task': 'Computational Task',
    'formulation': 'Mathematical Expression',
    'quantity': 'Quantity [Kind]',
    'problem': 'Research Problem',
    'field': 'Academic Discipline',
    'publication': 'Publication'
}

# Dictionary with list of property names
props = {
    'T2MF': [
        'assumes',
        'contains_analytical_solution',
        'contains_physical_law',
        'contains_computational_domain',
        'contains_constitutive_equation',
        'contains_weak_formulation',
        'contains_strong_formulation',
        'contains_formulation',
        'contains_boundary_condition',
        'contains_constraint_condition',
        'contains_coupling_condition',
        'contains_initial_condition',
        'contains_final_condition'
    ],
    'T2Q': [
        'contains_input',
        'contains_output',
        'contains_objective',
        'contains_parameter',
        'contains_constant'
    ],
    'RP2RF': [
        'contained_in_field'
    ],
    'MM2RP': [
        'models'
    ],
    'MM2T': [
        'used_by'
    ],
    'MM2MF': [
        'assumes',
        'contains_analytical_solution',
        'contains_physical_law',
        'contains_computational_domain',
        'contains_constitutive_equation',
        'contains_weak_formulation',
        'contains_strong_formulation',
        'contains_formulation',
        'contains_boundary_condition',
        'contains_constraint_condition',
        'contains_coupling_condition',
        'contains_initial_condition',
        'contains_final_condition'
    ],
    'MF2MF': [
        'assumes',
        'contains_formulation',
        'contains_boundary_condition',
        'contains_constraint_condition',
        'contains_coupling_condition',
        'contains_initial_condition',
        'contains_final_condition'
    ],
    'Field': [
        "specialized_by",
        "specializes",
        "similar_to"
    ],
    'Problem': [
        "specialized_by",
        "specializes",
        "similar_to"
    ],
    'Model': [
        'specialized_by',
        'specializes',
        'discretized_by',
        'discretizes',
        'contained_in_model',
        'contains_model',
        'approximated_by',
        'approximates',
        'linearized_by',
        'linearizes',
        'similar_to'
    ],
    'Task': [
        'specialized_by',
        'specializes',
        'discretized_by',
        'discretizes',
        'contained_in_task',
        'contains_task',
        'approximated_by',
        'approximates',
        'linearized_by',
        'linearizes',
        'similar_to'
    ],
    'Formulation': [
        'specialized_by',
        'specializes',
        'discretized_by',
        'discretizes',
        'approximated_by',
        'approximates',
        'linearized_by',
        'linearizes',
        'nondimensionalized_by',
        'nondimensionalizes',
        'similar_to'
    ],
    'Quantity': [
        "specialized_by",
        "specializes",
        "approximated_by",
        "approximates",
        "discretized_by",
        "discretizes",
        "linearized_by",
        "linearizes",
        "nondimensionalized_by",
        "nondimensionalizes",
        "similar_to"
    ],
}

# Index counters for different qclass combinations
index_counters = {
    ("Quantity", "Quantity"): 0,
    ("QuantityKind", "QuantityKind"): 0,
    ("Quantity", "QuantityKind"): 0,
    ("QuantityKind", "Quantity"): 0,
}

# URI mappings for quantity relations
relation_uris = {
    ("Quantity", "Quantity"): "Q2Q",
    ("QuantityKind", "QuantityKind"): "QK2QK",
    ("Quantity", "QuantityKind"): "Q2QK",
    ("QuantityKind", "Quantity"): "QK2Q",
}

# URI mappings for quantity relatants
relatant_uris = {
    ("Quantity", "Quantity"): "QQRelatant",
    ("QuantityKind", "QuantityKind"): "QKQKRelatant",
    ("Quantity", "QuantityKind"): "QQKRelatant",
    ("QuantityKind", "Quantity"): "QKQRelatant",
}

# DATA Properties
def get_data_properties(item_type):
    '''Data Properties for the Model Documentation'''
    mathmoddb = get_mathmoddb()
    items = get_items()
    data_properties = {
        mathmoddb['is_chemical_constant']: items.get('chemical constant'),
        mathmoddb['is_mathematical_constant']: items.get('mathematical constant'),
        mathmoddb['is_physical_constant']: items.get('physical constant'),
        mathmoddb['is_deterministic']: items.get(f'deterministic {item_type}'),
        mathmoddb['is_stochastic']: items.get(f'probabilistic {item_type}'),
        mathmoddb['is_dimensional']: items.get(f'dimensional {item_type}'),
        mathmoddb['is_dimensionless']: items.get(f'dimensionless {item_type}'),
        mathmoddb['is_dynamic']: items.get(f'dynamic {item_type}'),
        mathmoddb['is_static']: items.get(f'static {item_type}'),
        mathmoddb['is_linear']: items.get(f'linear {item_type}'),
        mathmoddb['is_not_linear']: items.get(f'nonlinear {item_type}'),
        mathmoddb['is_space_continuous']: items.get(f'continuous-space {item_type}'),
        mathmoddb['is_space_discrete']: items.get(f'discrete-space {item_type}'),
        mathmoddb['is_time_continuous']: items.get(f'continuous-time {item_type}'),
        mathmoddb['is_time_discrete']: items.get(f'discrete-time {item_type}')
    }
    return data_properties

# Relations
def get_relations():
    '''Relations for the Model Documentation'''
    mathmoddb = get_mathmoddb()
    items = get_items()
    properties = get_properties()
    relations = {
        # Map MathModDB Relation on Wikibase Property + Qualifier Item
        mathmoddb['assumes']: [
            properties['assumes']
        ],
        mathmoddb['contains_boundary_condition']: [
            properties['contains'],
            items['boundary condition']
        ],
        mathmoddb['contains_constraint_condition']: [
            properties['contains'],
            items['constraint']
        ],
        mathmoddb['contains_coupling_condition']: [
            properties['contains'],
            items['coupling condition']
        ],
        mathmoddb['contains_initial_condition']: [
            properties['contains'],
            items['initial condition']
        ],
        mathmoddb['contains_final_condition']: [
            properties['contains'],
            items['final condition']
        ],
        mathmoddb['contains_input']: [
            properties['contains'],
            items['input']
        ],
        mathmoddb['contains_constant']: [
            properties['contains'],
            items['constant']
        ],
        mathmoddb['contains_objective']: [
            properties['contains'],
            items['objective function']
        ],
        mathmoddb['contains_output']: [
            properties['contains'],
            items['output']
        ],
        mathmoddb['contains_parameter']: [
            properties['contains'],
            items['parameter']
        ],
        mathmoddb['contains_analytical_solution']: [
            properties['contains'],
            items['analytical solution']
        ],
        mathmoddb['contains_physical_law']: [
            properties['contains'],
            items['physical law']
        ],
        mathmoddb['contains_computational_domain']: [
            properties['contains'],
            items['computational domain']
        ],
        mathmoddb['contains_constitutive_equation']: [
            properties['contains'],
            items['constitutive equation']
        ],
        mathmoddb['contains_weak_formulation']: [
            properties['contains'],
            items['weak formulation']
        ],
        mathmoddb['contains_strong_formulation']: [
            properties['contains'],
            items['strong formulation']
        ],
        mathmoddb['documents']: [
            properties['described by source'],
            items['documentation']
        ],
        mathmoddb['invents']: [
            properties['described by source'],
            items['invention']
        ],
        mathmoddb['studies']: [
            properties['described by source'],
            items['study']
        ],
        mathmoddb['surveys']: [
            properties['described by source'],
            items['review']
        ],
        mathmoddb['uses']: [
            properties['described by source'],
            items['use']
        ],
        # Map MathModDB Relation on Wikibase Property + Direction
        mathmoddb['specialized_by']: [
            properties['specialized by'],
            'forward'
        ],
        mathmoddb['specializes']: [
            properties['specialized by'],
            'backward'
        ],
        mathmoddb['approximated_by']: [
            properties['approximated by'],
            'forward'
        ],
        mathmoddb['approximates']: [
            properties['approximated by'],
            'backward'
        ],
        mathmoddb['discretized_by']: [
            properties['discretized by'],
            'forward'
        ],
        mathmoddb['discretizes']: [
            properties['discretized by'],
            'backward'
        ],
        mathmoddb['linearized_by']: [
            properties['linearized by'],
            'forward'
        ],
        mathmoddb['linearizes']: [
            properties['linearized by'],
            'backward'
        ],
        mathmoddb['nondimensionalized_by']: [
            properties['nondimensionalized by'],
            'forward'
        ],
        mathmoddb['nondimensionalizes']: [
            properties['nondimensionalized by'],
            'backward'
        ],
        mathmoddb['contains']: [
            properties['contains'],
            'forward'
        ],
        mathmoddb['contained_in']: [
            properties['contains'],
            'backward'
        ],
        mathmoddb['similar_to']: [
            properties['similar to'],
            'forward'
        ]
    }
    return relations

# Parameter for Entity relations
preview_relations = [
    {
        "from_idx": "model",
        "to_idx": "problem",
        "relation": None,
        "old_name": "RPRelatant",
        "new_name": "RelationRP",
        "encryption": "RP",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "model",
        "to_idx": "formulation",
        "relation": "MM2MF",
        "old_name": "MFRelatant",
        "new_name": "RelationMF",
        "encryption": "ME",
        "formulation": True,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "model",
        "to_idx": "task",
        "relation": None,
        "old_name": "TRelatant",
        "new_name": "RelationT",
        "encryption": "T",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "model",
        "to_idx": "model",
        "relation": "IntraClassRelation",
        "old_name": "IntraClassElement",
        "new_name": "RelationMM",
        "encryption": "MM",
        "formulation": False,
        "task": False,
        "assumption": True,
    },
    {
        "from_idx": "task",
        "to_idx": "formulation",
        "relation": "T2MF",
        "old_name": "MFRelatant",
        "new_name": "RelationMF",
        "encryption": "ME",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "task",
        "to_idx": "quantity",
        "relation": "T2Q",
        "old_name": "QRelatant",
        "new_name": "RelationQQK",
        "encryption": "QQK",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "task",
        "to_idx": "task",
        "relation": "IntraClassRelation",
        "old_name": "IntraClassElement",
        "new_name": "RelationT",
        "encryption": "T",
        "formulation": False,
        "task": True,
        "assumption": True,
    },
    {
        "from_idx": "formulation",
        "to_idx": "formulation",
        "relation": "MF2MF",
        "old_name": "MFRelatant",
        "new_name": "RelationMF1",
        "encryption": "ME",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "formulation",
        "to_idx": "formulation",
        "relation": "IntraClassRelation",
        "old_name": "IntraClassElement",
        "new_name": "RelationMF2",
        "encryption": "ME",
        "formulation": False,
        "task": False,
        "assumption": True,
    },
    {
        "from_idx": "quantity",
        "to_idx": "quantity",
        "relation": "Q2Q",
        "old_name": "QRelatant-Q",
        "new_name": "RelationQQ",
        "encryption": "QQK",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "quantity",
        "to_idx": "quantity",
        "relation": "QK2QK",
        "old_name": "QKRelatant-QK",
        "new_name": "RelationQKQK",
        "encryption": "QQK",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "quantity",
        "to_idx": "quantity",
        "relation": "Q2QK",
        "old_name": "QKRelatant-Q",
        "new_name": "RelationQQK",
        "encryption": "QQK",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "quantity",
        "to_idx": "quantity",
        "relation": "QK2Q",
        "old_name": "QRelatant-QK",
        "new_name": "RelationQKQ",
        "encryption": "QQK",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "field",
        "to_idx": "field",
        "relation": "IntraClassRelation",
        "old_name": "IntraClassElement",
        "new_name": "RelationRF",
        "encryption": "AD",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "problem",
        "to_idx": "field",
        "relation": None,
        "old_name": "RFRelatant",
        "new_name": "RelationRF",
        "encryption": "AD",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "problem",
        "to_idx": "problem",
        "relation": "IntraClassRelation",
        "old_name": "IntraClassElement",
        "new_name": "RelationRP",
        "encryption": "RP",
        "formulation": False,
        "task": False,
        "assumption": False,
    },
    {
        "from_idx": "publication",
        "to_idx": [
            "field", "problem", "model",
            "formulation", "quantity", "task",
        ],
        "relation": "P2E",
        "old_name": "EntityRelatant",
        "new_name": "RelationP",
        "encryption": ["RF", "RP", "MM", "ME", "QQK", "T"],
        "formulation": False,
        "task": False,
        "assumption": False,
    },
]

preview_map_general = [
    # fromIDX, toIDX, entityOld, entityNew, enc
    ('model', 'formulation', 'assumption', 'assumptionMapped', 'ME'),
    ('task', 'formulation', 'assumption', 'assumptionMapped', 'ME'),
    ('formulation', 'formulation', 'assumption', 'assumptionMapped', 'ME'),
]

preview_map_quantity = [
    # type
    ('formulation'),
    ('quantity'),
]

# URI PREFIX Map (I)
def get_uri_prefix_map():
    '''URI Prefixes for the Model Documentation'''
    questions = get_questions('model')
    uri_prefix_map = {
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
            "prefix": "CT"
        }
    }
    return uri_prefix_map
