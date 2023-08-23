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

statement_obj="""?t p:P"""+P4+""" ?s.
?t rdfs:label ?label.
?t schema:description ?quote.
"""

statement_mms="""?y rdfs:label ?label."""

#SPARQL Keys for Queries

keys={'wkpub':' ?qid_doi ?label_doi ?quote_doi ?qid_jou ?label_jou ?quote_jou ?qid_lan ?label_lan ?quote_lan ?qid_tit ?label_tit ?quote_tit',
      'mkpub':' ?qid_doi ?qid_ch1 ?qid_jou ?qid2_jou ?qid3_jou ?qid_lan ?qid2_lan ?qid3_lan ?qid_tit ?qid_ch6 ?qid_ch7',
      'wkmod':' ?label_model ?quote_model ?label_ms ?quote_ms',
      'mkmod':' ?label_model ?quote_model ?qid_model ?qid2_model ?label_ms ?quote_ms ?qid_ms',
      'wkmet':'','mkmet':'','wksof':'','mksof':'','wkinp':'','mkinp':'','wkout':'','mkout':'','wkdis':'','mkdis':''}

keys_flex={'wkpub':' ?qid_{0} ?label_{0} ?quote_{0}','mkpub':' ?qid_aut_{0} ?qid2_aut_{0} ?qid3_aut_{0}',
           'wkmet':' ?label_m_{0} ?quote_m_{0} ?label_ms_{0} ?quote_ms_{0}','mkmet':' ?qid_m_{0} ?label_m_{0} ?quote_m_{0} ?qid2_m_{0} ?label_ms_{0} ?quote_ms_{0} ?qid_ms_{0}',
           'wksof':[' ?label_s_{0} ?quote_s_{0}',' ?label_pl_{0}_{1} ?quote_pl_{0}_{1}'],
           'mksof':[' ?qid_s_{0} ?label_s_{0} ?quote_s_{0} ?qid2_s_{0}',' ?qid_pl_{0}_{1} ?label_pl_{0}_{1} ?quote_pl_{0}_{1}'],
           'wkinp':' ?label_in_{0} ?quote_in_{0}','mkinp':' ?qid_in_{0} ?label_in_{0} ?quote_in_{0} ?qid2_in_{0}',
           'wkout':' ?label_ou_{0} ?quote_ou_{0}','mkout':' ?qid_ou_{0} ?label_ou_{0} ?quote_ou_{0} ?qid2_ou_{0}',
           'wkdis':' ?label_di_{0} ?quote_di_{0}','mkdis':' ?qid_di_{0} ?label_di_{0} ?quote_di_{0}',
           'wkmod':'','mkmod':''}

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

wbmod = '''
OPTIONAL{{wd:{0} rdfs:label ?label_model; schema:description ?quote_model. FILTER (lang(?label_model) = 'en') FILTER (lang(?quote_model) = 'en')}}
OPTIONAL{{wd:{1} rdfs:label ?label_ms; schema:description ?quote_ms. FILTER (lang(?label_ms) = 'en')FILTER (lang(?quote_ms) = 'en')}}
'''

wbmet = '''
OPTIONAL{{wd:{1} rdfs:label ?label_m_{0}; schema:description ?quote_m_{0}. FILTER (lang(?label_m_{0}) = 'en') FILTER (lang(?quote_m_{0}) = 'en')}}
OPTIONAL{{wd:{2} rdfs:label ?label_ms_{0}; schema:description ?quote_ms_{0}. FILTER (lang(?label_ms_{0}) = 'en')FILTER (lang(?quote_ms_{0}) = 'en')}}
'''

wbsof = '''
OPTIONAL{{wd:{1} rdfs:label ?label_s_{0}; schema:description ?quote_s_{0}. FILTER (lang(?label_s_{0}) = 'en') FILTER (lang(?quote_s_{0}) = 'en')}}
{2}
'''

wbpla = '''
OPTIONAL{{wd:{2} rdfs:label ?label_pl_{0}_{1}; schema:description ?quote_pl_{0}_{1} FILTER (lang(?label_pl_{0}_{1}) = 'en') FILTER (lang(?quote_pl_{0}_{1}) = 'en')}}
'''

wbinp = '''
OPTIONAL{{wd:{1} rdfs:label ?label_in_{0}; schema:description ?quote_in_{0}. FILTER (lang(?label_in_{0}) = 'en') FILTER (lang(?quote_in_{0}) = 'en')}}
'''

wbout = '''
OPTIONAL{{wd:{1} rdfs:label ?label_ou_{0}; schema:description ?quote_ou_{0}. FILTER (lang(?label_ou_{0}) = 'en') FILTER (lang(?quote_ou_{0}) = 'en')}}
'''

wbdis = '''
OPTIONAL{{wd:{1} rdfs:label ?label_di_{0};schema:description ?quote_di_{0}.FILTER (lang(?label_di_{0}) = 'en') FILTER (lang(?quote_di_{0}) = 'en')}}
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

mbmod = '''
OPTIONAL{{wd:{0} rdfs:label ?label_model; schema:description ?quote_model. FILTER (lang(?label_model) = 'en') FILTER (lang(?quote_model) = 'en')}}
OPTIONAL{{?mchk rdfs:label '{1}'@en;schema:description '{2}'@en.BIND(STRAFTER(STR(?mchk),STR(wd:)) AS ?qid_model).}}
OPTIONAL{{?mchk2 rdfs:label '{3}'@en;schema:description '{4}'@en.BIND(STRAFTER(STR(?mchk2),STR(wd:)) AS ?qid2_model).}}
OPTIONAL{{wd:{5} rdfs:label ?label_ms; schema:description ?quote_ms. FILTER (lang(?label_ms) = 'en')FILTER (lang(?quote_ms) = 'en')}}
OPTIONAL{{?mschk rdfs:label '{6}'@en;schema:description '{7}'@en.BIND(STRAFTER(STR(?mschk),STR(wd:)) AS ?qid_ms).}}
'''

mbmet = '''
OPTIONAL{{wd:{1} rdfs:label ?label_m_{0}; schema:description ?quote_m_{0}. FILTER (lang(?label_m_{0}) = 'en') FILTER (lang(?quote_m_{0}) = 'en')}}
OPTIONAL{{?mechk_{0} rdfs:label '{2}'@en;schema:description '{3}'@en.BIND(STRAFTER(STR(?mechk_{0}),STR(wd:)) AS ?qid_m_{0}).}}
OPTIONAL{{?mechk2_{0} rdfs:label '{4}'@en;schema:description '{5}'@en.BIND(STRAFTER(STR(?mechk2_{0}),STR(wd:)) AS ?qid2_m_{0}).}}
OPTIONAL{{wd:{6} rdfs:label ?label_ms_{0}; schema:description ?quote_ms_{0}. FILTER (lang(?label_ms_{0}) = 'en')FILTER (lang(?quote_ms_{0}) = 'en')}}
OPTIONAL{{?memschk_{0} rdfs:label '{7}'@en;schema:description '{8}'@en.BIND(STRAFTER(STR(?memschk_{0}),STR(wd:)) AS ?qid_ms_{0}).}}
'''

mbsof = '''
OPTIONAL{{wd:{1} rdfs:label ?label_s_{0}; schema:description ?quote_s_{0}. FILTER (lang(?label_s_{0}) = 'en') FILTER (lang(?quote_s_{0}) = 'en')}}
OPTIONAL{{?schk_{0} rdfs:label '{2}'@en;schema:description '{3}'@en.BIND(STRAFTER(STR(?schk_{0}),STR(wd:)) AS ?qid_s_{0}).}}
OPTIONAL{{?schk2_{0} rdfs:label '{4}'@en;schema:description '{5}'@en.BIND(STRAFTER(STR(?schk2_{0}),STR(wd:)) AS ?qid2_s_{0}).}}
{6}
'''

mbpla = '''
OPTIONAL{{wd:{2} rdfs:label ?label_pl_{0}_{1}; schema:description ?quote_pl_{0}_{1} FILTER (lang(?label_pl_{0}_{1}) = 'en') FILTER (lang(?quote_pl_{0}_{1}) = 'en')}}
OPTIONAL{{?plchk_{0} rdfs:label '{3}'@en;schema:description '{4}'@en.BIND(STRAFTER(STR(?plchk_{0}),STR(wd:)) AS ?qid_pl_{0}_{1}).}}
'''

mbinp = '''
OPTIONAL{{wd:{1} rdfs:label ?label_in_{0}; schema:description ?quote_in_{0}. FILTER (lang(?label_in_{0}) = 'en') FILTER (lang(?quote_in_{0}) = 'en')}}
OPTIONAL{{?ichk_{0} rdfs:label '{2}'@en;schema:description "{3}"@en.BIND(STRAFTER(STR(?ichk_{0}),STR(wd:)) AS ?qid_in_{0}).}}
OPTIONAL{{?ichk2_{0} rdfs:label '{4}'@en;schema:description '{5}'@en.BIND(STRAFTER(STR(?ichk2_{0}),STR(wd:)) AS ?qid2_in_{0}).}}
'''

mbout = '''
OPTIONAL{{wd:{1} rdfs:label ?label_ou_{0}; schema:description ?quote_ou_{0}. FILTER (lang(?label_ou_{0}) = 'en') FILTER (lang(?quote_ou_{0}) = 'en')}}
OPTIONAL{{?ochk_{0} rdfs:label '{2}'@en;schema:description "{3}"@en.BIND(STRAFTER(STR(?ochk_{0}),STR(wd:)) AS ?qid_ou_{0}).}}
OPTIONAL{{?ochk2_{0} rdfs:label '{4}'@en;schema:description '{5}'@en.BIND(STRAFTER(STR(?ochk2_{0}),STR(wd:)) AS ?qid2_ou_{0}).}}
'''

mbdis = '''
OPTIONAL{{wd:{1} rdfs:label ?label_di_{0}; schema:description ?quote_di_{0}. FILTER (lang(?label_di_{0}) = 'en') FILTER (lang(?quote_di_{0}) = 'en')}}
OPTIONAL{{?dchk_{0} rdfs:label '{2}'@en;schema:description "{3}"@en.BIND(STRAFTER(STR(?dchk_{0}),STR(wd:)) AS ?qid_di_{0}).}}
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

