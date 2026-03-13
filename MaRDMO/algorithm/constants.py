'''Module containing Constants for the Algorithm Documentation'''

from ..constants import BASE_URI, SECTION_MAP_BASE
from ..getters import get_items, get_mathalgodb, get_properties, get_questions

#Dictionary for internal / external section names
SECTION_MAP = {**SECTION_MAP_BASE, 'problem': 'Algorithmic Task'}

# Dictionary with list of property names
PROPS = {
    'A2P': ['solves'],
    'A2S': ['implemented_by'],
    'P2B': ['manifests'],
    'S2B': ['tested_by'],
    'Algorithm': ['has_component', 'component_of', 'has_subclass', 'subclass_of', 'related_to'],
    'Problem': ['specializes', 'specialized_by']
}

software_reference_ids = [
    'DOI',
    'SWMATH',
    'SOURCECODE_URL',
    'DESCRIPTION_URL'
]

benchmark_reference_ids = [
    'DOI',
    'MORWIKI',
    'SOURCECODE_URL',
    'DESCRIPTION_URL'
]

# Relations
def get_relations():
    '''Relations for the Model Documentation'''
    mathalgodb = get_mathalgodb()
    items = get_items()
    properties = get_properties()
    relations = {
        # Map MathModDB Relation on Wikibase Property + Qualifier Item
        mathalgodb.get(key='manifests')['url']: [
            properties['manifestation of']
        ],
        mathalgodb.get(key='solves')['url']: [
            properties['solved by']
        ],
        mathalgodb.get(key='tested_by')['url']: [
            properties['tested by']
        ],
        mathalgodb.get(key='implemented_by')['url']: [
            properties['implemented by']
        ],
        mathalgodb.get(key='documents')['url']: [
            properties['described by source'],
            items['documentation']
        ],
        mathalgodb.get(key='invents')['url']: [
            properties['described by source'],
            items['invention']
        ],
        mathalgodb.get(key='studies')['url']: [
            properties['described by source'],
            items['study']
        ],
        mathalgodb.get(key='surveys')['url']: [
            properties['described by source'],
            items['review']
        ],
        mathalgodb.get(key='uses')['url']: [
            properties['described by source'],
            items['use']
        ],
        mathalgodb.get(key='applies')['url']: [
            properties['described by source'],
            items['application']
        ],
        mathalgodb.get(key='analyzes')['url']: [
            properties['described by source'],
            items['analysis']
        ],
        # Map MathModDB Relation on Wikibase Property + Direction
        mathalgodb.get(key='specialized_by')['url']: [
            properties['specialized by'],
            'forward'
        ],
        mathalgodb.get(key='specializes')['url']: [
            properties['specialized by'],
            'backward'
        ],
        mathalgodb.get(key='has_component')['url']: [
            properties['has part(s)'],
            'forward'
        ],
        mathalgodb.get(key='component_of')['url']: [
            properties['has part(s)'],
            'backward'
        ],
        mathalgodb.get(key='has_subclass')['url']: [
            properties['subclass of'],
            'forward'
        ],
        mathalgodb.get(key='subclass_of')['url']: [
            properties['subclass of'],
            'backward'
        ],
        mathalgodb.get(key='related_to')['url']: [
            properties['similar to'],
            'forward'
        ],
    }
    return relations

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
            "prefix": "AT"
        },
        f'{BASE_URI}{questions["Algorithm"]["SRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Software"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Software"]["ID"]["uri"]}',
            "prefix": "S"
        }
    }
    return uri_prefix_map

# Parameter for Entity relations
preview_relations = [
    {
        "from_idx": "algorithm",
        "to_idx": "problem",
        "relation": None,
        "old_name": "PRelatant",
        "new_name": "RelationP",
        "encryption": "AT"
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
        "encryption": "AT"
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
        "to_idx": [
            "benchmark", "software"
        ],
        "relation": "P2BS",
        "old_name": "BSRelatant",
        "new_name": "RelationBS",
        "encryption": ["B", "S"]
    }
]
