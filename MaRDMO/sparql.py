from .config import wd, wdt 

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

mbody2 = '''
OPTIONAL{{?chk rdfs:label '{0}'@en;schema:description '{1}'@en.BIND(STRAFTER(STR(?chk),STR(wd:)) AS ?qid).}}
OPTIONAL{{?chk wdt:P{2} ?author.}}
OPTIONAL{{?author wdt:P{3} ?orcid.}}
OPTIONAL{{?author wdt:P{4} ?zbmath.}}
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

#SPARQL Query for additional entities

pl_vars = '?qid ?label ?quote'

pl_query = '''
OPTIONAL{{wd:{0} wdt:{1} ?pl. ?pl rdfs:label ?label; schema:description ?quote.BIND(STRAFTER(STR(?pl),STR(wd:)) AS ?qid).FILTER (lang(?label) = 'en').FILTER (lang(?quote) = 'en').}}
'''

pro_vars = '?qid ?label ?quote'

pro_query = '''
OPTIONAL{{?pro wdt:{0} '{1}'. ?pro rdfs:label ?label; schema:description ?quote.BIND(STRAFTER(STR(?pro),STR(wd:)) AS ?qid).FILTER (lang(?label) = 'en').FILTER (lang(?quote) = 'en').}}
'''


#Queries to MaRDI KG and Wikidata for Publication Handler

queryPublication = {

       'All': '''SELECT ?publicationQid ?publicationLabel ?publicationDescription1         
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
                     OPTIONAL {{?publication wdt:P{12} ?page.}}}}''',

       'WikiCheck': '''# Query for MaRDI portal                                              

             SELECT  ?publicationQid ?publicationLabel ?publicationDescription1                                               
             
             WHERE {{
                     # Publication via Wikidata QID

                     ?publication wdt:P{0} "{1}";
                             rdfs:label ?publicationLabel.
                     OPTIONAL {{?publication schema:description ?publicationDescription.}}

                     BIND(COALESCE(?publicationDescription, "") As ?publicationDescription1)
                     BIND(STRAFTER(STR(?publication),STR(wd:)) AS ?publicationQid).
                   
                   }}''',


       'AuthorViaOrcid': '''SELECT ?authorQid ?authorLabel ?authorDescription ?authorId        # Author of Publication via ORCID/zbMath

             WHERE {{

                     VALUES ?authorId {{{0}}}

                     OPTIONAL {{
                                # Author via ORCID
                                ?author wdt:P{1} ?authorId
                                BIND(STRAFTER(STR(?author),STR(wd:)) AS ?authorQid)
                              }}

                      SERVICE wikibase:label {{bd:serviceParam wikibase:language "en,en".}}

                    }}''',

       'AuthorViaWikidataQID': '''SELECT ?wikidataQid ?mardiQid ?authorLabel ?authorDescription         # Author of Publication via Wikidata QID

             WHERE {{

                     VALUES ?wikidataQid {{{0}}}

                     OPTIONAL {{
                                # Author via Wikidata QID
                                ?author wdt:P{1} ?wikidataQid
                                BIND(STRAFTER(STR(?author),STR(wd:)) AS ?mardiQid)
                              }}

                     SERVICE wikibase:label {{bd:serviceParam wikibase:language "en,en".}}

                   }}'''
       }

### SPARQL queries to get additional information from MathModDB during export

queryModelDocumentation = {
    
                  'IDCheck': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                SELECT ?ID ?qC                   
                                WHERE {{
                                        ?ID rdfs:label {0}@en.
                                        ?ID a ?qC.
                                        FILTER (?qC IN (:ResearchField, :ResearchProblem, :MathematicalModel, :MathematicalFormulation, :Quantity, :QuantityKind, :ComputationalTask, :Publication))
                                      }}
                                      GROUP BY ?ID ?qC''',

                  'Quantity': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            
                            SELECT ?Quantity ?qlabel ?qquote ?qk ?qklabel ?qkquote ?label ?quote ?isLinear ?isNotLinear ?isDimensionless ?isDimensional
                            WHERE {{
                              VALUES ?Quantity {{{0}}}
                              # Handle Quantities
                              OPTIONAL {{
                                         ?Quantity a :Quantity .
                                         ?Quantity rdfs:label ?qlabel .
                                         FILTER (lang(?qlabel) = 'en')
    
                                         OPTIONAL {{ ?Quantity rdfs:comment ?qquote . FILTER (lang(?qquote) = 'en') }}
                                         OPTIONAL {{ ?Quantity :isLinear ?isLinear . BIND(IF(?isLinear = false, true, false) AS ?isNotLinear) }}
                                         OPTIONAL {{ ?Quantity :isDimensionless ?isDimensionless . BIND(IF(?isDimensionless = false, true, false) AS ?isDimensional) }}

                                         # Match QuantityKind with zero to n intermediates
                                         OPTIONAL {{ 
                                                    ?Quantity (:generalizesQuantity|:generalizedByQuantity|:similarToQuantity)* ?intermediate .
                                                    ?intermediate a :Quantity .
                                                    ?intermediate (:generalizedByQuantity|:similarToQuantity) ?qk .
                                                    ?qk a :QuantityKind .
                                                    ?qk rdfs:label ?qklabel .
                                                    FILTER (lang(?qklabel) = 'en')
      
                                                    # Optional comment for QuantityKind
                                                    OPTIONAL {{ ?qk rdfs:comment ?qkquote . FILTER (lang(?qkquote) = 'en') }}
                                                  }}
    
                                         BIND(?qlabel AS ?label)
                                         BIND(?qquote AS ?quote)
                                       }}
                            
                              # Handle QuantityKinds
                              OPTIONAL {{
                                ?Quantity a :QuantityKind .
                                ?Quantity rdfs:label ?qklabel .
                                FILTER (lang(?qklabel) = 'en')
                                
                                OPTIONAL {{ ?Quantity rdfs:comment ?qkquote . FILTER (lang(?qkquote) = 'en') }}
                                OPTIONAL {{ ?Quantity :isDimensionless ?isDimensionless . BIND(IF(?isDimensionless = false, true, false) AS ?isDimensional) }}
                                BIND(IF(BOUND(?qlabel), ?qlabel, ?qklabel) AS ?label)
                                BIND(IF(BOUND(?qquote), ?qquote, ?qkquote) AS ?quote)
                              }}

                           }}
                            GROUP BY ?Quantity ?qlabel ?qquote ?qk ?qklabel ?qkquote ?label ?quote ?isLinear ?isNotLinear ?isDimensionless ?isDimensional''',

                  'QuantityDefinition': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  
                                 SELECT ?q ?qlabel ?MathematicalFormulation ?label ?quote ?isLinear ?isNotLinear ?isConvex ?isNotConvex ?isDynamic ?isStatic ?isDeterministic ?isStochastic 
                                        ?isDimensionless ?isDimensional ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent ?isSpaceContinuous ?isSpaceDiscrete ?isSpaceIndependent
                                        (GROUP_CONCAT(DISTINCT(?elements); separator=" <|> ") AS ?formula_elements) (GROUP_CONCAT(DISTINCT(?formulas); separator=" <|> ") AS ?formula)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?qID), " >|< ", STR(?qL), " >|< ", STR(?qC))); separator=" <|> ") AS ?ContainsQuantity)
                  
                                 WHERE {{
                                        
                                        VALUES ?q {{{0}}}
                  
                                        ?q rdfs:label ?qlabel.
                                        FILTER (lang(?qlabel) = 'en')
                                        
                                        ?q :definedBy ?MathematicalFormulation.
                  
                                        OPTIONAL {{ ?MathematicalFormulation rdfs:label ?label.
                                                    FILTER (lang(?label) = 'en')}}
                  
                                        OPTIONAL {{ ?MathematicalFormulation rdfs:comment ?quote.
                                                    FILTER (lang(?quote) = 'en')}}
                  
                                        OPTIONAL {{ ?MathematicalFormulation :isLinear ?isLinear.
                                                    BIND(IF(?isLinear = false, true, false) AS ?isNotLinear)}}
                                        OPTIONAL {{ ?MathematicalFormulation :isConvex ?isConvex.
                                                    BIND(IF(?isConvex = false, true, false) AS ?isNotConvex)}}  
                                        OPTIONAL {{ ?MathematicalFormulation :isDynamic ?isDynamic.
                                                    BIND(IF(?isDynamic = false, true, false) AS ?isStatic)}}                             
                                        OPTIONAL {{ ?MathematicalFormulation :isDeterministic ?isDeterministic.
                                                    BIND(IF(?isDeterministic = false, true, false) AS ?isStochastic)}}
                          		          OPTIONAL {{ ?MathematicalFormulation :isDimensionless ?isDimensionless.
                                                    BIND(IF(?isDimensionless = false, true, false) AS ?isDimensional)}}
                                        OPTIONAL {{ ?MathematicalFormulation :isTimeContinuous ?isTimeContinuous.
                                                    BIND(IF(BOUND(?isTimeContinuous) && ?isTimeContinuous = false, true, false) AS ?isTimeDiscrete)}}
                                                    BIND(IF(!BOUND(?isTimeContinuous), true, false) AS ?isTimeIndependent)
                                        OPTIONAL {{ ?MathematicalFormulation :isSpaceContinuous ?isSpaceContinuous.
                                                    BIND(IF(BOUND(?isSpaceContinuous) && ?isSpaceContinuous = false, true, false) AS ?isSpaceDiscrete)}}
                                                    BIND(IF(!BOUND(?isSpaceContinuous), true, false) AS ?isSpaceIndependent)
                  
                                        OPTIONAL {{ ?MathematicalFormulation :definingFormulation ?formulas.}}
                                        OPTIONAL {{ ?MathematicalFormulation :inDefiningFormulation ?elements.}}
                  
                                        OPTIONAL {{ ?MathematicalFormulation :containsQuantity ?qID.
                                                    ?qID rdfs:label ?qL;
                                                                a ?qc.
                                                    FILTER (?qc IN (:Quantity, :QuantityKind))
                                                    BIND(STRAFTER(STR(?qc), "#") AS ?qC)
                                                    FILTER (lang(?qL) = 'en')}}
                  
                                        }}
                  
                                        GROUP BY ?q ?qlabel ?MathematicalFormulation ?label ?quote ?isLinear ?isNotLinear ?isConvex ?isNotConvex ?isDynamic ?isStatic ?isDeterministic ?isStochastic 
                                                 ?isDimensionless ?isDimensional ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent ?isSpaceContinuous ?isSpaceDiscrete ?isSpaceIndependent''',
                                    
                  'Task': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  
                                 SELECT ?Task ?subclass ?quote ?isLinear ?isNotLinear
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?mm), " >|< ", STR(?mmL))); separator=" <|> ") AS ?appliesModel)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?f), " >|< ", STR(?fL))); separator=" <|> ") AS ?containsFormulation)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?a), " >|< ", STR(?aL))); separator=" <|> ") AS ?containsAssumption)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?bc), " >|< ", STR(?bcL))); separator=" <|> ") AS ?containsBoundaryCondition)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?cc), " >|< ", STR(?ccL))); separator=" <|> ") AS ?containsConstraintCondition)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?cpc), " >|< ", STR(?cpcL))); separator=" <|> ") AS ?containsCouplingCondition)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?ic), " >|< ", STR(?icL))); separator=" <|> ") AS ?containsInitialCondition)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?fc), " >|< ", STR(?fcL))); separator=" <|> ") AS ?containsFinalCondition)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?ct), " >|< ", STR(?ctL))); separator=" <|> ") AS ?containsTask)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?ict), " >|< ", STR(?ictL))); separator=" <|> ") AS ?containedInTask)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?in), " >|< ", STR(?inL))); separator=" <|> ") AS ?containsInput)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?o), " >|< ", STR(?oL))); separator=" <|> ") AS ?containsOutput)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?ob), " >|< ", STR(?obL))); separator=" <|> ") AS ?containsObjective)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?pa), " >|< ", STR(?paL))); separator=" <|> ") AS ?containsParameter)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?co), " >|< ", STR(?coL))); separator=" <|> ") AS ?containsConstant)
                                        
                                 WHERE {{
                                        VALUES ?Task {{{0}}}
                  
                                        OPTIONAL {{ ?sclass rdfs:subClassOf :Task.
                                                    ?Task a ?sclass .
                                                    BIND(STRAFTER(STR(?sclass), "#") AS ?subclass)}}
                                        OPTIONAL {{ ?Task rdfs:comment ?quote.
                                                    FILTER (lang(?quote) = 'en')}}
                                        OPTIONAL {{ ?Task :isLinear ?isLinear.
                                                    BIND(IF(?isLinear = false, true, false) AS ?isNotLinear)}}
                                        OPTIONAL {{ ?Task :appliesModel ?mm. 
                                                    ?mm rdfs:label ?mmL.
                                                    FILTER (lang(?mmL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsFormulation ?f. 
                                                    ?f rdfs:label ?fL.
                                                    FILTER (lang(?fL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsAssumption ?a. 
                                                    ?a rdfs:label ?aL.
                                                    FILTER (lang(?aL) = 'en')}}
                                       OPTIONAL {{ ?Task :containsBoundaryCondition ?bc. 
                                                    ?bc rdfs:label ?bcL.
                                                    FILTER (lang(?bcL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsConstraintCondition ?cc. 
                                                    ?cc rdfs:label ?ccL.
                                                    FILTER (lang(?ccL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsCouplingCondition ?cpc. 
                                                    ?cpc rdfs:label ?cpcL.
                                                    FILTER (lang(?cpcL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsInitialCondition ?ic. 
                                                    ?ic rdfs:label ?icL.
                                                    FILTER (lang(?icL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsFinalCondition ?fc. 
                                                    ?fc rdfs:label ?fcL.
                                                    FILTER (lang(?fcL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsTask ?ct. 
                                                    ?ct rdfs:label ?ctL.
                                                    FILTER (lang(?ctL) = 'en')}}
                                        OPTIONAL {{ ?Task :containedInTask ?ict. 
                                                    ?ict rdfs:label ?ictL.
                                                    FILTER (lang(?ictL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsInput ?in.
                                                    ?in rdfs:label ?inL.
                                                    FILTER (lang(?inL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsOutput ?o.
                                                    ?o rdfs:label ?oL.   
                                                    FILTER (lang(?oL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsObjective ?ob.
                                                    ?ob rdfs:label ?obL.
                                                    FILTER (lang(?obL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsParameter ?pa.
                                                    ?pa rdfs:label ?paL.
                                                    FILTER (lang(?paL) = 'en')}}
                                        OPTIONAL {{ ?Task :containsConstant ?co.
                                                    ?co rdfs:label ?coL.
                                                    FILTER (lang(?coL) = 'en')}}
                                       }}
                  
                                 GROUP BY ?Task ?subclass ?quote ?isLinear ?isNotLinear''',
                  
                  'IntraClass': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  
                                        SELECT ?t ?tc ?tC ?TC
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?t), " >|< ", STR(?TC))); separator=" <|> ") AS ?Item)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?gb), " >|< ", STR(?gbL), " >|< ", STR(?tC), " >|< ", STR(?gbC))); separator=" <|> ") AS ?generalizedBy)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?g), " >|< ", STR(?gL), " >|< ", STR(?tC), " >|< ", STR(?gC))); separator=" <|> ") AS ?generalizes)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?ab), " >|< ", STR(?abL), " >|< ", STR(?tC), " >|< ", STR(?abC))); separator=" <|> ") AS ?approximatedBy)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?a), " >|< ", STR(?aL), " >|< ", STR(?tC), " >|< ", STR(?aC))); separator=" <|> ") AS ?approximates)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?db), " >|< ", STR(?dbL), " >|< ", STR(?tC), " >|< ", STR(?dbC))); separator=" <|> ") AS ?discretizedBy)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?d), " >|< ", STR(?dL), " >|< ", STR(?tC), " >|< ", STR(?dC))); separator=" <|> ") AS ?discretizes)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?lb), " >|< ", STR(?lbL), " >|< ", STR(?tC), " >|< ", STR(?lbC))); separator=" <|> ") AS ?linearizedBy)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?l), " >|< ", STR(?lL), " >|< ", STR(?tC), " >|< ", STR(?lC))); separator=" <|> ") AS ?linearizes)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?nb), " >|< ", STR(?nbL), " >|< ", STR(?tC), " >|< ", STR(?nbC))); separator=" <|> ") AS ?nondimensionalizedBy)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?n), " >|< ", STR(?nL), " >|< ", STR(?tC), " >|< ", STR(?nC))); separator=" <|> ") AS ?nondimensionalizes)
                                               (GROUP_CONCAT(DISTINCT(CONCAT(STR(?s), " >|< ", STR(?sL), " >|< ", STR(?tC), " >|< ", STR(?sC))); separator=" <|> ") AS ?similarTo)
                                               
                                        WHERE {{
                                                 VALUES ?t {{{0}}}
                                                 ?t a ?tc.
                                                 FILTER (?tc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind, :ResearchField, :ResearchProblem))
                                                 BIND(STRAFTER(STR(?tc), "#") AS ?tC)
                                                 BIND(IF(STRAFTER(STR(?tc), "#") = "ComputationalTask", "Task", IF(STRAFTER(STR(?tc), "#") = "QuantityKind", "Quantity", STRAFTER(STR(?tc), "#"))) AS ?TC)
                                                 OPTIONAL {{ 
                                                             ?t (:generalizedByTask | :generalizedByModel | :generalizedByFormulation | :generalizedByQuantity | :generalizedByField | :generalizedByProblem)  ?gb. 
                                                             ?gb rdfs:label ?gbL.
                                                             ?gb a ?gbc.
                                                             FILTER (lang(?gbL) = 'en')
                                                             FILTER (?gbc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind, :ResearchField, :ResearchProblem))
                                                             BIND(STRAFTER(STR(?gbc), "#") AS ?gbC)
                                                          }}
                                                 OPTIONAL {{ 
                                                             ?t (:generalizesTask | :generalizesModel | :generalizesFormulation | :generalizesQuantity | :generalizesField | :generalizesProblem) ?g. 
                                                             ?g rdfs:label ?gL.
                                                             ?g a ?gc.
                                                             FILTER (lang(?gL) = 'en')
                                                             FILTER (?gc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind, :ResearchField, :ResearchProblem))
                                                             BIND(STRAFTER(STR(?gc), "#") AS ?gC)
                                                          }}
                                                 OPTIONAL {{ 
                                                             ?t (:approximatedByTask | :approximatedByModel | :approximatedByFormulation | :approximatedByQuantity) ?ab. 
                                                             ?ab rdfs:label ?abL.
                                                             ?ab a ?abc.
                                                             FILTER (lang(?abL) = 'en')
                                                             FILTER (?abc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind))
                                                             BIND(STRAFTER(STR(?abc), "#") AS ?abC)
                                                          }}
                                                 OPTIONAL {{ 
                                                             ?t (:approximatesTask | :approximatesModel | :approximatesFormulation | :approximatesQuantity) ?a. 
                                                             ?a rdfs:label ?aL.
                                                             ?a a ?ac.
                                                             FILTER (lang(?aL) = 'en')
                                                             FILTER (?ac IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind))
                                                             BIND(STRAFTER(STR(?ac), "#") AS ?aC)
                                                          }}
                                                 OPTIONAL {{ 
                                                             ?t (:discretizedByTask | :discretizedByModel | :discretizedByFormulation) ?db. 
                                                             ?db rdfs:label ?dbL.
                                                             ?db a ?dbc.
                                                             FILTER (lang(?dbL) = 'en')
                                                             FILTER (?dbc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind))
                                                             BIND(STRAFTER(STR(?dbc), "#") AS ?dbC)
                                                          }}
                                                 OPTIONAL {{ ?t (:discretizesTask | :discretizesModel | :discretizesFormulation) ?d. 
                                                             ?d rdfs:label ?dL.
                                                             ?d a ?dc.
                                                             FILTER (lang(?dL) = 'en')
                                                             FILTER (?dc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind))
                                                             BIND(STRAFTER(STR(?dc), "#") AS ?dC)
                                                          }}
                                                 OPTIONAL {{ 
                                                             ?t (:linearizedByTask | :linearizedByModel | :linearizedByFormulation | :linearizedByQuantity) ?lb.
                                                             ?lb rdfs:label ?lbL.
                                                             ?lb a ?lbc.
                                                             FILTER (lang(?lbL) = 'en')
                                                             FILTER (?lbc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind))
                                                             BIND(STRAFTER(STR(?lbc), "#") AS ?lbC)
                                                          }}
                                                 OPTIONAL {{ 
                                                             ?t (:linearizesTask | :linearizesModel | :linearizesFormulation | :linearizesQuantity) ?l.
                                                             ?l rdfs:label ?lL.
                                                             ?l a ?lc.
                                                             FILTER (lang(?lL) = 'en')
                                                             FILTER (?lc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind))
                                                             BIND(STRAFTER(STR(?lc), "#") AS ?lC)
                                                          }}
                                                 OPTIONAL {{ 
                                                             ?t (:nondimensionalizedByFormulation | :nondimensionalizedByQuantity) ?nb.
                                                             ?nb rdfs:label ?nbL.
                                                             ?nb a ?nbc.
                                                             FILTER (lang(?nbL) = 'en')
                                                             FILTER (?nbc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind))
                                                             BIND(STRAFTER(STR(?nbc), "#") AS ?nbC)
                                                          }}
                                                 OPTIONAL {{ 
                                                             ?t (:nondimensionalizesFormulation | :nondimensionalizesQuantity) ?n.
                                                             ?n rdfs:label ?nL.
                                                             ?n a ?nc.
                                                             FILTER (lang(?nL) = 'en')
                                                             FILTER (?nc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind))
                                                             BIND(STRAFTER(STR(?nc), "#") AS ?nC)
                                                          }}
                                                 OPTIONAL {{ 
                                                             ?t (:similarToTask | :similarToModel | :similarToFormulation | :similarToQuantity) ?s. 
                                                             ?s rdfs:label ?sL.
                                                             ?s a ?sc.
                                                             FILTER (lang(?sL) = 'en')
                                                             FILTER (?sc IN (:MathematicalModel, :MathematicalFormulation, :ComputationalTask, :Quantity, :QuantityKind))
                                                             BIND(STRAFTER(STR(?sc), "#") AS ?sC)
                                                          }}
                                              }}
                  
                                  GROUP BY ?t ?tc ?tC ?TC''',
                                  
                  'MathematicalFormulation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  
                                 SELECT ?MathematicalFormulation ?quote ?isLinear ?isNotLinear ?isConvex ?isNotConvex ?isDynamic ?isStatic ?isDeterministic ?isStochastic 
                                        ?isDimensionless ?isDimensional ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent ?isSpaceContinuous ?isSpaceDiscrete ?isSpaceIndependent
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?f), " >|< ", STR(?fL))); separator=" <|> ") AS ?containsFormulation)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?a), " >|< ", STR(?aL))); separator=" <|> ") AS ?containsAssumption)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?bc), " >|< ", STR(?bcL))); separator=" <|> ") AS ?containsBoundaryCondition)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?cc), " >|< ", STR(?ccL))); separator=" <|> ") AS ?containsConstraintCondition)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?cpc), " >|< ", STR(?cpcL))); separator=" <|> ") AS ?containsCouplingCondition)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?ic), " >|< ", STR(?icL))); separator=" <|> ") AS ?containsInitialCondition)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?fc), " >|< ", STR(?fcL))); separator=" <|> ") AS ?containsFinalCondition)
                                        (GROUP_CONCAT(DISTINCT(?elements); separator=" <|> ") AS ?formula_elements) (GROUP_CONCAT(DISTINCT(?formulas); separator=" <|> ") AS ?formula)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?qID), " >|< ", STR(?qL), " >|< ", STR(?qC))); separator=" <|> ") AS ?ContainsQuantity)
                  
                                 WHERE {{
                                        
                                        VALUES ?MathematicalFormulation {{{0}}}
                  
                                        OPTIONAL {{ ?MathematicalFormulation rdfs:comment ?quote.
                                                    FILTER (lang(?quote) = 'en')}}
                  
                                        OPTIONAL {{ ?MathematicalFormulation :isLinear ?isLinear.
                                                    BIND(IF(?isLinear = false, true, false) AS ?isNotLinear)}}
                                        OPTIONAL {{ ?MathematicalFormulation :isConvex ?isConvex.
                                                    BIND(IF(?isConvex = false, true, false) AS ?isNotConvex)}}  
                                        OPTIONAL {{ ?MathematicalFormulation :isDynamic ?isDynamic.
                                                    BIND(IF(?isDynamic = false, true, false) AS ?isStatic)}}                             
                                        OPTIONAL {{ ?MathematicalFormulation :isDeterministic ?isDeterministic.
                                                    BIND(IF(?isDeterministic = false, true, false) AS ?isStochastic)}}
                          		          OPTIONAL {{ ?MathematicalFormulation :isDimensionless ?isDimensionless.
                                                    BIND(IF(?isDimensionless = false, true, false) AS ?isDimensional)}}
                                        OPTIONAL {{ ?MathematicalFormulation :isTimeContinuous ?isTimeContinuous.
                                                    BIND(IF(BOUND(?isTimeContinuous) && ?isTimeContinuous = false, true, false) AS ?isTimeDiscrete)}}
                                                    BIND(IF(!BOUND(?isTimeContinuous), true, false) AS ?isTimeIndependent)
                                        OPTIONAL {{ ?MathematicalFormulation :isSpaceContinuous ?isSpaceContinuous.
                                                    BIND(IF(BOUND(?isSpaceContinuous) && ?isSpaceContinuous = false, true, false) AS ?isSpaceDiscrete)}}
                                                    BIND(IF(!BOUND(?isSpaceContinuous), true, false) AS ?isSpaceIndependent)

                                        OPTIONAL {{ ?MathematicalFormulation :containsFormulation ?f.
                                                    ?f rdfs:label ?fL.
                                                    FILTER (lang(?fL) = 'en')}}
                                        OPTIONAL {{ ?MathematicalFormulation :containsAssumption ?a.
                                                    ?a rdfs:label ?aL.
                                                    FILTER (lang(?aL) = 'en')}}
                                        OPTIONAL {{ ?MathematicalFormulation :containsBoundaryCondition ?bc.
                                                    ?bc rdfs:label ?bcL.
                                                    FILTER (lang(?bcL) = 'en')}}
                                        OPTIONAL {{ ?MathematicalFormulation :containsConstraintCondition ?cc.
                                                    ?cc rdfs:label ?ccL.
                                                    FILTER (lang(?ccL) = 'en')}}
                                        OPTIONAL {{ ?MathematicalFormulation :containsCouplingCondition ?cpc.
                                                    ?cpc rdfs:label ?cpcL.
                                                    FILTER (lang(?cpcL) = 'en')}}
                                        OPTIONAL {{ ?MathematicalFormulation :containsInitialCondition ?ic.
                                                    ?ic rdfs:label ?icL.
                                                    FILTER (lang(?icL) = 'en')}}
                                        OPTIONAL {{ ?MathematicalFormulation :containsFinalCondition ?fc.
                                                    ?fc rdfs:label ?fcL.
                                                    FILTER (lang(?fcL) = 'en')}}
                  
                                        OPTIONAL {{ ?MathematicalFormulation :definingFormulation ?formulas.}}
                                        OPTIONAL {{ ?MathematicalFormulation :inDefiningFormulation ?elements.}}
                  
                                        OPTIONAL {{ ?MathematicalFormulation :containsQuantity ?qID.
                                                    ?qID rdfs:label ?qL;
                                                                a ?qc.
                                                    FILTER (?qc IN (:Quantity, :QuantityKind))
                                                    FILTER (lang(?qL) = 'en')
                                                    BIND(STRAFTER(STR(?qc), "#") AS ?qC)}}
                  
                                        }}
                  
                                        GROUP BY ?MathematicalFormulation ?quote ?isLinear ?isNotLinear ?isConvex ?isNotConvex ?isDynamic ?isStatic ?isDeterministic ?isStochastic ?isDimensionless 
                                                 ?isDimensional ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent ?isSpaceContinuous ?isSpaceDiscrete ?isSpaceIndependent''',
                  
                  'PublicationModel': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                  
                                 SELECT ?item ?label ?class
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?item), " >|< ", STR(?class))); separator=" <|> ") AS ?Item)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?pu1), " >|< ", STR(?label1))); separator=" <|> ") AS ?documentedIn)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?pu2), " >|< ", STR(?label2))); separator=" <|> ") AS ?inventedIn)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?pu3), " >|< ", STR(?label3))); separator=" <|> ") AS ?studiedIn)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?pu4), " >|< ", STR(?label4))); separator=" <|> ") AS ?surveyedIn)
                                        (GROUP_CONCAT(DISTINCT(CONCAT(STR(?pu5), " >|< ", STR(?label5))); separator=" <|> ") AS ?usedIn)
                  
                                 WHERE {{
                  
                                        VALUES ?item {{{0}}}
                                        
                                        ?item rdfs:label ?label;
                                              a ?itemclass.
                                        
                                        FILTER (lang(?label) = 'en')
                                        FILTER (?itemclass IN (:ResearchField, :ResearchProblem, :MathematicalModel, :MathematicalFormulation, :Quantity, :QuantityKind, :ComputationalTask))
                                        
                                        BIND(IF(STRAFTER(STR(?itemclass), "#") = "ComputationalTask", "Task", IF(STRAFTER(STR(?itemclass), "#") = "QuantityKind", "Quantity", STRAFTER(STR(?itemclass), "#"))) AS ?class)

                                        OPTIONAL {{ ?item :documentedIn ?pu1.
                                                    ?pu1 rdfs:label ?label1.
                                                    FILTER (lang(?label1) = 'en')
                                                 }}
                  
                                        OPTIONAL {{ ?item :inventedIn ?pu2.
                                                    ?pu2 rdfs:label ?label2.
                                                    FILTER (lang(?label2) = 'en')
                                                 }}
                  
                                        OPTIONAL {{ ?item :studiedIn ?pu3.
                                                    ?pu3 rdfs:label ?label3.
                                                    FILTER (lang(?label3) = 'en')
                                                 }}
                  
                                        OPTIONAL {{ ?item :surveyedIn ?pu4.
                                                    ?pu4 rdfs:label ?label4.
                                                    FILTER (lang(?label4) = 'en')
                                                 }}
                  
                                        OPTIONAL {{ ?item :usedIn ?pu5.
                                                    ?pu5 rdfs:label ?label5.
                                                    FILTER (lang(?label5) = 'en')
                                                 }}
                  
                                       }}
                  
                                 GROUP BY ?item ?label ?class ?Documents ?Invents ?Studies ?Surveys  ?Uses'''
                 }    

queryProvider = {
                 'RT': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                          SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)
                          WHERE {{
                                  {0} :appliedByTask ?answer .
                                  ?answer rdfs:label ?l .
                                  FILTER (lang(?l) = 'en')
                                }}
                         GROUP BY ?answer ?label''',

                 'RF': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                              SELECT DISTINCT ?id ?label ?quote
                              WHERE { 
                                     ?idraw a :ResearchField .
                                     BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                     OPTIONAL {?idraw rdfs:label ?labelraw .
                                               FILTER (lang(?labelraw) = 'en')}
                                     BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                     OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                               FILTER (lang(?quoteraw) = 'en')}
                                     BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                    }
                               GROUP BY ?id ?label ?quote''',
                 
                 'RP': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                              SELECT DISTINCT ?id ?label ?quote
                              WHERE { 
                                     ?idraw a :ResearchProblem .
                                     BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                     OPTIONAL {?idraw rdfs:label ?labelraw .
                                               FILTER (lang(?labelraw) = 'en')}
                                     BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                     OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                               FILTER (lang(?quoteraw) = 'en')}
                                     BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                    }
                               GROUP BY ?id ?label ?quote''',
                 
                  'MM': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                              SELECT DISTINCT ?id ?label ?quote
                              WHERE { 
                                     ?idraw a :MathematicalModel .
                                     BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                     OPTIONAL {?idraw rdfs:label ?labelraw .
                                               FILTER (lang(?labelraw) = 'en')}
                                     BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                     OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                               FILTER (lang(?quoteraw) = 'en')}
                                     BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                    }
                               GROUP BY ?id ?label ?quote''',

                 
                 'MF': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                                WHERE { 
                                       ?answer a :MathematicalFormulation .
                                       ?answer rdfs:label ?l .
                                       FILTER (lang(?l) = 'en')
                                      }
                                GROUP BY ?answer ?label''',
                 
                 'Q': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                             SELECT DISTINCT ?id ?label ?quote
                              WHERE { 
                                     ?idraw a :Quantity .
                                     BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                     OPTIONAL {?idraw rdfs:label ?labelraw .
                                               FILTER (lang(?labelraw) = 'en')}
                                     BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                     OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                               FILTER (lang(?quoteraw) = 'en')}
                                     BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                    }
                               GROUP BY ?id ?label ?quote''',
                 
                 'QK': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                              SELECT DISTINCT ?id ?label ?quote
                              WHERE { 
                                     ?idraw a :QuantityKind .
                                     BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                     OPTIONAL {?idraw rdfs:label ?labelraw .
                                               FILTER (lang(?labelraw) = 'en')}
                                     BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                     OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                               FILTER (lang(?quoteraw) = 'en')}
                                     BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                    }
                               GROUP BY ?id ?label ?quote''',
                 
                 'T': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                              SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                              WHERE {
                                     ?answer a :ComputationalTask . 
                                     ?answer rdfs:label ?l .
                                     FILTER (lang(?l) = 'en')
                                    }
                               GROUP BY ?answer ?label''',
                 
                 'P': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                              SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                              WHERE {
                                     ?answer a :Publication . 
                                     ?answer rdfs:label ?l .
                                     FILTER (lang(?l) = 'en')
                                    }
                               GROUP BY ?answer ?label''',
                 
                 'QQK': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                               SELECT DISTINCT ?id ?label ?quote
                               WHERE { 
                                     { ?idraw a :Quantity }
                                     UNION
                                     { ?idraw a :QuantityKind }
                                     BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                     OPTIONAL {?idraw rdfs:label ?labelraw .
                                               FILTER (lang(?labelraw) = 'en')}
                                     BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                     OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                               FILTER (lang(?quoteraw) = 'en')}
                                     BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                    }
                               GROUP BY ?id ?label ?quote'''
                }

queryModelHandler = {
    
       'All':   '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
             
                   SELECT DISTINCT ?mm ?mml ?mmd ?rp ?rpl ?rpd ?rf ?rfl ?rfd ?ta ?tal 
                                   (GROUP_CONCAT(DISTINCT(?mf); SEPARATOR=" / ") AS ?MF)
                                   (GROUP_CONCAT(DISTINCT(?mfl); SEPARATOR=" / ") AS ?MFL)
                                   (GROUP_CONCAT(DISTINCT(?mfd); SEPARATOR=" / ") AS ?MFD)
                                   (GROUP_CONCAT(DISTINCT(?q); SEPARATOR=" / ") AS ?Q)
                                   (GROUP_CONCAT(DISTINCT(?ql); SEPARATOR=" / ") AS ?QL)
                                   (GROUP_CONCAT(DISTINCT(?qd); SEPARATOR=" / ") AS ?QD)

                   WHERE {{ 
                   
                           VALUES ?mmraw {{{0}}}

                           BIND(STRAFTER(STR(?mmraw), "#") AS ?mm)
                     
                           OPTIONAL {{
                                      ?mmraw rdfs:label ?mmlraw
                                      FILTER (lang(?mmlraw) = 'en')
                                    }}
                                                                  
                           BIND(COALESCE(?mmlraw, "No Label Provided!") AS ?mml)

                           OPTIONAL {{
                                      ?mmraw rdfs:comment ?mmdraw
                                      FILTER (lang(?mmdraw) = 'en')
                                    }}

                           BIND(COALESCE(?mmdraw, "No Description Provided!") AS ?mmd)

                           OPTIONAL {{
                                      ?mmraw (:containsFormulation | :containsBoundaryCondition | :containsAssumption | :containsConstraintCondition | :containsCouplingCondition | :containsInitialCondition | :containsFinalCondition) ?mfraw.
                                      
                                      BIND(STRAFTER(STR(?mfraw), "#") AS ?mf)

                                      OPTIONAL {{
                                                 ?mfraw rdfs:label ?mflraw
                                                 FILTER (lang(?mflraw) = 'en')
                                               }}
                                                                  
                                      BIND(COALESCE(?mflraw, "No Label Provided!") AS ?mfl)

                                      OPTIONAL {{
                                                 ?mfraw rdfs:comment ?mfdraw
                                                 FILTER (lang(?mfdraw) = 'en')
                                               }}
                                                                  
                                      BIND(COALESCE(?mfdraw, "No Label Provided!") AS ?mfd)
                                    
                                      OPTIONAL {{
                                                 ?mfraw :containsQuantity ?qraw.
                                                 
                                                 BIND(STRAFTER(STR(?qraw), "#") AS ?q)
                                                 
                                                 OPTIONAL {{
                                                            ?qraw rdfs:label ?qlraw
                                                            FILTER (lang(?qlraw) = 'en')
                                                          }}
                                                                  
                                                 BIND(COALESCE(?qlraw, "No Label Provided!") AS ?ql)

                                                 OPTIONAL {{
                                                            ?qraw rdfs:comment ?qdraw
                                                            FILTER (lang(?qdraw) = 'en')
                                                          }}
                                                                  
                                                 BIND(COALESCE(?qdraw, "No Label Provided!") AS ?qd)
                                               }}
                                    }}

                           OPTIONAL {{
                                      ?mmraw :models ?rpraw.
                                      BIND(STRAFTER(STR(?rpraw), "#") AS ?rp)
                                      OPTIONAL {{ ?rpraw rdfs:label ?rplraw .
                                                  FILTER (lang(?rplraw) = 'en') }}
                                      BIND(COALESCE(?rplraw, "No Label Provided!") AS ?rpl)
                                      OPTIONAL {{ ?rpraw rdfs:comment ?rpdraw.
                                                  FILTER (lang(?rpdraw) = 'en') }}
                                      BIND(COALESCE(?rpdraw, "No Description Provided!") AS ?rpd)  

                                      OPTIONAL {{
                                                 ?rpraw :containedInField ?rfraw.
                                                 BIND(STRAFTER(STR(?rfraw), "#") AS ?rf)
                                                 OPTIONAL {{ ?rfraw rdfs:label ?rflraw .
                                                             FILTER (lang(?rflraw) = 'en') }}
                                                 BIND(COALESCE(?rflraw, "No Label Provided!") AS ?rfl)
                                                 OPTIONAL {{ ?rfraw rdfs:comment ?rfdraw.
                                                             FILTER (lang(?rfdraw) = 'en') }}
                                                 BIND(COALESCE(?rfdraw, "No Description Provided!") AS ?rfd)
                                               }}

                                    }}

                           OPTIONAL {{         
                                      ?mmraw :appliedByTask ?ta.
                                      ?ta rdfs:label ?tal.
                                      FILTER (lang(?tal) = 'en')
                                    }} 
                    }}

               GROUP BY ?mm ?mml ?mmd ?fmf ?rp ?rpl ?rpd ?rf ?rfl ?rfd ?ta ?tal''',

       'MFRelations':  '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                          SELECT ?mf 
                                 (GROUP_CONCAT(DISTINCT(?f); separator=" <|> ") AS ?F) (GROUP_CONCAT(DISTINCT(?fL); SEPARATOR=" <|> ") AS ?FL)
                                 (GROUP_CONCAT(DISTINCT(?fd); separator=" <|> ") AS ?FD) (GROUP_CONCAT(DISTINCT(?fdL); SEPARATOR=" <|> ") AS ?FDL)
                                 (GROUP_CONCAT(DISTINCT(?a); separator=" <|> ") AS ?A) (GROUP_CONCAT(DISTINCT(?aL); SEPARATOR=" <|> ") AS ?AL)
                                 (GROUP_CONCAT(DISTINCT(?ad); separator=" <|> ") AS ?AD) (GROUP_CONCAT(DISTINCT(?adL); SEPARATOR=" <|> ") AS ?ADL)
                                 (GROUP_CONCAT(DISTINCT(?bc); separator=" <|> ") AS ?BC) (GROUP_CONCAT(DISTINCT(?bcL); SEPARATOR=" <|> ") AS ?BCL)
                                 (GROUP_CONCAT(DISTINCT(?bcd); separator=" <|> ") AS ?BCD) (GROUP_CONCAT(DISTINCT(?bcdL); SEPARATOR=" <|> ") AS ?BCDL)
                                 (GROUP_CONCAT(DISTINCT(?cc); separator=" <|> ") AS ?CC) (GROUP_CONCAT(DISTINCT(?ccL); SEPARATOR=" <|> ") AS ?CCL)
                                 (GROUP_CONCAT(DISTINCT(?ccd); separator=" <|> ") AS ?CCD) (GROUP_CONCAT(DISTINCT(?ccdL); SEPARATOR=" <|> ") AS ?CCDL)
                                 (GROUP_CONCAT(DISTINCT(?cpc); separator=" <|> ") AS ?CPC) (GROUP_CONCAT(DISTINCT(?cpcL); SEPARATOR=" <|> ") AS ?CPCL)
                                 (GROUP_CONCAT(DISTINCT(?cpcd); separator=" <|> ") AS ?CPCD) (GROUP_CONCAT(DISTINCT(?cpcdL); SEPARATOR=" <|> ") AS ?CPCDL)
                                 (GROUP_CONCAT(DISTINCT(?ic); separator=" <|> ") AS ?IC) (GROUP_CONCAT(DISTINCT(?icL); SEPARATOR=" <|> ") AS ?ICL)
                                 (GROUP_CONCAT(DISTINCT(?icd); separator=" <|> ") AS ?ICD) (GROUP_CONCAT(DISTINCT(?icdL); SEPARATOR=" <|> ") AS ?ICDL)
                                 (GROUP_CONCAT(DISTINCT(?fc); separator=" <|> ") AS ?FC) (GROUP_CONCAT(DISTINCT(?fcL); SEPARATOR=" <|> ") AS ?FCL)
                                 (GROUP_CONCAT(DISTINCT(?fcd); separator=" <|> ") AS ?FCD) (GROUP_CONCAT(DISTINCT(?fcdL); SEPARATOR=" <|> ") AS ?FCDL)
                                 (GROUP_CONCAT(DISTINCT(?fgbf); separator=" <|> ") AS ?FGBF) (GROUP_CONCAT(DISTINCT(?fgbfL); SEPARATOR=" <|> ") AS ?FGBFL)
                                 (GROUP_CONCAT(DISTINCT(?fgf); separator=" <|> ") AS ?FGF) (GROUP_CONCAT(DISTINCT(?fgfL); SEPARATOR=" <|> ") AS ?FGFL)
                                 (GROUP_CONCAT(DISTINCT(?fabf); separator=" <|> ") AS ?FABF) (GROUP_CONCAT(DISTINCT(?fabfL); SEPARATOR=" <|> ") AS ?FABFL)
                                 (GROUP_CONCAT(DISTINCT(?faf); separator=" <|> ") AS ?FAF) (GROUP_CONCAT(DISTINCT(?fafL); SEPARATOR=" <|> ") AS ?FAFL)
                                 (GROUP_CONCAT(DISTINCT(?fdbf); separator=" <|> ") AS ?FDBF) (GROUP_CONCAT(DISTINCT(?fdbfL); SEPARATOR=" <|> ") AS ?FDBFL)
                                 (GROUP_CONCAT(DISTINCT(?fdf); separator=" <|> ") AS ?FDF) (GROUP_CONCAT(DISTINCT(?fdfL); SEPARATOR=" <|> ") AS ?FDFL)
                                 (GROUP_CONCAT(DISTINCT(?flbf); separator=" <|> ") AS ?FLBF) (GROUP_CONCAT(DISTINCT(?flbfL); SEPARATOR=" <|> ") AS ?FLBFL)
                                 (GROUP_CONCAT(DISTINCT(?flf); separator=" <|> ") AS ?FLF) (GROUP_CONCAT(DISTINCT(?flfL); SEPARATOR=" <|> ") AS ?FLFL)
                                 (GROUP_CONCAT(DISTINCT(?fnbf); separator=" <|> ") AS ?FNBF) (GROUP_CONCAT(DISTINCT(?fnbfL); SEPARATOR=" <|> ") AS ?FNBFL)
                                 (GROUP_CONCAT(DISTINCT(?fnf); separator=" <|> ") AS ?FNF) (GROUP_CONCAT(DISTINCT(?fnfL); SEPARATOR=" <|> ") AS ?FNFL)
                                 (GROUP_CONCAT(DISTINCT(?fsf); separator=" <|> ") AS ?FSF) (GROUP_CONCAT(DISTINCT(?fsfL); SEPARATOR=" <|> ") AS ?FSFL)
                                 
                          WHERE {{
                                 
                                 VALUES ?mf {{{0}}}
          
                                 OPTIONAL {{ ?mf :containsFormulation ?f.
                                             ?f a :MathematicalFormulation.
                                             ?f rdfs:label ?fL.
                                             FILTER (lang(?fL) = 'en')}}

                                 OPTIONAL {{ ?mf :containedAsFormulationIn ?fd.
                                             ?fd a :MathematicalFormulation.
                                             ?fd rdfs:label ?fdL.
                                             FILTER (lang(?fdL) = 'en')}}

                                 OPTIONAL {{ ?mf :containsAssumption ?a.
                                             ?a a :MathematicalFormulation.
                                             ?a rdfs:label ?aL.
                                             FILTER (lang(?aL) = 'en')}}

                                 OPTIONAL {{ ?mf :containedAsAssumptionIn ?ad.
                                             ?ad a :MathematicalFormulation.
                                             ?ad rdfs:label ?adL.
                                             FILTER (lang(?adL) = 'en')}}

                                 OPTIONAL {{ ?mf :containsBoundaryCondition ?bc.
                                             ?bc a :MathematicalFormulation.
                                             ?bc rdfs:label ?bcL.
                                             FILTER (lang(?bcL) = 'en')}}

                                 OPTIONAL {{ ?mf :containedAsBoundaryConditionIn ?bcd.
                                             ?bcd a :MathematicalFormulation.
                                             ?bcd rdfs:label ?bcdL.
                                             FILTER (lang(?bcdL) = 'en')}}

                                 OPTIONAL {{ ?mf :containsConstraintCondition ?cc.
                                             ?cc a :MathematicalFormulation.
                                             ?cc rdfs:label ?ccL.
                                             FILTER (lang(?ccL) = 'en')}}

                                 OPTIONAL {{ ?mf :containedAsConstraintConditionIn ?ccd.
                                             ?ccd a :MathematicalFormulation.
                                             ?ccd rdfs:label ?ccdL.
                                             FILTER (lang(?ccdL) = 'en')}}

                                 OPTIONAL {{ ?mf :containsCouplingCondition ?cpc.
                                             ?cpc a :MathematicalFormulation.
                                             ?cpc rdfs:label ?cpcL.
                                             FILTER (lang(?cpcL) = 'en')}}

                                 OPTIONAL {{ ?mf :containedAsCouplingConditionIn ?cpcd.
                                             ?cpcd a :MathematicalFormulation.
                                             ?cpcd rdfs:label ?cpcdL.
                                             FILTER (lang(?cpcdL) = 'en')}}

                                 OPTIONAL {{ ?mf :containsInitialCondition ?ic.
                                             ?ic a :MathematicalFormulation.
                                             ?ic rdfs:label ?icL.
                                             FILTER (lang(?icL) = 'en')}}

                                 OPTIONAL {{ ?mf :containedAsInitialConditionIn ?icd.
                                             ?icd a :MathematicalFormulation. 
                                             ?icd rdfs:label ?icdL.
                                             FILTER (lang(?icdL) = 'en')}}

                                 OPTIONAL {{ ?mf :containsFinalCondition ?fc.
                                             ?fc a :MathematicalFormulation.
                                             ?fc rdfs:label ?fcL.
                                             FILTER (lang(?fcL) = 'en')}}
                                
                                 OPTIONAL {{ ?mf :containedAsFinalConditionIn ?fcd.
                                             ?fcd a :MathematicalFormulation.
                                             ?fcd rdfs:label ?fcdL.
                                             FILTER (lang(?fcdL) = 'en')}}

                                 OPTIONAL {{ 
                                           ?mf :generalizedByFormulation ?fgbf. 
                                           ?fgbf rdfs:label ?fgbfL.
                                           FILTER (lang(?fgbfL) = 'en')
                                        }}

                               OPTIONAL {{ 
                                           ?mf :generalizesFormulation ?fgf. 
                                           ?fgf rdfs:label ?fgfL.
                                           FILTER (lang(?fgfL) = 'en')
                                        }}
                               OPTIONAL {{ 
                                           ?mf :approximatedByFormulation ?fabf. 
                                           ?fabf rdfs:label ?fabfL.
                                           FILTER (lang(?abL) = 'en')
                                        }}
                               OPTIONAL {{ 
                                           ?mf :approximatesFormulation ?faf. 
                                           ?faf rdfs:label ?fafL.
                                           FILTER (lang(?fafL) = 'en')
                                        }}
                               OPTIONAL {{ 
                                           ?mf :discretizedByFormulation ?fdbf. 
                                           ?fdbf rdfs:label ?fdbfL.
                                           FILTER (lang(?fdbfL) = 'en')
                                        }}
                               OPTIONAL {{ ?mf :discretizesFormulation ?fdf. 
                                           ?fdf rdfs:label ?fdfL.
                                           FILTER (lang(?fdfL) = 'en')
                                        }}
                               OPTIONAL {{ 
                                           ?mf :linearizedByFormulation ?flbf.
                                           ?flbf rdfs:label ?flbfL.
                                           FILTER (lang(?flbfL) = 'en')
                                        }}
                               OPTIONAL {{ 
                                           ?mf :linearizesFormulation ?flf.
                                           ?flf rdfs:label ?flfL.
                                           FILTER (lang(?flfL) = 'en')
                                        }}
                               OPTIONAL {{ 
                                           ?mf :nondimensionalizedByFormulation ?fnbf.
                                           ?fnbf rdfs:label ?fnbfL.
                                           FILTER (lang(?fnbfL) = 'en')
                                        }}
                               OPTIONAL {{ 
                                           ?mf :nondimensionalizesFormulation ?fnf.
                                           ?fnf rdfs:label ?fnfL.
                                           FILTER (lang(?fnfL) = 'en')
                                        }}
                               OPTIONAL {{ 
                                           ?mf :similarToFormulation ?fsf. 
                                           ?fsf rdfs:label ?fsfL.
                                           FILTER (lang(?fsfL) = 'en')
                                        }}

                                }}
          
                              GROUP BY ?mf ?F ?FL ?A ?AL ?BC ?BCL ?CC ?CCL ?CPC ?CPCL ?IC ?ICL ?FC ?FCL 
                                           ?FD ?FDL ?AD ?ADL ?BCD ?BCDL ?CCD ?CCDL ?CPCD ?CPCDL ?ICD ?ICDL ?FCD ?FCDL
                                           ?FGBF ?FGBFL ?FGF ?FGFL ?FABF ?FABFL ?FAF ?FAFL ?FDBF ?FDBFL ?FDF ?FDFL ?FLBF ?FLBFL ?FLF ?FLFL
                                           ?FNBF ?FNBFL ?FNF ?FNFL ?FSF ?FSFL''',

       'TRelation':    '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
                          SELECT ?t 
                                 (GROUP_CONCAT(DISTINCT(?tgbt); separator=" <|> ") AS ?TGBT) (GROUP_CONCAT(DISTINCT(?tgbtL); SEPARATOR=" <|> ") AS ?TGBTL)
                                 (GROUP_CONCAT(DISTINCT(?tgt); separator=" <|> ") AS ?TGT) (GROUP_CONCAT(DISTINCT(?tgtL); SEPARATOR=" <|> ") AS ?TGTL)
                                 (GROUP_CONCAT(DISTINCT(?tabt); separator=" <|> ") AS ?TABT) (GROUP_CONCAT(DISTINCT(?tabtL); SEPARATOR=" <|> ") AS ?TABTL)
                                 (GROUP_CONCAT(DISTINCT(?tat); separator=" <|> ") AS ?TAT) (GROUP_CONCAT(DISTINCT(?tatL); SEPARATOR=" <|> ") AS ?TATL)
                                 (GROUP_CONCAT(DISTINCT(?tdbt); separator=" <|> ") AS ?TDBT) (GROUP_CONCAT(DISTINCT(?tdbtL); SEPARATOR=" <|> ") AS ?TDBTL)
                                 (GROUP_CONCAT(DISTINCT(?tdt); separator=" <|> ") AS ?TDT) (GROUP_CONCAT(DISTINCT(?tdtL); SEPARATOR=" <|> ") AS ?TDTL)
                                 (GROUP_CONCAT(DISTINCT(?tict); separator=" <|> ") AS ?TICT) (GROUP_CONCAT(DISTINCT(?tictL); SEPARATOR=" <|> ") AS ?TICTL)
                                 (GROUP_CONCAT(DISTINCT(?tct); separator=" <|> ") AS ?TCT) (GROUP_CONCAT(DISTINCT(?tctL); SEPARATOR=" <|> ") AS ?TCTL)
                                 (GROUP_CONCAT(DISTINCT(?tlbt); separator=" <|> ") AS ?TLBT) (GROUP_CONCAT(DISTINCT(?tlbtL); SEPARATOR=" <|> ") AS ?TLBTL)
                                 (GROUP_CONCAT(DISTINCT(?tlt); separator=" <|> ") AS ?TLT) (GROUP_CONCAT(DISTINCT(?tltL); SEPARATOR=" <|> ") AS ?TLTL)
                                 (GROUP_CONCAT(DISTINCT(?tst); separator=" <|> ") AS ?TST) (GROUP_CONCAT(DISTINCT(?tstL); SEPARATOR=" <|> ") AS ?TSTL) 
                                                              
                          WHERE {{
                                   VALUES ?t {{{0}}}
                                   
                                   OPTIONAL {{ 
                                               ?t :generalizedByTask ?tgbt. 
                                               ?tgbt rdfs:label ?tgbtL.
                                               FILTER (lang(?tgbtL) = 'en')
                                            }}
                                   OPTIONAL {{ 
                                               ?t :generalizesTask ?tgt. 
                                               ?tgt rdfs:label ?tgtL.
                                               FILTER (lang(?tgtL) = 'en')
                                            }}
                                   OPTIONAL {{ 
                                               ?t :approximatedByTask ?tabt. 
                                               ?tabt rdfs:label ?tabtL.
                                               FILTER (lang(?tabtL) = 'en')
                                            }}
                                   OPTIONAL {{ 
                                               ?t :approximatesTask ?tat. 
                                               ?tat rdfs:label ?tatL.
                                               FILTER (lang(?tatL) = 'en')
                                            }}
                                   OPTIONAL {{ 
                                               ?t :discretizedByTask ?tdbt. 
                                               ?tdbt rdfs:label ?tdbtL.
                                               FILTER (lang(?tdbtL) = 'en')
                                            }}
                                   OPTIONAL {{ ?t :discretizesTask ?tdt. 
                                               ?tdt rdfs:label ?tdtL.
                                               FILTER (lang(?tdtL) = 'en')
                                            }}
                                   OPTIONAL {{ 
                                               ?t :containedInTask ?tict. 
                                               ?tict rdfs:label ?tictL.
                                               FILTER (lang(?tictL) = 'en')
                                            }}
                                   OPTIONAL {{ ?t :containsTask ?tct. 
                                               ?tct rdfs:label ?tctL.
                                               FILTER (lang(?tctL) = 'en')
                                            }}
                                   OPTIONAL {{ 
                                               ?t :linearizedByTask ?tlbt.
                                               ?tlbt rdfs:label ?tlbtL.
                                               FILTER (lang(?tlbtL) = 'en')
                                            }}
                                   OPTIONAL {{ 
                                               ?t :linearizesTask ?tlt.
                                               ?tlt rdfs:label ?tltL.
                                               FILTER (lang(?tltL) = 'en')
                                            }}
                                   OPTIONAL {{ 
                                               ?t :similarToTask ?tst. 
                                               ?tst rdfs:label ?tstL.
                                               FILTER (lang(?tstL) = 'en')
                                            }}
                                }}
    
                    GROUP BY ?t ?TGBT ?TGBTL ?TGT ?TGTL ?TABT ?TABTL ?TAT ?TATL ?TDBT ?TDBTL ?TDT ?TDTL ?TICT ?TICTL ?TCT ?TCTL ?TLBT ?TLBTL ?TLT ?TLTL 
                             ?TST ?TSTL''',

       'PRelation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                       PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
         
                       SELECT ?item ?label ?class
                              (GROUP_CONCAT(DISTINCT(?pu1); separator=" <|> ") AS ?PU1) (GROUP_CONCAT(DISTINCT(?label1); separator=" <|> ") AS ?LABEL1)
                              (GROUP_CONCAT(DISTINCT(?pu2); separator=" <|> ") AS ?PU2) (GROUP_CONCAT(DISTINCT(?label2); separator=" <|> ") AS ?LABEL2)
                              (GROUP_CONCAT(DISTINCT(?pu3); separator=" <|> ") AS ?PU3) (GROUP_CONCAT(DISTINCT(?label3); separator=" <|> ") AS ?LABEL3)
                              (GROUP_CONCAT(DISTINCT(?pu4); separator=" <|> ") AS ?PU4) (GROUP_CONCAT(DISTINCT(?label4); separator=" <|> ") AS ?LABEL4)
                              (GROUP_CONCAT(DISTINCT(?pu5); separator=" <|> ") AS ?PU5) (GROUP_CONCAT(DISTINCT(?label5); separator=" <|> ") AS ?LABEL5)
         
                       WHERE {{
         
                              VALUES ?item {{{0}}}
                              
                              ?item rdfs:label ?label;
                                    a ?class.
                              
                              FILTER (lang(?label) = 'en')
                              FILTER (?class IN (:ResearchField, :ResearchProblem, :MathematicalModel, :MathematicalFormulation, :Quantity, :QuantityKind, :ComputationalTask))
         
                              OPTIONAL {{ ?item :documentedIn ?pu1.
                                          ?pu1 rdfs:label ?label1.
                                          FILTER (lang(?label1) = 'en')
                                       }}
         
                              OPTIONAL {{ ?item :inventedIn ?pu2.
                                          ?pu2 rdfs:label ?label2.
                                          FILTER (lang(?label2) = 'en')
                                       }}
         
                              OPTIONAL {{ ?item :studiedIn ?pu3.
                                          ?pu3 rdfs:label ?label3.
                                          FILTER (lang(?label3) = 'en')
                                       }}
         
                              OPTIONAL {{ ?item :surveyedIn ?pu4.
                                          ?pu4 rdfs:label ?label4.
                                          FILTER (lang(?label4) = 'en')
                                       }}
         
                              OPTIONAL {{ ?item :usedIn ?pu5.
                                          ?pu5 rdfs:label ?label5.
                                          FILTER (lang(?label5) = 'en')
                                       }}
         
                             }}
         
                       GROUP BY ?item ?label ?class ?PU1 ?LABEL1 ?PU2 ?LABEL2 ?PU3 ?LABEL3 ?PU4 ?LABEL4 ?PU5 ?LABEL5''' 
       }

queryHandler = {
    'researchFieldInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT ?id 
                                                               (GROUP_CONCAT(DISTINCT(?gbf); SEPARATOR=" / ") AS ?generalizedByField)
                                                               (GROUP_CONCAT(DISTINCT(?gbfl); SEPARATOR=" / ") AS ?generalizedByFieldLabel)
                                                               (GROUP_CONCAT(DISTINCT(?gbfd); SEPARATOR=" / ") AS ?generalizedByFieldDescription)
                                                               (GROUP_CONCAT(DISTINCT(?gf); SEPARATOR=" / ") AS ?generalizesField)
                                                               (GROUP_CONCAT(DISTINCT(?gfl); SEPARATOR=" / ") AS ?generalizesFieldLabel)
                                                               (GROUP_CONCAT(DISTINCT(?gfd); SEPARATOR=" / ") AS ?generalizesFieldDescription)
                                                               (GROUP_CONCAT(DISTINCT(?sf); SEPARATOR=" / ") AS ?similarToField)
                                                               (GROUP_CONCAT(DISTINCT(?sfl); SEPARATOR=" / ") AS ?similarToFieldLabel)
                                                               (GROUP_CONCAT(DISTINCT(?sfd); SEPARATOR=" / ") AS ?similarToFieldDescription)
                                               WHERE {{ 
                                                       VALUES ?id {{{0}}} 
                                                      
                                                        OPTIONAL {{
                                                                  ?id :generalizedByField ?gbfraw.
                                                                  BIND(STRAFTER(STR(?gbfraw), "#") AS ?gbf)

                                                                  OPTIONAL {{
                                                                             ?gbfraw rdfs:label ?gbflraw
                                                                             FILTER (lang(?gbflraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gbflraw, "No Label Provided!") AS ?gbfl)

                                                                  OPTIONAL {{
                                                                             ?gbfraw rdfs:comment ?gbfdraw
                                                                             FILTER (lang(?gbfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gbfdraw, "No Description Provided!") AS ?gbfd)
                                                                }}
                                                        
                                                        OPTIONAL {{
                                                                  ?id :generalizesField ?gfraw.
                                                                  BIND(STRAFTER(STR(?gfraw), "#") AS ?gf)

                                                                  OPTIONAL {{
                                                                             ?gfraw rdfs:label ?gflraw
                                                                             FILTER (lang(?gflraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gflraw, "No Label Provided!") AS ?gfl)

                                                                  OPTIONAL {{
                                                                             ?gfraw rdfs:comment ?gfdraw
                                                                             FILTER (lang(?gfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gfdraw, "No Description Provided!") AS ?gfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :similarToField ?sfraw.
                                                                  BIND(STRAFTER(STR(?sfraw), "#") AS ?sf)

                                                                  OPTIONAL {{
                                                                             ?sfraw rdfs:label ?sflraw
                                                                             FILTER (lang(?sflraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?sflraw, "No Label Provided!") AS ?sfl)

                                                                  OPTIONAL {{
                                                                             ?sfraw rdfs:comment ?sfdraw
                                                                             FILTER (lang(?sfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?sfdraw, "No Description Provided!") AS ?sfd)
                                                                }}
 
                                                       }}
                                                       GROUP BY ?id''',

    'researchProblemInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT ?id 
                                                               (GROUP_CONCAT(DISTINCT(?rf); SEPARATOR=" / ") AS ?containedInField)
                                                               (GROUP_CONCAT(DISTINCT(?rfl); SEPARATOR=" / ") AS ?containedInFieldLabel)
                                                               (GROUP_CONCAT(DISTINCT(?rfd); SEPARATOR=" / ") AS ?containedInFieldDescription)
                                                               (GROUP_CONCAT(DISTINCT(?gbp); SEPARATOR=" / ") AS ?generalizedByProblem)
                                                               (GROUP_CONCAT(DISTINCT(?gbpl); SEPARATOR=" / ") AS ?generalizedByProblemLabel)
                                                               (GROUP_CONCAT(DISTINCT(?gbpd); SEPARATOR=" / ") AS ?generalizedByProblemDescription)
                                                               (GROUP_CONCAT(DISTINCT(?gp); SEPARATOR=" / ") AS ?generalizesProblem)
                                                               (GROUP_CONCAT(DISTINCT(?gpl); SEPARATOR=" / ") AS ?generalizesProblemLabel)
                                                               (GROUP_CONCAT(DISTINCT(?gpd); SEPARATOR=" / ") AS ?generalizesProblemDescription)
                                                               (GROUP_CONCAT(DISTINCT(?sp); SEPARATOR=" / ") AS ?similarToProblem)
                                                               (GROUP_CONCAT(DISTINCT(?spl); SEPARATOR=" / ") AS ?similarToProblemLabel)
                                                               (GROUP_CONCAT(DISTINCT(?spd); SEPARATOR=" / ") AS ?similarToProblemDescription)
                                               WHERE {{ 
                                                       VALUES ?id {{{0}}} 
                                                       
                                                        OPTIONAL {{
                                                                   ?id :containedInField ?rfraw.
                                                                   BIND(STRAFTER(STR(?rfraw), "#") AS ?rf)

                                                                   OPTIONAL {{
                                                                              ?rfraw rdfs:label ?rflraw.
                                                                              FILTER (lang(?rflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?rflraw, "No Label Provided!") AS ?rfl)

                                                                  OPTIONAL {{
                                                                             ?rfraw rdfs:comment ?rfdraw
                                                                             FILTER (lang(?rfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?rfdraw, "No Description Provided!") AS ?rfd)
                                                               }}

                                                        OPTIONAL {{
                                                                  ?id :generalizedByProblem ?gbpraw.
                                                                  BIND(STRAFTER(STR(?gbpraw), "#") AS ?gbp)

                                                                  OPTIONAL {{
                                                                             ?gbpraw rdfs:label ?gbplraw
                                                                             FILTER (lang(?gbplraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gbplraw, "No Label Provided!") AS ?gbpl)

                                                                  OPTIONAL {{
                                                                             ?gbpraw rdfs:comment ?gbpdraw
                                                                             FILTER (lang(?gbpdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gbpdraw, "No Description Provided!") AS ?gbpd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :generalizesProblem ?gpraw.
                                                                  BIND(STRAFTER(STR(?gpraw), "#") AS ?gp)

                                                                  OPTIONAL {{
                                                                             ?gpraw rdfs:label ?gplraw
                                                                             FILTER (lang(?gplraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gplraw, "No Label Provided!") AS ?gpl)

                                                                  OPTIONAL {{
                                                                             ?gpraw rdfs:comment ?gpdraw
                                                                             FILTER (lang(?gpdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gpdraw, "No Description Provided!") AS ?gpd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :similarToProblem ?spraw.
                                                                  BIND(STRAFTER(STR(?spraw), "#") AS ?sp)

                                                                  OPTIONAL {{
                                                                             ?spraw rdfs:label ?splraw
                                                                             FILTER (lang(?splraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?splraw, "No Label Provided!") AS ?spl)

                                                                  OPTIONAL {{
                                                                             ?spraw rdfs:comment ?spdraw
                                                                             FILTER (lang(?spdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?spdraw, "No Description Provided!") AS ?spd)
                                                                }}
 
                                                       }}

                                                       GROUP BY ?id''',

              'mathematicalModelInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT ?id 
                                                               ?isLinear ?isNotLinear
                                                               ?isConvex ?isNotConvex
                                                               ?isDynamic ?isStatic
                                                               ?isDeterministic ?isStochastic
                                                               ?isDimensionless ?isDimensional
                                                               ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent
                                                               ?isSpaceContinuous ?isSpaceDiscrete ?isSpaceIndependent
                                                               (GROUP_CONCAT(DISTINCT(?rp); SEPARATOR=" / ") AS ?models)
                                                               (GROUP_CONCAT(DISTINCT(?rpl); SEPARATOR=" / ") AS ?modelsLabel)
                                                               (GROUP_CONCAT(DISTINCT(?rpd); SEPARATOR=" / ") AS ?modelsDescription)
                                                               (GROUP_CONCAT(DISTINCT(?gbm); SEPARATOR=" / ") AS ?generalizedByModel)
                                                               (GROUP_CONCAT(DISTINCT(?gbml); SEPARATOR=" / ") AS ?generalizedByModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?gbmd); SEPARATOR=" / ") AS ?generalizedByModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?gm); SEPARATOR=" / ") AS ?generalizesModel)
                                                               (GROUP_CONCAT(DISTINCT(?gml); SEPARATOR=" / ") AS ?generalizesModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?gmd); SEPARATOR=" / ") AS ?generalizesModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?dbm); SEPARATOR=" / ") AS ?discretizedByModel)
                                                               (GROUP_CONCAT(DISTINCT(?dbml); SEPARATOR=" / ") AS ?discretizedByModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?dbmd); SEPARATOR=" / ") AS ?discretizedByModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?dm); SEPARATOR=" / ") AS ?discretizesModel)
                                                               (GROUP_CONCAT(DISTINCT(?dml); SEPARATOR=" / ") AS ?discretizesModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?dmd); SEPARATOR=" / ") AS ?discretizesModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?cim); SEPARATOR=" / ") AS ?containedInModel)
                                                               (GROUP_CONCAT(DISTINCT(?ciml); SEPARATOR=" / ") AS ?containedInModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?cimd); SEPARATOR=" / ") AS ?containedInModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?cm); SEPARATOR=" / ") AS ?containsModel)
                                                               (GROUP_CONCAT(DISTINCT(?cml); SEPARATOR=" / ") AS ?containsModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?cmd); SEPARATOR=" / ") AS ?containsModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?abm); SEPARATOR=" / ") AS ?approximatedByModel)
                                                               (GROUP_CONCAT(DISTINCT(?abml); SEPARATOR=" / ") AS ?approximatedByModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?abmd); SEPARATOR=" / ") AS ?approximatedByModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?am); SEPARATOR=" / ") AS ?approximatesModel)
                                                               (GROUP_CONCAT(DISTINCT(?aml); SEPARATOR=" / ") AS ?approximatesModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?amd); SEPARATOR=" / ") AS ?approximatesModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?lbm); SEPARATOR=" / ") AS ?linearizedByModel)
                                                               (GROUP_CONCAT(DISTINCT(?lbml); SEPARATOR=" / ") AS ?linearizedByModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?lbmd); SEPARATOR=" / ") AS ?linearizedByModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?lm); SEPARATOR=" / ") AS ?linearizesModel)
                                                               (GROUP_CONCAT(DISTINCT(?lml); SEPARATOR=" / ") AS ?linearizesModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?lmd); SEPARATOR=" / ") AS ?linearizesModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?sm); SEPARATOR=" / ") AS ?similarToModel)
                                                               (GROUP_CONCAT(DISTINCT(?sml); SEPARATOR=" / ") AS ?similarToModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?smd); SEPARATOR=" / ") AS ?similarToModelDescription)
                                               WHERE {{ 
                                                       VALUES ?id {{{0}}} 

                                                        OPTIONAL {{ ?id :isLinear ?isLinear.
                                                                BIND(IF(?isLinear = false, true, false) AS ?isNotLinear)}}

                                                       OPTIONAL {{ ?id :isConvex ?isConvex.
                                                                BIND(IF(?isConvex = false, true, false) AS ?isNotConvex)}}  
                                        
                                                       OPTIONAL {{ ?id :isDynamic ?isDynamic.
                                                                BIND(IF(?isDynamic = false, true, false) AS ?isStatic)}}                             
                                        
                                                       OPTIONAL {{ ?id :isDeterministic ?isDeterministic.
                                                                BIND(IF(?isDeterministic = false, true, false) AS ?isStochastic)}}
                                     
                                                       OPTIONAL {{ ?id :isDimensionless ?isDimensionless.
                                                                BIND(IF(?isDimensionless = false, true, false) AS ?isDimensional)}}
                                        
                                                       OPTIONAL {{ ?id :isTimeContinuous ?isTimeContinuous.
                                                                BIND(IF(BOUND(?isTimeContinuous) && ?isTimeContinuous = false, true, false) AS ?isTimeDiscrete)}}
                                                                BIND(IF(!BOUND(?isTimeContinuous), true, false) AS ?isTimeIndependent)
                                        
                                                       OPTIONAL {{ ?id :isSpaceContinuous ?isSpaceContinuous.
                                                                BIND(IF(BOUND(?isSpaceContinuous) && ?isSpaceContinuous = false, true, false) AS ?isSpaceDiscrete)}}
                                                                BIND(IF(!BOUND(?isSpaceContinuous), true, false) AS ?isSpaceIndependent) 

                                                        OPTIONAL {{
                                                                   ?id :models ?rpraw.
                                                                   BIND(STRAFTER(STR(?rpraw), "#") AS ?rp)

                                                                   OPTIONAL {{
                                                                              ?rpraw rdfs:label ?rplraw.
                                                                              FILTER (lang(?rplraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?rplraw, "No Label Provided!") AS ?rpl)

                                                                  OPTIONAL {{
                                                                             ?rpraw rdfs:comment ?rpdraw
                                                                             FILTER (lang(?rpdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?rpdraw, "No Description Provided!") AS ?rpd)
                                                               }}

                                                        OPTIONAL {{
                                                                  ?id :generalizedByModel ?gbmraw.
                                                                  BIND(STRAFTER(STR(?gbmraw), "#") AS ?gbm)

                                                                  OPTIONAL {{
                                                                             ?gbmraw rdfs:label ?gbmlraw
                                                                             FILTER (lang(?gbmlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gbmlraw, "No Label Provided!") AS ?gbml)

                                                                  OPTIONAL {{
                                                                             ?gbmraw rdfs:comment ?gbmdraw
                                                                             FILTER (lang(?gbmdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gbmdraw, "No Description Provided!") AS ?gbmd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :generalizesModel ?gmraw.
                                                                  BIND(STRAFTER(STR(?gmraw), "#") AS ?gm)

                                                                  OPTIONAL {{
                                                                             ?gmraw rdfs:label ?gmlraw
                                                                             FILTER (lang(?gmlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gmlraw, "No Label Provided!") AS ?gml)

                                                                  OPTIONAL {{
                                                                             ?gmraw rdfs:comment ?gmdraw
                                                                             FILTER (lang(?gmdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gmdraw, "No Description Provided!") AS ?gmd)
                                                                }}

                                                      OPTIONAL {{
                                                                  ?id :discretizedByModel ?dbmraw.
                                                                  BIND(STRAFTER(STR(?dbmraw), "#") AS ?dbm)

                                                                  OPTIONAL {{
                                                                             ?dbmraw rdfs:label ?dbmlraw
                                                                             FILTER (lang(?dbmlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?dbmlraw, "No Label Provided!") AS ?dbml)

                                                                  OPTIONAL {{
                                                                             ?dbmraw rdfs:comment ?dbmdraw
                                                                             FILTER (lang(?dbmdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dbmdraw, "No Description Provided!") AS ?dbmd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :discretizesModel ?dmraw.
                                                                  BIND(STRAFTER(STR(?dmraw), "#") AS ?dm)

                                                                  OPTIONAL {{
                                                                             ?dmraw rdfs:label ?dmlraw
                                                                             FILTER (lang(?dmlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?dmlraw, "No Label Provided!") AS ?dml)

                                                                  OPTIONAL {{
                                                                             ?dmraw rdfs:comment ?dmdraw
                                                                             FILTER (lang(?dmdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dmdraw, "No Description Provided!") AS ?dmd)
                                                                }}

                                                      OPTIONAL {{
                                                                  ?id :containedInModel ?cimraw.
                                                                  BIND(STRAFTER(STR(?cimraw), "#") AS ?cim)

                                                                  OPTIONAL {{
                                                                             ?cimraw rdfs:label ?cimlraw
                                                                             FILTER (lang(?cimlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?cimlraw, "No Label Provided!") AS ?ciml)

                                                                  OPTIONAL {{
                                                                             ?cimraw rdfs:comment ?cimdraw
                                                                             FILTER (lang(?cimdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cimdraw, "No Description Provided!") AS ?cimd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :containsModel ?cmraw.
                                                                  BIND(STRAFTER(STR(?cmraw), "#") AS ?cm)

                                                                  OPTIONAL {{
                                                                             ?cmraw rdfs:label ?cmlraw
                                                                             FILTER (lang(?cmlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?cmlraw, "No Label Provided!") AS ?cml)

                                                                  OPTIONAL {{
                                                                             ?cmraw rdfs:comment ?cmdraw
                                                                             FILTER (lang(?cmdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmdraw, "No Description Provided!") AS ?cmd)
                                                                }}

                                                      OPTIONAL {{
                                                                  ?id :approximatedByModel ?abmraw.
                                                                  BIND(STRAFTER(STR(?abmraw), "#") AS ?abm)

                                                                  OPTIONAL {{
                                                                             ?abmraw rdfs:label ?abmlraw
                                                                             FILTER (lang(?abmlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?abmlraw, "No Label Provided!") AS ?abml)

                                                                  OPTIONAL {{
                                                                             ?abmraw rdfs:comment ?abmdraw
                                                                             FILTER (lang(?abmdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abmdraw, "No Description Provided!") AS ?abmd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :approximatesModel ?amraw.
                                                                  BIND(STRAFTER(STR(?amraw), "#") AS ?am)

                                                                  OPTIONAL {{
                                                                             ?amraw rdfs:label ?amlraw
                                                                             FILTER (lang(?amlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?amlraw, "No Label Provided!") AS ?aml)

                                                                  OPTIONAL {{
                                                                             ?amraw rdfs:comment ?amdraw
                                                                             FILTER (lang(?amdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?amdraw, "No Description Provided!") AS ?amd)
                                                                }}

                                                      OPTIONAL {{
                                                                  ?id :linearizedByModel ?lbmraw.
                                                                  BIND(STRAFTER(STR(?lbmraw), "#") AS ?lbm)

                                                                  OPTIONAL {{
                                                                             ?lbmraw rdfs:label ?lbmlraw
                                                                             FILTER (lang(?lbmlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?lbmlraw, "No Label Provided!") AS ?lbml)

                                                                  OPTIONAL {{
                                                                             ?lbmraw rdfs:comment ?lbmdraw
                                                                             FILTER (lang(?lbmdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbmdraw, "No Description Provided!") AS ?lbmd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :linearizesModel ?lmraw.
                                                                  BIND(STRAFTER(STR(?lmraw), "#") AS ?lm)

                                                                  OPTIONAL {{
                                                                             ?lmraw rdfs:label ?lmlraw
                                                                             FILTER (lang(?lmlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?lmlraw, "No Label Provided!") AS ?lml)

                                                                  OPTIONAL {{
                                                                             ?lmraw rdfs:comment ?lmdraw
                                                                             FILTER (lang(?lmdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lmdraw, "No Description Provided!") AS ?lmd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :similarToModel ?smraw.
                                                                  BIND(STRAFTER(STR(?smraw), "#") AS ?sm)

                                                                  OPTIONAL {{
                                                                             ?smraw rdfs:label ?smlraw
                                                                             FILTER (lang(?smlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?smlraw, "No Label Provided!") AS ?sml)

                                                                  OPTIONAL {{
                                                                             ?smraw rdfs:comment ?smdraw
                                                                             FILTER (lang(?smdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?smdraw, "No Description Provided!") AS ?smd)
                                                                }}
 
                                                       }}
                                                       GROUP BY ?id ?isLinear ?isNotLinear ?isConvex ?isNotConvex ?isDynamic ?isStatic ?isDeterministic ?isStochastic
                                                               ?isDimensionless ?isDimensional ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent ?isSpaceContinuous 
                                                               ?isSpaceDiscrete ?isSpaceIndependent''',

                    'quantityOrQuantityKindInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT ?id ?class ?qudtID
                                                               ?isLinear ?isNotLinear
                                                               ?isDimensionless ?isDimensional
                                                               (GROUP_CONCAT(DISTINCT(?label); SEPARATOR=" / ") AS ?Label) 
                                                               (GROUP_CONCAT(DISTINCT(?description); SEPARATOR=" / ") AS ?Description)
                                                               (GROUP_CONCAT(DISTINCT(?mf); SEPARATOR=" / ") AS ?definedBy)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gbq, " | ", ?gbql, " | ", ?gbqd, " | ", ?gbqc); separator=" / ") AS ?generalizedByQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gq, " | ", ?gql, " | ", ?gqd, " | ", ?gqc); separator=" / ") AS ?generalizesQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?abq, " | ", ?abql, " | ", ?abqd, " | ", ?abqc); separator=" / ") AS ?approximatedByQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?aq, " | ", ?aql, " | ", ?aqd, " | ", ?aqc); separator=" / ") AS ?approximatesQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lbq, " | ", ?lbql, " | ", ?lbqd, " | ", ?lbqc); separator=" / ") AS ?linearizedByQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lq, " | ", ?lql, " | ", ?lqd, " | ", ?lqc); separator=" / ") AS ?linearizesQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?nbq, " | ", ?nbql, " | ", ?nbqd, " | ", ?nbqc); separator=" / ") AS ?nondimensionalizedByQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?nq, " | ", ?nql, " | ", ?nqd, " | ", ?nqc); separator=" / ") AS ?nondimensionalizesQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?sq, " | ", ?sql, " | ", ?sqd, " | ", ?sqc); separator=" / ") AS ?similarToQuantity)
                                                               
                                               WHERE {{ 
                                                       VALUES ?id {{{0}}}
                                                       
                                                       ?id a ?classraw
                                                       FILTER (?classraw IN (:Quantity, :QuantityKind))
                                                       BIND(STRAFTER(STR(?classraw), "#") AS ?class). 
                                                     
                                                       OPTIONAL {{
                                                                  ?id :definedBy ?mfraw.
                                                                  BIND(STRAFTER(STR(?mfraw), "#") AS ?mf).
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :qudtID ?qudtID.
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id rdfs:label ?labelraw .
                                                                  FILTER (lang(?labelraw) = 'en')
                                                                }}
                                                                
                                                                BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)

                                                       OPTIONAL {{
                                                                  ?id rdfs:comment ?descriptionraw .
                                                                  FILTER (lang(?descriptionraw) = 'en')
                                                                }}
                                                                
                                                                BIND(COALESCE(?descriptionraw, "No Description Provided!") AS ?description)

                                                       OPTIONAL {{ ?id :isLinear ?isLinear.
                                                                BIND(IF(?isLinear = false, true, false) AS ?isNotLinear)}}
 
                                                       OPTIONAL {{ ?id :isDimensionless ?isDimensionless.
                                                                BIND(IF(?isDimensionless = false, true, false) AS ?isDimensional)}}
                                        
                                                        OPTIONAL {{
                                                                  ?id :generalizedByQuantity ?gbqraw.
                                                                  BIND(STRAFTER(STR(?gbqraw), "#") AS ?gbq)
                                                                  
                                                                  ?gbqraw a ?gbqcraw
                                                                  FILTER (?gbqcraw IN (:Quantity, :QuantityKind))
                                                                  BIND(STRAFTER(STR(?gbqcraw), "#") AS ?gbqc). 

                                                                  OPTIONAL {{
                                                                             ?gbqraw rdfs:label ?gbqlraw
                                                                             FILTER (lang(?gbqlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gbqlraw, "No Label Provided!") AS ?gbql)

                                                                  OPTIONAL {{
                                                                             ?gbqraw rdfs:comment ?gbqdraw
                                                                             FILTER (lang(?gbqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gbqdraw, "No Description Provided!") AS ?gbqd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :generalizesQuantity ?gqraw.
                                                                  BIND(STRAFTER(STR(?gqraw), "#") AS ?gq)

                                                                  ?gqraw a ?gqcraw
                                                                  FILTER (?gqcraw IN (:Quantity, :QuantityKind))
                                                                  BIND(STRAFTER(STR(?gqcraw), "#") AS ?gqc).

                                                                  OPTIONAL {{
                                                                             ?gqraw rdfs:label ?gqlraw
                                                                             FILTER (lang(?gqlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gqlraw, "No Label Provided!") AS ?gql)

                                                                  OPTIONAL {{
                                                                             ?gqraw rdfs:comment ?gqdraw
                                                                             FILTER (lang(?gqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gqdraw, "No Description Provided!") AS ?gqd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :approximatedByQuantity ?abqraw.
                                                                  BIND(STRAFTER(STR(?abqraw), "#") AS ?abq)

                                                                  ?abqraw a ?abqcraw
                                                                  FILTER (?abqcraw IN (:Quantity, :QuantityKind))
                                                                  BIND(STRAFTER(STR(?abqcraw), "#") AS ?abqc).

                                                                  OPTIONAL {{
                                                                             ?abqraw rdfs:label ?abqlraw
                                                                             FILTER (lang(?abqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abqlraw, "No Label Provided!") AS ?abql)

                                                                  OPTIONAL {{
                                                                             ?abqraw rdfs:comment ?abqdraw
                                                                             FILTER (lang(?abqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abqdraw, "No Description Provided!") AS ?abqd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :approximatesQuantity ?aqraw.
                                                                  BIND(STRAFTER(STR(?aqraw), "#") AS ?aq)

                                                                  ?aqraw a ?aqcraw
                                                                  FILTER (?aqcraw IN (:Quantity, :QuantityKind))
                                                                  BIND(STRAFTER(STR(?aqcraw), "#") AS ?aqc).

                                                                  OPTIONAL {{
                                                                             ?aqraw rdfs:label ?aqlraw
                                                                             FILTER (lang(?aqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?aqlraw, "No Label Provided!") AS ?aql)

                                                                  OPTIONAL {{
                                                                             ?aqraw rdfs:comment ?aqdraw
                                                                             FILTER (lang(?aqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?aqdraw, "No Description Provided!") AS ?aqd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :linearizedByQuantity ?lbqraw.
                                                                  BIND(STRAFTER(STR(?lbqraw), "#") AS ?lbq)

                                                                  ?lbqraw a ?lbqcraw
                                                                  FILTER (?lbqcraw IN (:Quantity, :QuantityKind))
                                                                  BIND(STRAFTER(STR(?lbqcraw), "#") AS ?lbqc).

                                                                  OPTIONAL {{
                                                                             ?lbqraw rdfs:label ?lbqlraw
                                                                             FILTER (lang(?lbqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbqlraw, "No Label Provided!") AS ?lbql)

                                                                  OPTIONAL {{
                                                                             ?lbqraw rdfs:comment ?lbqdraw
                                                                             FILTER (lang(?lbqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbqdraw, "No Description Provided!") AS ?lbqd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :linearizesQuantity ?lqraw.
                                                                  BIND(STRAFTER(STR(?lqraw), "#") AS ?lq)

                                                                  ?lqraw a ?lqcraw
                                                                  FILTER (?lqcraw IN (:Quantity, :QuantityKind))
                                                                  BIND(STRAFTER(STR(?lqcraw), "#") AS ?lqc).

                                                                  OPTIONAL {{
                                                                             ?lqraw rdfs:label ?lqlraw
                                                                             FILTER (lang(?lqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lqlraw, "No Label Provided!") AS ?lql)

                                                                  OPTIONAL {{
                                                                             ?lqraw rdfs:comment ?lqdraw
                                                                             FILTER (lang(?lqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lqdraw, "No Description Provided!") AS ?lqd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :nondimensionalizedByQuantity ?nbqraw.
                                                                  BIND(STRAFTER(STR(?nbqraw), "#") AS ?nbq)

                                                                  ?nbqraw a ?nbqcraw
                                                                  FILTER (?nbqcraw IN (:Quantity, :QuantityKind))
                                                                  BIND(STRAFTER(STR(?nbqcraw), "#") AS ?nbqc).

                                                                  OPTIONAL {{
                                                                             ?nbqraw rdfs:label ?nbqlraw
                                                                             FILTER (lang(?nbqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nbqlraw, "No Label Provided!") AS ?nbql)

                                                                  OPTIONAL {{
                                                                             ?nbqraw rdfs:comment ?nbqdraw
                                                                             FILTER (lang(?nbqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nbqdraw, "No Description Provided!") AS ?nbqd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :nondimensionalizesQuantity ?nqraw.
                                                                  BIND(STRAFTER(STR(?nqraw), "#") AS ?nq)

                                                                  ?nqraw a ?nqcraw
                                                                  FILTER (?nqcraw IN (:Quantity, :QuantityKind))
                                                                  BIND(STRAFTER(STR(?nqcraw), "#") AS ?nqc).

                                                                  OPTIONAL {{
                                                                             ?nqraw rdfs:label ?nqlraw
                                                                             FILTER (lang(?nqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nqlraw, "No Label Provided!") AS ?nql)

                                                                  OPTIONAL {{
                                                                             ?nqraw rdfs:comment ?nqdraw
                                                                             FILTER (lang(?nqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nqdraw, "No Description Provided!") AS ?nqd)
                                                                }}


                                                       OPTIONAL {{
                                                                  ?id :similarToQuantity ?sqraw.
                                                                  BIND(STRAFTER(STR(?sqraw), "#") AS ?sq)

                                                                  ?sqraw a ?sqcraw
                                                                  FILTER (?sqcraw IN (:Quantity, :QuantityKind))
                                                                  BIND(STRAFTER(STR(?sqcraw), "#") AS ?sqc).

                                                                  OPTIONAL {{
                                                                             ?sqraw rdfs:label ?sqlraw
                                                                             FILTER (lang(?sqlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?sqlraw, "No Label Provided!") AS ?sql)

                                                                  OPTIONAL {{
                                                                             ?sqraw rdfs:comment ?sqdraw
                                                                             FILTER (lang(?sqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?sqdraw, "No Description Provided!") AS ?sqd)
                                                                }}
 
                                                       }}
                                                       GROUP BY ?id ?class ?qudtID ?isLinear ?isNotLinear ?isDimensionless ?isDimensional'''
                                                      }

                      
