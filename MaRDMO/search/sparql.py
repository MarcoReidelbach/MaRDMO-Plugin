#SPARQL Query Base and Components for Portal Search

query_base="""
SELECT DISTINCT ?label ?qid
WHERE {{
?workflow wdt:{instance of} wd:{research workflow};
          rdfs:label ?label;
          {0}
          {1}
          {2}
{3}
BIND(STRAFTER(STR(?workflow),STR(wd:)) AS ?qid).
}}
LIMIT 10"""

quote_sparql = "schema:description ?quote;"
res_obj_sparql = "FILTER(CONTAINS(lcase(str(?quote)), '{}'@en)).\n"
res_disc_sparql = "wdt:{field of work} wd:{0};\n"
mmsio_sparql = "wdt:{uses} wd:{0};\n"

query_base_model="""
SELECT DISTINCT ?label ?qid
WHERE {{
?model wdt:{instance of} wd:{mathematical model};
          rdfs:label ?label.
{0}
{1}
{2}
{3}
{4}
{5}
BIND(STRAFTER(STR(?model), STR(wd:)) AS ?qid)
}}
LIMIT 10"""

problem_sparql = """
?problem wdt:{modelled by} ?model;
         wdt:{instance of} wd:{research problem};
         rdfs:label ?problemlabel.
FILTER(lang(?problemlabel) = 'en')"""
problem_filter_sparql = """
FILTER(CONTAINS(lcase(str(?problemlabel)), '{0}'))."""
field_sparql = """
?problem wdt:{modelled by} ?model.
wd:{} wdt:{contains} ?problem;
      wdt:{instance of} wd:{academic discipline}.
"""
formulation_sparql = """
?model wdt:{contains} wd:{0}.
wd:{0} wdt:{instance of} wd:{mathematical expression}.
"""
task_sparql = """
?model wdt:{used by} wd:{0}.
wd:{0} wdt:{instance of} wd:{computational task}.
"""
quantity_sparql = """
{{
  ?model wdt:{contains} ?intermediate .
  ?intermediate wdt:{instance of} wd:{mathematical expression}.
}}
UNION
{{
  ?model wdt:{used by} ?intermediate .
  ?intermediate wdt:{instance of} wd:{computational task}.
}}
VALUES ?type {{ wd:{quantity} wd:{kind of quantity} }} .
"""
quantity_filter_sparql = """
{{
  ?intermediate wdt:{contains} wd:{0}.
  wd:{0} wdt:{instance of} ?type .
}}
""" 

query_base_algorithm="""
PREFIX mathalgodb: <https://mardi4nfdi.de/mathalgodb/0.1#>
PREFIX algorithm: <https://mardi4nfdi.de/mathalgodb/0.1/algorithm#>
PREFIX software: <https://mardi4nfdi.de/mathalgodb/0.1/software#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?label ?qid
WHERE {{
?algorithm a mathalgodb:algorithm;
          rdfs:label ?label.
{0}
{1}
{2}
BIND(STRAFTER(STR(?algorithm),"#") AS ?qid).
}}
LIMIT 10"""

algorithmic_problem_sparql = """
?algorithm mathalgodb:solves ?problem.
?problem rdfs:label ?problemlabel"""
algorithmic_problem_filter_sparql = """
FILTER(CONTAINS(lcase(str(?problemlabel)), '{}'))."""
software_sparql = """
?algorithm mathalgodb:implementedBy {}.
"""