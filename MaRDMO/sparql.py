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

#SPARQL Query parts

mbody = '''
OPTIONAL{{?chk rdfs:label '{0}'@en;schema:description '{1}'@en.BIND(STRAFTER(STR(?chk),STR(wd:)) AS ?qid).}}
'''

wini='''
SELECT {0}
WHERE
{{
{1}
}}
LIMIT {2}'''

mini='''
PREFIX wdt:'''+wdt+''' PREFIX wd:'''+wd+wini

#SPARQL Query for additional programming language queries

pl_vars = '?qid ?label ?quote'

pl_query = '''
OPTIONAL{{wd:{0} wdt:{1} ?pl. ?pl rdfs:label ?label; schema:description ?quote.BIND(STRAFTER(STR(?pl),STR(wd:)) AS ?qid).FILTER (lang(?label) = 'en').FILTER (lang(?quote) = 'en').}}
'''

#Queries to MaRDI KG and Wikidata for Publication Handler

query_1  = '''SELECT ?publicationQid ?publicationLabel ?publicationDescription1         
                     ?authorInfo                                                        
                     ?entrytypeQid ?entrytypeLabel ?entrytypeDescription1               
                     ?journalQid ?journalLabel ?journalDescription1                     
                     ?languageQid ?languageLabel ?languageDescription1                  
                     ?title ?otherAuthor ?publicationDate ?volume ?issue ?page          

              WHERE {{?publication wdt:P{0} "{1}";
                              rdfs:label ?publicationLabel.
                      OPTIONAL {{?publication schema:description ?publicationDescription.}}
                      FILTER (lang(?publicationLabel) = 'en')
                      FILTER (lang(?publicationDescription) = 'en') 
                      BIND(COALESCE(?publicationDescription, "") As ?publicationDescription1)
                      BIND(STRAFTER(STR(?publication),STR(wd:)) AS ?publicationQid).
                      OPTIONAL {{?publication wdt:P{2} ?author.
                                 ?author rdfs:label ?authorLabel;
                                 OPTIONAL {{?author schema:description ?authorDescription.}}  
                                 OPTIONAL {{?author wdt:P{3} ?authorOrcid.}}
                                 OPTIONAL {{?author wdt:P{13} ?authorWikidataQid}}
                                 OPTIONAL {{?author wdt:P{14} ?authorZbmathID}}
                                 BIND(COALESCE(?authorOrcid, "") As ?authorOrcid1)
                                 BIND(COALESCE(?authorWikidataQid, "") As ?authorWikidataQid1)
                                 BIND(COALESCE(?authorZbmathID, "") As ?authorZbmathID1)
                                 BIND(COALESCE(?authorDescription, "") As ?authorDescription1)
                                 BIND(STRAFTER(STR(?author),STR(wd:)) AS ?authorQid).
                                 FILTER (lang(?authorLabel) = 'en')
                                 FILTER (lang(?authorDescription) = 'en')
                                 BIND(concat(?authorQid," <|> ",?authorLabel," <|> ",?authorDescription1," <|> ",?authorOrcid1,
                                             " <|> ",?authorWikidataQid1, " <|> ",?authorZbmathID1) AS ?authorInfo)}} 
                     OPTIONAL {{?publication wdt:P{4} ?entrytype.
                                ?entrytype rdfs:label ?entrytypeLabel.
                                OPTIONAL {{?entrytype schema:description ?entrytypeDescription.}}
                                FILTER (lang(?entrytypeLabel) = 'en')
                                FILTER (lang(?entrytypeDescription) = 'en')
                                BIND(COALESCE(?entrytypeDescription, "") As ?entrytypeDescription1)
                                BIND(STRAFTER(STR(?entrytype),STR(wd:)) AS ?entrytypeQid).}}
                     OPTIONAL {{?publication wdt:P{5} ?journal.
                                ?journal rdfs:label ?journalLabel.
                                OPTIONAL {{?journal schema:description ?journalDescription.}}
                                FILTER (lang(?journalLabel) = 'en')
                                FILTER (lang(?journalDescription) = 'en')
                                BIND(COALESCE(?journalDescription, "") As ?journalDescription1)
                                BIND(STRAFTER(STR(?journal),STR(wd:)) AS ?journalQid).}}
                     OPTIONAL {{?publication wdt:P{6} ?language.
                                ?language rdfs:label ?languageLabel.
                                OPTIONAL {{?language schema:description ?languageDescription.}}
                                FILTER (lang(?languageLabel) = 'en')
                                FILTER (lang(?languageDescription) = 'en')
                                BIND(COALESCE(?languageDescription, "") As ?languageDescription1)
                                BIND(STRAFTER(STR(?language),STR(wd:)) AS ?languageQid).}}
                     OPTIONAL {{?publication wdt:P{7} ?title.}}
                     OPTIONAL {{?publication wdt:P{8} ?otherAuthor.}}
                     OPTIONAL {{?publication wdt:P{9} ?publicationDate.}}
                     OPTIONAL {{?publication wdt:P{10} ?volume.}}
                     OPTIONAL {{?publication wdt:P{11} ?issue.}}
                     OPTIONAL {{?publication wdt:P{12} ?page.}}}}'''

query_2 = '''# Query for MaRDI portal                                              

             SELECT  ?publicationQid ?publicationLabel ?publicationDescription1                                               
             
             WHERE {{
                     # Publication via Wikidata QID

                     ?publication wdt:P{0} "{1}";
                             rdfs:label ?publicationLabel.
                     OPTIONAL {{?publication schema:description ?publicationDescription.}}

                     BIND(COALESCE(?publicationDescription, "") As ?publicationDescription1)
                     BIND(STRAFTER(STR(?publication),STR(wd:)) AS ?publicationQid).
                   
                   }}'''


query_3 = '''SELECT ?authorQid ?authorLabel ?authorDescription ?authorId        # Author of Publication via ORCID/zbMath

             WHERE {{

                     VALUES ?authorId {{{0}}}

                     OPTIONAL {{
                                # Author via ORCID
                                ?author wdt:P{1} ?authorId
                                BIND(STRAFTER(STR(?author),STR(wd:)) AS ?authorQid)
                              }}

                      SERVICE wikibase:label {{bd:serviceParam wikibase:language "en,en".}}

                    }}'''

query_4 = '''SELECT ?wikidataQid ?mardiQid ?authorLabel ?authorDescription         # Author of Publication via Wikidata QID

             WHERE {{

                     VALUES ?wikidataQid {{{0}}}

                     OPTIONAL {{
                                # Author via Wikidata QID
                                ?author wdt:P{1} ?wikidataQid
                                BIND(STRAFTER(STR(?author),STR(wd:)) AS ?mardiQid)
                              }}

                     SERVICE wikibase:label {{bd:serviceParam wikibase:language "en,en".}}

                   }}'''


