from ..config import wd, wdt 

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