#RDMO BASE URI
BASE_URI = 'https://rdmo.mardi4nfdi.de/terms/'

#SPARQL Prefixes
wd = '<https://portal.mardi4nfdi.de/entity/>'
wdt = '<https://portal.mardi4nfdi.de/prop/direct/>'

# Endpoints
endpoint = {'mardi': {
                      'api': 'https://staging.mardi4nfdi.org/w/api.php', #'https://portal.mardi4nfdi.de/w/api.php', #"http://localhost:8888/w/api.php"
                      'sparql': 'https://query.staging.mardi4nfdi.org/proxy/wdqs/bigdata/namespace/wdq/sparql', #'https://query.portal.mardi4nfdi.de/proxy/wdqs/bigdata/namespace/wdq/sparql', #"http://localhost:8834/proxy/wdqs/bigdata/namespace/wdq/sparql"
                      'uri': 'https://staging.mardi4nfdi.org/', #"https://portal.mardi4nfdi.de/wiki/Item:", "http://localhost:8888/wiki/Item:"
                     },
           'wikidata': {
                        'api': 'https://www.wikidata.org/w/api.php',
                        'sparql': 'https://query.wikidata.org/sparql',
                        'uri': 'https://www.wikidata.org/wiki/Item:'
                       },
           'mathalgodb': {
                          'sparql': 'http://localhost:3030/mathalgodb/query', #'https://sparql.mtsr2024.m1.mardi.ovh/mathalgodb/query'
                          'update': 'http://localhost:3030/mathalgodb/update',
                          'uri': 'http://localhost:8080/' #'https://mtsr2024.m1.mardi.ovh/'
                         },
           'mathmoddb': {
                          'sparql': 'http://localhost:3030/mathalgodb/query', #'https://sparql.mtsr2024.m1.mardi.ovh/mathalgodb/query'
                          'update': 'http://localhost:3030/mathalgodb/update',
                          'uri': 'http://localhost:8080/' #https://mtsr2024.m1.mardi.ovh/
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
                      'api': 'https://api.zbmath.org/v1/document/_structured_search?page=0&results_per_page=100&external%20id='
                     },
           'orcid': {
                     'api': 'https://pub.orcid.org/v3.0'
                    }
           }


