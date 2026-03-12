'''General Constants used in MaRDMO'''

from . import rules

#RDMO BASE URI
BASE_URI = 'https://rdmo.mardi4nfdi.de/terms/'

#MaRDMO Catalog URIs
CATALOG_MODEL        = 'https://rdmo.mardi4nfdi.de/terms/questions/mardmo-model-catalog'
CATALOG_MODEL_BASICS = 'https://rdmo.mardi4nfdi.de/terms/questions/mardmo-model-basics-catalog'
CATALOG_ALGORITHM    = 'https://rdmo.mardi4nfdi.de/terms/questions/mardmo-algorithm-catalog'

#MaRDMO Section Mapt (Base)
SECTION_MAP_BASE = {
    'model':       'Mathematical Model',
    'task':        'Computational Task',
    'formulation': 'Mathematical Expression',
    'quantity':    'Quantity [Kind]',
    'field':       'Academic Discipline',
    'algorithm':   'Algorithm',
    'software':    'Software',
    'benchmark':   'Benchmark',
    'publication': 'Publication',
}

flag_dict = {
    (False, False, False, False, False): rules.rule_0,
    (True, False, False, False, False): rules.rule_1,
    (False, True, False, False, False): rules.rule_2,
    (True, True, False, False, False): rules.rule_3,
    (False, True, True, False, False): rules.rule_4,
    (True, False, True, False, False): rules.rule_5,
    (True, True, True, False, False): rules.rule_6,
    (True, False, False, False, True): rules.rule_7,
    (False, True, False, False, True): rules.rule_8,
    (False, False, False, True, False): rules.rule_9,
    (False, False, True, False, False): rules.rule_10,
    (False, False, True, True, False): rules.rule_11,
    (False, True, False, True, False): rules.rule_12,
    (True, False, False, True, False): rules.rule_13,
    (True, True, False, True, False): rules.rule_14,
    (True, False, True, True, False): rules.rule_15,
    (True, True, True, True, False): rules.rule_16,
}
