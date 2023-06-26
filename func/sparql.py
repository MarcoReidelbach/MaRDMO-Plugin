from .config import *
from .id import *

#SPARQL Query stringis for Workflow Search Base + Specifics

query_base="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""
SELECT DISTINCT ?label
WHERE {
ITEMFINDER
STATEMENT
FILTER
}
LIMIT 10"""

statement_obj="""?t p:P"""+instance_of+""" ?s.
?t rdfs:label ?label.
?t schema:description ?quote.
"""

statement_mms="""?y rdfs:label ?label."""

#SPARQL Query strings for MaRDI Knowledge Graph Integration
##Queries to MaRDI Knowledge Graph 

doi_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?qid WHERE {{?publication wdt:P"+DOI+" '{}'.BIND(STRAFTER(STR(?publication),STR(wd:)) AS ?qid)}} LIMIT 1",
           "SELECT ?qid ?label ?quote WHERE {{?publication wdt:P356 '{}';rdfs:label ?label;schema:description ?quote.BIND(STRAFTER(STR(?publication),STR(wd:)) AS ?qid) FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1"]

author_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?qid WHERE {{?author wdt:P"+ORCID_iD+" '{}'.BIND(STRAFTER(STR(?author),STR(wd:)) AS ?qid)}} LIMIT 1",
              "SELECT ?qid ?label ?quote WHERE {{?author wdt:P496 '{}';rdfs:label ?label;schema:description ?quote.BIND(STRAFTER(STR(?author),STR(wd:)) AS ?qid) FILTER (lang(?label) = 'en')FILTER (lang(?quote) = 'en')}} LIMIT 1"]

journal_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?qid WHERE {{?journal rdfs:label ?label.FILTER (lcase(str(?label)) = '{}') BIND(STRAFTER(STR(?journal),STR(wd:)) AS ?qid)}} LIMIT 1",
               "SELECT ?qid ?label ?quote WHERE {{?journal wdt:P31 wd:Q5633421;rdfs:label ?label;schema:description ?quote. FILTER (lcase(str(?label)) = '{}') FILTER (lang(?quote) = 'en') BIND(STRAFTER(STR(?journal),STR(wd:)) AS ?qid)}} LIMIT 1"]

model_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}}",
             "SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}}"]

method_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1",
              "SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1"]

software_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1",
                "SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1"]

input_query=["PREFIX wdt:"+wdt+"PREFIX wd:"+wd+" SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1",
             "SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1"]

output_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1",
              "SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1"]

discipline_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label;schema:description ?quote.FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1",                  "SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label;schema:description ?quote.FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1"]

planguage_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1",
                 "SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en')}} LIMIT 1"]

main_subject_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en')FILTER (lang(?quote) = 'en')}} LIMIT 1",
                    "SELECT ?label ?quote WHERE {{wd:{} rdfs:label ?label; schema:description ?quote. FILTER (lang(?label) = 'en'). FILTER (lang(?quote) = 'en')}} LIMIT 1"]

language_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?qid WHERE {{?language rdfs:label '{}'@en; skos:altLabel '{}'@en; BIND(STRAFTER(STR(?language),STR(wd:)) AS ?qid)}} LIMIT 1",
                "SELECT ?qid ?label ?quote WHERE {{?language rdfs:label '{}'@en; rdfs:label ?label; schema:description ?quote; skos:altLabel '{}'@en. FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en') BIND(STRAFTER(STR(?language),STR(wd:)) AS ?qid)}} LIMIT 1"]

title_query=["PREFIX wdt:"+wdt+" PREFIX wd:"+wd+" SELECT ?qid WHERE {{?publication rdfs:label '{}'@en.BIND(STRAFTER(STR(?language),STR(wd:)) AS ?qid)}} LIMIT 1",
             "SELECT ?qid ?label ?quote WHERE {{?publication rdfs:label '{}'@en; rdfs:label ?label;schema:description ?quote; FILTER (lang(?label) = 'en') FILTER (lang(?quote) = 'en') BIND(STRAFTER(STR(?publication),STR(wd:)) AS ?qid)}} LIMIT 1"]

check_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?item ?qid 
WHERE 
{
?item rdfs:label "LABEL"@en;
      schema:description "DESCRIPTION"@en.
BIND(STRAFTER(STR(?item),STR(wd:)) AS ?qid)
}"""

