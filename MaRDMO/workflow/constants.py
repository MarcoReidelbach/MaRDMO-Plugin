from ..utils import get_data

options = get_data('data/options.json')

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
    'S2DP': ['dependsOnSoftware']
}

# Order of References
reference_order_software = {
            'doi': (0, options['DOI']),
            'swmath': (1, options['SWMATH']),
            'url': (2, options['URL']),
            }