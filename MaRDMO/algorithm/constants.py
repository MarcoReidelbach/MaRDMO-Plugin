from ..config import BASE_URI
from ..utils import get_data, get_questionsAL

options = get_data('data/options.json')

# Dictionary with list of property names
PROPS = {
    'A2P': ['solves'],
    'A2S': ['implementedBy'],
    'P2B': ['instantiates'],
    'S2B': ['tests'],
    'Algorithm': ['hasComponent', 'componentOf', 'hasSubclass', 'subclassOf', 'relatedTo'],
    'Problem': ['specializes', 'specializedBy']
}

# Order of References
reference_order_benchmark = {
            'doi': (0, options['DOI']),
            'morwiki': (1, options['MORWIKI']),
            'url': (2, options['URL']),
            }

reference_order_software = {
            'doi': (0, options['DOI']),
            'swmath': (1, options['SWMATH']),
            'url': (2, options['URL']),
            }

# URI PREFIX Map
def get_URI_PREFIX_MAP():
    questions = get_questionsAL()
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
