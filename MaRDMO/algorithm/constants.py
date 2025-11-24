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
PREVIEW_RELATIONS = [
    # fromIDX, toIDX, relationOld, entityOld, entityNew, enc
    ('algorithm', 'problem', 'A2P', 'PRelatant', 'RelationP', 'AP'),
    ('algorithm', 'software', 'A2S', 'SRelatant', 'RelationS', 'S'),
    ('algorithm', 'algorithm', 'IntraClassRelation', 'IntraClassElement', 'RelationA', 'A'),
    ('problem', 'benchmark', 'P2B', 'BRelatant', 'RelationB', 'B'),
    ('problem', 'problem', 'IntraClassRelation', 'IntraClassElement', 'RelationP', 'AP'),
    ('software', 'benchmark', 'S2B', 'BRelatant', 'RelationB', 'B'),
    ('publication', 'algorithm', 'P2A', 'ARelatant', 'RelationA', 'A'),
    ('publication', 'benchmark', 'P2B', 'BRelatant', 'RelationB', 'B'),
    ('publication', 'software', 'P2S', 'SRelatant', 'RelationS', 'S')
]
