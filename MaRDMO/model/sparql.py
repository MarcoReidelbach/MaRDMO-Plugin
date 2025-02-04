queryModelDocumentation = {
    
                  'IDCheck': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                SELECT ?ID ?quote                   
                                WHERE {{
                                        ?idraw rdfs:label {0}@en.
                                        BIND(STRAFTER(STR(?idraw), "#") AS ?ID)
                                        OPTIONAL {{?idraw rdfs:comment ?quoteraw.
                                                   FILTER (lang(?quoteraw) = 'en')}}
                                        BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                      }}
                                      GROUP BY ?ID ?quote''',
}
    

queryProviderMM = {
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
                              
                                SELECT DISTINCT ?id ?label ?quote
                              WHERE { 
                                     ?idraw a :MathematicalFormulation .
                                     BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                     OPTIONAL {?idraw rdfs:label ?labelraw .
                                               FILTER (lang(?labelraw) = 'en')}
                                     BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                     OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                               FILTER (lang(?quoteraw) = 'en')}
                                     BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                    }
                               GROUP BY ?id ?label ?quote''',
                 
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
                              
                              SELECT DISTINCT ?id ?label ?quote
                              WHERE { 
                                     ?idraw a :ComputationalTask .
                                     BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                     OPTIONAL {?idraw rdfs:label ?labelraw .
                                               FILTER (lang(?labelraw) = 'en')}
                                     BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                     OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                               FILTER (lang(?quoteraw) = 'en')}
                                     BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                    }
                               GROUP BY ?id ?label ?quote''',
                 
                 'PU': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                              SELECT DISTINCT ?id ?label ?quote
                              WHERE { 
                                     ?idraw a :Publication .
                                     BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                     OPTIONAL {?idraw rdfs:label ?labelraw .
                                               FILTER (lang(?labelraw) = 'en')}
                                     BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                     OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                               FILTER (lang(?quoteraw) = 'en')}
                                     BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                    }
                               GROUP BY ?id ?label ?quote''',
                 
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

queryHandler = {
    
    'publicationInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                 PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                                 SELECT DISTINCT ?MathModDBID ?DOI ?MaRDIPortalID ?WikidataID
                                                 (GROUP_CONCAT(DISTINCT(CONCAT(?documentsentity, " | ", ?documentsentitylabel, " | ", ?documentsentitydescription)); SEPARATOR=" / ") AS ?documents)
                                                 (GROUP_CONCAT(DISTINCT(CONCAT(?inventsentity, " | ", ?inventsentitylabel, " | ", ?inventsentitydescription)); SEPARATOR=" / ") AS ?invents)
                                                 (GROUP_CONCAT(DISTINCT(CONCAT(?studiesentity, " | ", ?studiesentitylabel, " | ", ?studiesentitydescription)); SEPARATOR=" / ") AS ?studies)
                                                 (GROUP_CONCAT(DISTINCT(CONCAT(?surveysentity, " | ", ?surveysentitylabel, " | ", ?surveysentitydescription)); SEPARATOR=" / ") AS ?surveys)
                                                 (GROUP_CONCAT(DISTINCT(CONCAT(?usesentity, " | ", ?usesentitylabel, " | ", ?usesentitydescription)); SEPARATOR=" / ") AS ?uses)
                                                                                   
                                 WHERE {{
                                         VALUES ?idraw {{{0}}}

                                         ?idraw :doiID ?doiraw .
                                         ?idraw a :Publication.
                                         
                                         BIND(STRAFTER(STR(?idraw), "#") AS ?MathModDBID)
                                         BIND(REPLACE(STR(?doiraw), "https://doi.org/", "") AS ?DOI)
                                         OPTIONAL {{ ?idraw :mardiID ?MaRDIPortalID }}
                                         OPTIONAL {{ ?idraw :wikidataID ?WikidataID }}
                                         
                                         OPTIONAL {{?idraw :documents ?docuemntsentityraw.
                                                    BIND(CONCAT("mathmoddb:", STRAFTER(STR(?documentsentityraw), "#")) AS ?documentsentity)

                                                    OPTIONAL {{?docuemntsentityraw rdfs:label ?documentsentitylabelraw.
                                                               FILTER (lang(?documentsentitylabelraw) = 'en')}}
                                                    BIND(COALESCE(?documentsentitylabelraw, "No Label Provided!") As ?documentsentitylabel)

                                                    OPTIONAL {{?docuemntsentityraw rdfs:comment ?docuemntsentitydescriptionraw.
                                                               FILTER (lang(?docuemntsentitydescriptionraw) = 'en')}}
                                                    BIND(COALESCE(?docuemntsentitydescriptionraw, "No Description Provided!") As ?docuemntsentitydescription)
                                                  }}

                                         OPTIONAL {{?idraw :invents ?inventsentityraw.
                                                    BIND(CONCAT("mathmoddb:", STRAFTER(STR(?inventsentityraw), "#")) AS ?inventsentity)

                                                    OPTIONAL {{?inventsentityraw rdfs:label ?inventsentitylabelraw.
                                                               FILTER (lang(?inventsentitylabelraw) = 'en')}}
                                                    BIND(COALESCE(?inventsentitylabelraw, "No Label Provided!") As ?inventsentitylabel)

                                                    OPTIONAL {{?inventsentityraw rdfs:comment ?inventsentitydescriptionraw.
                                                               FILTER (lang(?inventsentitydescriptionraw) = 'en')}}
                                                    BIND(COALESCE(?inventsentitydescriptionraw, "No Description Provided!") As ?inventsentitydescription)
                                                  }}

                                         OPTIONAL {{?idraw :studies ?studiesentityraw.
                                                    BIND(CONCAT("mathmoddb:", STRAFTER(STR(?studiesentityraw), "#")) AS ?studiesentity)

                                                    OPTIONAL {{?studiesentityraw rdfs:label ?studiesentitylabelraw.
                                                               FILTER (lang(?studiesentitylabelraw) = 'en')}}
                                                    BIND(COALESCE(?studiesentitylabelraw, "No Label Provided!") As ?studiesentitylabel)

                                                    OPTIONAL {{?studiesentityraw rdfs:comment ?studiesentitydescriptionraw.
                                                               FILTER (lang(?studiesentitydescriptionraw) = 'en')}}
                                                    BIND(COALESCE(?studiesentitydescriptionraw, "No Description Provided!") As ?studiesentitydescription)
                                                  }}

                                         OPTIONAL {{?idraw :surveys ?surveysentityraw.
                                                    BIND(CONCAT("mathmoddb:", STRAFTER(STR(?surveysentityraw), "#")) AS ?surveysentity)

                                                    OPTIONAL {{?surveysentityraw rdfs:label ?surveysentitylabelraw.
                                                               FILTER (lang(?surveysentitylabelraw) = 'en')}}
                                                    BIND(COALESCE(?surveysentitylabelraw, "No Label Provided!") As ?surveysentitylabel)

                                                    OPTIONAL {{?surveysentityraw rdfs:comment ?surveysentitydescriptionraw.
                                                               FILTER (lang(?surveysentitydescriptionraw) = 'en')}}
                                                    BIND(COALESCE(?surveysentitydescriptionraw, "No Description Provided!") As ?surveysentitydescription)
                                                  }}

                                         OPTIONAL {{?idraw :uses ?usesentityraw.
                                                    BIND(CONCAT("mathmoddb:", STRAFTER(STR(?usesentityraw), "#")) AS ?usesentity)

                                                    OPTIONAL {{?usesentityraw rdfs:label ?usesentitylabelraw.
                                                               FILTER (lang(?usesentitylabelraw) = 'en')}}
                                                    BIND(COALESCE(?usesentitylabelraw, "No Label Provided!") As ?usesentitylabel)

                                                    OPTIONAL {{?usesentityraw rdfs:comment ?usesentitydescriptionraw.
                                                               FILTER (lang(?usesentitydescriptionraw) = 'en')}}
                                                    BIND(COALESCE(?usesentitydescriptionraw, "No Description Provided!") As ?usesentitydescription)
                                                  }}

                                       }}
                                 GROUP BY ?MathModDBID ?DOI ?MaRDIPortalID ?WikidataID''',

    'researchFieldInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT (GROUP_CONCAT(DISTINCT CONCAT(?gbf, " | ", ?gbfl, " | ", ?gbfd); separator=" / ") AS ?generalizedByField)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gf, " | ", ?gfl, " | ", ?gfd); separator=" / ") AS ?generalizesField)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?sf, " | ", ?sfl, " | ", ?sfd); separator=" / ") AS ?similarToField)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)
                                                               
                                               WHERE {{ 
                                                       VALUES ?id {{ :{0} }} 

                                                        OPTIONAL {{
                                                                   ?id (:documentedIn | :inventedIn | :studiedIn | :surveyedIn | :usedIn) ?pubraw.
                                                                   BIND(CONCAT("mathmoddb:", STRAFTER(STR(?pubraw), "#")) AS ?pub)
                                                                   OPTIONAL {{ ?pubraw rdfs:label ?publraw
                                                                               FILTER (lang(?publraw) = 'en') }}
                                                                   BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)
                                                                   OPTIONAL {{ ?pubraw rdfs:comment ?pubdraw
                                                                               FILTER (lang(?pubdraw) = 'en') }}
                                                                   BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                                 }}
                                                      
                                                        OPTIONAL {{
                                                                  ?id :generalizedByField ?gbfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gbfraw), "#")) AS ?gbf)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gfraw), "#")) AS ?gf)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?sfraw), "#")) AS ?sf)

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
 
                                                       }}''',

    'researchProblemInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT (GROUP_CONCAT(DISTINCT CONCAT(?rf, " | ", ?rfl, " | ", ?rfd); separator=" / ") AS ?containedInField)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gbp, " | ", ?gbpl, " | ", ?gbpd); separator=" / ") AS ?generalizedByProblem)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gp, " | ", ?gpl, " | ", ?gpd); separator=" / ") AS ?generalizesProblem)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?sp, " | ", ?spl, " | ", ?spd); separator=" / ") AS ?similarToProblem)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)

                                               WHERE {{ 
                                                       VALUES ?id {{ :{0} }} 

                                                        OPTIONAL {{
                                                                   ?id (:documentedIn | :inventedIn | :studiedIn | :surveyedIn | :usedIn) ?pubraw.
                                                                   BIND(CONCAT("mathmoddb:", STRAFTER(STR(?pubraw), "#")) AS ?pub)
                                                                   OPTIONAL {{ ?pubraw rdfs:label ?publraw
                                                                               FILTER (lang(?publraw) = 'en') }}
                                                                   BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)
                                                                   OPTIONAL {{ ?pubraw rdfs:comment ?pubdraw
                                                                               FILTER (lang(?pubdraw) = 'en') }}
                                                                   BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                                 }}
                                                       
                                                        OPTIONAL {{
                                                                   ?id :containedInField ?rfraw.
                                                                   BIND(CONCAT("mathmoddb:", STRAFTER(STR(?rfraw), "#")) AS ?rf)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gbpraw), "#")) AS ?gbp)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gpraw), "#")) AS ?gp)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?spraw), "#")) AS ?sp)

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
 
                                                       }}''',

              'mathematicalModelInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT ?isLinear ?isNotLinear
                                                               ?isConvex ?isNotConvex
                                                               ?isDynamic ?isStatic
                                                               ?isDeterministic ?isStochastic
                                                               ?isDimensionless ?isDimensional
                                                               ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent
                                                               ?isSpaceContinuous ?isSpaceDiscrete ?isSpaceIndependent
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mf, " | ", ?mfl, " | ", ?mfd); separator=" / ") AS ?formulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?ta, " | ", ?tal, " | ", ?tad); separator=" / ") AS ?appliedByTask)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?rp, " | ", ?rpl, " | ", ?rpd); separator=" / ") AS ?models)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gbm, " | ", ?gbml, " | ", ?gbmd); separator=" / ") AS ?generalizedByModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gm, " | ", ?gml, " | ", ?gmd); separator=" / ") AS ?generalizesModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?dbm, " | ", ?dbml, " | ", ?dbmd); separator=" / ") AS ?discretizedByModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?dm, " | ", ?dml, " | ", ?dmd); separator=" / ") AS ?discretizesModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cim, " | ", ?ciml, " | ", ?cimd); separator=" / ") AS ?containedInModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cm, " | ", ?cml, " | ", ?cmd); separator=" / ") AS ?containsModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?abm, " | ", ?abml, " | ", ?abmd); separator=" / ") AS ?approximatedByModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?am, " | ", ?aml, " | ", ?amd); separator=" / ") AS ?approximatesModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lbm, " | ", ?lbml, " | ", ?lbmd); separator=" / ") AS ?linearizedByModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lm, " | ", ?lml, " | ", ?lmd); separator=" / ") AS ?linearizesModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?sm, " | ", ?sml, " | ", ?smd); separator=" / ") AS ?similarToModel)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)

                                               WHERE {{ 
                                                       VALUES ?id {{ :{0} }} 

                                                        OPTIONAL {{
                                                                   ?id (:documentedIn | :inventedIn | :studiedIn | :surveyedIn | :usedIn) ?pubraw.
                                                                   BIND(CONCAT("mathmoddb:", STRAFTER(STR(?pubraw), "#")) AS ?pub)
                                                                   OPTIONAL {{ ?pubraw rdfs:label ?publraw
                                                                               FILTER (lang(?publraw) = 'en') }}
                                                                   BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)
                                                                   OPTIONAL {{ ?pubraw rdfs:comment ?pubdraw
                                                                               FILTER (lang(?pubdraw) = 'en') }}
                                                                   BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                                 }}
                                                       
                                                       OPTIONAL {{
                                                                  ?id(:containsFormulation | :containsBoundaryCondition | :containsAssumption | :containsConstraintCondition | :containsCouplingCondition | :containsInitialCondition | :containsFinalCondition) ?mfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mfraw), "#")) AS ?mf)
                                                                  OPTIONAL {{ ?mfraw rdfs:label ?mflraw
                                                                              FILTER (lang(?mflraw) = 'en') }}
                                                                  BIND(COALESCE(?mflraw, "No Label Provided!") AS ?mfl)
                                                                  OPTIONAL {{ ?mfraw rdfs:comment ?mfdraw
                                                                              FILTER (lang(?mfdraw) = 'en') }}
                                                                  BIND(COALESCE(?mfdraw, "No Description Provided!") AS ?mfd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :appliedByTask ?taraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?taraw), "#")) AS ?ta)
                                                                  OPTIONAL {{ ?taraw rdfs:label ?talraw
                                                                              FILTER (lang(?talraw) = 'en') }}
                                                                  BIND(COALESCE(?talraw, "No Label Provided!") AS ?tal)
                                                                  OPTIONAL {{ ?taraw rdfs:comment ?tadraw
                                                                              FILTER (lang(?tadraw) = 'en') }}
                                                                  BIND(COALESCE(?tadraw, "No Description Provided!") AS ?tad)
                                                                }}

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
                                                                   BIND(CONCAT("mathmoddb:", STRAFTER(STR(?rpraw), "#")) AS ?rp)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gbmraw), "#")) AS ?gbm)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gmraw), "#")) AS ?gm)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?dbmraw), "#")) AS ?dbm)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?dmraw), "#")) AS ?dm)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?cimraw), "#")) AS ?cim)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?cmraw), "#")) AS ?cm)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?abmraw), "#")) AS ?abm)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?amraw), "#")) AS ?am)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?lbmraw), "#")) AS ?lbm)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?lmraw), "#")) AS ?lm)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?smraw), "#")) AS ?sm)

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
                                                       GROUP BY ?isLinear ?isNotLinear ?isConvex ?isNotConvex ?isDynamic ?isStatic ?isDeterministic ?isStochastic
                                                               ?isDimensionless ?isDimensional ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent ?isSpaceContinuous 
                                                               ?isSpaceDiscrete ?isSpaceIndependent''',

                    'quantityOrQuantityKindInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT ?class ?qudtID
                                                               ?isLinear ?isNotLinear
                                                               ?isDimensionless ?isDimensional
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mf, " | ", ?mfl, " | ", ?mfd); separator=" / ") AS ?definedBy)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gbq, " | ", ?gbql, " | ", ?gbqd, " | ", ?gbqc); separator=" / ") AS ?generalizedByQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gq, " | ", ?gql, " | ", ?gqd, " | ", ?gqc); separator=" / ") AS ?generalizesQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?abq, " | ", ?abql, " | ", ?abqd, " | ", ?abqc); separator=" / ") AS ?approximatedByQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?aq, " | ", ?aql, " | ", ?aqd, " | ", ?aqc); separator=" / ") AS ?approximatesQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lbq, " | ", ?lbql, " | ", ?lbqd, " | ", ?lbqc); separator=" / ") AS ?linearizedByQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lq, " | ", ?lql, " | ", ?lqd, " | ", ?lqc); separator=" / ") AS ?linearizesQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?nbq, " | ", ?nbql, " | ", ?nbqd, " | ", ?nbqc); separator=" / ") AS ?nondimensionalizedByQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?nq, " | ", ?nql, " | ", ?nqd, " | ", ?nqc); separator=" / ") AS ?nondimensionalizesQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?sq, " | ", ?sql, " | ", ?sqd, " | ", ?sqc); separator=" / ") AS ?similarToQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)
                                                               
                                               WHERE {{ 
                                                       VALUES ?id {{ :{0} }} 

                                                        OPTIONAL {{
                                                                   ?id (:documentedIn | :inventedIn | :studiedIn | :surveyedIn | :usedIn) ?pubraw.
                                                                   BIND(CONCAT("mathmoddb:", STRAFTER(STR(?pubraw), "#")) AS ?pub)
                                                                   OPTIONAL {{ ?pubraw rdfs:label ?publraw
                                                                               FILTER (lang(?publraw) = 'en') }}
                                                                   BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)
                                                                   OPTIONAL {{ ?pubraw rdfs:comment ?pubdraw
                                                                               FILTER (lang(?pubdraw) = 'en') }}
                                                                   BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                                 }}
                                                       
                                                       ?id a ?classraw
                                                       FILTER (?classraw IN (:Quantity, :QuantityKind))
                                                       BIND(STRAFTER(STR(?classraw), "#") AS ?class). 
                                                     
                                                       OPTIONAL {{
                                                                  ?id :definedBy ?mfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mfraw), "#")) AS ?mf)

                                                                  OPTIONAL {{
                                                                             ?mfraw rdfs:label ?mflraw
                                                                             FILTER (lang(?mflraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?mflraw, "No Label Provided!") AS ?mfl)

                                                                  OPTIONAL {{
                                                                             ?mfraw rdfs:comment ?mfdraw
                                                                             FILTER (lang(?mfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfdraw, "No Description Provided!") AS ?mfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :qudtID ?qudtID.
                                                                }}

                                                       OPTIONAL {{ ?id :isLinear ?isLinear.
                                                                BIND(IF(?isLinear = false, true, false) AS ?isNotLinear)}}
 
                                                       OPTIONAL {{ ?id :isDimensionless ?isDimensionless.
                                                                BIND(IF(?isDimensionless = false, true, false) AS ?isDimensional)}}
                                        
                                                        OPTIONAL {{
                                                                  ?id :generalizedByQuantity ?gbqraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gbqraw), "#")) AS ?gbq)
                                                                  
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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gqraw), "#")) AS ?gq)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?abqraw), "#")) AS ?abq)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?aqraw), "#")) AS ?aq)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?lbqraw), "#")) AS ?lbq)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?lqraw), "#")) AS ?lq)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?nbqraw), "#")) AS ?nbq)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?nqraw), "#")) AS ?nq)

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
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?sqraw), "#")) AS ?sq)

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
                                                       GROUP BY ?class ?qudtID ?isLinear ?isNotLinear ?isDimensionless ?isDimensional''',

                      'mathematicalFormulationInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT ?isLinear ?isNotLinear
                                                               ?isConvex ?isNotConvex
                                                               ?isDynamic ?isStatic
                                                               ?isDeterministic ?isStochastic
                                                               ?isDimensionless ?isDimensional
                                                               ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent
                                                               ?isSpaceContinuous ?isSpaceDiscrete ?isSpaceIndependent
                                                               (GROUP_CONCAT(DISTINCT(?formula); SEPARATOR=" / ") AS ?formulas)
                                                               (GROUP_CONCAT(DISTINCT(?term); SEPARATOR=" / ") AS ?terms)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?dq, " | ", ?dql, " | ", ?dqd); separator=" / ") AS ?defines)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?q, " | ", ?ql, " | ", ?qd); separator=" / ") AS ?containsQuantity)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mmmf, " | ", ?mmmfl, " | ", ?mmmfd); separator=" / ") AS ?containedAsFormulationInMM)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mma, " | ", ?mmal, " | ", ?mmad); separator=" / ") AS ?containedAsAssumptionInMM)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mmbc, " | ", ?mmbcl, " | ", ?mmbcd); separator=" / ") AS ?containedAsBoundaryConditionInMM)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mmfc, " | ", ?mmfcl, " | ", ?mmfcd); separator=" / ") AS ?containedAsFinalConditionInMM)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mmic, " | ", ?mmicl, " | ", ?mmicd); separator=" / ") AS ?containedAsInitialConditionInMM)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mmcc, " | ", ?mmccl, " | ", ?mmccd); separator=" / ") AS ?containedAsConstraintConditionInMM)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mmcpc, " | ", ?mmcpcl, " | ", ?mmcpcd); separator=" / ") AS ?containedAsCouplingConditionInMM)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mfmf, " | ", ?mfmfl, " | ", ?mfmfd); separator=" / ") AS ?containedAsFormulationInMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mfa, " | ", ?mfal, " | ", ?mfad); separator=" / ") AS ?containedAsAssumptionInMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mfbc, " | ", ?mfbcl, " | ", ?mfbcd); separator=" / ") AS ?containedAsBoundaryConditionInMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mffc, " | ", ?mffcl, " | ", ?mffcd); separator=" / ") AS ?containedAsFinalConditionInMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mfic, " | ", ?mficl, " | ", ?mficd); separator=" / ") AS ?containedAsInitialConditionInMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mfcc, " | ", ?mfccl, " | ", ?mfccd); separator=" / ") AS ?containedAsConstraintConditionInMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?mfcpc, " | ", ?mfcpcl, " | ", ?mfcpcd); separator=" / ") AS ?containedAsCouplingConditionInMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cmfmf, " | ", ?cmfmfl, " | ", ?cmfmfd); separator=" / ") AS ?containsFormulationMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cmfa, " | ", ?cmfal, " | ", ?cmfad); separator=" / ") AS ?containsAssumptionMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cmfbc, " | ", ?cmfbcl, " | ", ?cmfbcd); separator=" / ") AS ?containsBoundaryConditionMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cmffc, " | ", ?cmffcl, " | ", ?cmffcd); separator=" / ") AS ?containsFinalConditionMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cmfic, " | ", ?cmficl, " | ", ?cmficd); separator=" / ") AS ?containsInitialConditionMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cmfcc, " | ", ?cmfccl, " | ", ?cmfccd); separator=" / ") AS ?containsConstraintConditionMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cmfcpc, " | ", ?cmfcpcl, " | ", ?cmfcpcd); separator=" / ") AS ?containsCouplingConditionMF)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?dbmf, " | ", ?dbmfl, " | ", ?dbmfd); separator=" / ") AS ?discretizedByFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?dmf, " | ", ?dmfl, " | ", ?dmfd); separator=" / ") AS ?discretizesFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gbmf, " | ", ?gbmfl, " | ", ?gbmfd); separator=" / ") AS ?generalizedByFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?gmf, " | ", ?gmfl, " | ", ?gmfd); separator=" / ") AS ?generalizesFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?abmf, " | ", ?abmfl, " | ", ?abmfd); separator=" / ") AS ?approximatedByFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?amf, " | ", ?amfl, " | ", ?amfd); separator=" / ") AS ?approximatesFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lbmf, " | ", ?lbmfl, " | ", ?lbmfd); separator=" / ") AS ?linearizedByFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lmf, " | ", ?lmfl, " | ", ?lmfd); separator=" / ") AS ?linearizesFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?nbmf, " | ", ?nbmfl, " | ", ?nbmfd); separator=" / ") AS ?nondimensionalizedByFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?nmf, " | ", ?nmfl, " | ", ?nmfd); separator=" / ") AS ?nondimensionalizesFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?smf, " | ", ?smfl, " | ", ?smfd); separator=" / ") AS ?similarToFormulation)
                                                               (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)

                                                WHERE {{ 
                                                       VALUES ?id {{ :{0} }} 

                                                        OPTIONAL {{
                                                                   ?id (:documentedIn | :inventedIn | :studiedIn | :surveyedIn | :usedIn) ?pubraw.
                                                                   BIND(CONCAT("mathmoddb:", STRAFTER(STR(?pubraw), "#")) AS ?pub)
                                                                   OPTIONAL {{ ?pubraw rdfs:label ?publraw
                                                                               FILTER (lang(?publraw) = 'en') }}
                                                                   BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)
                                                                   OPTIONAL {{ ?pubraw rdfs:comment ?pubdraw
                                                                               FILTER (lang(?pubdraw) = 'en') }}
                                                                   BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                                 }}
                                                       
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
                                                        
                                                        OPTIONAL {{?id :definingFormulation ?formula.}}

                                                        OPTIONAL {{?id :inDefiningFormulation ?term.}}

                                                        OPTIONAL {{?id :defines ?dqraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?dqraw), "#")) AS ?dq)
                                                       
                                                                  OPTIONAL {{
                                                                             ?dqraw rdfs:label ?dqlraw
                                                                             FILTER (lang(?dqlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?dqlraw, "No Label Provided!") AS ?dql)

                                                                  OPTIONAL {{
                                                                             ?dqraw rdfs:comment ?dqdraw
                                                                             FILTER (lang(?dqdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dqdraw, "No Description Provided!") AS ?dqd)
                                                                }}
                                                       

                                                        OPTIONAL {{?id :containsQuantity ?qraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?qraw), "#")) AS ?q)

                                                                  OPTIONAL {{
                                                                             ?qraw rdfs:label ?qlraw
                                                                             FILTER (lang(?qlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?qlraw, "No Label Provided!") AS ?ql)

                                                                  OPTIONAL {{
                                                                             ?qraw rdfs:comment ?qdraw
                                                                             FILTER (lang(?qdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?qdraw, "No Description Provided!") AS ?qd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsFormulationIn ?mmmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mmmfraw), "#")) AS ?mmmf)
                                                                  ?mmmfraw a :MathematicalModel. 

                                                                  OPTIONAL {{
                                                                             ?mmmfraw rdfs:label ?mmmflraw
                                                                             FILTER (lang(?mmmflraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?mmmflraw, "No Label Provided!") AS ?mmmfl)

                                                                  OPTIONAL {{
                                                                             ?mmmfraw rdfs:comment ?mmmfdraw
                                                                             FILTER (lang(?mmmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmmfdraw, "No Description Provided!") AS ?mmmfd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsFormulationIn ?mfmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mfmfraw), "#")) AS ?mfmf)
                                                                  ?mfmfraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?mfmfraw rdfs:label ?mfmflraw
                                                                             FILTER (lang(?mfmflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfmflraw, "No Label Provided!") AS ?mfmfl)

                                                                  OPTIONAL {{
                                                                             ?mfmfraw rdfs:comment ?mfmfdraw
                                                                             FILTER (lang(?mfmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfmfdraw, "No Description Provided!") AS ?mfmfd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsFormulation ?cmfmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?cmfmfraw), "#")) AS ?cmfmf)
                                                                  ?cmfmfraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?cmfmfraw rdfs:label ?cmfmflraw
                                                                             FILTER (lang(?cmfmflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfmflraw, "No Label Provided!") AS ?cmfmfl)

                                                                  OPTIONAL {{
                                                                             ?cmfmfraw rdfs:comment ?cmfmfdraw
                                                                             FILTER (lang(?cmfmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfmfdraw, "No Description Provided!") AS ?cmfmfd)
                                                                }}
                                                        
                                                        OPTIONAL {{
                                                                  ?id :containedAsBoundaryConditionIn ?mmbcraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mmbcraw), "#")) AS ?mmbc)
                                                                  ?mmbcraw a :MathematicalModel.

                                                                  OPTIONAL {{
                                                                             ?mmbcraw rdfs:label ?mmbclraw
                                                                             FILTER (lang(?mmbclraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?mmbclraw, "No Label Provided!") AS ?mmbcl)

                                                                  OPTIONAL {{
                                                                             ?mmbcraw rdfs:comment ?mmbcdraw
                                                                             FILTER (lang(?mmbcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmbcdraw, "No Description Provided!") AS ?mmbcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsBoundaryConditionIn ?mfbcraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mfbcraw), "#")) AS ?mfbc)
                                                                  ?mfbcraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?mfbcraw rdfs:label ?mfbclraw
                                                                             FILTER (lang(?mfbclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfbclraw, "No Label Provided!") AS ?mfbcl)

                                                                  OPTIONAL {{
                                                                             ?mfbcraw rdfs:comment ?mfbcdraw
                                                                             FILTER (lang(?mfbcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfbcdraw, "No Description Provided!") AS ?mfbcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsBoundaryCondition ?cmfbcraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?cmfbcraw), "#")) AS ?cmfbc)
                                                                  ?cmfbcraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?cmfbcraw rdfs:label ?cmfbclraw
                                                                             FILTER (lang(?cmfbclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfbclraw, "No Label Provided!") AS ?cmfbcl)

                                                                  OPTIONAL {{
                                                                             ?cmfbcraw rdfs:comment ?cmfbcdraw
                                                                             FILTER (lang(?cmfbcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfbcdraw, "No Description Provided!") AS ?cmfbcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsConstraintConditionIn ?mmccraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mmccraw), "#")) AS ?mmcc)
                                                                  ?mmccraw a :MathematicalModel.

                                                                  OPTIONAL {{
                                                                             ?mmccraw rdfs:label ?mmcclraw
                                                                             FILTER (lang(?mmcclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmcclraw, "No Label Provided!") AS ?mmccl)

                                                                  OPTIONAL {{
                                                                             ?mmccraw rdfs:comment ?mmccdraw
                                                                             FILTER (lang(?mmccdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmccdraw, "No Description Provided!") AS ?mmccd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsConstraintConditionIn ?mfccraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mfccraw), "#")) AS ?mfcc)
                                                                  ?mfccraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?mfccraw rdfs:label ?mfcclraw
                                                                             FILTER (lang(?mfcclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfcclraw, "No Label Provided!") AS ?mfccl)

                                                                  OPTIONAL {{
                                                                             ?mfccraw rdfs:comment ?mfccdraw
                                                                             FILTER (lang(?mfccdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfccdraw, "No Description Provided!") AS ?mfccd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsConstraintCondition ?cmfccraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?cmfccraw), "#")) AS ?cmfcc)
                                                                  ?cmfccraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?cmfccraw rdfs:label ?cmfcclraw
                                                                             FILTER (lang(?cmfcclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfcclraw, "No Label Provided!") AS ?cmfccl)

                                                                  OPTIONAL {{
                                                                             ?cmfccraw rdfs:comment ?cmfccdraw
                                                                             FILTER (lang(?cmfccdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfccdraw, "No Description Provided!") AS ?cmfccd)
                                                                }}


                                                        OPTIONAL {{
                                                                  ?id :containedAsCouplingConditionIn ?mmcpcraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mmcpcraw), "#")) AS ?mmcpc)
                                                                  ?mmcpcraw a :MathematicalModel.

                                                                  OPTIONAL {{
                                                                             ?mmcpcraw rdfs:label ?mmcpclraw
                                                                             FILTER (lang(?mmcpclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmcpclraw, "No Label Provided!") AS ?mmcpcl)

                                                                  OPTIONAL {{
                                                                             ?mmcpcraw rdfs:comment ?mmcpcdraw
                                                                             FILTER (lang(?mmcpcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmcpcdraw, "No Description Provided!") AS ?mmcpcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsCouplingConditionIn ?mfcpcraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mfcpcraw), "#")) AS ?mfcpc)
                                                                  ?mfcpcraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?mfcpcraw rdfs:label ?mfcpclraw
                                                                             FILTER (lang(?mfcpclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfcpclraw, "No Label Provided!") AS ?mfcpcl)

                                                                  OPTIONAL {{
                                                                             ?mfcpcraw rdfs:comment ?mfcpcdraw
                                                                             FILTER (lang(?mfcpcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfcpcdraw, "No Description Provided!") AS ?mfcpcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsCouplingCondition ?cmfcpcraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?cmfcpcraw), "#")) AS ?cmfcpc)
                                                                  ?cmfcpcraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?cmfcpcraw rdfs:label ?cmfcpclraw
                                                                             FILTER (lang(?cmfcpclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfcpclraw, "No Label Provided!") AS ?cmfcpcl)

                                                                  OPTIONAL {{
                                                                             ?cmfcpcraw rdfs:comment ?cmfcpcdraw
                                                                             FILTER (lang(?cmfcpcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfcpcdraw, "No Description Provided!") AS ?cmfcpcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsAssumptionIn ?mmaraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mmaraw), "#")) AS ?mma)
                                                                  ?mmaraw a :MathematicalModel

                                                                  OPTIONAL {{
                                                                             ?mmaraw rdfs:label ?mmalraw
                                                                             FILTER (lang(?mmalraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmalraw, "No Label Provided!") AS ?mmal)

                                                                  OPTIONAL {{
                                                                             ?mmaraw rdfs:comment ?mmadraw
                                                                             FILTER (lang(?mmadraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmadraw, "No Description Provided!") AS ?mmad)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsAssumptionIn ?mfaraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mfaraw), "#")) AS ?mfa)
                                                                  ?mfaraw a :MathematicalFormulation

                                                                  OPTIONAL {{
                                                                             ?mfaraw rdfs:label ?mfalraw
                                                                             FILTER (lang(?mfalraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfalraw, "No Label Provided!") AS ?mfal)

                                                                  OPTIONAL {{
                                                                             ?mfaraw rdfs:comment ?mfadraw
                                                                             FILTER (lang(?mfadraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mfadraw, "No Description Provided!") AS ?mfad)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsAssumption ?cmfaraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?cmfaraw), "#")) AS ?cmfa)
                                                                  ?cmfaraw a :MathematicalFormulation

                                                                  OPTIONAL {{
                                                                             ?cmfaraw rdfs:label ?cmfalraw
                                                                             FILTER (lang(?cmfalraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfalraw, "No Label Provided!") AS ?cmfal)

                                                                  OPTIONAL {{
                                                                             ?cmfaraw rdfs:comment ?cmfadraw
                                                                             FILTER (lang(?cmfadraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmfadraw, "No Description Provided!") AS ?cmfad)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsInitialConditionIn ?mmicraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mmicraw), "#")) AS ?mmic)
                                                                  ?mmicraw a :MathematicalModel.

                                                                  OPTIONAL {{
                                                                             ?mmicraw rdfs:label ?mmiclraw
                                                                             FILTER (lang(?mmiclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmiclraw, "No Label Provided!") AS ?mmicl)

                                                                  OPTIONAL {{
                                                                             ?mmicraw rdfs:comment ?mmicdraw
                                                                             FILTER (lang(?mmicdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmicdraw, "No Description Provided!") AS ?mmicd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsInitialConditionIn ?mficraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mficraw), "#")) AS ?mfic)
                                                                  ?mficraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?mficraw rdfs:label ?mficlraw
                                                                             FILTER (lang(?mficlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mficlraw, "No Label Provided!") AS ?mficl)

                                                                  OPTIONAL {{
                                                                             ?mficraw rdfs:comment ?mficdraw
                                                                             FILTER (lang(?mficdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mficdraw, "No Description Provided!") AS ?mficd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsInitialCondition ?cmficraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?cmficraw), "#")) AS ?cmfic)
                                                                  ?cmficraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?cmficraw rdfs:label ?cmficlraw
                                                                             FILTER (lang(?cmficlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmficlraw, "No Label Provided!") AS ?cmficl)

                                                                  OPTIONAL {{
                                                                             ?cmficraw rdfs:comment ?cmficdraw
                                                                             FILTER (lang(?cmficdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmficdraw, "No Description Provided!") AS ?cmficd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsFinalConditionIn ?mmfcraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mmfcraw), "#")) AS ?mmfc)
                                                                  ?mmfcraw a :MathematicalModel.

                                                                  OPTIONAL {{
                                                                             ?mmfcraw rdfs:label ?mmfclraw
                                                                             FILTER (lang(?mmfclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmfclraw, "No Label Provided!") AS ?mmfcl)

                                                                  OPTIONAL {{
                                                                             ?mmfcraw rdfs:comment ?mmfcdraw
                                                                             FILTER (lang(?mmfcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mmfcdraw, "No Description Provided!") AS ?mmfcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containedAsFinalConditionIn ?mffcraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?mffcraw), "#")) AS ?mffc)
                                                                  ?mffcraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?mffcraw rdfs:label ?mffclraw
                                                                             FILTER (lang(?mffclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mffclraw, "No Label Provided!") AS ?mffcl)

                                                                  OPTIONAL {{
                                                                             ?mffcraw rdfs:comment ?mffcdraw
                                                                             FILTER (lang(?mffcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?mffcdraw, "No Description Provided!") AS ?mffcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsFinalCondition ?cmffcraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?cmffcraw), "#")) AS ?cmffc)
                                                                  ?cmffcraw a :MathematicalFormulation.

                                                                  OPTIONAL {{
                                                                             ?cmffcraw rdfs:label ?cmffclraw
                                                                             FILTER (lang(?cmffclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmffclraw, "No Label Provided!") AS ?cmffcl)

                                                                  OPTIONAL {{
                                                                             ?cmffcraw rdfs:comment ?cmffcdraw
                                                                             FILTER (lang(?cmffcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cmffcdraw, "No Description Provided!") AS ?cmffcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :generalizedByFormulation ?gbmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gbmfraw), "#")) AS ?gbmf)
                                                                  
                                                                  OPTIONAL {{
                                                                             ?gbmfraw rdfs:label ?gbmflraw
                                                                             FILTER (lang(?gbmflraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gbmflraw, "No Label Provided!") AS ?gbmfl)

                                                                  OPTIONAL {{
                                                                             ?gbmfraw rdfs:comment ?gbmfdraw
                                                                             FILTER (lang(?gbmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gbmfdraw, "No Description Provided!") AS ?gbmfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :generalizesFormulation ?gmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?gmfraw), "#")) AS ?gmf)

                                                                  OPTIONAL {{
                                                                             ?gmfraw rdfs:label ?gmflraw
                                                                             FILTER (lang(?gmflraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gmflraw, "No Label Provided!") AS ?gmfl)

                                                                  OPTIONAL {{
                                                                             ?gmfraw rdfs:comment ?gmfdraw
                                                                             FILTER (lang(?gmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gmfdraw, "No Description Provided!") AS ?gmfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :approximatedByFormulation ?abmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?abmfraw), "#")) AS ?abmf)

                                                                  OPTIONAL {{
                                                                             ?abmfraw rdfs:label ?abmflraw
                                                                             FILTER (lang(?abmflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abmflraw, "No Label Provided!") AS ?abmfl)

                                                                  OPTIONAL {{
                                                                             ?abmfraw rdfs:comment ?abmfdraw
                                                                             FILTER (lang(?abmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abmfdraw, "No Description Provided!") AS ?abmfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :approximatesFormulation ?amfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?amfraw), "#")) AS ?amf)

                                                                  OPTIONAL {{
                                                                             ?amfraw rdfs:label ?amflraw
                                                                             FILTER (lang(?amflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?amflraw, "No Label Provided!") AS ?amfl)

                                                                  OPTIONAL {{
                                                                             ?amfraw rdfs:comment ?amfdraw
                                                                             FILTER (lang(?amfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?amfdraw, "No Description Provided!") AS ?amfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :linearizedByFormulation ?lbmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?lbmfraw), "#")) AS ?lbmf)

                                                                  OPTIONAL {{
                                                                             ?lbmfraw rdfs:label ?lbmflraw
                                                                             FILTER (lang(?lbmflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbmflraw, "No Label Provided!") AS ?lbmfl)

                                                                  OPTIONAL {{
                                                                             ?lbmfraw rdfs:comment ?lbmfdraw
                                                                             FILTER (lang(?lbmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbmfdraw, "No Description Provided!") AS ?lbmfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :linearizesFormulation ?lmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?lmfraw), "#")) AS ?lmf)

                                                                  OPTIONAL {{
                                                                             ?lmfraw rdfs:label ?lmflraw
                                                                             FILTER (lang(?lmflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lmflraw, "No Label Provided!") AS ?lmfl)

                                                                  OPTIONAL {{
                                                                             ?lmfraw rdfs:comment ?lmfdraw
                                                                             FILTER (lang(?lmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lmfdraw, "No Description Provided!") AS ?lmfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :nondimensionalizedByFormulation ?nbmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?nbmfraw), "#")) AS ?nbmf)

                                                                  OPTIONAL {{
                                                                             ?nbmfraw rdfs:label ?nbmflraw
                                                                             FILTER (lang(?nbmflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nbmflraw, "No Label Provided!") AS ?nbmfl)

                                                                  OPTIONAL {{
                                                                             ?nbmfraw rdfs:comment ?nbmfdraw
                                                                             FILTER (lang(?nbmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nbmfdraw, "No Description Provided!") AS ?nbmfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :nondimensionalizesFormulation ?nmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?nmfraw), "#")) AS ?nmf)

                                                                  OPTIONAL {{
                                                                             ?nmfraw rdfs:label ?nmflraw
                                                                             FILTER (lang(?nmflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nmflraw, "No Label Provided!") AS ?nmfl)

                                                                  OPTIONAL {{
                                                                             ?nmfraw rdfs:comment ?nmfdraw
                                                                             FILTER (lang(?nmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nmfdraw, "No Description Provided!") AS ?nmfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :discretizedByFormulation ?dbmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?dbmfraw), "#")) AS ?dbmf)

                                                                  OPTIONAL {{
                                                                             ?dbmfraw rdfs:label ?dbmflraw
                                                                             FILTER (lang(?dbmflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dbmflraw, "No Label Provided!") AS ?dbmfl)

                                                                  OPTIONAL {{
                                                                             ?dbmfraw rdfs:comment ?dbmfdraw
                                                                             FILTER (lang(?dbmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dbmfdraw, "No Description Provided!") AS ?dbmfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :discretizesFormulation ?dmfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?dmfraw), "#")) AS ?dmf)

                                                                  OPTIONAL {{
                                                                             ?dmfraw rdfs:label ?dmflraw
                                                                             FILTER (lang(?dmflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dmflraw, "No Label Provided!") AS ?dmfl)

                                                                  OPTIONAL {{
                                                                             ?dmfraw rdfs:comment ?dmfdraw
                                                                             FILTER (lang(?dmfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dmfdraw, "No Description Provided!") AS ?dmfd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :similarToFormulation ?smfraw.
                                                                  BIND(CONCAT("mathmoddb:", STRAFTER(STR(?smfraw), "#")) AS ?smf)

                                                                  OPTIONAL {{
                                                                             ?smfraw rdfs:label ?smflraw
                                                                             FILTER (lang(?smflraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?smflraw, "No Label Provided!") AS ?smfl)

                                                                  OPTIONAL {{
                                                                             ?smfraw rdfs:comment ?smfdraw
                                                                             FILTER (lang(?smfdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?smfdraw, "No Description Provided!") AS ?smfd)
                                                                }}
                                                     
                                                     }}
                                                     GROUP BY ?isLinear ?isNotLinear ?isConvex ?isNotConvex ?isDynamic ?isStatic ?isDeterministic ?isStochastic ?isDimensionless 
                                                              ?isDimensional ?isTimeContinuous ?isTimeDiscrete ?isTimeIndependent ?isSpaceContinuous ?isSpaceDiscrete ?isSpaceIndependent''',

                              'taskInformation': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                              
                                               SELECT DISTINCT ?id
                                                               ?isLinear ?isNotLinear
                                                               (GROUP_CONCAT(DISTINCT(?mm); SEPARATOR=" / ") AS ?appliesModel)
                                                               (GROUP_CONCAT(DISTINCT(?mml); SEPARATOR=" / ") AS ?appliesModelLabel)
                                                               (GROUP_CONCAT(DISTINCT(?mmd); SEPARATOR=" / ") AS ?appliesModelDescription)
                                                               (GROUP_CONCAT(DISTINCT(?mf); SEPARATOR=" / ") AS ?containsFormulation)
                                                               (GROUP_CONCAT(DISTINCT(?mfl); SEPARATOR=" / ") AS ?containsFormulationLabel)
                                                               (GROUP_CONCAT(DISTINCT(?mfd); SEPARATOR=" / ") AS ?containsFormulationDescription)
                                                               (GROUP_CONCAT(DISTINCT(?a); SEPARATOR=" / ") AS ?containsAssumption)
                                                               (GROUP_CONCAT(DISTINCT(?al); SEPARATOR=" / ") AS ?containsAssumptionLabel)
                                                               (GROUP_CONCAT(DISTINCT(?ad); SEPARATOR=" / ") AS ?containsAssumptionDescription)
                                                               (GROUP_CONCAT(DISTINCT(?bc); SEPARATOR=" / ") AS ?containsBoundaryCondition)
                                                               (GROUP_CONCAT(DISTINCT(?bcl); SEPARATOR=" / ") AS ?containsBoundaryConditionLabel)
                                                               (GROUP_CONCAT(DISTINCT(?bcd); SEPARATOR=" / ") AS ?containsBoundaryConditionDescription)
                                                               (GROUP_CONCAT(DISTINCT(?cc); SEPARATOR=" / ") AS ?containsConstraintCondition)
                                                               (GROUP_CONCAT(DISTINCT(?ccl); SEPARATOR=" / ") AS ?containsConstraintConditionLabel)
                                                               (GROUP_CONCAT(DISTINCT(?ccd); SEPARATOR=" / ") AS ?containsConstraintConditionDescription)
                                                               (GROUP_CONCAT(DISTINCT(?cpc); SEPARATOR=" / ") AS ?containsCouplingCondition)
                                                               (GROUP_CONCAT(DISTINCT(?cpcl); SEPARATOR=" / ") AS ?containsCouplingConditionConditionLabel)
                                                               (GROUP_CONCAT(DISTINCT(?cpcd); SEPARATOR=" / ") AS ?containsCouplingConditionConditionDescription)
                                                               (GROUP_CONCAT(DISTINCT(?ic); SEPARATOR=" / ") AS ?containsInitialCondition)
                                                               (GROUP_CONCAT(DISTINCT(?icl); SEPARATOR=" / ") AS ?containsInitialConditionLabel)
                                                               (GROUP_CONCAT(DISTINCT(?icd); SEPARATOR=" / ") AS ?containsInitialConditionDescription)
                                                               (GROUP_CONCAT(DISTINCT(?fc); SEPARATOR=" / ") AS ?containsFinalCondition)
                                                               (GROUP_CONCAT(DISTINCT(?fcl); SEPARATOR=" / ") AS ?containsFinalConditionLabel)
                                                               (GROUP_CONCAT(DISTINCT(?fcd); SEPARATOR=" / ") AS ?containsFinalConditionDescription)
                                                               (GROUP_CONCAT(DISTINCT(?in); SEPARATOR=" / ") AS ?containsInput)
                                                               (GROUP_CONCAT(DISTINCT(?inl); SEPARATOR=" / ") AS ?containsInputLabel)
                                                               (GROUP_CONCAT(DISTINCT(?ind); SEPARATOR=" / ") AS ?containsInputDescription)
                                                               (GROUP_CONCAT(DISTINCT(?ou); SEPARATOR=" / ") AS ?containsOutput)
                                                               (GROUP_CONCAT(DISTINCT(?oul); SEPARATOR=" / ") AS ?containsOutputLabel)
                                                               (GROUP_CONCAT(DISTINCT(?oud); SEPARATOR=" / ") AS ?containsOutputDescription)
                                                               (GROUP_CONCAT(DISTINCT(?ob); SEPARATOR=" / ") AS ?containsObjective)
                                                               (GROUP_CONCAT(DISTINCT(?obl); SEPARATOR=" / ") AS ?containsObjectiveLabel)
                                                               (GROUP_CONCAT(DISTINCT(?obd); SEPARATOR=" / ") AS ?containsObjectiveDescription)
                                                               (GROUP_CONCAT(DISTINCT(?pa); SEPARATOR=" / ") AS ?containsParameter)
                                                               (GROUP_CONCAT(DISTINCT(?pal); SEPARATOR=" / ") AS ?containsParameterLabel)
                                                               (GROUP_CONCAT(DISTINCT(?pad); SEPARATOR=" / ") AS ?containsParameterDescription)
                                                               (GROUP_CONCAT(DISTINCT(?co); SEPARATOR=" / ") AS ?containsConstant)
                                                               (GROUP_CONCAT(DISTINCT(?col); SEPARATOR=" / ") AS ?containsConstantLabel)
                                                               (GROUP_CONCAT(DISTINCT(?cod); SEPARATOR=" / ") AS ?containsConstantDescription)
                                                               (GROUP_CONCAT(DISTINCT(?gt); SEPARATOR=" / ") AS ?generalizesTask)
                                                               (GROUP_CONCAT(DISTINCT(?gtl); SEPARATOR=" / ") AS ?generalizesTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?gtd); SEPARATOR=" / ") AS ?generalizesTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?gbt); SEPARATOR=" / ") AS ?generalizedByTask)
                                                               (GROUP_CONCAT(DISTINCT(?gbtl); SEPARATOR=" / ") AS ?generalizedByTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?gbtd); SEPARATOR=" / ") AS ?generalizedByTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?at); SEPARATOR=" / ") AS ?approximatesTask)
                                                               (GROUP_CONCAT(DISTINCT(?atl); SEPARATOR=" / ") AS ?approximatesTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?atd); SEPARATOR=" / ") AS ?approximatesTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?abt); SEPARATOR=" / ") AS ?approximatedByTask)
                                                               (GROUP_CONCAT(DISTINCT(?abtl); SEPARATOR=" / ") AS ?approximatedByTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?abtd); SEPARATOR=" / ") AS ?approximatedByTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?ct); SEPARATOR=" / ") AS ?containsTask)
                                                               (GROUP_CONCAT(DISTINCT(?ctl); SEPARATOR=" / ") AS ?containsTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?ctd); SEPARATOR=" / ") AS ?containsTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?cit); SEPARATOR=" / ") AS ?containedInTask)
                                                               (GROUP_CONCAT(DISTINCT(?citl); SEPARATOR=" / ") AS ?containedInTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?citd); SEPARATOR=" / ") AS ?containedInTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?lt); SEPARATOR=" / ") AS ?linearizesTask)
                                                               (GROUP_CONCAT(DISTINCT(?ltl); SEPARATOR=" / ") AS ?linearizesTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?ltd); SEPARATOR=" / ") AS ?linearizesTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?lbt); SEPARATOR=" / ") AS ?linearizedByTask)
                                                               (GROUP_CONCAT(DISTINCT(?lbtl); SEPARATOR=" / ") AS ?linearizedByTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?lbtd); SEPARATOR=" / ") AS ?linearizedByTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?dt); SEPARATOR=" / ") AS ?discretizesTask)
                                                               (GROUP_CONCAT(DISTINCT(?dtl); SEPARATOR=" / ") AS ?discretizesTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?dtd); SEPARATOR=" / ") AS ?discretizesTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?dbt); SEPARATOR=" / ") AS ?discretizedByTask)
                                                               (GROUP_CONCAT(DISTINCT(?dbtl); SEPARATOR=" / ") AS ?discretizedByTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?dbtd); SEPARATOR=" / ") AS ?discretizedByTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?st); SEPARATOR=" / ") AS ?similarToTask)
                                                               (GROUP_CONCAT(DISTINCT(?stl); SEPARATOR=" / ") AS ?similarToTaskLabel)
                                                               (GROUP_CONCAT(DISTINCT(?std); SEPARATOR=" / ") AS ?similarToTaskDescription)
                                                               (GROUP_CONCAT(DISTINCT(?pub); SEPARATOR=" / ") AS ?publication)
                                                               (GROUP_CONCAT(DISTINCT(?publ); SEPARATOR=" / ") AS ?publicationLabel)
                                                               (GROUP_CONCAT(DISTINCT(?pubd); SEPARATOR=" / ") AS ?publicationDescription)
                                               WHERE {{ 
                                                       VALUES ?id {{{0}}} 

                                                        OPTIONAL {{
                                                                   ?id (:documentedIn | :inventedIn | :studiedIn | :surveyedIn | :usedIn) ?pubraw.
                                                                   BIND(STRAFTER(STR(?pubraw), "#") AS ?pub)
                                                                   OPTIONAL {{ ?pubraw rdfs:label ?publraw
                                                                               FILTER (lang(?publraw) = 'en') }}
                                                                   BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)
                                                                   OPTIONAL {{ ?pubraw rdfs:comment ?pubdraw
                                                                               FILTER (lang(?pubdraw) = 'en') }}
                                                                   BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
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

                                                       OPTIONAL {{
                                                                  ?id :appliesModel ?mmraw.
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
                                                                }}   
                                                       OPTIONAL {{
                                                                  ?id :containsFormulation ?mfraw.
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

                                                                  BIND(COALESCE(?mfdraw, "No Description Provided!") AS ?mfd)
                                                                }}
                                                        
                                                        OPTIONAL {{
                                                                  ?id :containsBoundaryCondition ?bcraw.
                                                                  BIND(STRAFTER(STR(?bcraw), "#") AS ?bc)

                                                                  OPTIONAL {{
                                                                             ?bcraw rdfs:label ?bclraw
                                                                             FILTER (lang(?bclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?bclraw, "No Label Provided!") AS ?bcl)

                                                                  OPTIONAL {{
                                                                             ?bcraw rdfs:comment ?bcdraw
                                                                             FILTER (lang(?bcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?bcdraw, "No Description Provided!") AS ?bcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsConstraintCondition ?ccraw.
                                                                  BIND(STRAFTER(STR(?ccraw), "#") AS ?cc)
                                                                  
                                                                  OPTIONAL {{
                                                                             ?ccraw rdfs:label ?cclraw
                                                                             FILTER (lang(?cclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cclraw, "No Label Provided!") AS ?ccl)

                                                                  OPTIONAL {{
                                                                             ?ccraw rdfs:comment ?ccdraw
                                                                             FILTER (lang(?ccdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?ccdraw, "No Description Provided!") AS ?ccd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsCouplingCondition ?cpcraw.
                                                                  BIND(STRAFTER(STR(?cpcraw), "#") AS ?cpc)

                                                                  OPTIONAL {{
                                                                             ?cpcraw rdfs:label ?cpclraw
                                                                             FILTER (lang(?cpclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cpclraw, "No Label Provided!") AS ?cpcl)

                                                                  OPTIONAL {{
                                                                             ?cpcraw rdfs:comment ?cpcdraw
                                                                             FILTER (lang(?cpcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?cpcdraw, "No Description Provided!") AS ?cpcd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsAssumption ?araw.
                                                                  BIND(STRAFTER(STR(?araw), "#") AS ?a)

                                                                  OPTIONAL {{
                                                                             ?araw rdfs:label ?alraw
                                                                             FILTER (lang(?alraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?alraw, "No Label Provided!") AS ?al)

                                                                  OPTIONAL {{
                                                                             ?araw rdfs:comment ?adraw
                                                                             FILTER (lang(?adraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?adraw, "No Description Provided!") AS ?ad)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsInitialCondition ?icraw.
                                                                  BIND(STRAFTER(STR(?icraw), "#") AS ?ic)
                                                                  
                                                                  OPTIONAL {{
                                                                             ?icraw rdfs:label ?iclraw
                                                                             FILTER (lang(?iclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?iclraw, "No Label Provided!") AS ?icl)

                                                                  OPTIONAL {{
                                                                             ?icraw rdfs:comment ?icdraw
                                                                             FILTER (lang(?icdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?icdraw, "No Description Provided!") AS ?icd)
                                                                }}

                                                        OPTIONAL {{
                                                                  ?id :containsFinalCondition ?fcraw.
                                                                  BIND(STRAFTER(STR(?fcraw), "#") AS ?fc)

                                                                  OPTIONAL {{
                                                                             ?fcraw rdfs:label ?fclraw
                                                                             FILTER (lang(?fclraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?fclraw, "No Label Provided!") AS ?fcl)

                                                                  OPTIONAL {{
                                                                             ?fcraw rdfs:comment ?fcdraw
                                                                             FILTER (lang(?fcdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?fcdraw, "No Description Provided!") AS ?fcd)
                                                                }}
                                                        OPTIONAL {{
                                                                  ?id :containsInput ?inraw.
                                                                  BIND(STRAFTER(STR(?inraw), "#") AS ?in)

                                                                  OPTIONAL {{
                                                                             ?inraw rdfs:label ?inlraw
                                                                             FILTER (lang(?inlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?inlraw, "No Label Provided!") AS ?inl)

                                                                  OPTIONAL {{
                                                                             ?inraw rdfs:comment ?indraw
                                                                             FILTER (lang(?indraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?indraw, "No Description Provided!") AS ?ind)
                                                                }}
                                                        OPTIONAL {{
                                                                  ?id :containsOutput ?ouraw.
                                                                  BIND(STRAFTER(STR(?ouraw), "#") AS ?ou)

                                                                  OPTIONAL {{
                                                                             ?ouraw rdfs:label ?oulraw
                                                                             FILTER (lang(?oulraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?oulraw, "No Label Provided!") AS ?oul)

                                                                  OPTIONAL {{
                                                                             ?ouraw rdfs:comment ?oudraw
                                                                             FILTER (lang(?oudraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?oudraw, "No Description Provided!") AS ?oud)
                                                                }}
                                                        OPTIONAL {{
                                                                  ?id :containsObjective ?obraw.
                                                                  BIND(STRAFTER(STR(?obraw), "#") AS ?ob)

                                                                  OPTIONAL {{
                                                                             ?obraw rdfs:label ?oblraw
                                                                             FILTER (lang(?oblraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?oblraw, "No Label Provided!") AS ?obl)

                                                                  OPTIONAL {{
                                                                             ?obraw rdfs:comment ?obdraw
                                                                             FILTER (lang(?obdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?obdraw, "No Description Provided!") AS ?obd)
                                                                }}
                                                        OPTIONAL {{
                                                                  ?id :containsParameter ?paraw.
                                                                  BIND(STRAFTER(STR(?paraw), "#") AS ?pa)

                                                                  OPTIONAL {{
                                                                             ?paraw rdfs:label ?palraw
                                                                             FILTER (lang(?palraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?palraw, "No Label Provided!") AS ?pal)

                                                                  OPTIONAL {{
                                                                             ?paraw rdfs:comment ?padraw
                                                                             FILTER (lang(?padraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?padraw, "No Description Provided!") AS ?pad)
                                                                }}
                                                        OPTIONAL {{
                                                                  ?id :containsConstant ?coraw.
                                                                  BIND(STRAFTER(STR(?coraw), "#") AS ?co)

                                                                  OPTIONAL {{
                                                                             ?coraw rdfs:label ?colraw
                                                                             FILTER (lang(?colraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?colraw, "No Label Provided!") AS ?col)

                                                                  OPTIONAL {{
                                                                             ?coraw rdfs:comment ?codraw
                                                                             FILTER (lang(?codraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?codraw, "No Description Provided!") AS ?cod)
                                                                }}
                                                        OPTIONAL {{
                                                                  ?id :generalizedByTask ?gbtraw.
                                                                  BIND(STRAFTER(STR(?gbtraw), "#") AS ?gbt)

                                                                  OPTIONAL {{
                                                                             ?gbtraw rdfs:label ?gbtlraw
                                                                             FILTER (lang(?gbtlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gbtlraw, "No Label Provided!") AS ?gbtl)

                                                                  OPTIONAL {{
                                                                             ?gbtraw rdfs:comment ?gbtdraw
                                                                             FILTER (lang(?gbtdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gbtdraw, "No Description Provided!") AS ?gbtd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :generalizesTask ?gtraw.
                                                                  BIND(STRAFTER(STR(?gtraw), "#") AS ?gt)

                                                                  OPTIONAL {{
                                                                             ?gtraw rdfs:label ?gtlraw
                                                                             FILTER (lang(?gtlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?gtlraw, "No Label Provided!") AS ?gtl)

                                                                  OPTIONAL {{
                                                                             ?gtraw rdfs:comment ?gtdraw
                                                                             FILTER (lang(?gtdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?gtdraw, "No Description Provided!") AS ?gtd)
                                                                }}

                                                      OPTIONAL {{
                                                                  ?id :discretizedByTask ?dbtraw.
                                                                  BIND(STRAFTER(STR(?dbtraw), "#") AS ?dbt)

                                                                  OPTIONAL {{
                                                                             ?dbtraw rdfs:label ?dbtlraw
                                                                             FILTER (lang(?dbtlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?dbtlraw, "No Label Provided!") AS ?dbtl)

                                                                  OPTIONAL {{
                                                                             ?dbtraw rdfs:comment ?dbtdraw
                                                                             FILTER (lang(?dbtdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dbtdraw, "No Description Provided!") AS ?dbtd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :discretizesModel ?dtraw.
                                                                  BIND(STRAFTER(STR(?dtraw), "#") AS ?dt)

                                                                  OPTIONAL {{
                                                                             ?dtraw rdfs:label ?dtlraw
                                                                             FILTER (lang(?dtlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?dtlraw, "No Label Provided!") AS ?dtl)

                                                                  OPTIONAL {{
                                                                             ?dtraw rdfs:comment ?dtdraw
                                                                             FILTER (lang(?dtdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dtdraw, "No Description Provided!") AS ?dtd)
                                                                }}

                                                      OPTIONAL {{
                                                                  ?id :containedInTask ?citraw.
                                                                  BIND(STRAFTER(STR(?citraw), "#") AS ?cit)

                                                                  OPTIONAL {{
                                                                             ?citraw rdfs:label ?citlraw
                                                                             FILTER (lang(?citlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?citlraw, "No Label Provided!") AS ?citl)

                                                                  OPTIONAL {{
                                                                             ?citraw rdfs:comment ?citdraw
                                                                             FILTER (lang(?citdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?citdraw, "No Description Provided!") AS ?citd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :containsTask ?ctraw.
                                                                  BIND(STRAFTER(STR(?ctraw), "#") AS ?ct)

                                                                  OPTIONAL {{
                                                                             ?ctraw rdfs:label ?ctlraw
                                                                             FILTER (lang(?ctlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?ctlraw, "No Label Provided!") AS ?ctl)

                                                                  OPTIONAL {{
                                                                             ?ctraw rdfs:comment ?ctdraw
                                                                             FILTER (lang(?ctdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?ctdraw, "No Description Provided!") AS ?ctd)
                                                                }}

                                                      OPTIONAL {{
                                                                  ?id :approximatedByTask ?abtraw.
                                                                  BIND(STRAFTER(STR(?abtraw), "#") AS ?abt)

                                                                  OPTIONAL {{
                                                                             ?abtraw rdfs:label ?abtlraw
                                                                             FILTER (lang(?abtlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?abtlraw, "No Label Provided!") AS ?abtl)

                                                                  OPTIONAL {{
                                                                             ?abtraw rdfs:comment ?abtdraw
                                                                             FILTER (lang(?abtdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abtdraw, "No Description Provided!") AS ?abtd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :approximatesTask ?atraw.
                                                                  BIND(STRAFTER(STR(?atraw), "#") AS ?at)

                                                                  OPTIONAL {{
                                                                             ?atraw rdfs:label ?atlraw
                                                                             FILTER (lang(?atlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?atlraw, "No Label Provided!") AS ?atl)

                                                                  OPTIONAL {{
                                                                             ?atraw rdfs:comment ?atdraw
                                                                             FILTER (lang(?atdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?atdraw, "No Description Provided!") AS ?atd)
                                                                }}

                                                      OPTIONAL {{
                                                                  ?id :linearizedByTask ?lbtraw.
                                                                  BIND(STRAFTER(STR(?lbtraw), "#") AS ?lbt)

                                                                  OPTIONAL {{
                                                                             ?lbtraw rdfs:label ?lbtlraw
                                                                             FILTER (lang(?lbtlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?lbtlraw, "No Label Provided!") AS ?lbtl)

                                                                  OPTIONAL {{
                                                                             ?lbtraw rdfs:comment ?lbtdraw
                                                                             FILTER (lang(?lbtdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbtdraw, "No Description Provided!") AS ?lbtd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :linearizesTask ?ltraw.
                                                                  BIND(STRAFTER(STR(?ltraw), "#") AS ?lt)

                                                                  OPTIONAL {{
                                                                             ?ltraw rdfs:label ?ltlraw
                                                                             FILTER (lang(?ltlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?ltlraw, "No Label Provided!") AS ?ltl)

                                                                  OPTIONAL {{
                                                                             ?ltraw rdfs:comment ?ltdraw
                                                                             FILTER (lang(?ltdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?ltdraw, "No Description Provided!") AS ?ltd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :discretizedByTask ?dbtraw.
                                                                  BIND(STRAFTER(STR(?dbtraw), "#") AS ?dbt)

                                                                  OPTIONAL {{
                                                                             ?dbtraw rdfs:label ?dbtlraw
                                                                             FILTER (lang(?dbtlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?dbtlraw, "No Label Provided!") AS ?dbtl)

                                                                  OPTIONAL {{
                                                                             ?dbtraw rdfs:comment ?dbtdraw
                                                                             FILTER (lang(?dbtdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dbtdraw, "No Description Provided!") AS ?dbtd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :discretizesTask ?dtraw.
                                                                  BIND(STRAFTER(STR(?dtraw), "#") AS ?dt)

                                                                  OPTIONAL {{
                                                                             ?dtraw rdfs:label ?dtlraw
                                                                             FILTER (lang(?dtlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?dtlraw, "No Label Provided!") AS ?dtl)

                                                                  OPTIONAL {{
                                                                             ?dtraw rdfs:comment ?dtdraw
                                                                             FILTER (lang(?dtdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dtdraw, "No Description Provided!") AS ?dtd)
                                                                }}

                                                       OPTIONAL {{
                                                                  ?id :similarToTask ?straw.
                                                                  BIND(STRAFTER(STR(?straw), "#") AS ?st)

                                                                  OPTIONAL {{
                                                                             ?straw rdfs:label ?stlraw
                                                                             FILTER (lang(?stlraw) = 'en')
                                                                           }}
                                                                  
                                                                  BIND(COALESCE(?stlraw, "No Label Provided!") AS ?stl)

                                                                  OPTIONAL {{
                                                                             ?straw rdfs:comment ?stdraw
                                                                             FILTER (lang(?stdraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?stdraw, "No Description Provided!") AS ?std)
                                                                }}
                                                     }}
                                                     GROUP BY ?id ?isLinear ?isNotLinear'''
                                      
                                                      }