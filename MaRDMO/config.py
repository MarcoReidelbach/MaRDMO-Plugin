# this should be refactored into one Config object,
# it could be simple dict, or configDict, or BaseModel
# and then all the configuration settings should be collected here
# maybe reuse the django.conf settings

#RDMO BASE URI
BASE_URI = 'https://rdmo.mardi4nfdi.de/terms/'

#Portal Wiki, Api and SPARQL Endpoint
mardi_wiki="https://portal.mardi4nfdi.de/wiki/"
mardi_api="https://portal.mardi4nfdi.de/w/api.php"
mardi_endpoint="https://query.portal.mardi4nfdi.de/proxy/wdqs/bigdata/namespace/wdq/sparql"

#Wikidata SPARQL, Api Endpoint
wikidata_endpoint="https://query.wikidata.org/sparql"
wikidata_api="https://www.wikidata.org/w/api.php"

#MathModDB SPARQL Endpoint
mathmoddb_endpoint = 'https://sparql.mtsr2024.m1.mardi.ovh/mathalgodb/query'
mathmoddb_update = 'https://sparql.mtsr2024.m1.mardi.ovh/mathalgodb/update'

#SPARQL Prefixes
wd = '<https://portal.mardi4nfdi.de/entity/>'
wdt = '<https://portal.mardi4nfdi.de/prop/direct/>'
