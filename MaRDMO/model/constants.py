from ..utils import get_data

mathmoddb = get_data('model/data/mapping.json')

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



