from .config import *
from .id import *

#SPARQL Query strings for Workflow Search Base + Specifics

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

#SPARQL Queries to Wikidata KG and MaRDI KG for related Paper integration. _ini/keys - entire query, header/body - orcid author specific.  

wkeys=['qid_doi','label_doi','quote_doi','qid_jou','label_jou','quote_jou','qid_lan','label_lan','quote_lan','qid_tit','label_tit','quote_tit']
mkeys=['qid_doi','qid_ch1','qid_jou','qid2_jou','qid3_jou','qid_lan','qid2_lan','qid3_lan','qid_tit','qid_ch6','qid_ch7']

wheader="?qid_{0} ?label_{0} ?quote_{0} "
wbody  ='''OPTIONAL{{?aut_{0} wdt:P496 '{1}';rdfs:label ?label_{0};schema:description ?quote_{0}.BIND(STRAFTER(STR(?aut_{0}),STR(wd:)) AS ?qid_{0}).FILTER (lang(?label_{0}) = 'en').FILTER (lang(?quote_{0}) = 'en')}}
'''

mheader="?qid_aut_{0} ?qid2_aut_{0} ?qid3_aut_{0} "
mbody='''OPTIONAL{{?aut_{0} wdt:P'''+ORCID_iD+''' '{1}'.BIND(STRAFTER(STR(?aut_{0}),STR(wd:)) AS ?qid_aut_{0})}}
         OPTIONAL{{?achk_{0}a rdfs:label '{2}'@en;schema:description '{3}'@en.BIND(STRAFTER(STR(?achk_{0}a),STR(wd:)) AS ?qid2_aut_{0}).}}
         OPTIONAL{{?achk_{0}b rdfs:label '{4}'@en;schema:description 'researcher'@en.BIND(STRAFTER(STR(?achk_{0}b),STR(wd:)) AS ?qid3_aut_{0}).}}
         '''

wquery_ini='''
SELECT ?qid_doi ?label_doi ?quote_doi ?qid_jou ?label_jou ?quote_jou ?qid_lan ?label_lan ?quote_lan ?qid_tit ?label_tit ?quote_tit {0}
WHERE 
{{OPTIONAL{{?doi wdt:P356 '{1}';rdfs:label ?label_doi;schema:description ?quote_doi.BIND(STRAFTER(STR(?doi),STR(wd:)) AS ?qid_doi).FILTER (lang(?label_doi) = 'en').FILTER (lang(?quote_doi) = 'en').}}
  OPTIONAL{{?jou wdt:P31 wd:Q5633421;rdfs:label ?label_jou;schema:description ?quote_jou.FILTER (lcase(str(?label_jou)) = '{2}').FILTER (lang(?quote_jou) = 'en').BIND(STRAFTER(STR(?jou),STR(wd:)) AS ?qid_jou).}}
  OPTIONAL{{?lan rdfs:label '{3}'@en;rdfs:label ?label_lan;schema:description ?quote_lan;skos:altLabel '{4}'@en.FILTER (lang(?label_lan) = 'en').FILTER (lang(?quote_lan) = 'en').BIND(STRAFTER(STR(?lan),STR(wd:)) AS ?qid_lan).}}
  OPTIONAL{{?tit rdfs:label '{5}'@en;rdfs:label ?label_tit;schema:description ?quote_tit.FILTER (lang(?label_tit) = 'en').FILTER (lang(?quote_tit) = 'en').BIND(STRAFTER(STR(?tit),STR(wd:)) AS ?qid_tit).}}
  {6}
}} 
LIMIT 1'''

mquery_ini='''
PREFIX wdt:'''+wdt+''' PREFIX wd:'''+wd+'''SELECT ?qid_doi ?qid_ch1 ?qid_jou ?qid2_jou ?qid3_jou ?qid_lan ?qid2_lan ?qid3_lan ?qid_tit ?qid_ch6 ?qid_ch7 {0}
WHERE 
{{OPTIONAL{{?doi wdt:P'''+DOI+''' '{1}'.BIND(STRAFTER(STR(?doi),STR(wd:)) AS ?qid_doi).}}
  OPTIONAL{{?ch1 rdfs:label '{2}'@en;schema:description '{3}'@en.BIND(STRAFTER(STR(?ch1),STR(wd:)) AS ?qid_ch1).}}
  OPTIONAL{{?jou rdfs:label ?label.FILTER (lcase(str(?label)) = '{4}') BIND(STRAFTER(STR(?jou),STR(wd:)) AS ?qid_jou).}}
  OPTIONAL{{?ch2 rdfs:label '{5}'@en;schema:description '{6}'@en.BIND(STRAFTER(STR(?ch2),STR(wd:)) AS ?qid2_jou).}}
  OPTIONAL{{?ch3 rdfs:label '{4}'@en;schema:description 'scientific journal'@en.BIND(STRAFTER(STR(?ch3),STR(wd:)) AS ?qid3_jou).}}
  OPTIONAL{{?lan rdfs:label '{7}'@en; skos:altLabel '{8}'@en; BIND(STRAFTER(STR(?lan),STR(wd:)) AS ?qid_lan)}}
  OPTIONAL{{?ch4 rdfs:label '{9}'@en;schema:description '{10}'@en.BIND(STRAFTER(STR(?ch4),STR(wd:)) AS ?qid2_lan).}}
  OPTIONAL{{?ch5 rdfs:label '{7}'@en;schema:description 'language'@en.BIND(STRAFTER(STR(?ch5),STR(wd:)) AS ?qid3_lan).}}
  OPTIONAL{{?tit rdfs:label '{11}'@en.BIND(STRAFTER(STR(?tit),STR(wd:)) AS ?qid_tit)}}
  {12}
}} 
LIMIT 1'''

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

