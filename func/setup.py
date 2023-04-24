from wikibaseintegrator import wbi_login, WikibaseIntegrator
from wikibaseintegrator.datatypes import Item, Property
from wikibaseintegrator.wbi_enums import ActionIfExists
from wikibaseintegrator.wbi_config import config as wbi_config

from config import *
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
    x=str(item.write())
    qid=re.search("_BaseEntity__id='(.*?)'",x).group(1)
    return qid

def property_entry(PROP):
    '''Generates Property for Testing'''
    wbi = wikibase_login()
    prop = wbi.property.new()
    # Item name as label, description is 'MaRDMO Test Property'
    prop.labels.set(language='en', value=PROP)
    prop.descriptions.set(language='en', value='MaRDMO Property')
    prop.datatype = 'wikibase-item'
    x=str(prop.write())
    pid=re.search("_BaseEntity__id='(.*?)'",x).group(1)
    return pid

items = [['scholarly_article','scholarly article'],['research_workflow','research workflow'],['mathematical_model','mathematical model'],['method','method'],
         ['software','software'],['data_set','data set'],['human','human'],['researcher','researcher'],['scientific_journal','scientific journal'],['publication','publication'],
         ['language','language']]

properties = [['wikidata_pid','Wikidata PID','external-id'],['wikidata_qid','Wikidata QID','external-id'],['cites_work','cites work','wikibase-item'],['instance_of','instance of','wikibase-item'],
              ['field_of_work','field of work','wikibase-item'],['uses','uses','wikibase-item'],['title','title','monolingualtext'],['Author','author','wikibase-item'],
              ['author_name_string','author name string','string'],['language_of_work_or_name','language of work or name','wikibase-item'],['publication_date','publication date','time'],
              ['published_in','published in','wikibase-item'],['volume','volume','string'],['issue','issue','string'],['pages','page(s)','string'],['DOI','DOI','external-id'],
              ['main_subject','main subject','wikibase-item'],['defining_formula','defining formula','math'],['programmed_in','programmed in','wikibase-item'],
              ['swMath_work_ID','swMath work ID','external-id'],['occupation','occupation','wikibase-item'],['ORCID_iD','ORCID iD','external-id']]


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

f=open('id.py','w')
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
        pid=property_entry(prop[1])
        f.write(prop[0]+"='"+pid[1:]+"'\n")



