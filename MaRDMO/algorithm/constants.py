from ..utils import get_data

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
