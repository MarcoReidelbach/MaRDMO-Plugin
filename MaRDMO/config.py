'''BASE URI and Endpoints required by MaRDMO'''

#RDMO BASE URI
BASE_URI = 'https://rdmo.mardi4nfdi.de/terms/'

# Endpoints
endpoint = {
    'mardi': {
        'api': 'https://portal.mardi4nfdi.de/w/api.php',
        'sparql': 'https://query.portal.mardi4nfdi.de/sparql',
        'uri': 'https://portal.mardi4nfdi.de'
              },
    'wikidata': {
        'api': 'https://www.wikidata.org/w/api.php',
        'sparql': 'https://query-main.wikidata.org/sparql',
        'sparql-scholarly': 'https://query-scholarly.wikidata.org/sparql',
        'uri': 'https://www.wikidata.org/wiki/Item:'
                },
    'mathalgodb': {
        'sparql': 'https://sparql.cordi2025.m1.mardi.ovh/mathalgodb/query',
        'update': 'https://sparql.cordi2025.m1.mardi.ovh/mathalgodb/update',
        'uri': 'https://cordi2025.m1.mardi.ovh/'
                  },
    'crossref': {
        'api': 'https://api.crossref.org/works/'
                 },
    'datacite': {
        'api': 'https://api.datacite.org/dois/'
                 },
    'doi': {
        'api': 'https://citation.doi.org/metadata?doi='
            },
    'zbmath': {
        'api': ('https://api.zbmath.org/v1/document/_structured_search'
                '?page=0&results_per_page=100&DOI=')
              },
    'orcid': {
        'api': 'https://pub.orcid.org/v3.0'
             }
    }
