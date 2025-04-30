# Dictionary with list of property names
PROPS = {
    'T2MF': ['containsAssumption','containsFormulation','containsBoundaryCondition','containsConstraintCondition','containsCouplingCondition','containsInitialCondition','containsFinalCondition'],
    'T2Q': ['containsInput','containsOutput','containsObjective','containsParameter','containsConstant'],
    'Q2MF': ['defines'],
    'RP2RF': ['containedInField'],
    'MM2RP': ['models'],
    'MM2T': ['usedBy'],
    'MM2MF': ['assumes', 'containsFormulation', 'containsBoundaryCondition', 'containsConstraintCondition', 'containsCouplingCondition', 'containsInitialCondition', 'containsFinalCondition'],
    'MF2MF': ['containedAsAssumptionIn','containedAsFormulationIn','containedAsBoundaryConditionIn','containedAsConstraintConditionIn','containedAsCouplingConditionIn','containedAsInitialConditionIn','containedAsFinalConditionIn','containsAssumption','containsFormulation','containsBoundaryCondition','containsConstraintCondition','containsCouplingCondition','containsInitialCondition','containsFinalCondition'],
    'Field': ["generalizedByField", "generalizesField", "similarToField"],
    'Problem': ["generalizedByProblem", "generalizesProblem", "similarToProblem"],
    'Model': ['specializedBy','specializes','discretizedBy','discretizes','containedInModel','containsModel','approximatedBy','approximates','linearizedBy','linearizes','similarTo'],
    'Task': ['generalizedByTask','generalizesTask','discretizedByTask','discretizesTask','containedInTask','containsTask','approximatedByTask','approximatesTask','linearizedByTask','linearizesTask','similarToTask'],
    'Formulation': ['generalizedByFormulation','generalizesFormulation','discretizedByFormulation','discretizesFormulation','approximatedByFormulation','approximatesFormulation','linearizedByFormulation','linearizesFormulation','nondimensionalizedByFormulation','nondimensionalizesFormulation','similarToFormulation'],
    'Quantity': ["generalizedByQuantity", "generalizesQuantity", "approximatedByQuantity", "approximatesQuantity", "linearizedByQuantity", "linearizesQuantity", "nondimensionalizedByQuantity", "nondimensionalizesQuantity", "similarToQuantity"],
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
