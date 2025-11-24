'''General Constants used in MaRDMO'''

from . import rules

#RDMO BASE URI
BASE_URI = 'https://rdmo.mardi4nfdi.de/terms/'

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
