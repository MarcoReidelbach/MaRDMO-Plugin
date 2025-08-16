'''Functional Rules to feed User Answers in Dict'''

from .helpers import basic_dict, basic_list

def rule_0(value, attribute, config, _prefix_idx):
    "Handle Flag Combo 0 for Get Answers"
    entry = getattr(value, attribute)
    path = [config["key1"], config["key2"]]
    return entry, path

def rule_1(value, attribute, config, prefix_idx):
    "Handle Flag Combo 1 for Get Answers"
    entry = getattr(value, attribute)
    path = [config["key1"], prefix_idx, config["key2"]]
    return entry, path

def rule_2(value, attribute, config, _prefix_idx):
    "Handle Flag Combo 2 for Get Answers"
    entry = getattr(value, attribute)
    path = [config["key1"], value.set_index, config["key2"]]
    return entry, path

def rule_3(value, attribute, config, prefix_idx):
    "Handle Flag Combo 3 for Get Answers"
    entry = getattr(value, attribute)
    path = [config["key1"], prefix_idx, config["key2"], value.set_index]
    if config["key3"]:
        path.append(config["key3"])
    return entry, path

def rule_4(value, attribute, config, _prefix_idx):
    "Handle Flag Combo 4 for Get Answers"
    if attribute == 'text':
        entry = getattr(value, attribute)
    else:
        entry = basic_list(value)
    path = [config["key1"], value.set_index, config["key2"], value.collection_index]
    if config["key3"]:
        path.append(config["key3"])
    return entry, path

def rule_5(value, attribute, config, prefix_idx):
    "Handle Flag Combo 5 for Get Answers"
    if config["key2"] == 'reference':
        entry = basic_list(value)
    else:
        entry = getattr(value, attribute)
    path = [config["key1"], prefix_idx, config["key2"], value.collection_index]
    return entry, path

def rule_6(value, _attribute, config, prefix_idx):
    "Handle Flag Combo 6 for Get Answers"
    entry = basic_list(value)
    path = [config["key1"], prefix_idx, config["key2"], value.set_index, value.collection_index]
    return entry, path

def rule_7(value, _attribute, config, prefix_idx):
    "Handle Flag Combo 7 for Get Answers"
    entry = basic_list(value)
    path = [config["key1"], prefix_idx, config["key2"]]
    return entry, path

def rule_8(value, _attribute, config, _prefix_idx):
    "Handle Flag Combo 8 for Get Answers"
    entry = basic_list(value)
    path = [config["key1"], value.set_index, config["key2"]]
    return entry, path

def rule_9(value, _attribute, config, _prefix_idx):
    "Handle Flag Combo 9 for Get Answers"
    entry = basic_dict(value)
    path = [config["key1"]]
    return entry, path

def rule_10(value, attribute, config, _prefix_idx):
    "Handle Flag Combo 10 for Get Answers"
    entry = getattr(value, attribute)
    path = [config["key1"], config["key2"], value.collection_index]
    return entry, path

def rule_11(value, _attribute, config, _prefix_idx):
    "Handle Flag Combo 11 for Get Answers"
    entry = basic_dict(value)
    path = [config["key1"], config["key2"], value.collection_index]
    return entry, path

def rule_12(value, _attribute, config, _prefix_idx):
    "Handle Flag Combo 12 for Get Answers"
    entry = value.external_id
    path = [config["key1"], value.set_index, config["key2"]]
    return entry, path

def rule_13(value, _attribute, config, prefix_idx):
    "Handle Flag Combo 13 for Get Answers"
    if config["key2"] == 'DefinedQuantity':
        entry = basic_dict(value)
    else:
        entry = value.external_id
    path = [config["key1"], prefix_idx, config["key2"]]
    return entry, path

def rule_14(value, _attribute, config, prefix_idx):
    "Handle Flag Combo 14 for Get Answers"
    entry = basic_dict(value)
    path = [config["key1"], prefix_idx, config["key2"], value.set_index]
    if config["key3"]:
        path.append(config["key3"])
    return entry, path

def rule_15(value, _attribute, config, prefix_idx):
    "Handle Flag Combo 15 for Get Answers"
    entry = basic_dict(value)
    path = [config["key1"], prefix_idx,config["key2"], value.collection_index]
    return entry, path

def rule_16(value, _attribute, config, prefix_idx):
    "Handle Flag Combo 16 for Get Answers"
    entry = basic_dict(value)
    path = [config["key1"], prefix_idx, config["key2"], value.set_index, value.collection_index]
    return entry, path
