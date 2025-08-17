queryHandler = {
    
    'researchFieldInformation': '''SELECT DISTINCT ?descriptionLong
                                                   (GROUP_CONCAT(DISTINCT CONCAT(?sbrf, " | ", ?sbrfl, " | ", ?sbrfd); separator=" / ") AS ?specializedBy)
                                                   (GROUP_CONCAT(DISTINCT CONCAT(?srf, " | ", ?srfl, " | ", ?srfd); separator=" / ") AS ?specializes)
                                                   (GROUP_CONCAT(DISTINCT CONCAT(?strf, " | ", ?strfl, " | ", ?strfd); separator=" / ") AS ?similarTo)
                                                   (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)

                                     WHERE {{
                                                   
                                                    VALUES ?id {{wd:{0}}}

                                                    OPTIONAL {{ ?id wdt:{description} ?descriptionLong }}

                                                    OPTIONAL {{
                                                                   ?id wdt:{specialized by} ?sbrfraw.
                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?sbrfraw), STR(wd:))) AS ?sbrf)
                                                                   
                                                                   ?sbrfraw wdt:{instance of} wd:{academic discipline}.
                                                                   
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
                                                                   ?srfraw wdt:{specialized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?srfraw), STR(wd:))) AS ?srf)
                                                                   
                                                                   ?srfraw wdt:{instance of} wd:{academic discipline}.
                                                                   
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
                                                                   ?id wdt:{similar to} ?strfraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?strfraw), STR(wd:))) AS ?strf)
                                                                   
                                                                   ?strfraw wdt:{instance of} wd:{academic discipline}.
                                                                   
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
                                                                  ?id p:{described by source} ?statement .
                                                                  ?statement ps:{described by source} ?pubraw .
                                                                  ?statement pq:{object has role} ?role .
                                                                  VALUES ?role {{ wd:{documentation} wd:{invention} wd:{review} wd:{study} wd:{use} }}

                                                                  BIND(CONCAT("mardi:", STRAFTER(STR(?pubraw), STR(wd:))) AS ?pub)

                                                                  OPTIONAL {{
                                                                    ?pubraw rdfs:label ?publraw .
                                                                    FILTER (lang(?publraw) = 'en')
                                                                  }}
                                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)

                                                                  OPTIONAL {{
                                                                    ?pubraw schema:description ?pubdraw .
                                                                    FILTER (lang(?pubdraw) = 'en')
                                                                  }}
                                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                               }}

                                          }} 
                                          GROUP BY ?descriptionLong''',

    'researchProblemInformation': '''SELECT DISTINCT ?descriptionLong
                                                     (GROUP_CONCAT(DISTINCT CONCAT(?rf, " | ", ?rfl, " | ", ?rfd); separator=" / ") AS ?containedInField)
                                                     (GROUP_CONCAT(DISTINCT CONCAT(?sbrp, " | ", ?sbrpl, " | ", ?sbrpd); separator=" / ") AS ?specializedBy)
                                                     (GROUP_CONCAT(DISTINCT CONCAT(?srp, " | ", ?srpl, " | ", ?srpd); separator=" / ") AS ?specializes)
                                                     (GROUP_CONCAT(DISTINCT CONCAT(?strp, " | ", ?strpl, " | ", ?strpd); separator=" / ") AS ?similarTo)
                                                     (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)

                                     WHERE {{
                                                   
                                                    VALUES ?id {{wd:{0}}}

                                                    OPTIONAL {{ ?id wdt:{description} ?descriptionLong }}
                                                   
                                                    OPTIONAL {{
                                                                   ?rfraw wdt:{contains} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?rfraw), STR(wd:))) AS ?rf)
                                                                   
                                                                   ?rfraw wdt:{instance of} wd:{academic discipline}.

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
                                                                   ?id wdt:{specialized by} ?sbrpraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?sbrpraw), STR(wd:))) AS ?sbrp)
                                                                   
                                                                   ?sbrpraw wdt:{instance of} wd:{research problem}.
                                                                   
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
                                                                   ?srpraw wdt:{specialized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?srpraw), STR(wd:))) AS ?srp)
                                                                   
                                                                   ?srpraw wdt:{instance of} wd:{research problem}.
                                                                   
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
                                                                   ?id wdt: ?strpraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?strpraw), STR(wd:))) AS ?strp)
                                                                   
                                                                   ?strpraw wdt:{instance of} wd:{research problem}.
                                                                   
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
                                                                   ?id wdt:{described by source} ?pubraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?pubraw), STR(wd:))) AS ?pub)
                                                                   
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
                                          GROUP BY ?descriptionLong''',

    'mathematicalModelInformation': '''SELECT DISTINCT ?descriptionLong
                                                       ?isLinear ?isNotLinear
                                                       ?isDynamic ?isStatic
                                                       ?isDeterministic ?isStochastic
                                                       ?isDimensionless ?isDimensional
                                                       ?isSpaceContinuous ?isSpaceDiscrete
                                                       ?isTimeContinuous ?isTimeDiscrete
                                                       (GROUP_CONCAT(DISTINCT CONCAT(?rp, " | ", ?rpl, " | ", ?rpd); separator=" / ") AS ?models)
                                                       (GROUP_CONCAT(DISTINCT CONCAT(?ass, " | ", ?assl, " | ", ?assd); separator=" / ") AS ?assumes)
                                                       (GROUP_CONCAT(DISTINCT CONCAT(?conf, " | ", ?confl, " | ", ?confd, " | ", ?confq, " >|< ", ?confq2); separator=" / ") AS ?containsFormulation)
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

                                                    OPTIONAL {{ ?id wdt:{description} ?descriptionLong }}
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{linear model} }}, "True", "False" ) AS ?isLinear)
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{nonlinear model} }}, "True", "False" ) AS ?isNotLinear)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{dynamic model} }}, "True", "False" ) AS ?isDynamic)
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{static model} }}, "True", "False" ) AS ?isStatic)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{deterministic model} }}, "True", "False" ) AS ?isDeterministic)
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{probabilistic model} }}, "True", "False" ) AS ?isStochastic)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{dimensionless model} }}, "True", "False" ) AS ?isDimensionless)
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{dimensional model} }}, "True", "False" ) AS ?isDimensional)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-space model} }}, "True", "False" ) AS ?isSpaceContinuous)
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-space model} }}, "True", "False" ) AS ?isSpaceDiscrete)
                                                   
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-time model} }}, "True", "False" ) AS ?isTimeContinuous)
                                                    BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-time model} }}, "True", "False" ) AS ?isTimeDiscrete)

                                                    OPTIONAL {{
                                                                   ?rpraw wdt:{modelled by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?rpraw), STR(wd:))) AS ?rp)
                                                                   
                                                                   ?rpraw wdt:{instance of} wd:{research problem}.

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
                                                                   ?id wdt:{assumes} ?assraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?assraw), STR(wd:))) AS ?ass)
                                                                   
                                                                   ?assraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?id p:{contains} ?statement.
                                                                   ?statement ps:{contains} ?confraw.

                                                                   ?confraw wdt:{instance of} wd:{mathematical expression}.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?confraw), STR(wd:))) AS ?conf)
                                                                   
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
                                                                             ?statement pq:{object has role} ?quaraw.
                                                                             BIND(CONCAT("mardi:", STRAFTER(STR(?quaraw), STR(wd:))) AS ?qua)
                                                                           }}
                                                                  BIND(COALESCE(?qua, "") AS ?confq)

                                                                  OPTIONAL {{
                                                                             ?statement pq:{series ordinal} ?qua2raw.
                                                                           }}
                                                                  BIND(COALESCE(?qua2raw, "") AS ?confq2)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:{used by} ?taraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?taraw), STR(wd:))) AS ?ta)
                                                                   
                                                                   ?taraw wdt:{instance of} wd:{computational task}.

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
                                                     
                                                              ?id p:{specialized by} ?statement2.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement2 pq:{assumes} ?qua2raw.

                                                                 BIND(CONCAT("mardi:", STRAFTER(STR(?qua2raw), STR(wd:))) AS ?qua2)
                                                                 
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
                                                        
                                                          ?id p:{specialized by} ?statement2.
                                                          ?statement2 ps:{specialized by} ?sbmraw.
                                                          
                                                          BIND(CONCAT("mardi:", STRAFTER(STR(?sbmraw), STR(wd:))) AS ?sbm)
                                                          
                                                          ?sbmraw wdt:{instance of} wd:{mathematical model}.
                                                        
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
                                                     
                                                              ?smraw p:{specialized by} ?statement3.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement3 pq:{assumes} ?qua3raw.

                                                                 BIND(CONCAT("mardi:", STRAFTER(STR(?qua3raw), STR(wd:))) AS ?qua3)
                                                                 
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
                                                        
                                                          ?smraw p:{specialized by} ?statement3.
                                                          ?statement3 ps:{specialized by} ?id.
                                                          
                                                          BIND(CONCAT("mardi:", STRAFTER(STR(?smraw), STR(wd:))) AS ?sm)
                                                          
                                                          ?smraw wdt:{instance of} wd:{mathematical model}.
                                                        
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
                                                                   ?id wdt:{approximated by} ?abmraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?abmraw), STR(wd:))) AS ?abm)
                                                                   
                                                                   ?abmraw wdt:{instance of} wd:{mathematical model}.

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
                                                                   ?amraw wdt:{approximated by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?amraw), STR(wd:))) AS ?am)
                                                                   
                                                                   ?amraw wdt:{instance of} wd:{mathematical model}.

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
                                                                   ?id wdt:{contains} ?conmraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?conmraw), STR(wd:))) AS ?conm)
                                                                   
                                                                   ?conmraw wdt:{instance of} wd:{mathematical model}.

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
                                                                   ?conimraw wdt:{contains} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?conimraw), STR(wd:))) AS ?conim)
                                                                   
                                                                   ?conimraw wdt:{instance of} wd:{mathematical model}.

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
                                                                   ?id wdt:{discretized by} ?dbmraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?dbmraw), STR(wd:))) AS ?dbm)
                                                                   
                                                                   ?dbmraw wdt:{instance of} wd:{mathematical model}.

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
                                                                   ?dmraw wdt:{discretized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?dmraw), STR(wd:))) AS ?dm)
                                                                   
                                                                   ?dmraw wdt:{instance of} wd:{mathematical model}.

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
                                                                   ?id wdt:{linearized by} ?lbmraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?lbmraw), STR(wd:))) AS ?lbm)
                                                                   
                                                                   ?lbmraw wdt:{instance of} wd:{mathematical model}.

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
                                                                   ?lmraw wdt:{linearized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?lmraw), STR(wd:))) AS ?lm)
                                                                   
                                                                   ?lmraw wdt:{instance of} wd:{mathematical model}.

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
                                                                   ?id wdt:{similar to} ?stmraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?stmraw), STR(wd:))) AS ?stm)
                                                                   
                                                                   ?stmraw wdt:{instance of} wd:{mathematical model}.

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
                                                                   ?id wdt:{described by source} ?pubraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?pubraw), STR(wd:))) AS ?pub)
                                                                   
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
                                                   GROUP BY ?descriptionLong ?isLinear ?isNotLinear ?isDynamic ?isStatic ?isDeterministic ?isStochastic ?isDimensionless 
                                                            ?isDimensional ?isSpaceContinuous ?isSpaceDiscrete ?isTimeContinuous ?isTimeDiscrete''',

              'quantityOrQuantityKindInformation': '''SELECT DISTINCT ?descriptionLong
                                                                      ?isDynamic ?isStatic
                                                                      ?isDeterministic ?isStochastic
                                                                      ?isDimensionless ?isDimensional
                                                                      ?isSpaceContinuous ?isSpaceDiscrete
                                                                      ?isTimeContinuous ?isTimeDiscrete
                                                                      ?isChemicalConstant ?isMathematicalConstant ?isPhysicalConstant
                                                                      ?class ?reference
                                                                      (GROUP_CONCAT(DISTINCT(?formula); SEPARATOR=" / ") AS ?formulas)
                                                                      (GROUP_CONCAT(DISTINCT CONCAT(?symbol, " | ", ?cq, " | ", ?cql, " | ", ?cqd); separator=" / ") AS ?containsQuantity)
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

                                                        OPTIONAL {{ ?id wdt:{description} ?descriptionLong }}

                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{dynamic quantity} }}, "True", "False" ) AS ?isDynamic)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{static quantity} }}, "True", "False" ) AS ?isStatic)

                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd: }}, "True", "False" ) AS ?isDeterministic)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd: }}, "True", "False" ) AS ?isStochastic)

                                                        BIND(EXISTS {{ ?id wdt:{instance of} wd:{dimensionless quantity} }} AS ?dimensionlessQuantity)
                                                        BIND(EXISTS {{ ?id wdt:{instance of} wd:{dimensionless quantity kind} }} AS ?dimensionlessQuantityKind)
                                                        BIND(IF(?dimensionlessQuantity || ?dimensionlessQuantityKind, "True", "False") AS ?dimensionless)
                                                        BIND(COALESCE(?dimensionless, "False") AS ?isDimensionless)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{dimensional quantity} }}, "True", "False" ) AS ?isDimensional)

                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-space quantity} }}, "True", "False" ) AS ?isSpaceContinuous)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-space quantity} }}, "True", "False" ) AS ?isSpaceDiscrete)

                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-time quantity} }}, "True", "False" ) AS ?isTimeContinuous)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-time quantity} }}, "True", "False" ) AS ?isTimeDiscrete)

                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{chemical constant} }}, "True", "False" ) AS ?isChemicalConstant)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{mathematical constant} }}, "True", "False" ) AS ?isMathematicalConstant)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{physical constant} }}, "True", "False" ) AS ?isPhysicalConstant)

                                                        {{
                                                          ?id wdt:{instance of} wd:{quantity}.
                                                          BIND("Quantity" AS ?class)
                                                        }}
                                                        UNION
                                                        {{
                                                          ?id wdt:{instance of} wd:{kind of quantity}.
                                                          BIND("QuantityKind" AS ?class)
                                                        }}

                                                        OPTIONAL {{
                                                                   ?id wdt:{QUDT quantity kind ID} ?reference
                                                                 }}

                                                        OPTIONAL {{
                                                                     ?id wdt:{defining formula} ?formula.
                                                                 }}
                                                        
                                                        OPTIONAL {{
                                                                     ?id p:{in defining formula} ?statement.
                                                                     ?statement ps:{in defining formula} ?symbol.
  
                                                                    OPTIONAL {{
                                                                               ?statement pq:{symbol represents} ?cqraw.
                                                                               
                                                                               BIND(CONCAT("mardi:", STRAFTER(STR(?cqraw), STR(wd:))) AS ?cq)
                                                                               
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
                                                                   ?id wdt:{specialized by} ?sbqraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?sbqraw), STR(wd:))) AS ?sbq)
                                                                   
                                                                   {{
                                                                     ?sbqraw wdt:{instance of} wd:{quantity}.
                                                                     BIND("Quantity" AS ?sbqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?sbqraw wdt:{instance of} wd:{kind of quantity}.
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
                                                                   ?sqraw wdt:{specialized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?sqraw), STR(wd:))) AS ?sq)
                                                                   
                                                                   {{
                                                                     ?sqraw wdt:{instance of} wd:{quantity}.
                                                                     BIND("Quantity" AS ?sqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?sqraw wdt:{instance of} wd:{kind of quantity}.
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
                                                                   ?id wdt:{approximated by} ?abqraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?abqraw), STR(wd:))) AS ?abq)
                                                                   
                                                                   {{
                                                                     ?abqraw wdt:{instance of} wd:{quantity}.
                                                                     BIND("Quantity" AS ?abqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?abqraw wdt:{instance of} wd:{kind of quantity}.
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
                                                                   ?aqraw wdt:{approximated by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?aqraw), STR(wd:))) AS ?aq)
                                                                   
                                                                   {{
                                                                     ?aqraw wdt:{instance of} wd:{quantity}.
                                                                     BIND("Quantity" AS ?aqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?aqraw wdt:{instance of} wd:{kind of quantity}.
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
                                                                   ?id wdt:{linearized by} ?lbqraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?lbqraw), STR(wd:))) AS ?lbq)
                                                                   
                                                                   {{
                                                                     ?lbqraw wdt:{instance of} wd:{quantity}.
                                                                     BIND("Quantity" AS ?lbqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?lbqraw wdt:{instance of} wd:{kind of quantity}.
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
                                                                   ?lqraw wdt:{linearized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?lqraw), STR(wd:))) AS ?lq)
                                                                   
                                                                   {{
                                                                     ?lqraw wdt:{instance of} wd:{quantity}.
                                                                     BIND("Quantity" AS ?lqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?lqraw wdt:{instance of} wd:{kind of quantity}.
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
                                                                   ?id wdt:{nondimensionalized by} ?nbqraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?nbqraw), STR(wd:))) AS ?nbq)
                                                                   
                                                                   {{
                                                                     ?nbqraw wdt:{instance of} wd:{quantity}.
                                                                     BIND("Quantity" AS ?nbqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?nbqraw wdt:{instance of} wd:{kind of quantity}.
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
                                                                   ?nqraw wdt:{nondimensionalized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?nqraw), STR(wd:))) AS ?nq)
                                                                   
                                                                   {{
                                                                     ?nqraw wdt:{instance of} wd:{quantity}.
                                                                     BIND("Quantity" AS ?nqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?nqraw wdt:{instance of} wd:{kind of quantity}.
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
                                                                   ?id wdt:{similar to} ?stqraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?stqraw), STR(wd:))) AS ?stq)
                                                                   
                                                                   {{
                                                                     ?stqraw wdt:{instance of} wd:{quantity}.
                                                                     BIND("Quantity" AS ?stqc)
                                                                   }}
                                                                   UNION
                                                                   {{
                                                                     ?stqraw wdt:{instance of} wd:{kind of quantity}.
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
                                                                   ?id wdt:{described by source} ?pubraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?pubraw), STR(wd:))) AS ?pub)
                                                                   
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
                                                      GROUP BY ?descriptionLong ?isDynamic ?isStatic ?isDeterministic ?isStochastic ?isDimensionless 
                                                               ?isDimensional ?isSpaceContinuous ?isSpaceDiscrete ?isTimeContinuous ?isTimeDiscrete
                                                               ?isChemicalConstant ?isMathematicalConstant ?isPhysicalConstant ?class ?reference''',

              'mathematicalFormulationInformation': '''SELECT DISTINCT ?descriptionLong
                                                                       ?isLinear ?isNotLinear
                                                                       ?isDynamic ?isStatic
                                                                       ?isDeterministic ?isStochastic
                                                                       ?isDimensionless ?isDimensional
                                                                       ?isTimeContinuous ?isTimeDiscrete
                                                                       ?isSpaceContinuous ?isSpaceDiscrete
                                                                       (GROUP_CONCAT(DISTINCT(?formula); SEPARATOR=" / ") AS ?formulas)
                                                                       (GROUP_CONCAT(DISTINCT CONCAT(?symbol, " | ", ?cq, " | ", ?cql, " | ", ?cqd); separator=" / ") AS ?containsQuantity)
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

                                                                       OPTIONAL {{ ?id wdt:{description} ?descriptionLong }}

                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{linear equation} }}, "True", "False" ) AS ?isLinear)
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{nonlinear equation} }}, "True", "False" ) AS ?isNotLinear)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{dynamic equation} }}, "True", "False" ) AS ?isDynamic)
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{static equation} }}, "True", "False" ) AS ?isStatic)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{deterministic equation} }}, "True", "False" ) AS ?isDeterministic)
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{probabilistic equation} }}, "True", "False" ) AS ?isStochastic)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{dimensionless equation} }}, "True", "False" ) AS ?isDimensionless)
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd: }}, "True", "False" ) AS ?isDimensional)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-space equation} }}, "True", "False" ) AS ?isSpaceContinuous)
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-space equation} }}, "True", "False" ) AS ?isSpaceDiscrete)
                                                                     
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-time equation} }}, "True", "False" ) AS ?isTimeContinuous)
                                                                       BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-time equation} }}, "True", "False" ) AS ?isTimeDiscrete)

                                                                       OPTIONAL {{
                                                                                    ?id wdt:{defining formula} ?formula.
                                                                                }}

                                                                       OPTIONAL {{
                                                                                    ?id p:{in defining formula} ?statement.
                                                                                    ?statement ps:{in defining formula} ?symbol.
                 
                                                                                   OPTIONAL {{
                                                                                              ?statement pq:{symbol represents} ?cqraw.

                                                                                              BIND(CONCAT("mardi:", STRAFTER(STR(?cqraw), STR(wd:))) AS ?cq)
                                                                                              
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
                                                                                   ?id wdt:{assumes} ?assraw.

                                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?assraw), STR(wd:))) AS ?ass)
                                                                                   
                                                                                   ?assraw wdt:{instance of} wd:{mathematical expression}.
                
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
                                                                                      ?id p:{contains} ?statement2.
                                                                                      ?statement2 ps:{contains} ?confraw.
                   
                                                                                      ?confraw wdt:{instance of} wd:{mathematical expression}.
                   
                                                                                      BIND(CONCAT("mardi:", STRAFTER(STR(?confraw), STR(wd:))) AS ?conf)
                                                                                      
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
                                                                                                ?statement2 pq:{object has role} ?quaraw.
                                                                                                BIND(CONCAT("mardi:", STRAFTER(STR(?quaraw), STR(wd:))) AS ?qua)
                                                                                              }}
                                                                                     BIND(COALESCE(?qua, "") AS ?confq)
                                                                                  }}

                                                                       OPTIONAL {{   
                                                    
                                                        OPTIONAL {{
                                                          
                                                          {{
                                                            SELECT ?statement3 (GROUP_CONCAT(DISTINCT ?sbfq_entry; separator=" <|> ") AS ?sbfq)
                                                            WHERE {{
                                                     
                                                              ?id p:{specialized by} ?statement3.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement3 pq:{assumes} ?qua3raw.

                                                                 BIND(CONCAT("mardi:", STRAFTER(STR(?qua3raw), STR(wd:))) AS ?qua3)
                                                                 
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
                                                        
                                                          ?id p:{specialized by} ?statement3.
                                                          ?statement3 ps:{specialized by} ?sbfraw.
                                                          
                                                          BIND(CONCAT("mardi:", STRAFTER(STR(?sbfraw), STR(wd:))) AS ?sbf)
                                                          
                                                          ?sbfraw wdt:{instance of} wd:{mathematical expression}.
                                                        
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
                                                     
                                                              ?sfraw p:{specialized by} ?statement4.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement4 pq:{assumes} ?qua4raw.

                                                                 BIND(CONCAT("mardi:", STRAFTER(STR(?qua4raw), STR(wd:))) AS ?qua4)
                                                                 
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
                                                        
                                                          ?sfraw p:{specialized by} ?statement4.
                                                          ?statement4 ps:{specialized by} ?id.
                                                          
                                                          BIND(CONCAT("mardi:", STRAFTER(STR(?sfraw), STR(wd:))) AS ?sf)
                                                          
                                                          ?sfraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?id wdt:{approximated by} ?abfraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?abfraw), STR(wd:))) AS ?abf)
                                                                   
                                                                   ?abfraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?afraw wdt:{approximated by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?afraw), STR(wd:))) AS ?af)
                                                                   
                                                                   ?afraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?id wdt:{nondimensionalized by} ?nbfraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?nbfraw), STR(wd:))) AS ?nbf)
                                                                   
                                                                   ?nbfraw wdt:{instance of} wd:{mathematical expression}.
                                                                   
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
                                                                   ?nfraw wdt:{nondimensionalized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?nfraw), STR(wd:))) AS ?nf)
                                                                   
                                                                   ?nfraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?id wdt:{discretized by} ?dbfraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?dbfraw), STR(wd:))) AS ?dbf)
                                                                   
                                                                   ?dbfraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?dfraw wdt:{discretized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?dfraw), STR(wd:))) AS ?df)
                                                                   
                                                                   ?dbfraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?id wdt:{linearized by} ?lbfraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?lbfraw), STR(wd:))) AS ?lbf)
                                                                   
                                                                   ?lbfraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?lfraw wdt:{linearized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?lfraw), STR(wd:))) AS ?lf)
                                                                   
                                                                   ?lfraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?id wdt:{similar to} ?stfraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?stfraw), STR(wd:))) AS ?stf)
                                                                   
                                                                   ?stfraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?id wdt:{described by source} ?pubraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?pubraw), STR(wd:))) AS ?pub)
                                                                   
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
                                                                     GROUP BY ?descriptionLong ?isLinear ?isNotLinear ?isDynamic ?isStatic ?isDeterministic ?isStochastic ?isDimensionless 
                                                                              ?isDimensional ?isSpaceContinuous ?isSpaceDiscrete ?isTimeContinuous ?isTimeDiscrete''',
                                                                                             
                              'taskInformation': '''SELECT DISTINCT ?descriptionLong
                                                                    ?isLinear ?isNotLinear
                                                                    ?isSpaceContinuous ?isSpaceDiscrete
                                                                    ?isTimeContinuous ?isTimeDiscrete
                                                                    (GROUP_CONCAT(DISTINCT ?descriptionLong; separator=" / ") AS ?description)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?ass, " | ", ?assl, " | ", ?assd); separator=" / ") AS ?assumes)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?conf, " | ", ?confl, " | ", ?confd, " | ", ?confq); separator=" / ") AS ?containsFormulation)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?quan, " | ", ?quanl, " | ", ?quand, " | ", ?quanq); separator=" / ") AS ?containsQuantity)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?sbt, " | ", ?sbtl, " | ", ?sbtd, " | ", ?sbtq); separator=" / ") AS ?specializedBy)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?st, " | ", ?stl, " | ", ?std, " | ", ?stq); separator=" / ") AS ?specializes)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?abt, " | ", ?abtl, " | ", ?abtd); separator=" / ") AS ?approximatedBy)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?at, " | ", ?atl, " | ", ?atd); separator=" / ") AS ?approximates)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?cont, " | ", ?contl, " | ", ?contd, " | ", " >|< ", ?corder); separator=" / ") AS ?containsTask)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?conit, " | ", ?conitl, " | ", ?conitd, " | ", " >|< ", ?ciorder); separator=" / ") AS ?containedInTask)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?dbt, " | ", ?dbtl, " | ", ?dbtd); separator=" / ") AS ?discretizedBy)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?dt, " | ", ?dtl, " | ", ?dtd); separator=" / ") AS ?discretizes)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?lbt, " | ", ?lbtl, " | ", ?lbtd); separator=" / ") AS ?linearizedBy)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?lt, " | ", ?ltl, " | ", ?ltd); separator=" / ") AS ?linearizes)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?stt, " | ", ?sttl, " | ", ?sttd); separator=" / ") AS ?similarTo)
                                                                    (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publications)
                        
                                                    WHERE {{

                                                        VALUES ?id {{wd:{0}}}

                                                        OPTIONAL {{ ?id wdt:{description} ?descriptionLong }}

                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{linear task} }}, "True", "False" ) AS ?isLinear)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{nonlinear task} }}, "True", "False" ) AS ?isNotLinear)

                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-space task} }}, "True", "False" ) AS ?isSpaceContinuous)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-space task} }}, "True", "False" ) AS ?isSpaceDiscrete)
                                                      
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-time task} }}, "True", "False" ) AS ?isTimeContinuous)
                                                        BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-time task} }}, "True", "False" ) AS ?isTimeDiscrete)

                                                        OPTIONAL {{
                                                                   ?id wdt:{assumes} ?assraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?assraw), STR(wd:))) AS ?ass)
                                                                   
                                                                   ?assraw wdt:{instance of} wd:{mathematical expression}.

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
                                                                   ?id p:{contains} ?statement.
                                                                   ?statement ps:{contains} ?confraw.

                                                                   ?confraw wdt:{instance of} wd:{mathematical expression}.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?confraw), STR(wd:))) AS ?conf)
                                                                   
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
                                                                             ?statement pq:{object has role} ?quaraw.
                                                                             BIND(CONCAT("mardi:", STRAFTER(STR(?quaraw), STR(wd:))) AS ?qua)
                                                                           }}
                                                                  BIND(COALESCE(?qua, "") AS ?confq)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id p:{contains} ?statement2.
                                                                   ?statement2 ps:{contains} ?quanraw.

                                                                   {{
                                                                      ?quanraw wdt:{instance of} wd:{quantity}.
                                                                   }}
                                                                      UNION
                                                                   {{
                                                                      ?quanraw wdt:{instance of} wd:{kind of quantity}.
                                                                   }}

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?quanraw), STR(wd:))) AS ?quan)
                                                                   
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
                                                                             ?statement2 pq:{object has role} ?qua2raw.
                                                                             BIND(CONCAT("mardi:", STRAFTER(STR(?qua2raw), STR(wd:))) AS ?qua2)
                                                                           }}
                                                                  BIND(COALESCE(?qua2, "") AS ?quanq)
                                                               }}

                                                    OPTIONAL {{   
                                                    
                                                        OPTIONAL {{
                                                          
                                                          {{
                                                            SELECT ?statement3 (GROUP_CONCAT(DISTINCT ?sbtq_entry; separator=" <|> ") AS ?sbtq)
                                                            WHERE {{
                                                     
                                                              ?id p:{specialized by} ?statement3.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement3 pq:{assumes} ?qua3raw.
                                                                 BIND(CONCAT("mardi:", STRAFTER(STR(?qua3raw), STR(wd:))) AS ?qua3)
                                                                 
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
                                                        
                                                          ?id p:{specialized by} ?statement3.
                                                          ?statement3 ps:{specialized by} ?sbtraw.
                                                          
                                                          BIND(CONCAT("mardi:", STRAFTER(STR(?sbtraw), STR(wd:))) AS ?sbt)
                                                          
                                                          ?sbtraw wdt:{instance of} wd:{computational task}.

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
                                                     
                                                              ?straw p:{specialized by} ?statement4.
                                                              
                                                              OPTIONAL {{
                                                     
                                                                 ?statement4 pq:{assumes} ?qua4raw.
                                                                 BIND(CONCAT("mardi:", STRAFTER(STR(?qua4raw), STR(wd:))) AS ?qua4)
                                                                 
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
                                                        
                                                          ?straw p:{specialized by} ?statement4.
                                                          ?statement4 ps:{specialized by} ?id.
                                                          
                                                          BIND(CONCAT("mardi:", STRAFTER(STR(?straw), STR(wd:))) AS ?st)
                                                          
                                                          ?straw wdt:{instance of} wd:{computational task}.

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
                                                                   ?id wdt:{approximated by} ?abtraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?abtraw), STR(wd:))) AS ?abt)
                                                                   
                                                                   ?abtraw wdt:{instance of} wd:{computational task}.

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
                                                                   ?atraw wdt:{approximated by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?atraw), STR(wd:))) AS ?at)
                                                                   
                                                                   ?atraw wdt:{instance of} wd:{computational task}.

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
                                                                   ?id p:{contains} ?statement5.
                                                                   ?statement5 ps:{contains} ?contraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?contraw), STR(wd:))) AS ?cont)
                                                                   
                                                                   ?contraw wdt:{instance of} wd:{computational task}.

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

                                                                  OPTIONAL {{
                                                                             ?statement5 pq:{series ordinal} ?corder_raw.
                                                                           }}
                                                                  BIND(COALESCE(?corder_raw, "") AS ?corder)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?conitraw p:{contains} ?statement6.
                                                                   ?statement6 ps:{contains} ?conitraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?conitraw), STR(wd:))) AS ?conit)
                                                                   
                                                                   ?conitraw wdt:{instance of} wd:{computational task}.

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

                                                                  OPTIONAL {{
                                                                             ?statement6 pq:{series ordinal} ?ciorder_raw.
                                                                           }}
                                                                  BIND(COALESCE(?ciorder_raw, "") AS ?ciorder)
                                                               }}

                                                    OPTIONAL {{
                                                                   ?id wdt:{discretized by} ?dbtraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?dbtraw), STR(wd:))) AS ?dbt)
                                                                   
                                                                   ?dbtraw wdt:{instance of} wd:{computational task}.

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
                                                                   ?dtraw wdt:{discretized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?dtraw), STR(wd:))) AS ?dt)
                                                                   
                                                                   ?dtraw wdt:{instance of} wd:{computational task}.

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
                                                                   ?id wdt:{linearized by} ?lbtraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?lbtraw), STR(wd:))) AS ?lbt)
                                                                   
                                                                   ?lbtraw wdt:{instance of} wd:{computational task}.

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
                                                                   ?ltraw wdt:{linearized by} ?id.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?ltraw), STR(wd:))) AS ?lt)
                                                                   
                                                                   ?ltraw wdt:{instance of} wd:{computational task}.

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
                                                                   ?id wdt:{similar to} ?sttraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?sttraw), STR(wd:))) AS ?stt)
                                                                   
                                                                   ?sttraw wdt:{instance of} wd:{computational task}.

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
                                                                   ?id wdt:{described by source} ?pubraw.

                                                                   BIND(CONCAT("mardi:", STRAFTER(STR(?pubraw), STR(wd:))) AS ?pub)
                                                                   
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
                                                        GROUP BY ?descriptionLong ?isLinear ?isNotLinear ?isSpaceContinuous ?isSpaceDiscrete ?isTimeContinuous ?isTimeDiscrete''',        
                                                      }