from ..config import BASE_URI
from ..getters import get_questions_algorithm

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
def get_URI_PREFIX_MAP():
    questions = get_questions_algorithm()
    URI_PREFIX_MAP = {
        f'{BASE_URI}{questions["Problem BRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Benchmark"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Benchmark ID"]["uri"]}',
            "prefix": "B"
        },
        f'{BASE_URI}{questions["Software BRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Benchmark"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Benchmark ID"]["uri"]}',
            "prefix": "B"
        },
        f'{BASE_URI}{questions["Algorithm PRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Problem"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Problem ID"]["uri"]}',
            "prefix": "AP"
        },
        f'{BASE_URI}{questions["Algorithm SRelatant"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Software"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Software ID"]["uri"]}',
            "prefix": "S"
        }
    }
    return URI_PREFIX_MAP
