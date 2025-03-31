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

query_base_model="""
PREFIX mathmoddb: <https://mardi4nfdi.de/mathmoddb#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
SELECT DISTINCT ?label ?qid
WHERE {{
?model a mathmoddb:MathematicalModel;
          rdfs:label ?label.
{0}
{1}
{2}
{3}
{4}
{5}
BIND(STRAFTER(STR(?model),"#") AS ?qid).
}}
LIMIT 10"""

problem_sparql = """
?model mathmoddb:models ?problem.
?problem rdfs:label ?problemlabel
FILTER(lang(?problemlabel) = 'en')"""
problem_filter_sparql = """
FILTER(CONTAINS(lcase(str(?problemlabel)), '{}'))."""
field_sparql = """
?model mathmoddb:models ?problem.
?problem mathmoddb:containedInField {}.
"""
formulation_sparql = """
?model (mathmoddb:containsFormulation | mathmoddb:containsAssumption | mathmoddb:containsBoundaryCondition | mathmoddb:containsConstraintCondition | mathmoddb:containsCouplingCondition | mathmoddb:containsInitialCondition | mathmoddb:containsFinalCondition) {}.
"""
task_sparql = """
?model (mathmoddb:appliedByTask) {}.
"""
quantity_sparql = """
?model (mathmoddb:containsFormulation | mathmoddb:containsAssumption | mathmoddb:containsBoundaryCondition | mathmoddb:containsConstraintCondition | mathmoddb:containsCouplingCondition | mathmoddb:containsInitialCondition | mathmoddb:containsFinalCondition | mathmoddb:appliedByTask) ?intermediate.
?intermediate (mathmoddb:containsQuantity | mathmoddb:containsInput | mathmoddb:containsOutput | mathmoddb:containsObjective | mathmoddb:containsParameter | mathmoddb:containsConstant) {}.
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