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

doi_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?qid
WHERE {
?publication wdt:P"""+DOI+""" "DOI".
BIND(STRAFTER(STR(?publication),STR(wd:)) AS ?qid)
}
LIMIT 1"""

doi_query_wikidata="""SELECT ?qid ?label ?quote
WHERE {
?publication wdt:P356 "DOI";
             rdfs:label ?label;
             schema:description ?quote.
BIND(STRAFTER(STR(?publication),STR(wd:)) AS ?qid)
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""

author_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?qid 
WHERE {
?author wdt:P"""+ORCID_iD+""" "ORCID".
BIND(STRAFTER(STR(?author),STR(wd:)) AS ?qid)
}
LIMIT 1"""

author_query_wikidata="""SELECT ?qid ?label ?quote 
WHERE {
?author wdt:P496 "ORCID";
        rdfs:label ?label;
        schema:description ?quote.
BIND(STRAFTER(STR(?author),STR(wd:)) AS ?qid)
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""

journal_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?qid
WHERE {
?journal rdfs:label ?label.
FILTER (lcase(str(?label)) = "JOURNAL")
BIND(STRAFTER(STR(?journal),STR(wd:)) AS ?qid)
}
LIMIT 1"""

journal_query_wikidata="""SELECT ?qid ?label ?quote
WHERE {
?journal wdt:P31 wd:Q5633421;
         rdfs:label ?label;
         schema:description ?quote.
FILTER (lcase(str(?label)) = "JOURNAL")
FILTER (lang(?quote) = 'en')
BIND(STRAFTER(STR(?journal),STR(wd:)) AS ?qid)
}
LIMIT 1"""

model_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?label ?quote 
WHERE {
MODEL rdfs:label ?label;
      schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""

model_query_wikidata="""SELECT ?label ?quote 
WHERE {
MODEL rdfs:label ?label;
      schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""


method_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?label ?quote
WHERE {
METHOD rdfs:label ?label;
      schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""

method_query_wikidata="""
SELECT ?label ?quote
WHERE {
METHOD rdfs:label ?label;
      schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""


software_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?label ?quote
WHERE {
SOFTWARE rdfs:label ?label;
      schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""

software_query_wikidata="""
SELECT ?label ?quote
WHERE {
SOFTWARE rdfs:label ?label;
      schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""

input_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?label ?quote
WHERE {
INPUT rdfs:label ?label;
      schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""

input_query_wikidata="""
SELECT ?label ?quote
WHERE {
INPUT rdfs:label ?label;
      schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}
LIMIT 1"""


discipline_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?label ?quote  
WHERE 
{
DISCIPLINE rdfs:label ?label;
        schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}"""

discipline_query_wikidata="""
SELECT ?label ?quote  
WHERE 
{
DISCIPLINE rdfs:label ?label;
        schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}"""

plang_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?label ?quote  
WHERE 
{
LANGUAGE rdfs:label ?label;
        schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}"""

plang_query_wikidata="""
SELECT ?label ?quote
WHERE
{
LANGUAGE rdfs:label ?label;
        schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}"""

main_subject_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?label ?quote  
WHERE 
{
MAIN SUBJECT rdfs:label ?label;
        schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}"""

main_subject_query_wikidata="""
SELECT ?label ?quote  
WHERE 
{
MAIN SUBJECT rdfs:label ?label;
        schema:description ?quote.
FILTER (lang(?label) = 'en')
FILTER (lang(?quote) = 'en')
}"""

language_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?qid
WHERE {
  ?language rdfs:label 'LANGUAGE'@en;
            skos:altLabel 'LANG_SHORT'@en;
  BIND(STRAFTER(STR(?language),STR(wd:)) AS ?qid)    
  }
LIMIT 1
"""

language_query_wikidata="""
SELECT ?qid ?label ?quote
WHERE {
  ?language rdfs:label 'LANGUAGE'@en;
            rdfs:label ?label;
            schema:description ?quote;
            skos:altLabel 'LANG_SHORT'@en.
            FILTER (lang(?label) = 'en')
            FILTER (lang(?quote) = 'en')
  BIND(STRAFTER(STR(?language),STR(wd:)) AS ?qid)  
  }
LIMIT 1
"""

title_query="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""

SELECT ?qid
WHERE {
  ?publication rdfs:label 'TITLE'@en.
  BIND(STRAFTER(STR(?language),STR(wd:)) AS ?qid)    
  }
LIMIT 1
"""

title_query_wikidata="""
SELECT ?qid ?label ?quote
WHERE {
  ?publication rdfs:label 'TITLE'@en;
            rdfs:label ?label;
            schema:description ?quote;
            FILTER (lang(?label) = 'en')
            FILTER (lang(?quote) = 'en')
  BIND(STRAFTER(STR(?publication),STR(wd:)) AS ?qid)  
  }
LIMIT 1
"""

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

