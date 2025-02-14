#RDMO BASE URI
BASE_URI = 'https://rdmo.mardi4nfdi.de/terms/'

#Portal URI, Wiki, API and SPARQL Endpoint
mardi_uri="https://portal.mardi4nfdi.de/wiki/Item:"
mardi_wiki="https://portal.mardi4nfdi.de/wiki/"
mardi_api="https://portal.mardi4nfdi.de/w/api.php"
mardi_endpoint="https://query.portal.mardi4nfdi.de/proxy/wdqs/bigdata/namespace/wdq/sparql"

#Wikidata URI, SPARQL, API Endpoint
wikidata_uri='https://www.wikidata.org/wiki/Item:'
wikidata_endpoint="https://query.wikidata.org/sparql"
wikidata_api="https://www.wikidata.org/w/api.php"

#MathModDB URI, SPARQL, Update Endpoint
mathmoddb_uri = 'https://mtsr2024.m1.mardi.ovh/object/mathmoddb:'
mathmoddb_endpoint = 'https://sparql.mtsr2024.m1.mardi.ovh/mathalgodb/query'
mathmoddb_update = 'https://sparql.mtsr2024.m1.mardi.ovh/mathalgodb/update'

#MathAlgoDB URI, SPARQL Endpoint
mathalgodb_endpoint = 'https://sparql.mtsr2024.m1.mardi.ovh/mathalgodb/query'
mathalgodb_uri = 'https://mtsr2024.m1.mardi.ovh/object/al:'

#SPARQL Prefixes
wd = '<https://portal.mardi4nfdi.de/entity/>'
wdt = '<https://portal.mardi4nfdi.de/prop/direct/>'

#Other APIs
crossref_api = 'https://api.crossref.org/works/'
datacite_api = 'https://api.datacite.org/dois/'
doi_api = 'https://citation.doi.org/metadata?doi='

# Endpoints
endpoint = {'mardi': {
                      'api': 'https://portal.mardi4nfdi.de/w/api.php',
                      'sparql': 'https://query.portal.mardi4nfdi.de/proxy/wdqs/bigdata/namespace/wdq/sparql',
                     },
           'wikidata': {
                        'api': 'https://www.wikidata.org/w/api.php',
                        'sparql': 'https://query.wikidata.org/sparql'
                       },
           'mathalgodb': {
                          'sparql': 'http://localhost:3030/mathalgodb/query',
                         },
           'mathmoddb': {
                          'sparql': 'http://localhost:3030/mathalgodb/query',
                         }
           }

