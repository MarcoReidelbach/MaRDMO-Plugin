'''Module containing Constants for the Workflow Documentation'''

from ..constants import BASE_URI
from ..getters import get_options, get_questions

software_reference_ids = [
    'DOI',
    'SWMATH',
    'SOURCECODE_URL',
    'DESCRIPTION_URL'
]

data_set_reference_ids = [
    'Yes',
    'DOI',
    'URL',
    'No'
]

# URI PREFIX Map
def get_uri_prefix_map():
    '''URI Prefixes for the Workflow Documentation'''
    questions = get_questions('workflow')
    URI_PREFIX_MAP = {
        f'{BASE_URI}{questions["Process Step"]["Input"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Data Set"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Data Set"]["ID"]["uri"]}',
            "prefix": "DS"
        },
        f'{BASE_URI}{questions["Process Step"]["Output"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Data Set"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Data Set"]["ID"]["uri"]}',
            "prefix": "DS"
        },
        f'{BASE_URI}{questions["Process Step"]["Method"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Method"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Method"]["ID"]["uri"]}',
            "prefix": "M"
        },
        f'{BASE_URI}{questions["Process Step"]["Environment-Software"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Software"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Software"]["ID"]["uri"]}',
            "prefix": "S"
        },
        f'{BASE_URI}{questions["Process Step"]["Environment-Instrument"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Instrument"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Instrument"]["ID"]["uri"]}',
            "prefix": "I"
        },
        f'{BASE_URI}{questions["Method"]["Software"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Software"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Software"]["ID"]["uri"]}',
            "prefix": "S"
        },
        f'{BASE_URI}{questions["Method"]["Instrument"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Instrument"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Instrument"]["ID"]["uri"]}',
            "prefix": "I"
        },
        f'{BASE_URI}{questions["Instrument"]["Software"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Software"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Software"]["ID"]["uri"]}',
            "prefix": "S"
        },
        f'{BASE_URI}{questions["Hardware"]["Software"]["uri"]}': {
            "question_set": f'{BASE_URI}{questions["Software"]["uri"]}',
            "question_id": f'{BASE_URI}{questions["Software"]["ID"]["uri"]}',
            "prefix": "S"
        }
    }
    return URI_PREFIX_MAP


# Dictionary with list of property names
PROPS = {
    'PS2IDS': ['input_data_set'],
    'PS2ODS': ['output_data_set'],
    'PS2M': ['uses'],
    'PS2PLS': ['platform_software'],
    'PS2PLI': ['platform_instrument'],
    'PS2F': ['field_of_work'],
    'PS2MA': ['msc_id'],
    'M2S': ['implemented_by_software'],
    'M2I': ['implemented_by_instrument'],
    'S2PL': ['programmed_in'],
    'S2DP': ['depends_on_software'],
    'H2CPU': ['cpu'],
    'DS2DT': ['data_type'],
    'DS2RF': ['representation_format']
}

# Order of toPublish Answers
def order_to_publish():
    options = get_options()
    order = {
        'Yes': (0, options['Yes']),
        'doi': (1, options['DOI']),
        'url': (2, options['URL']),
        'No': (3, options['No'])
        }
    return order

#Dictionary For Reproducibility
REPRODUCIBILITY = {
    'mathematical': 'mathematically reproducible research workflow',
    'runtime': 'runtime reproducible research workflow',
    'result': 'result reproducible research workflow',
    'originalplatform': 'original platform reproducible research workflow',
    'otherplatform': 'cross-platform reproducible research workflow'
    }
