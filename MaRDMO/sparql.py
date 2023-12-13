from .config import *
from .id import *

#SPARQL Query Base and components for Workflow Search

query_base="""
PREFIX wdt: """+wdt+"""
PREFIX wd: """+wd+"""
SELECT DISTINCT ?label ?qid
WHERE {{
?workflow wdt:P{0} wd:{1};
          rdfs:label ?label;
          {2}
          {3}
          {4}
{5}
BIND(STRAFTER(STR(?workflow),STR(wd:)) AS ?qid).
}}
LIMIT 10"""

quote_sparql = "schema:description ?quote;"
res_obj_sparql = "FILTER(CONTAINS(lcase(str(?quote)), '{}'@en)).\n"
res_disc_sparql = "wdt:P{0} wd:{1};\n"
mmsio_sparql = "wdt:P{0} wd:{1};\n"

#SPARQL Keys for Queries related to Publication

Keys={'wqpub':' ?qid_doi ?label_doi ?quote_doi ?qid_jou ?label_jou ?quote_jou ?qid_lan ?label_lan ?quote_lan ?qid_tit ?label_tit ?quote_tit',
      'mqpub':' ?qid_doi ?qid_ch1 ?qid_jou ?qid2_jou ?qid3_jou ?qid_lan ?qid2_lan ?qid3_lan ?qid_tit ?qid_ch6 ?qid_ch7'}

keys_flex={'wqpub':' ?qid_{0} ?label_{0} ?quote_{0}',
           'mqpub':' ?qid_aut_{0} ?qid2_aut_{0} ?qid3_aut_{0}'}

#SPARQL Bodies for Wikidata Queries

wbpub = '''
OPTIONAL{{?doi wdt:P356 '{0}';rdfs:label ?label_doi;schema:description ?quote_doi.BIND(STRAFTER(STR(?doi),STR(wd:)) AS ?qid_doi).FILTER (lang(?label_doi) = 'en').FILTER (lang(?quote_doi) = 'en').}}
OPTIONAL{{?jou wdt:P31 wd:Q5633421;rdfs:label ?label_jou;schema:description ?quote_jou.FILTER (lcase(str(?label_jou)) = '{1}').FILTER (lang(?quote_jou) = 'en').BIND(STRAFTER(STR(?jou),STR(wd:)) AS ?qid_jou).}}
OPTIONAL{{?lan rdfs:label '{2}'@en;rdfs:label ?label_lan;schema:description ?quote_lan;skos:altLabel '{3}'@en.FILTER (lang(?label_lan) = 'en').FILTER (lang(?quote_lan) = 'en').BIND(STRAFTER(STR(?lan),STR(wd:)) AS ?qid_lan).}}
OPTIONAL{{?tit rdfs:label '{4}'@en;rdfs:label ?label_tit;schema:description ?quote_tit.FILTER (lang(?label_tit) = 'en').FILTER (lang(?quote_tit) = 'en').BIND(STRAFTER(STR(?tit),STR(wd:)) AS ?qid_tit).}}
{5}
'''

wbaut  = '''
OPTIONAL{{?aut_{0} wdt:P496 '{1}';rdfs:label ?label_{0};schema:description ?quote_{0}.BIND(STRAFTER(STR(?aut_{0}),STR(wd:)) AS ?qid_{0}).FILTER (lang(?label_{0}) = 'en').FILTER (lang(?quote_{0}) = 'en')}}
'''

#SPARQL Bodies for MaRDI Queries

mbpub = '''
OPTIONAL{{?doi wdt:P'''+P16+''' '{0}'.BIND(STRAFTER(STR(?doi),STR(wd:)) AS ?qid_doi).}}
OPTIONAL{{?ch1 rdfs:label '{1}'@en;schema:description '{2}'@en.BIND(STRAFTER(STR(?ch1),STR(wd:)) AS ?qid_ch1).}}
OPTIONAL{{?jou rdfs:label ?label.FILTER (lcase(str(?label)) = '{3}') BIND(STRAFTER(STR(?jou),STR(wd:)) AS ?qid_jou).}}
OPTIONAL{{?ch2 rdfs:label '{4}'@en;schema:description '{5}'@en.BIND(STRAFTER(STR(?ch2),STR(wd:)) AS ?qid2_jou).}}
OPTIONAL{{?ch3 rdfs:label '{3}'@en;schema:description 'scientific journal'@en.BIND(STRAFTER(STR(?ch3),STR(wd:)) AS ?qid3_jou).}}
OPTIONAL{{?lan rdfs:label '{6}'@en; skos:altLabel '{7}'@en; BIND(STRAFTER(STR(?lan),STR(wd:)) AS ?qid_lan)}}
OPTIONAL{{?ch4 rdfs:label '{8}'@en;schema:description '{9}'@en.BIND(STRAFTER(STR(?ch4),STR(wd:)) AS ?qid2_lan).}}
OPTIONAL{{?ch5 rdfs:label '{6}'@en;schema:description 'language'@en.BIND(STRAFTER(STR(?ch5),STR(wd:)) AS ?qid3_lan).}}
OPTIONAL{{?tit rdfs:label '{10}'@en.BIND(STRAFTER(STR(?tit),STR(wd:)) AS ?qid_tit)}}
{11}
'''

mbaut = '''
OPTIONAL{{?aut_{0} wdt:P'''+P22+''' '{1}'.BIND(STRAFTER(STR(?aut_{0}),STR(wd:)) AS ?qid_aut_{0})}}
OPTIONAL{{?achk_{0}a rdfs:label '{2}'@en;schema:description '{3}'@en.BIND(STRAFTER(STR(?achk_{0}a),STR(wd:)) AS ?qid2_aut_{0}).}}
OPTIONAL{{?achk_{0}b rdfs:label '{4}'@en;schema:description 'researcher'@en.BIND(STRAFTER(STR(?achk_{0}b),STR(wd:)) AS ?qid3_aut_{0}).}}
'''

mbody = '''
OPTIONAL{{?chk rdfs:label '{0}'@en;schema:description '{1}'@en.BIND(STRAFTER(STR(?chk),STR(wd:)) AS ?qid).}}
'''

wini='''
SELECT {0}
WHERE
{{
{1}
}}
LIMIT 1'''

mini='''
PREFIX wdt:'''+wdt+''' PREFIX wd:'''+wd+wini

