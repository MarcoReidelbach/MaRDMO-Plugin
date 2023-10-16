from wikibaseintegrator import wbi_login, WikibaseIntegrator
from wikibaseintegrator.datatypes import Item, Property
from wikibaseintegrator.wbi_enums import ActionIfExists
from wikibaseintegrator.wbi_config import config as wbi_config

from MaRDMO.config import *
import re, requests

def wikibase_login():
    '''Login stuff for wikibase'''
    wbi_config['MEDIAWIKI_API_URL'] = mardi_api
    login_instance = wbi_login.Login(user=lgname, password=lgpassword)
    wbi = WikibaseIntegrator(login=login_instance)
    return wbi

def get_results(endpoint_url, query):
    '''Perform SPARQL Queries via Get requests'''
    req=requests.get(endpoint_url, params = {'format': 'json', 'query': query}).json()
    return req["results"]["bindings"]

def item_entry(ITEM):
    '''Generates Item for Testing'''
    wbi = wikibase_login()
    item = wbi.item.new()
    # Item name as label, description is 'MaRDMO Test Item'
    item.labels.set(language='en', value=ITEM)
    item.descriptions.set(language='en', value='MaRDMO Item')
    item.write()
    return item.id

def property_entry(NAME,PROPTYPE):
    '''Generates Property for Testing'''
    wbi = wikibase_login()
    prop = wbi.property.new()
    # Item name as label, description is 'MaRDMO Test Property'
    prop.labels.set(language='en', value=NAME)
    prop.descriptions.set(language='en', value='MaRDMO Property')
    prop.datatype = PROPTYPE
    prop.write()
    return prop.id

items = [['Q1','scholarly article'],['Q2','research workflow'],['Q3','mathematical model'],['Q4','method'],['Q5','software'],
        ['Q6','data set'],['Q7','human'],['Q8','researcher'],['Q9','scientific journal'],['Q10','publication'],['Q11','language']]

properties = [['P1','Wikidata PID','external-id'],['P2','Wikidata QID','external-id'],['P3','cites work','wikibase-item'],['P4','instance of','wikibase-item'],
              ['P5','field of work','wikibase-item'],['P6','uses','wikibase-item'],['P7','title','monolingualtext'],['P8','author','wikibase-item'],
              ['P9','author name string','string'],['P10','language of work or name','wikibase-item'],['P11','publication date','time'],
              ['P12','published in','wikibase-item'],['P13','volume','string'],['P14','issue','string'],['P15','page(s)','string'],['P16','DOI','external-id'],
              ['P17','main subject','wikibase-item'],['P18','defining formula','math'],['P19','programmed in','wikibase-item'],
              ['P20','swMath work ID','external-id'],['P21','occupation','wikibase-item'],['P22','ORCID iD','external-id']]


query_item='''
PREFIX wdt: '''+wdt+'''
PREFIX wd: '''+wd+'''
SELECT ?qid
WHERE {
?item rdfs:label "ITEM"@en.
BIND(STRAFTER(STR(?item),STR(wd:)) AS ?qid)
}
LIMIT 1'''

query_property='''
PREFIX wdt: '''+wdt+'''
PREFIX wd: '''+wd+'''
SELECT ?pid
WHERE {
?item rdfs:label "PROPERTY"@en;
      rdf:type ?type.
BIND(STRAFTER(STR(?item),STR(wd:)) AS ?pid)
}
LIMIT 1'''

f=open('MaRDMO/id.py','w')
f.write('#Item IDs (QIDs)\n\n')
for item in items:
    qid = get_results(mardi_endpoint,re.sub('ITEM',item[1],query_item))
    if qid:
        f.write(item[0]+"='"+qid[0]["qid"]["value"]+"'\n")
    else:
        qid=item_entry(item[1])
        f.write(item[0]+"='"+qid+"'\n")
f.write('\n#Property IDs (PIDs)\n\n')
for prop in properties:
    pid = get_results(mardi_endpoint,re.sub('PROPERTY',prop[1],query_property))
    if pid:
        f.write(prop[0]+"='"+pid[0]["pid"]["value"][1:]+"'\n")
    else:
        pid=property_entry(prop[1],prop[2])
        f.write(prop[0]+"='"+pid[1:]+"'\n")



