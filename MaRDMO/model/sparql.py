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

queryPortalProvider = {
    
                  'RP': '''SELECT ?id ?label ?quote
                           WHERE {
                             ?idraw wdt:P1495 wd:Q6534265;
                                 wdt:P31 wd:Q6032837.
                             ?idraw rdfs:label ?label.
                             FILTER (lang(?label) = 'en')
                             ?idraw schema:description ?quote.
                             FILTER (lang(?quote) = 'en')
                             BIND(replace( xsd:string(?idraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?id) 
                             }'''
}
    
queryProviderMM = {
                 'EN': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  
                          
                          SELECT DISTINCT ?id ?label ?quote
                          WHERE { 
                                 VALUES ?class { :MathematicalFormulation :ComputationalTask :Quantity :QuantityKind }
                                 ?idraw a ?class .
                                 BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                 OPTIONAL {?idraw rdfs:label ?labelraw .
                                           FILTER(lang(?labelraw) = 'en')}
                                 BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                 OPTIONAL {?idraw rdfs:comment ?quoteraw.
                                           FILTER(lang(?quoteraw) = 'en')}
                                 BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                }
                          GROUP BY ?id ?label ?quote''',

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

    'researchFieldInformation': '''SELECT DISTINCT (GROUP_CONCAT(DISTINCT CONCAT(?sbrf, " | ", ?sbrfl, " | ", ?sbrfd); separator=" / ") AS ?specializedBy)
                                                   (GROUP_CONCAT(DISTINCT CONCAT(?srf, " | ", ?srfl, " | ", ?srfd); separator=" / ") AS ?specializes)
                                                   (GROUP_CONCAT(DISTINCT CONCAT(?strf, " | ", ?strfl, " | ", ?strfd); separator=" / ") AS ?similarTo)
                                                   (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)

                                     WHERE {{
                                                   
                                                    VALUES ?id {{wd:{0}}}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1684 ?sbrfraw.
                                                                   BIND(replace( xsd:string(?sbrfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?sbrf)

                                                                   ?sbrfraw wdt:P31 wd:Q60231.
                                                                   
                                                                   OPTIONAL {{
                                                                              ?sbrfraw rdfs:label ?sbrflraw.
                                                                              FILTER (lang(?sbrflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?sbrflraw, "No Label Provided!") AS ?sbrfl)

                                                                  OPTIONAL {{
                                                                             ?sbrfraw schema:description ?sbrfdraw
                                                                             FILTER (lang(?sbrfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?sbrfdraw, "No Description Provided!") AS ?sbrfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?srfraw wdt:P1684 ?id.
                                                                   BIND(replace( xsd:string(?srfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?srf)

                                                                   ?srfraw wdt:P31 wd:Q60231.
                                                                   
                                                                   OPTIONAL {{
                                                                              ?srfraw rdfs:label ?srflraw.
                                                                              FILTER (lang(?srflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?srflraw, "No Label Provided!") AS ?srfl)

                                                                  OPTIONAL {{
                                                                             ?srfraw schema:description ?srfdraw
                                                                             FILTER (lang(?srfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?srfdraw, "No Description Provided!") AS ?srfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?strfraw wdt: ?id.
                                                                   BIND(replace( xsd:string(?strfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?strf)

                                                                   ?strfraw wdt:P31 wd:Q60231.
                                                                   
                                                                   OPTIONAL {{
                                                                              ?strfraw rdfs:label ?strflraw.
                                                                              FILTER (lang(?strflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?strflraw, "No Label Provided!") AS ?strfl)

                                                                  OPTIONAL {{
                                                                             ?strfraw schema:description ?strfdraw
                                                                             FILTER (lang(?strfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?strfdraw, "No Description Provided!") AS ?strfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P286 ?pubraw.
                                                                   BIND(replace( xsd:string(?pubraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?pub)

                                                                   OPTIONAL {{
                                                                              ?pubraw rdfs:label ?publraw.
                                                                              FILTER (lang(?publraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)

                                                                  OPTIONAL {{
                                                                             ?pubraw schema:description ?pubdraw
                                                                             FILTER (lang(?pubdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                               }}

                                          }}''',

    'researchProblemInformation': '''SELECT DISTINCT (GROUP_CONCAT(DISTINCT CONCAT(?rf, " | ", ?rfl, " | ", ?rfd); separator=" / ") AS ?containedInField)
                                                     (GROUP_CONCAT(DISTINCT CONCAT(?sbrp, " | ", ?sbrpl, " | ", ?sbrpd); separator=" / ") AS ?specializedBy)
                                                     (GROUP_CONCAT(DISTINCT CONCAT(?srp, " | ", ?srpl, " | ", ?srpd); separator=" / ") AS ?specializes)
                                                     (GROUP_CONCAT(DISTINCT CONCAT(?strp, " | ", ?strpl, " | ", ?strpd); separator=" / ") AS ?similarTo)
                                                     (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)

                                     WHERE {{
                                                   
                                                    VALUES ?id {{wd:{0}}}
                                                   
                                                    OPTIONAL {{
                                                                   ?rfraw wdt:P1560 ?id.
                                                                   BIND(replace( xsd:string(?rfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?rf)

                                                                   OPTIONAL {{
                                                                              ?rfraw rdfs:label ?rflraw.
                                                                              FILTER (lang(?rflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?rflraw, "No Label Provided!") AS ?rfl)

                                                                  OPTIONAL {{
                                                                             ?rfraw schema:description ?rfdraw
                                                                             FILTER (lang(?rfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?rfdraw, "No Description Provided!") AS ?rfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1684 ?sbrpraw.
                                                                   BIND(replace( xsd:string(?sbrpraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?sbrp)

                                                                   ?sbrpraw wdt:P31 wd:Q6032837.
                                                                   
                                                                   OPTIONAL {{
                                                                              ?sbrpraw rdfs:label ?sbrplraw.
                                                                              FILTER (lang(?sbrplraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?sbrplraw, "No Label Provided!") AS ?sbrpl)

                                                                  OPTIONAL {{
                                                                             ?sbrpraw schema:description ?sbrpdraw
                                                                             FILTER (lang(?sbrpdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?sbrpdraw, "No Description Provided!") AS ?sbrpd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?srpraw wdt:P1684 ?id.
                                                                   BIND(replace( xsd:string(?srpraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?srp)

                                                                   ?srpraw wdt:P31 wd:Q6032837.
                                                                   
                                                                   OPTIONAL {{
                                                                              ?srpraw rdfs:label ?srplraw.
                                                                              FILTER (lang(?srplraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?srplraw, "No Label Provided!") AS ?srpl)

                                                                  OPTIONAL {{
                                                                             ?srpraw schema:description ?srpdraw
                                                                             FILTER (lang(?srpdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?srpdraw, "No Description Provided!") AS ?srpd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?strpraw wdt: ?id.
                                                                   BIND(replace( xsd:string(?strpraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?strp)

                                                                   ?strpraw wdt:P31 wd:Q6032837.
                                                                   
                                                                   OPTIONAL {{
                                                                              ?strpraw rdfs:label ?strplraw.
                                                                              FILTER (lang(?strplraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?strplraw, "No Label Provided!") AS ?strpl)

                                                                  OPTIONAL {{
                                                                             ?strpraw schema:description ?strpdraw
                                                                             FILTER (lang(?strpdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?strpdraw, "No Description Provided!") AS ?strpd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P286 ?pubraw.
                                                                   BIND(replace( xsd:string(?pubraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?pub)

                                                                   OPTIONAL {{
                                                                              ?pubraw rdfs:label ?publraw.
                                                                              FILTER (lang(?publraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)

                                                                  OPTIONAL {{
                                                                             ?pubraw schema:description ?pubdraw
                                                                             FILTER (lang(?pubdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                               }}

                                          }}''',

    'mathematicalModelInformation': '''SELECT DISTINCT ?isLinear ?isNotLinear
                                                                 ?isDynamic ?isStatic
                                                                 ?isDeterministic ?isStochastic
                                                                 ?isDimensionless ?isDimensional
                                                                 ?isSpaceContinuous ?isSpaceDiscrete
                                                                 ?isTimeContinuous ?isTimeDiscrete
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?rp, " | ", ?rpl, " | ", ?rpd); separator=" / ") AS ?models)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?ass, " | ", ?assl, " | ", ?assd); separator=" / ") AS ?assumes)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?conf, " | ", ?confl, " | ", ?confd, " | ", ?confq); separator=" / ") AS ?containsFormulation)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?ta, " | ", ?tal, " | ", ?tad); separator=" / ") AS ?usedBy)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?sbm, " | ", ?sbml, " | ", ?sbmd, " | ", ?sbmq); separator=" / ") AS ?specializedBy)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?sm, " | ", ?sml, " | ", ?smd, " | ", ?smq); separator=" / ") AS ?specializes)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?abm, " | ", ?abml, " | ", ?abmd); separator=" / ") AS ?approximatedBy)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?am, " | ", ?aml, " | ", ?amd); separator=" / ") AS ?approximates)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?conm, " | ", ?conml, " | ", ?conmd); separator=" / ") AS ?containsModel)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?conim, " | ", ?coniml, " | ", ?conimd); separator=" / ") AS ?containedInModel)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?dbm, " | ", ?dbml, " | ", ?dbmd); separator=" / ") AS ?discretizedBy)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?dm, " | ", ?dml, " | ", ?dmd); separator=" / ") AS ?discretizes)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?lbm, " | ", ?lbml, " | ", ?lbmd); separator=" / ") AS ?linearizedBy)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?lm, " | ", ?lml, " | ", ?lmd); separator=" / ") AS ?linearizes)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?stm, " | ", ?stml, " | ", ?stmd); separator=" / ") AS ?similarTo)
                                                                 (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)
                                                                 
                                                 WHERE {{
                                                   
                                                    VALUES ?id {{wd:{0}}}
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672112 }}, "True", "False" ) AS ?isLinear)
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672110 }}, "True", "False" ) AS ?isNotLinear)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672082 }}, "True", "False" ) AS ?isDynamic)
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672084 }}, "True", "False" ) AS ?isStatic)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672076 }}, "True", "False" ) AS ?isDeterministic)
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672078 }}, "True", "False" ) AS ?isStochastic)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672080 }}, "True", "False" ) AS ?isDimensionless)
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isDimensional)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672089 }}, "True", "False" ) AS ?isSpaceContinuous)
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672093 }}, "True", "False" ) AS ?isSpaceDiscrete)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672091 }}, "True", "False" ) AS ?isTimeContinuous)
                                                    BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672095 }}, "True", "False" ) AS ?isTimeDiscrete)

                                                    OPTIONAL {{
                                                                   ?rpraw wdt:P1513 ?id.
                                                                   BIND(replace( xsd:string(?rpraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?rp)

                                                                   OPTIONAL {{
                                                                              ?rpraw rdfs:label ?rplraw.
                                                                              FILTER (lang(?rplraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?rplraw, "No Label Provided!") AS ?rpl)

                                                                  OPTIONAL {{
                                                                             ?rpraw schema:description ?rpdraw
                                                                             FILTER (lang(?rpdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?rpdraw, "No Description Provided!") AS ?rpd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1674 ?assraw.
                                                                   BIND(replace( xsd:string(?assraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?ass)

                                                                   ?assraw wdt:P31 wd:Q6481152.

                                                                   OPTIONAL {{
                                                                              ?assraw rdfs:label ?asslraw.
                                                                              FILTER (lang(?asslraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?asslraw, "No Label Provided!") AS ?assl)

                                                                  OPTIONAL {{
                                                                             ?assraw schema:description ?assdraw
                                                                             FILTER (lang(?assdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?assdraw, "No Description Provided!") AS ?assd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id p:P1560 ?statement.
                                                                   ?statement ps:P1560 ?confraw.

                                                                   ?confraw wdt:P31 wd:Q6481152.

                                                                   BIND(replace( xsd:string(?confraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?conf)

                                                                   OPTIONAL {{
                                                                              ?confraw rdfs:label ?conflraw.
                                                                              FILTER (lang(?conflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?conflraw, "No Label Provided!") AS ?confl)

                                                                  OPTIONAL {{
                                                                             ?confraw schema:description ?confdraw
                                                                             FILTER (lang(?confdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?confdraw, "No Description Provided!") AS ?confd)

                                                                  OPTIONAL {{
                                                                             ?statement pq:P560 ?quaraw.
                                                                             BIND(REPLACE(STR(?quaraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua)
                                                                           }}
                                                                  BIND(COALESCE(?qua, "") AS ?confq)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P147 ?taraw.
                                                                   BIND(replace( xsd:string(?taraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?ta)

                                                                   OPTIONAL {{
                                                                              ?taraw rdfs:label ?talraw.
                                                                              FILTER (lang(?talraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?talraw, "No Label Provided!") AS ?tal)

                                                                  OPTIONAL {{
                                                                             ?taraw schema:description ?tadraw
                                                                             FILTER (lang(?tadraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?tadraw, "No Description Provided!") AS ?tad)
                                                               }}

                                                    OPTIONAL {{   
                                                    
                                                        OPTIONAL {{
                                                          
                                                          {{
                                                            SELECT ?statement2 (GROUP_CONCAT(DISTINCT ?sbmq_entry; separator=" <|> ") AS ?sbmq)
                                                            WHERE {{
                                                     
                                                              ?id p:P1684 ?statement2.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement2 pq:P1674 ?qua2raw.
                                                                 BIND(REPLACE(STR(?qua2raw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua2)
 
                                                                 OPTIONAL {{
                                                                   ?qua2raw rdfs:label ?sbmqlraw.
                                                                   FILTER (lang(?sbmqlraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?sbmqlraw, "No Label Provided!") AS ?sbmql)
 
                                                                 OPTIONAL {{
                                                                   ?qua2raw schema:description ?sbmqdraw.
                                                                   FILTER (lang(?sbmqdraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?sbmqdraw, "No Description Provided!") AS ?sbmqd)
                                                               
                                                              }}
                                                              BIND(COALESCE(?qua2, "") AS ?qua2_final)
                                                              BIND(COALESCE(?sbmql, "") AS ?sbmql_final)
                                                              BIND(COALESCE(?sbmqd, "") AS ?sbmqd_final)
                                                              
                                                              BIND(IF((?qua2_final = "" && ?sbmql_final = "" && ?sbmqd_final = ""),"",CONCAT(?qua2_final, " | ", ?sbmql_final, " | ", ?sbmqd_final)) AS ?sbmq_entry)
                                                                 
                                                            }}
                                                            GROUP BY ?statement2
                                                          }}
                                                          }}
                                                        
                                                          ?id p:P1684 ?statement2.
                                                          ?statement2 ps:P1684 ?sbmraw.
                                                          
                                                          BIND(REPLACE(STR(?sbmraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?sbm)
                                                        
                                                          OPTIONAL {{
                                                            ?sbmraw rdfs:label ?sbmlraw
                                                            FILTER (lang(?sbmlraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?sbmlraw, "No Label Provided!") AS ?sbml)
                                                        
                                                          OPTIONAL {{
                                                            ?sbmraw schema:description ?sbmdraw
                                                            FILTER (lang(?sbmdraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?sbmdraw, "No Description Provided!") AS ?sbmd)
                                                  
                                                          }}

                                                    OPTIONAL {{   
                                                    
                                                        OPTIONAL {{
                                                          
                                                          {{
                                                            SELECT ?statement3 (GROUP_CONCAT(DISTINCT ?smq_entry; separator=" <|> ") AS ?smq)
                                                            WHERE {{
                                                     
                                                              ?smraw p:P1684 ?statement3.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement3 pq:P1674 ?qua3raw.
                                                                 BIND(REPLACE(STR(?qua3raw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua3)
 
                                                                 OPTIONAL {{
                                                                   ?qua3raw rdfs:label ?smqlraw.
                                                                   FILTER (lang(?smqlraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?smqlraw, "No Label Provided!") AS ?smql)
 
                                                                 OPTIONAL {{
                                                                   ?qua3raw schema:description ?smqdraw.
                                                                   FILTER (lang(?smqdraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?smqdraw, "No Description Provided!") AS ?smqd)
                                                               
                                                              }}
                                                              BIND(COALESCE(?qua3, "") AS ?qua3_final)
                                                              BIND(COALESCE(?smql, "") AS ?smql_final)
                                                              BIND(COALESCE(?smqd, "") AS ?smqd_final)
                                                              
                                                              BIND(IF((?qua3_final = "" && ?smql_final = "" && ?smqd_final = ""),"",CONCAT(?qua3_final, " | ", ?smql_final, " | ", ?smqd_final)) AS ?smq_entry)
                                                                 
                                                            }}
                                                            GROUP BY ?statement3
                                                          }}
                                                          }}
                                                        
                                                          ?smraw p:P1684 ?statement3.
                                                          ?statement3 ps:P1684 ?id.
                                                          
                                                          BIND(REPLACE(STR(?smraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?sm)
                                                        
                                                          OPTIONAL {{
                                                            ?smraw rdfs:label ?smlraw
                                                            FILTER (lang(?smlraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?smlraw, "No Label Provided!") AS ?sml)
                                                        
                                                          OPTIONAL {{
                                                            ?smraw schema:description ?smdraw
                                                            FILTER (lang(?smdraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?smdraw, "No Description Provided!") AS ?smd)
                                                  
                                                          }}
                                                    
                                                    OPTIONAL {{
                                                                   ?id wdt:P1655 ?abmraw.
                                                                   BIND(replace( xsd:string(?abmraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?abm)

                                                                   OPTIONAL {{
                                                                              ?abmraw rdfs:label ?abmlraw.
                                                                              FILTER (lang(?abmlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abmlraw, "No Label Provided!") AS ?abml)

                                                                  OPTIONAL {{
                                                                             ?abmraw schema:description ?abmdraw
                                                                             FILTER (lang(?abmdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?abmdraw, "No Description Provided!") AS ?abmd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?amraw wdt:P1655 ?id.
                                                                   BIND(replace( xsd:string(?amraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?am)

                                                                   OPTIONAL {{
                                                                              ?amraw rdfs:label ?amlraw.
                                                                              FILTER (lang(?amlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?amlraw, "No Label Provided!") AS ?aml)

                                                                  OPTIONAL {{
                                                                             ?amraw schema:description ?amdraw
                                                                             FILTER (lang(?amdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?amdraw, "No Description Provided!") AS ?amd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1560 ?conmraw.
                                                                   BIND(replace( xsd:string(?conmraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?conm)

                                                                   ?conmraw wdt:P31 wd:Q68663.

                                                                   OPTIONAL {{
                                                                              ?conmraw rdfs:label ?conmlraw.
                                                                              FILTER (lang(?conmlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?conmlraw, "No Label Provided!") AS ?conml)

                                                                  OPTIONAL {{
                                                                             ?conmraw schema:description ?conmdraw
                                                                             FILTER (lang(?conmdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?conmdraw, "No Description Provided!") AS ?conmd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?conimraw wdt:P1560 ?id.
                                                                   BIND(replace( xsd:string(?conimraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?conim)

                                                                   ?conimraw wdt:P31 wd:Q68663.

                                                                   OPTIONAL {{
                                                                              ?conimraw rdfs:label ?conimlraw.
                                                                              FILTER (lang(?conimlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?conimlraw, "No Label Provided!") AS ?coniml)

                                                                  OPTIONAL {{
                                                                             ?conimraw schema:description ?conimdraw
                                                                             FILTER (lang(?conimdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?conimdraw, "No Description Provided!") AS ?conimd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1656 ?dbmraw.
                                                                   BIND(replace( xsd:string(?dbmraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?dbm)

                                                                   OPTIONAL {{
                                                                              ?dbmraw rdfs:label ?dbmlraw.
                                                                              FILTER (lang(?dbmlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dbmlraw, "No Label Provided!") AS ?dbml)

                                                                  OPTIONAL {{
                                                                             ?dbmraw schema:description ?dbmdraw
                                                                             FILTER (lang(?dbmdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?dbmdraw, "No Description Provided!") AS ?dbmd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?dmraw wdt:P1656 ?id.
                                                                   BIND(replace( xsd:string(?dmraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?dm)

                                                                   OPTIONAL {{
                                                                              ?dmraw rdfs:label ?dmlraw.
                                                                              FILTER (lang(?dmlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dmlraw, "No Label Provided!") AS ?dml)

                                                                  OPTIONAL {{
                                                                             ?dmraw schema:description ?dmdraw
                                                                             FILTER (lang(?dmdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?dmdraw, "No Description Provided!") AS ?dmd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1657 ?lbmraw.
                                                                   BIND(replace( xsd:string(?lbmraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?lbm)

                                                                   OPTIONAL {{
                                                                              ?lbmraw rdfs:label ?lbmlraw.
                                                                              FILTER (lang(?lbmlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbmlraw, "No Label Provided!") AS ?lbml)

                                                                  OPTIONAL {{
                                                                             ?lbmraw schema:description ?lbmdraw
                                                                             FILTER (lang(?lbmdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?lbmdraw, "No Description Provided!") AS ?lbmd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?lmraw wdt:P1657 ?id.
                                                                   BIND(replace( xsd:string(?lmraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?lm)

                                                                   OPTIONAL {{
                                                                              ?lmraw rdfs:label ?lmlraw.
                                                                              FILTER (lang(?lmlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lmlraw, "No Label Provided!") AS ?lml)

                                                                  OPTIONAL {{
                                                                             ?lmraw schema:description ?lmdraw
                                                                             FILTER (lang(?lmdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?lmdraw, "No Description Provided!") AS ?lmd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?stmraw wdt: ?id.
                                                                   BIND(replace( xsd:string(?stmraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?stm)

                                                                   OPTIONAL {{
                                                                              ?stmraw rdfs:label ?stmlraw.
                                                                              FILTER (lang(?stmlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?stmlraw, "No Label Provided!") AS ?stml)

                                                                  OPTIONAL {{
                                                                             ?stmraw schema:description ?stmdraw
                                                                             FILTER (lang(?stmdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?stmdraw, "No Description Provided!") AS ?stmd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P286 ?pubraw.
                                                                   BIND(replace( xsd:string(?pubraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?pub)

                                                                   OPTIONAL {{
                                                                              ?pubraw rdfs:label ?publraw.
                                                                              FILTER (lang(?publraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)

                                                                  OPTIONAL {{
                                                                             ?pubraw schema:description ?pubdraw
                                                                             FILTER (lang(?pubdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                               }}
          
                                                   }}
                                                   GROUP BY ?isLinear ?isNotLinear ?isDynamic ?isStatic ?isDeterministic ?isStochastic ?isDimensionless 
                                                            ?isDimensional ?isSpaceContinuous ?isSpaceDiscrete ?isTimeContinuous ?isTimeDiscrete''',

              'quantityOrQuantityKindInformation': '''SELECT DISTINCT ?isDynamic ?isStatic
                                                                      ?isDeterministic ?isStochastic
                                                                      ?isDimensionless ?isDimensional
                                                                      ?isSpaceContinuous ?isSpaceDiscrete
                                                                      ?isTimeContinuous ?isTimeDiscrete
                                                                      ?isChemicalConstant ?isMathematicalConstant ?isPhysicalConstant
                                                                      ?class ?reference
                                                                      (GROUP_CONCAT(DISTINCT(?formula); SEPARATOR=" / ") AS ?formulas)
                                                                      (GROUP_CONCAT(DISTINCT(?symbol); SEPARATOR=" / ") AS ?symbols)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?cq, " | ", ?cql, " | ", ?cqd); separator=" / ") AS ?containsQuantity)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?sbq, " | ", ?sbql, " | ", ?sbqd, " | ", ?sbqc); separator=" / ") AS ?specializedBy)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?sq, " | ", ?sql, " | ", ?sqd, " | ", ?sqc); separator=" / ") AS ?specializes)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?abq, " | ", ?abql, " | ", ?abqd, " | ", ?abqc); separator=" / ") AS ?approximatedBy)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?aq, " | ", ?aql, " | ", ?aqd, " | ", ?aqc); separator=" / ") AS ?approximates)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?lbq, " | ", ?lbql, " | ", ?lbqd, " | ", ?lbqc); separator=" / ") AS ?linearizedBy)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?lq, " | ", ?lql, " | ", ?lqd, " | ", ?lqc); separator=" / ") AS ?linearizes)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?nbq, " | ", ?nbql, " | ", ?nbqd, " | ", ?nbqc); separator=" / ") AS ?nondimensionalizedBy)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?nq, " | ", ?nql, " | ", ?nqd, " | ", ?nqc); separator=" / ") AS ?nondimensionalizes)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?stq, " | ", ?stql, " | ", ?stqd, " | ", ?stqc); separator=" / ") AS ?similarTo)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)
                                                                      
                                                      WHERE {{
                                                   
                                                        VALUES ?id {{wd:{0}}}

                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672114 }}, "True", "False" ) AS ?isDynamic)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672115 }}, "True", "False" ) AS ?isStatic)

                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isDeterministic)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isStochastic)

                                                        BIND(EXISTS {{ ?id wdt:P31 wd:Q6482820 }} AS ?dimensionlessQuantity)
                                                        BIND(EXISTS {{ ?id wdt:P31 wd:Q6672113 }} AS ?dimensionlessQuantityKind)
                                                        BIND(IF(?dimensionlessQuantity || ?dimensionlessQuantityKind, "True", "False") AS ?dimensionless)
                                                        BIND(COALESCE(?dimensionless, "False") AS ?isDimensionless)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isDimensional)

                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672116 }}, "True", "False" ) AS ?isSpaceContinuous)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672117 }}, "True", "False" ) AS ?isSpaceDiscrete)

                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isTimeContinuous)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isTimeDiscrete)

                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672074 }}, "True", "False" ) AS ?isChemicalConstant)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672097 }}, "True", "False" ) AS ?isMathematicalConstant)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6534290 }}, "True", "False" ) AS ?isPhysicalConstant)

                                                        {{
                                                          ?id wdt:P31 wd:Q6534237.
                                                          BIND("Quantity" AS ?class)
                                                        }}
                                                        UNION
                                                        {{
                                                          ?id wdt:P31 wd:Q6534245.
                                                          BIND("QuantityKind" AS ?class)
                                                        }}

                                                        OPTIONAL {{
                                                                   ?id wdt:P1654 ?reference
                                                                 }}

                                                        OPTIONAL {{
                                                                     ?id wdt:P989 ?formula.
                                                                 }}
                                                        
                                                        OPTIONAL {{
                                                                     ?id p:P983 ?statement.
                                                                     ?statement ps:P983 ?symbol.
  
                                                                    OPTIONAL {{
                                                                               ?statement pq:P984 ?cqraw.
                                                                               BIND(REPLACE(STR(?cqraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?cq) 
                                                                               OPTIONAL {{
                                                                                           ?cqraw rdfs:label ?cqlraw.
                                                                                           FILTER (lang(?cqlraw) = 'en')
                                                                                        }}
                                                                               BIND(COALESCE(?cqlraw, "No Label Provided!") AS ?cql)
                                                                               OPTIONAL {{
                                                                                           ?cqraw schema:description ?cqdraw
                                                                                           FILTER (lang(?cqdraw) = 'en')
                                                                                        }}
                                                                               BIND(COALESCE(?cqdraw, "No Description Provided!") AS ?cqd)
                                                                             }}
                                                                 }}

                                                        OPTIONAL {{
                                                                   ?id wdt:P1684 ?sbqraw.
                                                                   BIND(replace( xsd:string(?sbqraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?sbq)

                                                                   {{
                                                                     ?sbqraw wdt:P31 wd:Q6534237.
                                                                     BIND("Quantity" AS ?sbqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?sbqraw wdt:P31 wd:Q6534245.
                                                                     BIND("QuantityKind" AS ?sbqc)
                                                                   }}

                                                                   OPTIONAL {{
                                                                              ?sbqraw rdfs:label ?sbqlraw.
                                                                              FILTER (lang(?sbqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?sbqlraw, "No Label Provided!") AS ?sbql)

                                                                  OPTIONAL {{
                                                                             ?sbqraw schema:description ?sbqdraw
                                                                             FILTER (lang(?sbqdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?sbqdraw, "No Description Provided!") AS ?sbqd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?sqraw wdt:P1684 ?id.
                                                                   BIND(replace( xsd:string(?sqraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?sq)

                                                                   {{
                                                                     ?sqraw wdt:P31 wd:Q6534237.
                                                                     BIND("Quantity" AS ?sqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?sqraw wdt:P31 wd:Q6534245.
                                                                     BIND("QuantityKind" AS ?sqc)
                                                                   }}

                                                                   OPTIONAL {{
                                                                              ?sqraw rdfs:label ?sqlraw.
                                                                              FILTER (lang(?sqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?sqlraw, "No Label Provided!") AS ?sql)

                                                                  OPTIONAL {{
                                                                             ?sqraw schema:description ?sqdraw
                                                                             FILTER (lang(?sqdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?sqdraw, "No Description Provided!") AS ?sqd)
                                                               }}

                                                      OPTIONAL {{
                                                                   ?id wdt:P1655 ?abqraw.
                                                                   BIND(replace( xsd:string(?abqraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?abq)

                                                                   {{
                                                                     ?abqraw wdt:P31 wd:Q6534237.
                                                                     BIND("Quantity" AS ?abqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?abqraw wdt:P31 wd:Q6534245.
                                                                     BIND("QuantityKind" AS ?abqc)
                                                                   }}

                                                                   OPTIONAL {{
                                                                              ?abqraw rdfs:label ?abqlraw.
                                                                              FILTER (lang(?abqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abqlraw, "No Label Provided!") AS ?abql)

                                                                  OPTIONAL {{
                                                                             ?abqraw schema:description ?abqdraw
                                                                             FILTER (lang(?abqdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?abqdraw, "No Description Provided!") AS ?abqd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?aqraw wdt:P1655 ?id.
                                                                   BIND(replace( xsd:string(?aqraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?aq)

                                                                   {{
                                                                     ?aqraw wdt:P31 wd:Q6534237.
                                                                     BIND("Quantity" AS ?aqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?aqraw wdt:P31 wd:Q6534245.
                                                                     BIND("QuantityKind" AS ?aqc)
                                                                   }}

                                                                   OPTIONAL {{
                                                                              ?aqraw rdfs:label ?aqlraw.
                                                                              FILTER (lang(?aqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?aqlraw, "No Label Provided!") AS ?aql)

                                                                  OPTIONAL {{
                                                                             ?aqraw schema:description ?aqdraw
                                                                             FILTER (lang(?aqdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?aqdraw, "No Description Provided!") AS ?aqd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1657 ?lbqraw.
                                                                   BIND(replace( xsd:string(?lbqraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?lbq)

                                                                   {{
                                                                     ?lbqraw wdt:P31 wd:Q6534237.
                                                                     BIND("Quantity" AS ?lbqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?lbqraw wdt:P31 wd:Q6534245.
                                                                     BIND("QuantityKind" AS ?lbqc)
                                                                   }}

                                                                   OPTIONAL {{
                                                                              ?lbqraw rdfs:label ?lbqlraw.
                                                                              FILTER (lang(?lbqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbqlraw, "No Label Provided!") AS ?lbql)

                                                                  OPTIONAL {{
                                                                             ?lbqraw schema:description ?lbqdraw
                                                                             FILTER (lang(?lbqdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?lbqdraw, "No Description Provided!") AS ?lbqd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?lqraw wdt:P1657 ?id.
                                                                   BIND(replace( xsd:string(?lqraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?lq)

                                                                   {{
                                                                     ?lqraw wdt:P31 wd:Q6534237.
                                                                     BIND("Quantity" AS ?lqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?lqraw wdt:P31 wd:Q6534245.
                                                                     BIND("QuantityKind" AS ?lqc)
                                                                   }}

                                                                   OPTIONAL {{
                                                                              ?lqraw rdfs:label ?lqlraw.
                                                                              FILTER (lang(?lqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lqlraw, "No Label Provided!") AS ?lql)

                                                                  OPTIONAL {{
                                                                             ?lqraw schema:description ?lqdraw
                                                                             FILTER (lang(?lqdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?lqdraw, "No Description Provided!") AS ?lqd)
                                                               }}

                                                      OPTIONAL {{
                                                                   ?id wdt:P1658 ?nbqraw.
                                                                   BIND(replace( xsd:string(?nbqraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?nbq)

                                                                   {{
                                                                     ?nbqraw wdt:P31 wd:Q6534237.
                                                                     BIND("Quantity" AS ?nbqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?nbqraw wdt:P31 wd:Q6534245.
                                                                     BIND("QuantityKind" AS ?nbqc)
                                                                   }}

                                                                   OPTIONAL {{
                                                                              ?nbqraw rdfs:label ?nbqlraw.
                                                                              FILTER (lang(?nbqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nbqlraw, "No Label Provided!") AS ?nbql)

                                                                  OPTIONAL {{
                                                                             ?nbqraw schema:description ?nbqdraw
                                                                             FILTER (lang(?nbqdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?nbqdraw, "No Description Provided!") AS ?nbqd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?nqraw wdt:P1658 ?id.
                                                                   BIND(replace( xsd:string(?nqraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?nq)

                                                                   {{
                                                                     ?nqraw wdt:P31 wd:Q6534237.
                                                                     BIND("Quantity" AS ?nqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?nqraw wdt:P31 wd:Q6534245.
                                                                     BIND("QuantityKind" AS ?nqc)
                                                                   }}

                                                                   OPTIONAL {{
                                                                              ?nqraw rdfs:label ?nqlraw.
                                                                              FILTER (lang(?nqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nqlraw, "No Label Provided!") AS ?nql)

                                                                  OPTIONAL {{
                                                                             ?nqraw schema:description ?nqdraw
                                                                             FILTER (lang(?nqdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?nqdraw, "No Description Provided!") AS ?nqd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?stqraw wdt: ?id.
                                                                   BIND(replace( xsd:string(?stqraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?stq)

                                                                   {{
                                                                     ?stqraw wdt:P31 wd:Q6534237.
                                                                     BIND("Quantity" AS ?stqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?stqraw wdt:P31 wd:Q6534245.
                                                                     BIND("QuantityKind" AS ?stqc)
                                                                   }}

                                                                   OPTIONAL {{
                                                                              ?stqraw rdfs:label ?stqlraw.
                                                                              FILTER (lang(?stqlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?stqlraw, "No Label Provided!") AS ?stql)

                                                                  OPTIONAL {{
                                                                             ?stqraw schema:description ?stqdraw
                                                                             FILTER (lang(?stqdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?stqdraw, "No Description Provided!") AS ?stqd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P286 ?pubraw.
                                                                   BIND(replace( xsd:string(?pubraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?pub)

                                                                   OPTIONAL {{
                                                                              ?pubraw rdfs:label ?publraw.
                                                                              FILTER (lang(?publraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)

                                                                  OPTIONAL {{
                                                                             ?pubraw schema:description ?pubdraw
                                                                             FILTER (lang(?pubdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                               }}

                                                      }}
                                                      GROUP BY ?isLinear ?isNotLinear ?isDynamic ?isStatic ?isDeterministic ?isStochastic ?isDimensionless 
                                                               ?isDimensional ?isSpaceContinuous ?isSpaceDiscrete ?isTimeContinuous ?isTimeDiscrete
                                                               ?isChemicalConstant ?isMathematicalConstant ?isPhysicalConstant ?class ?reference''',

              'mathematicalFormulationInformation': '''SELECT DISTINCT ?isLinear ?isNotLinear
                                                                               ?isDynamic ?isStatic
                                                                               ?isDeterministic ?isStochastic
                                                                               ?isDimensionless ?isDimensional
                                                                               ?isTimeContinuous ?isTimeDiscrete
                                                                               ?isSpaceContinuous ?isSpaceDiscrete
                                                                               (GROUP_CONCAT(DISTINCT(?formula); SEPARATOR=" / ") AS ?formulas)
                                                                               (GROUP_CONCAT(DISTINCT(?symbol); SEPARATOR=" / ") AS ?symbols)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?cq, " | ", ?cql, " | ", ?cqd); separator=" / ") AS ?containsQuantity)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?ass, " | ", ?assl, " | ", ?assd); separator=" / ") AS ?assumes)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?conf, " | ", ?confl, " | ", ?confd, " | ", ?confq); separator=" / ") AS ?containsFormulation)    
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?sbf, " | ", ?sbfl, " | ", ?sbfd, " | ", ?sbfq); separator=" / ") AS ?specializedBy)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?sf, " | ", ?sfl, " | ", ?sfd, " | ", ?sfq); separator=" / ") AS ?specializes)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?abf, " | ", ?abfl, " | ", ?abfd); separator=" / ") AS ?approximatedBy)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?af, " | ", ?afl, " | ", ?afd); separator=" / ") AS ?approximates)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?nbf, " | ", ?nbfl, " | ", ?nbfd); separator=" / ") AS ?nondimensionalizedBy)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?nf, " | ", ?nfl, " | ", ?nfd); separator=" / ") AS ?nondimensionalizes)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?dbf, " | ", ?dbfl, " | ", ?dbfd); separator=" / ") AS ?discretizedBy)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?df, " | ", ?dfl, " | ", ?dfd); separator=" / ") AS ?discretizes)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lbf, " | ", ?lbfl, " | ", ?lbfd); separator=" / ") AS ?linearizedBy)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?lf, " | ", ?lfl, " | ", ?lfd); separator=" / ") AS ?linearizes)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?stf, " | ", ?stfl, " | ", ?stfd); separator=" / ") AS ?similarTo)
                                                                               (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publications)
                                                                               
                                                               WHERE {{ 
                                                                       VALUES ?id {{wd:{0}}}

                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672107 }}, "True", "False" ) AS ?isLinear)
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672086 }}, "True", "False" ) AS ?isNotLinear)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672081 }}, "True", "False" ) AS ?isDynamic)
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672083 }}, "True", "False" ) AS ?isStatic)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672075 }}, "True", "False" ) AS ?isDeterministic)
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672077 }}, "True", "False" ) AS ?isStochastic)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672079 }}, "True", "False" ) AS ?isDimensionless)
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isDimensional)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672088 }}, "True", "False" ) AS ?isSpaceContinuous)
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672092 }}, "True", "False" ) AS ?isSpaceDiscrete)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672090 }}, "True", "False" ) AS ?isTimeContinuous)
                                                                       BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672094 }}, "True", "False" ) AS ?isTimeDiscrete)

                                                                       OPTIONAL {{
                                                                                    ?id wdt:P989 ?formula.
                                                                                }}

                                                                       OPTIONAL {{
                                                                                    ?id p:P983 ?statement.
                                                                                    ?statement ps:P983 ?symbol.
                 
                                                                                   OPTIONAL {{
                                                                                              ?statement pq:P984 ?cqraw.
                                                                                              BIND(REPLACE(STR(?cqraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?cq)

                                                                                              OPTIONAL {{
                                                                                                          ?cqraw rdfs:label ?cqlraw.
                                                                                                          FILTER (lang(?cqlraw) = 'en')
                                                                                                       }}
                                                                                              BIND(COALESCE(?cqlraw, "No Label Provided!") AS ?cql)

                                                                                              OPTIONAL {{
                                                                                                          ?cqraw schema:description ?cqdraw
                                                                                                          FILTER (lang(?cqdraw) = 'en')
                                                                                                       }}
                                                                                              BIND(COALESCE(?cqdraw, "No Description Provided!") AS ?cqd)
                                                                                            }}
                                                                                }}
                                                                      
                                                                       OPTIONAL {{
                                                                                   ?id wdt:P1674 ?assraw.
                                                                                   BIND(replace( xsd:string(?assraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?ass)
                
                                                                                   ?assraw wdt:P31 wd:Q6481152.
                
                                                                                   OPTIONAL {{
                                                                                              ?assraw rdfs:label ?asslraw.
                                                                                              FILTER (lang(?asslraw) = 'en')
                                                                                           }}
                
                                                                                  BIND(COALESCE(?asslraw, "No Label Provided!") AS ?assl)
                
                                                                                  OPTIONAL {{
                                                                                             ?assraw schema:description ?assdraw
                                                                                             FILTER (lang(?assdraw) = 'en')
                                                                                           }}
                                                                                  BIND(COALESCE(?assdraw, "No Description Provided!") AS ?assd)
                                                                               }}

                                                                       OPTIONAL {{
                                                                                      ?id p:P1560 ?statement2.
                                                                                      ?statement2 ps:P1560 ?confraw.
                   
                                                                                      ?confraw wdt:P31 wd:Q6481152.
                   
                                                                                      BIND(replace( xsd:string(?confraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?conf)
                   
                                                                                      OPTIONAL {{
                                                                                                 ?confraw rdfs:label ?conflraw.
                                                                                                 FILTER (lang(?conflraw) = 'en')
                                                                                              }}
                   
                                                                                     BIND(COALESCE(?conflraw, "No Label Provided!") AS ?confl)
                   
                                                                                     OPTIONAL {{
                                                                                                ?confraw schema:description ?confdraw
                                                                                                FILTER (lang(?confdraw) = 'en')
                                                                                              }}
                                                                                     BIND(COALESCE(?confdraw, "No Description Provided!") AS ?confd)
                   
                                                                                     OPTIONAL {{
                                                                                                ?statement2 pq:P560 ?quaraw.
                                                                                                BIND(REPLACE(STR(?quaraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua)
                                                                                              }}
                                                                                     BIND(COALESCE(?qua, "") AS ?confq)
                                                                                  }}

                                                                       OPTIONAL {{   
                                                    
                                                        OPTIONAL {{
                                                          
                                                          {{
                                                            SELECT ?statement3 (GROUP_CONCAT(DISTINCT ?sbfq_entry; separator=" <|> ") AS ?sbfq)
                                                            WHERE {{
                                                     
                                                              ?id p:P1684 ?statement3.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement3 pq:P1674 ?qua3raw.
                                                                 BIND(REPLACE(STR(?qua3raw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua3)
 
                                                                 OPTIONAL {{
                                                                   ?qua3raw rdfs:label ?sbfqlraw.
                                                                   FILTER (lang(?sbfqlraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?sbfqlraw, "No Label Provided!") AS ?sbfql)
 
                                                                 OPTIONAL {{
                                                                   ?qua3raw schema:description ?sbfqdraw.
                                                                   FILTER (lang(?sbfqdraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?sbfqdraw, "No Description Provided!") AS ?sbfqd)
                                                               
                                                              }}
                                                              BIND(COALESCE(?qua3, "") AS ?qua3_final)
                                                              BIND(COALESCE(?sbfql, "") AS ?sbfql_final)
                                                              BIND(COALESCE(?sbfqd, "") AS ?sbfqd_final)
                                                              
                                                              BIND(IF((?qua3_final = "" && ?sbfql_final = "" && ?sbfqd_final = ""),"",CONCAT(?qua3_final, " | ", ?sbfql_final, " | ", ?sbfqd_final)) AS ?sbfq_entry)
                                                                 
                                                            }}
                                                            GROUP BY ?statement3
                                                          }}
                                                          }}
                                                        
                                                          ?id p:P1684 ?statement3.
                                                          ?statement3 ps:P1684 ?sbfraw.
                                                          
                                                          BIND(REPLACE(STR(?sbfraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?sbf)
                                                        
                                                          OPTIONAL {{
                                                            ?sbfraw rdfs:label ?sbflraw
                                                            FILTER (lang(?sbflraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?sbflraw, "No Label Provided!") AS ?sbfl)
                                                        
                                                          OPTIONAL {{
                                                            ?sbfraw schema:description ?sbfdraw
                                                            FILTER (lang(?sbfdraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?sbfdraw, "No Description Provided!") AS ?sbfd)
                                                  
                                                          }}

                                                    OPTIONAL {{   
                                                    
                                                        OPTIONAL {{
                                                          
                                                          {{
                                                            SELECT ?statement4 (GROUP_CONCAT(DISTINCT ?sfq_entry; separator=" <|> ") AS ?sfq)
                                                            WHERE {{
                                                     
                                                              ?sfraw p:P1684 ?statement4.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement4 pq:P1674 ?qua4raw.
                                                                 BIND(REPLACE(STR(?qua4raw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua4)
 
                                                                 OPTIONAL {{
                                                                   ?qua4raw rdfs:label ?sfqlraw.
                                                                   FILTER (lang(?sfqlraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?sfqlraw, "No Label Provided!") AS ?sfql)
 
                                                                 OPTIONAL {{
                                                                   ?qua4raw schema:description ?sfqdraw.
                                                                   FILTER (lang(?sfqdraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?sfqdraw, "No Description Provided!") AS ?sfqd)
                                                               
                                                              }}
                                                              BIND(COALESCE(?qua4, "") AS ?qua4_final)
                                                              BIND(COALESCE(?sfql, "") AS ?sfql_final)
                                                              BIND(COALESCE(?sfqd, "") AS ?sfqd_final)
                                                              
                                                              BIND(IF((?qua4_final = "" && ?sfql_final = "" && ?sfqd_final = ""),"",CONCAT(?qua4_final, " | ", ?sfql_final, " | ", ?sfqd_final)) AS ?sfq_entry)
                                                                 
                                                            }}
                                                            GROUP BY ?statement4
                                                          }}
                                                          }}
                                                        
                                                          ?sfraw p:P1684 ?statement4.
                                                          ?statement4 ps:P1684 ?id.
                                                          
                                                          BIND(REPLACE(STR(?sfraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?sf)
                                                        
                                                          OPTIONAL {{
                                                            ?sfraw rdfs:label ?sflraw
                                                            FILTER (lang(?sflraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?sflraw, "No Label Provided!") AS ?sfl)
                                                        
                                                          OPTIONAL {{
                                                            ?sfraw schema:description ?sfdraw
                                                            FILTER (lang(?sfdraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?sfdraw, "No Description Provided!") AS ?sfd)
                                                  
                                                          }}
                                                    
                                                    OPTIONAL {{
                                                                   ?id wdt:P1655 ?abfraw.
                                                                   BIND(replace( xsd:string(?abfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?abf)

                                                                   OPTIONAL {{
                                                                              ?abfraw rdfs:label ?abflraw.
                                                                              FILTER (lang(?abflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abflraw, "No Label Provided!") AS ?abfl)

                                                                  OPTIONAL {{
                                                                             ?abfraw schema:description ?abfdraw
                                                                             FILTER (lang(?abfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?abfdraw, "No Description Provided!") AS ?abfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?afraw wdt:P1655 ?id.
                                                                   BIND(replace( xsd:string(?afraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?af)

                                                                   OPTIONAL {{
                                                                              ?afraw rdfs:label ?aflraw.
                                                                              FILTER (lang(?aflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?aflraw, "No Label Provided!") AS ?afl)

                                                                  OPTIONAL {{
                                                                             ?afraw schema:description ?afdraw
                                                                             FILTER (lang(?afdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?afdraw, "No Description Provided!") AS ?afd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1658 ?nbfraw.
                                                                   BIND(replace( xsd:string(?nbfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?nbf)

                                                                   ?nbraw wdt:P31 wd:Q68663.

                                                                   OPTIONAL {{
                                                                              ?nbfraw rdfs:label ?nbflraw.
                                                                              FILTER (lang(?nbflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nbflraw, "No Label Provided!") AS ?nbfl)

                                                                  OPTIONAL {{
                                                                             ?nbfraw schema:description ?nbfdraw
                                                                             FILTER (lang(?nbfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?nbfdraw, "No Description Provided!") AS ?nbfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?nfraw wdt:P1658 ?id.
                                                                   BIND(replace( xsd:string(?nfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?nf)

                                                                   ?nfraw wdt:P31 wd:Q68663.

                                                                   OPTIONAL {{
                                                                              ?nfraw rdfs:label ?nflraw.
                                                                              FILTER (lang(?nflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?nflraw, "No Label Provided!") AS ?nfl)

                                                                  OPTIONAL {{
                                                                             ?nfraw schema:description ?nfdraw
                                                                             FILTER (lang(?nfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?nfdraw, "No Description Provided!") AS ?nfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1656 ?dbfraw.
                                                                   BIND(replace( xsd:string(?dbfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?dbf)

                                                                   OPTIONAL {{
                                                                              ?dbfraw rdfs:label ?dbflraw.
                                                                              FILTER (lang(?dbflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dbflraw, "No Label Provided!") AS ?dbfl)

                                                                  OPTIONAL {{
                                                                             ?dbfraw schema:description ?dbfdraw
                                                                             FILTER (lang(?dbfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?dbfdraw, "No Description Provided!") AS ?dbfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?dfraw wdt:P1656 ?id.
                                                                   BIND(replace( xsd:string(?dfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?df)

                                                                   OPTIONAL {{
                                                                              ?dfraw rdfs:label ?dflraw.
                                                                              FILTER (lang(?dflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dflraw, "No Label Provided!") AS ?dfl)

                                                                  OPTIONAL {{
                                                                             ?dfraw schema:description ?dfdraw
                                                                             FILTER (lang(?dfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?dfdraw, "No Description Provided!") AS ?dfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1657 ?lbfraw.
                                                                   BIND(replace( xsd:string(?lbfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?lbf)

                                                                   OPTIONAL {{
                                                                              ?lbfraw rdfs:label ?lbflraw.
                                                                              FILTER (lang(?lbflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbflraw, "No Label Provided!") AS ?lbfl)

                                                                  OPTIONAL {{
                                                                             ?lbfraw schema:description ?lbfdraw
                                                                             FILTER (lang(?lbfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?lbfdraw, "No Description Provided!") AS ?lbfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?lfraw wdt:P1657 ?id.
                                                                   BIND(replace( xsd:string(?lfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?lf)

                                                                   OPTIONAL {{
                                                                              ?lfraw rdfs:label ?lflraw.
                                                                              FILTER (lang(?lflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lflraw, "No Label Provided!") AS ?lfl)

                                                                  OPTIONAL {{
                                                                             ?lfraw schema:description ?lfdraw
                                                                             FILTER (lang(?lfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?lfdraw, "No Description Provided!") AS ?lfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?stfraw wdt: ?id.
                                                                   BIND(replace( xsd:string(?stfraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?stf)

                                                                   OPTIONAL {{
                                                                              ?stfraw rdfs:label ?stflraw.
                                                                              FILTER (lang(?stflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?stflraw, "No Label Provided!") AS ?stfl)

                                                                  OPTIONAL {{
                                                                             ?stfraw schema:description ?stfdraw
                                                                             FILTER (lang(?stfdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?stfdraw, "No Description Provided!") AS ?stfd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P286 ?pubraw.
                                                                   BIND(replace( xsd:string(?pubraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?pub)

                                                                   OPTIONAL {{
                                                                              ?pubraw rdfs:label ?publraw.
                                                                              FILTER (lang(?publraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)

                                                                  OPTIONAL {{
                                                                             ?pubraw schema:description ?pubdraw
                                                                             FILTER (lang(?pubdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                               }}

                                                                     }}
                                                                     GROUP BY ?isLinear ?isNotLinear ?isDynamic ?isStatic ?isDeterministic ?isStochastic ?isDimensionless 
                                                                              ?isDimensional ?isSpaceContinuous ?isSpaceDiscrete ?isTimeContinuous ?isTimeDiscrete''',
                                                                                             
                              'taskInformation': '''SELECT DISTINCT ?isLinear ?isNotLinear
                                                                    ?isSpaceContinuous ?isSpaceDiscrete
                                                                    ?isTimeContinuous ?isTimeDiscrete
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?ass, " | ", ?assl, " | ", ?assd); separator=" / ") AS ?assumes)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?conf, " | ", ?confl, " | ", ?confd, " | ", ?confq); separator=" / ") AS ?containsFormulation)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?quan, " | ", ?quanl, " | ", ?quand, " | ", ?quanq); separator=" / ") AS ?containsQuantity)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?sbt, " | ", ?sbtl, " | ", ?sbtd, " | ", ?sbtq); separator=" / ") AS ?specializedBy)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?st, " | ", ?stl, " | ", ?std, " | ", ?stq); separator=" / ") AS ?specializes)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?abt, " | ", ?abtl, " | ", ?abtd); separator=" / ") AS ?approximatedBy)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?at, " | ", ?atl, " | ", ?atd); separator=" / ") AS ?approximates)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?cont, " | ", ?contl, " | ", ?contd); separator=" / ") AS ?containsModel)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?conit, " | ", ?conitl, " | ", ?conitd); separator=" / ") AS ?containedInModel)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?dbt, " | ", ?dbtl, " | ", ?dbtd); separator=" / ") AS ?discretizedBy)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?dt, " | ", ?dtl, " | ", ?dtd); separator=" / ") AS ?discretizes)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?lbt, " | ", ?lbtl, " | ", ?lbtd); separator=" / ") AS ?linearizedBy)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?lt, " | ", ?ltl, " | ", ?ltd); separator=" / ") AS ?linearizes)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?stt, " | ", ?sttl, " | ", ?sttd); separator=" / ") AS ?similarTo)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publications)
                        
                                                    WHERE {{

                                                        VALUES ?id {{wd:{0}}}

                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672085 }}, "True", "False" ) AS ?isLinear)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd:Q6672087 }}, "True", "False" ) AS ?isNotLinear)

                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isSpaceContinuous)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isSpaceDiscrete)
                                                      
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isTimeContinuous)
                                                        BIND(IF(EXISTS {{ ?id wdt:P31 wd: }}, "True", "False" ) AS ?isTimeDiscrete)

                                                        OPTIONAL {{
                                                                   ?id wdt:P1674 ?assraw.
                                                                   BIND(replace( xsd:string(?assraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?ass)

                                                                   ?assraw wdt:P31 wd:Q6481152.

                                                                   OPTIONAL {{
                                                                              ?assraw rdfs:label ?asslraw.
                                                                              FILTER (lang(?asslraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?asslraw, "No Label Provided!") AS ?assl)


                                                                  OPTIONAL {{
                                                                             ?assraw schema:description ?assdraw
                                                                             FILTER (lang(?assdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?assdraw, "No Description Provided!") AS ?assd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id p:P1560 ?statement.
                                                                   ?statement ps:P1560 ?confraw.

                                                                   ?confraw wdt:P31 wd:Q6481152.

                                                                   BIND(replace( xsd:string(?confraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?conf)

                                                                   OPTIONAL {{
                                                                              ?confraw rdfs:label ?conflraw.
                                                                              FILTER (lang(?conflraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?conflraw, "No Label Provided!") AS ?confl)

                                                                  OPTIONAL {{
                                                                             ?confraw schema:description ?confdraw
                                                                             FILTER (lang(?confdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?confdraw, "No Description Provided!") AS ?confd)

                                                                  OPTIONAL {{
                                                                             ?statement pq:P560 ?quaraw.
                                                                             BIND(REPLACE(STR(?quaraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua)
                                                                           }}
                                                                  BIND(COALESCE(?qua, "") AS ?confq)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id p:P1560 ?statement2.
                                                                   ?statement2 ps:P1560 ?quanraw.

                                                                   {{
                                                                      ?quanraw wdt:P31 wd:Q6534237.
                                                                   }}
                                                                      UNION
                                                                   {{
                                                                      ?quanraw wdt:P31 wd:Q6534245.
                                                                   }}

                                                                   BIND(replace( xsd:string(?quanraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?quan)

                                                                   OPTIONAL {{
                                                                              ?quanraw rdfs:label ?quanlraw.
                                                                              FILTER (lang(?quanlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?quanlraw, "No Label Provided!") AS ?quanl)

                                                                  OPTIONAL {{
                                                                             ?quanraw schema:description ?quandraw
                                                                             FILTER (lang(?quandraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?quandraw, "No Description Provided!") AS ?quand)

                                                                  OPTIONAL {{
                                                                             ?statement2 pq:P560 ?qua2raw.
                                                                             BIND(REPLACE(STR(?qua2raw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua2)
                                                                           }}
                                                                  BIND(COALESCE(?qua2, "") AS ?quanq)
                                                               }}

                                                    OPTIONAL {{   
                                                    
                                                        OPTIONAL {{
                                                          
                                                          {{
                                                            SELECT ?statement3 (GROUP_CONCAT(DISTINCT ?sbtq_entry; separator=" <|> ") AS ?sbtq)
                                                            WHERE {{
                                                     
                                                              ?id p:P1684 ?statement3.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement3 pq:P1674 ?qua3raw.
                                                                 BIND(REPLACE(STR(?qua3raw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua3)
 
                                                                 OPTIONAL {{
                                                                   ?qua3raw rdfs:label ?sbtqlraw.
                                                                   FILTER (lang(?sbtqlraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?sbtqlraw, "No Label Provided!") AS ?sbtql)
 
                                                                 OPTIONAL {{
                                                                   ?qua3raw schema:description ?sbtqdraw.
                                                                   FILTER (lang(?sbtqdraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?sbtqdraw, "No Description Provided!") AS ?sbtqd)
                                                               
                                                              }}
                                                              BIND(COALESCE(?qua3, "") AS ?qua3_final)
                                                              BIND(COALESCE(?sbtql, "") AS ?sbtql_final)
                                                              BIND(COALESCE(?sbtqd, "") AS ?sbtqd_final)
                                                              
                                                              BIND(IF((?qua3_final = "" && ?sbtql_final = "" && ?sbtqd_final = ""),"",CONCAT(?qua3_final, " | ", ?sbtql_final, " | ", ?sbtqd_final)) AS ?sbtq_entry)
                                                                 
                                                            }}
                                                            GROUP BY ?statement3
                                                          }}
                                                          }}
                                                        
                                                          ?id p:P1684 ?statement3.
                                                          ?statement3 ps:P1684 ?sbtraw.
                                                          
                                                          BIND(REPLACE(STR(?sbtraw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?sbt)
                                                        
                                                          OPTIONAL {{
                                                            ?sbtraw rdfs:label ?sbtlraw
                                                            FILTER (lang(?sbtlraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?sbtlraw, "No Label Provided!") AS ?sbtl)
                                                        
                                                          OPTIONAL {{
                                                            ?sbtraw schema:description ?sbtdraw
                                                            FILTER (lang(?sbtdraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?sbtdraw, "No Description Provided!") AS ?sbtd)
                                                  
                                                          }}

                                                    OPTIONAL {{   
                                                    
                                                        OPTIONAL {{
                                                          
                                                          {{
                                                            SELECT ?statement4 (GROUP_CONCAT(DISTINCT ?stq_entry; separator=" <|> ") AS ?stq)
                                                            WHERE {{
                                                     
                                                              ?straw p:P1684 ?statement4.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement4 pq:P1674 ?qua4raw.
                                                                 BIND(REPLACE(STR(?qua4raw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?qua4)
 
                                                                 OPTIONAL {{
                                                                   ?qua4raw rdfs:label ?stqlraw.
                                                                   FILTER (lang(?stqlraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?stqlraw, "No Label Provided!") AS ?stql)
 
                                                                 OPTIONAL {{
                                                                   ?qua4raw schema:description ?stqdraw.
                                                                   FILTER (lang(?stqdraw) = "en")
                                                                 }}
                                                                 BIND(COALESCE(?stqdraw, "No Description Provided!") AS ?stqd)
                                                               
                                                              }}
                                                              BIND(COALESCE(?qua4, "") AS ?qua4_final)
                                                              BIND(COALESCE(?stql, "") AS ?stql_final)
                                                              BIND(COALESCE(?stqd, "") AS ?stqd_final)
                                                              
                                                              BIND(IF((?qua4_final = "" && ?stql_final = "" && ?stqd_final = ""),"",CONCAT(?qua4_final, " | ", ?stql_final, " | ", ?stqd_final)) AS ?stq_entry)
                                                                 
                                                            }}
                                                            GROUP BY ?statement4
                                                          }}
                                                          }}
                                                        
                                                          ?straw p:P1684 ?statement4.
                                                          ?statement4 ps:P1684 ?id.
                                                          
                                                          BIND(REPLACE(STR(?straw), "https://portal.mardi4nfdi.de/entity/", "mardi:") AS ?st)
                                                        
                                                          OPTIONAL {{
                                                            ?straw rdfs:label ?stlraw
                                                            FILTER (lang(?stlraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?stlraw, "No Label Provided!") AS ?stl)
                                                        
                                                          OPTIONAL {{
                                                            ?straw schema:description ?stdraw
                                                            FILTER (lang(?stdraw) = 'en')
                                                          }}
                                                          BIND(COALESCE(?stdraw, "No Description Provided!") AS ?std)
                                                  
                                                          }}
                                                    
                                                    OPTIONAL {{
                                                                   ?id wdt:P1655 ?abtraw.
                                                                   BIND(replace( xsd:string(?abtraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?abt)

                                                                   OPTIONAL {{
                                                                              ?abtraw rdfs:label ?abtlraw.
                                                                              FILTER (lang(?abtlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?abtlraw, "No Label Provided!") AS ?abtl)

                                                                  OPTIONAL {{
                                                                             ?abtraw schema:description ?abtdraw
                                                                             FILTER (lang(?abtdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?abtdraw, "No Description Provided!") AS ?abtd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?atraw wdt:P1655 ?id.
                                                                   BIND(replace( xsd:string(?atraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?at)

                                                                   OPTIONAL {{
                                                                              ?atraw rdfs:label ?atlraw.
                                                                              FILTER (lang(?atlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?atlraw, "No Label Provided!") AS ?atl)

                                                                  OPTIONAL {{
                                                                             ?atraw schema:description ?atdraw
                                                                             FILTER (lang(?atdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?atdraw, "No Description Provided!") AS ?atd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1560 ?contraw.
                                                                   BIND(replace( xsd:string(?contraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?cont)

                                                                   ?contraw wdt:P31 wd:Q68663.

                                                                   OPTIONAL {{
                                                                              ?contraw rdfs:label ?contlraw.
                                                                              FILTER (lang(?contlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?contlraw, "No Label Provided!") AS ?contl)

                                                                  OPTIONAL {{
                                                                             ?contraw schema:description ?contdraw
                                                                             FILTER (lang(?contdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?contdraw, "No Description Provided!") AS ?contd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?conitraw wdt:P1560 ?id.
                                                                   BIND(replace( xsd:string(?conitraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?conit)

                                                                   ?conitraw wdt:P31 wd:Q68663.

                                                                   OPTIONAL {{
                                                                              ?conitraw rdfs:label ?conitlraw.
                                                                              FILTER (lang(?conitlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?conitlraw, "No Label Provided!") AS ?conitl)

                                                                  OPTIONAL {{
                                                                             ?conitraw schema:description ?conitdraw
                                                                             FILTER (lang(?conitdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?conitdraw, "No Description Provided!") AS ?conitd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1656 ?dbtraw.
                                                                   BIND(replace( xsd:string(?dbtraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?dbt)

                                                                   OPTIONAL {{
                                                                              ?dbtraw rdfs:label ?dbtlraw.
                                                                              FILTER (lang(?dbtlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dbtlraw, "No Label Provided!") AS ?dbtl)

                                                                  OPTIONAL {{
                                                                             ?dbtraw schema:description ?dbtdraw
                                                                             FILTER (lang(?dbtdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?dbtdraw, "No Description Provided!") AS ?dbtd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?dtraw wdt:P1656 ?id.
                                                                   BIND(replace( xsd:string(?dtraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?dt)

                                                                   OPTIONAL {{
                                                                              ?dtraw rdfs:label ?dtlraw.
                                                                              FILTER (lang(?dtlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?dtlraw, "No Label Provided!") AS ?dtl)

                                                                  OPTIONAL {{
                                                                             ?dtraw schema:description ?dtdraw
                                                                             FILTER (lang(?dtdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?dtdraw, "No Description Provided!") AS ?dtd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:P1657 ?lbtraw.
                                                                   BIND(replace( xsd:string(?lbtraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?lbt)

                                                                   OPTIONAL {{
                                                                              ?lbtraw rdfs:label ?lbtlraw.
                                                                              FILTER (lang(?lbtlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?lbtlraw, "No Label Provided!") AS ?lbtl)

                                                                  OPTIONAL {{
                                                                             ?lbtraw schema:description ?lbtdraw
                                                                             FILTER (lang(?lbtdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?lbtdraw, "No Description Provided!") AS ?lbtd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?ltraw wdt:P1657 ?id.
                                                                   BIND(replace( xsd:string(?ltraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?lt)

                                                                   OPTIONAL {{
                                                                              ?ltraw rdfs:label ?ltlraw.
                                                                              FILTER (lang(?ltlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?ltlraw, "No Label Provided!") AS ?ltl)

                                                                  OPTIONAL {{
                                                                             ?ltraw schema:description ?ltdraw
                                                                             FILTER (lang(?ltdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?ltdraw, "No Description Provided!") AS ?ltd)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?sttraw wdt: ?id.
                                                                   BIND(replace( xsd:string(?sttraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?stt)

                                                                   OPTIONAL {{
                                                                              ?sttraw rdfs:label ?sttlraw.
                                                                              FILTER (lang(?sttlraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?sttlraw, "No Label Provided!") AS ?sttl)

                                                                  OPTIONAL {{
                                                                             ?sttraw schema:description ?sttdraw
                                                                             FILTER (lang(?sttdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?sttdraw, "No Description Provided!") AS ?sttd)
                                                               }}
                                                      
                                                    OPTIONAL {{
                                                                   ?id wdt:P286 ?pubraw.
                                                                   BIND(replace( xsd:string(?pubraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?pub)

                                                                   OPTIONAL {{
                                                                              ?pubraw rdfs:label ?publraw.
                                                                              FILTER (lang(?publraw) = 'en')
                                                                           }}

                                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)

                                                                  OPTIONAL {{
                                                                             ?pubraw schema:description ?pubdraw
                                                                             FILTER (lang(?pubdraw) = 'en')
                                                                           }}
                                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                               }}

                                                        }}
                                                        GROUP BY ?isLinear ?isNotLinear''',        
                                                      }