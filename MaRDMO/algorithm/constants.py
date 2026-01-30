'''Module containing Constants for the Algorithm Documentation'''

from ..constants import BASE_URI
from ..getters import get_questions

# Dictionary with list of property names
PROPS = {
    'A2P': ['solves'],
    'A2S': ['implementedBy'],
    'P2B': ['instantiates'],
    'S2B': ['tests'],
    'Algorithm': ['hasComponent', 'componentOf', 'hasSubclass', 'subclassOf', 'relatedTo'],
    'Problem': ['specializes', 'specializedBy']
}

# URI PREFIX Map
def get_uri_prefix_map():
    '''URI Prefixes for the Algorithm Documentation'''
    questions = get_questions('algorithm')
    uri_prefix_map = {
        f'{BASE_URI}{questions["Problem"]["BRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Benchmark"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Benchmark"]["ID"]["uri"]}',
            "prefix": "B"
        },
        f'{BASE_URI}{questions["Software"]["BRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Benchmark"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Benchmark"]["ID"]["uri"]}',
            "prefix": "B"
        },
        f'{BASE_URI}{questions["Algorithm"]["PRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Problem"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Problem"]["ID"]["uri"]}',
            "prefix": "AP"
        },
        f'{BASE_URI}{questions["Algorithm"]["SRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Software"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Software"]["ID"]["uri"]}',
            "prefix": "S"
        }
    }
    return uri_prefix_map

class_prefix_map = {
        'algorithm': 'al',
        'problem': 'pr',
        'benchmark': 'bm',
        'software': 'sw',
        'publication': 'pb',
    }

# Parameter for Entity relations
preview_relations = [
    {
        "from_idx": "algorithm",
        "to_idx": "problem",
        "relation": None,
        "old_name": "PRelatant",
        "new_name": "RelationP",
        "encryption": "AP"
    },
    {
        "from_idx": "algorithm",
        "to_idx": "software",
        "relation": None,
        "old_name": "SRelatant",
        "new_name": "RelationS",
        "encryption": "S"
    },
    {
        "from_idx": "algorithm",
        "to_idx": "algorithm",
        "relation": "IntraClassRelation",
        "old_name": "IntraClassElement",
        "new_name": "RelationA",
        "encryption": "A"
    },
    {
        "from_idx": "problem",
        "to_idx": "benchmark",
        "relation": None,
        "old_name": "BRelatant",
        "new_name": "RelationB",
        "encryption": "B"
    },
    {
        "from_idx": "problem",
        "to_idx": "problem",
        "relation": "IntraClassRelation",
        "old_name": "IntraClassElement",
        "new_name": "RelationP",
        "encryption": "AP"
    },
    {
        "from_idx": "software",
        "to_idx": "benchmark",
        "relation": None,
        "old_name": "BRelatant",
        "new_name": "RelationB",
        "encryption": "B"
    },
    {
        "from_idx": "publication",
        "to_idx": "algorithm",
        "relation": "P2A",
        "old_name": "ARelatant",
        "new_name": "RelationA",
        "encryption": "A"
    },
    {
        "from_idx": "publication",
        "to_idx": "benchmark",
        "relation": "P2B",
        "old_name": "BRelatant",
        "new_name": "RelationB",
        "encryption": "B"
    },
    {
        "from_idx": "publication",
        "to_idx": "software",
        "relation": "P2S",
        "old_name": "SRelatant",
        "new_name": "RelationS",
        "encryption": "S"
    }
]
