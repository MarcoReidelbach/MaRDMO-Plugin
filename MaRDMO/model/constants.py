'''Module containing Constants for the Model Documentation'''

from ..constants import BASE_URI
from ..getters import get_items, get_mathmoddb, get_properties, get_questions

# Data Properties Label
data_properties_label = {
    'is_deterministic': 'Is Deterministic',
    'is_stochastic': 'Is Stochastic',
    'is_dimensionless': 'Is Dimensionless',
    'is_dimensional': 'Is Dimensional',
    'is_dynamic': 'Is Dynamic',
    'is_static': 'Is Static',
    'is_linear': 'Is Linear',
    'is_not_linear': 'Is Not Linear',
    'is_space_continuous': 'Is Space-Continuous',
    'is_space_discrete': 'Is Space-Discrete',
    'is_time_continuous': 'Is Time-Continuous',
    'is_time_discrete': 'Is Time-Discrete',
    'is_mathematical_constant': 'Is Mathematical Constant',
    'is_physical_constant': 'Is Physical Constant',
    'is_chemical_constant': 'Is Chemical Constant',
    'is_ordinary_differential_equation': 'Is Ordinary Differential Equation',
    'is_partial_differential_equation': 'Is Partial Differential Equation',
    'is_stochastic_differential_equation': 'Is Stochastic Differential Equation',
    'is_integro_differential_equation': 'Is Integro-Differential Equation',
}

# Data Properties Check
data_properties_check = [
    ('is_deterministic', 'is_stochastic'),
    ('is_dimensionless', 'is_dimensional'),
    ('is_dynamic', 'is_static'),
    ('is_linear', 'is_not_linear'),
    ('is_space_continuous', 'is_space_discrete'),
    ('is_time_continuous', 'is_time_discrete'),
    ('is_mathematical_constant', 'is_physical_constant'),
    ('is_mathematical_constant', 'is_physical_constant'),
    ('is_ordinary_differential_equation', 'is_partial_differential_equation'),
    ('is_ordinary_differential_equation', 'is_stochastic_differential_equation'),
    ('is_ordinary_differential_equation', 'is_integro_differential_equation'),
    ('is_partial_differential_equation', 'is_stochastic_differential_equation'),
    ('is_partial_differential_equation', 'is_integro_differential_equation'),
    ('is_stochastic_differential_equation', 'is_integro_differential_equation'),
]

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
        'is_time_discrete', 'is_space_continuous', 'is_space_discrete',
        'is_ordinary_differential_equation', 'is_partial_differential_equation',
        'is_stochastic_differential_equation', 'is_integro_differential_equation'
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
        'similar_to',
        'has_weak_formulation',
        'is_weak_formulation_of'
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
        'similar_to',
        'has_weak_formulation',
        'is_weak_formulation_of'
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
        mathmoddb.get(key='is_ordinary_differential_equation')["url"]: items.get('ordinary differential equation'),
        mathmoddb.get(key='is_partial_differential_equation')["url"]: items.get('partial differential equation'),
        mathmoddb.get(key='is_stochastic_differential_equation')["url"]: items.get('stochastic differential equation'),
        mathmoddb.get(key='is_integro_differential_equation')["url"]: items.get('integro-differential equation'),
        mathmoddb.get(key='is_chemical_constant')["url"]: items.get('chemical constant'),
        mathmoddb.get(key='is_mathematical_constant')["url"]: items.get('mathematical constant'),
        mathmoddb.get(key='is_physical_constant')["url"]: items.get('physical constant'),
        mathmoddb.get(key='is_deterministic')["url"]: items.get(f'deterministic {item_type}'),
        mathmoddb.get(key='is_stochastic')["url"]: items.get(f'probabilistic {item_type}'),
        mathmoddb.get(key='is_dimensional')["url"]: items.get(f'dimensional {item_type}'),
        mathmoddb.get(key='is_dimensionless')["url"]: items.get(f'dimensionless {item_type}'),
        mathmoddb.get(key='is_dynamic')["url"]: items.get(f'dynamic {item_type}'),
        mathmoddb.get(key='is_static')["url"]: items.get(f'static {item_type}'),
        mathmoddb.get(key='is_linear')["url"]: items.get(f'linear {item_type}'),
        mathmoddb.get(key='is_not_linear')["url"]: items.get(f'nonlinear {item_type}'),
        mathmoddb.get(key='is_space_continuous')["url"]: items.get(f'continuous-space {item_type}'),
        mathmoddb.get(key='is_space_discrete')["url"]: items.get(f'discrete-space {item_type}'),
        mathmoddb.get(key='is_time_continuous')["url"]: items.get(f'continuous-time {item_type}'),
        mathmoddb.get(key='is_time_discrete')["url"]: items.get(f'discrete-time {item_type}')
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
        mathmoddb.get(key='assumes')['url']: [
            properties['assumes']
        ],
        mathmoddb.get(key='contains_boundary_condition')['url']: [
            properties['contains'],
            items['boundary condition']
        ],
        mathmoddb.get(key='contains_constraint_condition')['url']: [
            properties['contains'],
            items['constraint']
        ],
        mathmoddb.get(key='contains_coupling_condition')['url']: [
            properties['contains'],
            items['coupling condition']
        ],
        mathmoddb.get(key='contains_initial_condition')['url']: [
            properties['contains'],
            items['initial condition']
        ],
        mathmoddb.get(key='contains_final_condition')['url']: [
            properties['contains'],
            items['final condition']
        ],
        mathmoddb.get(key='contains_input')['url']: [
            properties['contains'],
            items['input']
        ],
        mathmoddb.get(key='contains_constant')['url']: [
            properties['contains'],
            items['constant']
        ],
        mathmoddb.get(key='contains_objective')['url']: [
            properties['contains'],
            items['objective function']
        ],
        mathmoddb.get(key='contains_output')['url']: [
            properties['contains'],
            items['output']
        ],
        mathmoddb.get(key='contains_parameter')['url']: [
            properties['contains'],
            items['parameter']
        ],
        mathmoddb.get(key='contains_analytical_solution')['url']: [
            properties['contains'],
            items['analytical solution']
        ],
        mathmoddb.get(key='contains_physical_law')['url']: [
            properties['contains'],
            items['physical law']
        ],
        mathmoddb.get(key='contains_computational_domain')['url']: [
            properties['contains'],
            items['computational domain']
        ],
        mathmoddb.get(key='contains_constitutive_equation')['url']: [
            properties['contains'],
            items['constitutive equation']
        ],
        mathmoddb.get(key='contains_weak_formulation')['url']: [
            properties['contains'],
            items['weak formulation']
        ],
        mathmoddb.get(key='contains_strong_formulation')['url']: [
            properties['contains'],
            items['strong formulation']
        ],
        mathmoddb.get(key='documents')['url']: [
            properties['described by source'],
            items['documentation']
        ],
        mathmoddb.get(key='invents')['url']: [
            properties['described by source'],
            items['invention']
        ],
        mathmoddb.get(key='studies')['url']: [
            properties['described by source'],
            items['study']
        ],
        mathmoddb.get(key='surveys')['url']: [
            properties['described by source'],
            items['review']
        ],
        mathmoddb.get(key='uses')['url']: [
            properties['described by source'],
            items['use']
        ],
        # Map MathModDB Relation on Wikibase Property + Direction
        mathmoddb.get(key='specialized_by')['url']: [
            properties['specialized by'],
            'forward'
        ],
        mathmoddb.get(key='specializes')['url']: [
            properties['specialized by'],
            'backward'
        ],
        mathmoddb.get(key='approximated_by')['url']: [
            properties['approximated by'],
            'forward'
        ],
        mathmoddb.get(key='approximates')['url']: [
            properties['approximated by'],
            'backward'
        ],
        mathmoddb.get(key='discretized_by')['url']: [
            properties['discretized by'],
            'forward'
        ],
        mathmoddb.get(key='discretizes')['url']: [
            properties['discretized by'],
            'backward'
        ],
        mathmoddb.get(key='linearized_by')['url']: [
            properties['linearized by'],
            'forward'
        ],
        mathmoddb.get(key='linearizes')['url']: [
            properties['linearized by'],
            'backward'
        ],
        mathmoddb.get(key='nondimensionalized_by')['url']: [
            properties['nondimensionalized by'],
            'forward'
        ],
        mathmoddb.get(key='nondimensionalizes')['url']: [
            properties['nondimensionalized by'],
            'backward'
        ],
        mathmoddb.get(key='contains')['url']: [
            properties['contains'],
            'forward'
        ],
        mathmoddb.get(key='contained_in')['url']: [
            properties['contains'],
            'backward'
        ],
        mathmoddb.get(key='similar_to')['url']: [
            properties['similar to'],
            'forward'
        ],
        mathmoddb.get(key='has_weak_formulation')['url']: [
            properties['has weak formulation'],
            'forward'
        ],
        mathmoddb.get(key='is_weak_formulation_of')['url']: [
            properties['has weak formulation'],
            'backward'
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
        "encryption": "CT",
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
        "encryption": "CT",
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
        "encryption": ["RF", "RP", "MM", "ME", "QQK", "CT"],
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
