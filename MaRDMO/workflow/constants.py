from ..constants import BASE_URI
from ..getters import get_options, get_questions

# URI PREFIX Map
def get_uri_prefix_map():
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
    'PS2IDS': ['inputDataSet'],
    'PS2ODS': ['outputDataSet'],
    'PS2M': ['uses'],
    'PS2PLS': ['platformSoftware'],
    'PS2PLI': ['platformInstrument'],
    'PS2F': ['fieldOfWork'],
    'PS2MA': ['mscID'],
    'M2S': ['implementedBySoftware'],
    'M2I': ['implementedByInstrument'],
    'S2PL': ['programmedIn'],
    'S2DP': ['dependsOnSoftware'],
    'H2CPU': ['CPU'],
    'DS2DT': ['dataType'],
    'DS2RF': ['representationFormat']
}

# Order of toPublish Answers
def order_to_publish(): 
    options = get_options()
    order = {
        'Yes': (0, options['Yes']),
        'doi': (1, options['DOI']),
        'url': (2, options['URL']),
        'No': (3, options['URL'])
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

