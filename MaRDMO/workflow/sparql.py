queryInfo = {
            'mardi': {
                      'step':  '''PREFIX wdt:<https://portal.mardi4nfdi.de/prop/direct/>
                                  PREFIX wd:<https://portal.mardi4nfdi.de/entity/>

                                  SELECT (GROUP_CONCAT(DISTINCT(?msc); SEPARATOR=" / ") AS ?mscID)
                                         (GROUP_CONCAT(DISTINCT CONCAT(?input, " | ", ?inputl, " | ", ?inputd); separator=" / ") AS ?inputDataSet)
                                         (GROUP_CONCAT(DISTINCT CONCAT(?output, " | ", ?outputl, " | ", ?outputd); separator=" / ") AS ?outputDataSet)
                                         (GROUP_CONCAT(DISTINCT CONCAT(?method, " | ", ?methodl, " | ", ?methodd, " | ", STR(?methodurl)); separator=" / ") AS ?uses)
                                         (GROUP_CONCAT(DISTINCT CONCAT(?platformsoftware, " | ", ?platformsoftwarel, " | ", ?platformsoftwared); separator=" / ") AS ?platformSoftware)
                                         (GROUP_CONCAT(DISTINCT CONCAT(?platforminstrument, " | ", ?platforminstrumentl, " | ", ?platforminstrumentd); separator=" / ") AS ?platformInstrument)
                                         (GROUP_CONCAT(DISTINCT CONCAT(?field, " | ", ?fieldl, " | ", ?fieldd); separator=" / ") AS ?fieldOfWork)
                                  
                                  WHERE {{
                                          VALUES ?step {{ wd:{0} }}
                                          OPTIONAL {{
                                                     ?step wdt:P1605 ?inputraw
                                                     BIND(replace( xsd:string(?inputraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?input) 
                                                     
                                                     OPTIONAL {{
                                                                ?inputraw rdfs:label ?inputlraw
                                                                FILTER (lang(?inputlraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?inputlraw, "No Label Provided!") AS ?inputl)
                                                     
                                                     OPTIONAL {{
                                                                ?inputraw schema:description ?inputdraw
                                                                FILTER (lang(?inputdraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?inputdraw, "No Description Provided!") AS ?inputd)
                                                   }}
                                          OPTIONAL {{
                                                     ?step wdt:P1606 ?outputraw
                                                     BIND(replace( xsd:string(?outputraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?output) 
                                                     
                                                     OPTIONAL {{
                                                                ?outputraw rdfs:label ?outputlraw
                                                                FILTER (lang(?outputlraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?outputlraw, "No Label Provided!") AS ?outputl)
                                                     
                                                     OPTIONAL {{
                                                                ?outputraw schema:description ?outputdraw
                                                                FILTER (lang(?outputdraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?outputdraw, "No Description Provided!") AS ?outputd)
                                                   }}
                                          OPTIONAL {{
                                                     ?step wdt:P557 ?methodraw
                                                     BIND(replace( xsd:string(?methodraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?method) 
                                                     
                                                     OPTIONAL {{
                                                                ?methodraw rdfs:label ?methodlraw
                                                                FILTER (lang(?methodlraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?methodlraw, "No Label Provided!") AS ?methodl)
                                                     
                                                     OPTIONAL {{
                                                                ?methodraw schema:description ?methoddraw
                                                                FILTER (lang(?methoddraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?methoddraw, "No Description Provided!") AS ?methodd)
                                                     OPTIONAL {{
                                                                ?methodraw wdt:P188 ?methodurl
                                                              }}
                                                     BIND(COALESCE(?methodurl, "") AS ?methodurl)
                                                   }}
                                          OPTIONAL {{
                                                     ?step p:P143 ?statement0.
                                                     ?statement0 ps:P143 ?platformsoftwareraw.
                                                    
                                                     ?statement pq:P560 ?platformsoftwaretyperaw.
                                                     BIND(replace( xsd:string(?platformsoftwaretyperaw),'https://portal.mardi4nfdi.de/entity/','') as ?platformsoftwaretype)
                                                     FILTER (?platformsoftwaretype = "Q56614")
                                                     BIND(replace( xsd:string(?platformsoftwareraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?platformsoftware) 
                                                     
                                                     OPTIONAL {{
                                                                ?platformsoftwareraw rdfs:label ?platformsoftwarelraw
                                                                FILTER (lang(?platformsoftwarelraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?platformsoftwarelraw, "No Label Provided!") AS ?platformsoftwarel)
                                                     
                                                     OPTIONAL {{
                                                                ?platformsoftwareraw schema:description ?platformsoftwaredraw
                                                                FILTER (lang(?platformsoftwaredraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?platformsoftwaredraw, "No Description Provided!") AS ?platformsoftwared)
                                                   }}
                                          OPTIONAL {{
                                                     ?step p:P143 ?statement1.
                                                     ?statement1 ps:P143 ?platforminstrumentraw.
                                                     
                                                     ?statement pq:P560 ?platforminstrumenttyperaw.
                                                     BIND(replace( xsd:string(?platforminstrumenttyperaw),'https://portal.mardi4nfdi.de/entity/','') as ?platforminstrumenttype)
                                                     FILTER (?platforminstrumenttype = "Q77076")
                                                              
                                                     BIND(replace( xsd:string(?platforminstrumentraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?platforminstrument) 
                                                     
                                                     OPTIONAL {{
                                                                ?platforminstrumentraw rdfs:label ?platforminstrumentlraw
                                                                FILTER (lang(?platforminstrumentlraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?platforminstrumentlraw, "No Label Provided!") AS ?platforminstrumentl)
                                                     
                                                     OPTIONAL {{
                                                                ?platforminstrumentraw schema:description ?platforminstrumentdraw
                                                                FILTER (lang(?platforminstrumentdraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?platforminstrumentdraw, "No Description Provided!") AS ?platforminstrumentd)
                                                   }}
                                          OPTIONAL {{
                                                     ?step wdt:P437 ?fieldraw.
                                                     BIND(replace( xsd:string(?fieldraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?field)
                                                     OPTIONAL {{
                                                                ?fieldraw rdfs:label ?fieldlraw
                                                                FILTER (lang(?fieldlraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?fieldlraw, "No Label Provided!") AS ?fieldl)
                                                     
                                                     OPTIONAL {{
                                                                ?fieldraw schema:description ?fielddraw
                                                                FILTER (lang(?fielddraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?fielddraw, "No Description Provided!") AS ?fieldd)
                                                   }}
                                          OPTIONAL {{
                                                     ?step wdt:P226 ?msc.
                                                   }}
                                  }}''',

                         'method':  '''PREFIX wdt:<https://portal.mardi4nfdi.de/prop/direct/>
                                       PREFIX wd:<https://portal.mardi4nfdi.de/entity/>
     
                                       SELECT (GROUP_CONCAT(DISTINCT CONCAT(?impSoft, " | ", ?impSoftl, " | ", ?impSoftd); separator=" / ") AS ?implementedBySoftware)
                                              (GROUP_CONCAT(DISTINCT CONCAT(?impInst, " | ", ?impInstl, " | ", ?impInstd); separator=" / ") AS ?implementedByInstrument)
                                              
                                       WHERE {{
                                               VALUES ?method {{ wd:{0} }}
                                               OPTIONAL {{
                                                          ?method wdt:P ?impSoftraw.
                                                          ?impSoftraw wdt:P31 wd:Q56614.

                                                          BIND(replace( xsd:string(?impSoftraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?impSoft) 
                                                          
                                                          OPTIONAL {{
                                                                     ?impSoftraw rdfs:label ?impSoftlraw
                                                                     FILTER (lang(?impSoftlraw) = 'en')
                                                                   }}
                                                          
                                                          BIND(COALESCE(?impSoftlraw, "No Label Provided!") AS ?impSoftl)
                                                          
                                                          OPTIONAL {{
                                                                     ?impSoftraw schema:description ?impSoftdraw
                                                                     FILTER (lang(?impSoftdraw) = 'en')
                                                                   }}
                                                          
                                                          BIND(COALESCE(?impSoftdraw, "No Description Provided!") AS ?impSoftd)
                                                        }}
                                                        
                                              OPTIONAL {{
                                                          ?method wdt:P ?impInstraw.
                                                          ?impInstraw wdt:P31 wd:Q77076.
                                                          
                                                          BIND(replace( xsd:string(?impInstraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?impInst) 
                                                          
                                                          OPTIONAL {{
                                                                     ?impInstraw rdfs:label ?impInstlraw
                                                                     FILTER (lang(?impInstlraw) = 'en')
                                                                   }}
                                                          
                                                          BIND(COALESCE(?impInstlraw, "No Label Provided!") AS ?impInstl)
                                                          
                                                          OPTIONAL {{
                                                                     ?impInstraw schema:description ?impInstdraw
                                                                     FILTER (lang(?impInstdraw) = 'en')
                                                                   }}
                                                          
                                                          BIND(COALESCE(?impInstdraw, "No Description Provided!") AS ?impInstd)
                                                        }}
                                            }}''',

                         'software': '''PREFIX wdt:<https://portal.mardi4nfdi.de/prop/direct/>
                                        PREFIX wd:<https://portal.mardi4nfdi.de/entity/>
        
                                        SELECT ?userManualURL ?sourceCodeRepository ?reference
                                               (GROUP_CONCAT(DISTINCT CONCAT(?pl, " | ", ?pll, " | ", ?pld); separator=" / ") AS ?programmedIn)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?dp, " | ", ?dpl, " | ", ?dpd); separator=" / ") AS ?dependsOnSoftware)
               
                                        WHERE {{
                                          
                                          VALUES ?software {{ wd:{0} }}
                                          
                                          # Get Programming Language
                                          OPTIONAL {{
                                                     ?software wdt:P114 ?plraw.
                                                     BIND(replace( xsd:string(?plraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?pl) 
                                                     
                                                     OPTIONAL {{
                                                                ?plraw rdfs:label ?pllraw
                                                                FILTER (lang(?pllraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?pllraw, "No Label Provided!") AS ?pll)
                                                     
                                                     OPTIONAL {{
                                                                ?plraw schema:description ?pldraw
                                                                FILTER (lang(?pldraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?pldraw, "No Description Provided!") AS ?pld)
                                                   }}  
                                          
                                          # Get Dependencies
                                          OPTIONAL {{
                                                     ?software wdt:P342 ?dpraw.
                                                     BIND(replace( xsd:string(?dpraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?dp) 
                                                     
                                                     OPTIONAL {{
                                                                ?dpraw rdfs:label ?dplraw
                                                                FILTER (lang(?dplraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?dplraw, "No Label Provided!") AS ?dpl)
                                                     
                                                     OPTIONAL {{
                                                                ?dpraw schema:description ?dpdraw
                                                                FILTER (lang(?dpdraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?dpdraw, "No Description Provided!") AS ?dpd)
                                                   }}
        
                                          # Source Code Repository
                                          OPTIONAL {{
                                                     ?software wdt:P339 ?sourceCodeRepository.
                                                   }}
        
                                          # User Manual URL
                                          OPTIONAL {{
                                                     ?software wdt:P340 ?userManualURL.
                                                   }}
                                          # DOI
                                          OPTIONAL {{
                                                     ?software wdt:P27 ?doi.
                                                   }}
                                          
                                          # SWMATH
                                          OPTIONAL {{
                                                     ?software wdt:P13 ?swmath.
                                                   }}

                                          # URL
                                          OPTIONAL {{
                                                     ?software wdt:P188 ?url.
                                                   }}

                                         BIND(
                                              CONCAT(
                                                  IF(BOUND(?doi), CONCAT("doi:", STR(?doi), " | "), ""),
                                                  IF(BOUND(?swmath), CONCAT("swmath:", STR(?swmath), " | "), ""),
                                                  IF(BOUND(?url), STR(?url), "")
                                              ) AS ?referenceraw
                                          )
                                          
                                          BIND(IF(STRENDS(?referenceraw, " | "), STRBEFORE(?referenceraw, " | "), ?referenceraw) AS ?reference)

                                        }}  
                                        
                                        GROUP BY ?sourceCodeRepository ?userManualURL ?reference''',

                         'hardware': '''PREFIX wdt:<https://portal.mardi4nfdi.de/prop/direct/>
                                        PREFIX wd:<https://portal.mardi4nfdi.de/entity/>
        
                                        SELECT ?nodes ?cores
                                               (GROUP_CONCAT(DISTINCT CONCAT(?cpu, " | ", ?cpul, " | ", ?cpud); separator=" / ") AS ?CPU)
               
                                        WHERE {{

                                          VALUES ?hardware {{ wd:{0} }}
        
                                          # Get CPU
                                          OPTIONAL {{
                                                     ?hardware p:P1540 ?statement.
                                                     ?statement ps:P1540 ?cpuraw.
                                                     BIND(replace( xsd:string(?cpuraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?cpu) 
                                                     
                                                     OPTIONAL {{
                                                                ?cpuraw rdfs:label ?cpulraw
                                                                FILTER (lang(?cpulraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?cpulraw, "No Label Provided!") AS ?cpul)
                                                     
                                                     OPTIONAL {{
                                                                ?cpuraw schema:description ?cpudraw
                                                                FILTER (lang(?cpudraw) = 'en')
                                                              }}
                                                     
                                                     BIND(COALESCE(?cpudraw, "No Description Provided!") AS ?cpud)
        
                                                     OPTIONAL {{
                                                                ?cpuraw wdt:P1565 ?cores.
                                                              }}
                                                                
                                                     OPTIONAL {{
                                                                ?statement pq:P149 ?nodes.
                                                              }}
                                                   }}
                                              }}
                                        GROUP BY ?nodes ?cores ''',

                         'data-set':  '''PREFIX wdt:<https://portal.mardi4nfdi.de/prop/direct/>
                                         PREFIX wd:<https://portal.mardi4nfdi.de/entity/>
         
                                         SELECT ?sizeValue ?sizeUnit ?sizeRecord ?fileFormat ?binaryOrText ?proprietary
                                                ?DOI ?URL ?publish ?archive ?endTime
                                                (GROUP_CONCAT(DISTINCT CONCAT(?datatype, " | ", ?datatypel, " | ", ?datatyped); separator=" / ") AS ?dataType)
                                                (GROUP_CONCAT(DISTINCT CONCAT(?representationformat, " | ", ?representationformatl, " | ", ?representationformatd); separator=" / ") AS ?representationFormat)
                
                                         WHERE {{

                                           VALUES ?dataset {{ wd:{0} }}
         
                                           # Get Size (bytes)
                                           OPTIONAL {{
                                                      ?dataset p:P1542 ?statementNode.          
                                                      ?statementNode psv:P1542 ?valueNode.      
                                                      ?valueNode wikibase:quantityAmount ?sizeValue; 
                                                                 wikibase:quantityUnit ?unit.
                                                      ?unit rdfs:label ?sizeUnit.
                                                      FILTER (lang(?sizeUnit) = 'en')
                                                    }}

                                           # Get Size (number of items)
                                           OPTIONAL {{
                                                      ?dataset wdt:P139 ?sizeRecord
                                                    }}
         
                                           # Data Type
                                           OPTIONAL {{
                                                      ?dataset p:P557 ?statement_dt.
                                                      ?statement_dt ps:P557 ?datatyperaw. 
                                                      ?statement_dt pq:P560 ?qualifier.
                                                      FILTER (?qualifier = wd:Q78802)
         
                                                      BIND(replace( xsd:string(?datatyperaw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?datatype)
                                                      
                                                      OPTIONAL {{
                                                                 ?datatyperaw rdfs:label ?datatypelraw
                                                                 FILTER (lang(?datatypelraw) = 'en')
                                                               }}
                                                      
                                                      BIND(COALESCE(?datatypelraw, "No Label Provided!") AS ?datatypel)
                                                      
                                                      OPTIONAL {{
                                                                 ?datatyperaw schema:description ?datatypedraw
                                                                 FILTER (lang(?datatypedraw) = 'en')
                                                               }}
                                                      
                                                      BIND(COALESCE(?datatypedraw, "No Description Provided!") AS ?datatyped)
                                                    }}  
           
                                           #Representation Format
                                           OPTIONAL {{
                                                      ?dataset p:P557 ?statement_dt2.
                                                      ?statement_dt2 ps:P557 ?representationformatraw. 
                                                      ?statement_dt2 pq:P560 ?qualifier2.
                                                      FILTER (?qualifier2 = wd:Q6534222)
         
                                                      BIND(replace( xsd:string(?representationformatraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?representationformat)
                                                      
                                                      OPTIONAL {{
                                                                 ?representationformatraw rdfs:label ?representationformatlraw
                                                                 FILTER (lang(?representationformatlraw) = 'en')
                                                               }}
                                                      
                                                      BIND(COALESCE(?representationformatlraw, "No Label Provided!") AS ?representationformatl)
                                                      
                                                      OPTIONAL {{
                                                                 ?representationformatraw schema:description ?representationformatdraw
                                                                 FILTER (lang(?representationformatdraw) = 'en')
                                                               }}
                                                      
                                                      BIND(COALESCE(?representationformatdraw, "No Description Provided!") AS ?representationformatd)
                                                    }}
         
                                           # Get file extension
                                           OPTIONAL {{
                                                      ?dataset wdt:P921 ?fileFormat
                                                    }}
                                               
                                           # Binary or Text
                                           BIND(IF(EXISTS {{ ?dataset wdt:P31 wd:Q6480276 }}, "binary", IF(EXISTS {{ ?dataset wdt:P31 wd:Q6534207 }}, "text", "" )) AS ?binaryOrText)
         
                                           # Proprietary
                                           BIND(IF(EXISTS {{ ?dataset wdt:P31 wd:Q6480367 }}, "Yes", IF(EXISTS {{ ?dataset wdt:P31 wd:Q6480313 }}, "No", "" )) AS ?proprietary)
                                           
                                           # Bind DOI and URL if they exist
                                           OPTIONAL {{ ?dataset wdt:P27 ?DOI. }}
                                           OPTIONAL {{ ?dataset wdt:P188 ?URL. }}
         
                                           # Data Publishing
                                           BIND(IF(EXISTS {{ ?dataset wdt:P1563 wd:Q6480291 }}, "Yes", "No") AS ?publish)
         
                                           # Data Archiving
                                           BIND(IF(EXISTS {{ ?dataset wdt:P1563 wd:Q6480370 }}, "YesText", "NoText") AS ?archive)
         
                                           OPTIONAL {{
                                                      ?dataset p:P1563 ?statementNode2.
                                                      ?statementNode2 ps:P1563 wd:Q6480370.
                                                      OPTIONAL {{
                                                                  ?statementNode2 pq:P411 ?endTime.
                                                               }}
                                                    }}
                                           }}    
                                           GROUP BY ?sizeValue ?sizeUnit ?sizeRecord ?fileFormat ?binaryOrText ?proprietary ?DOI ?URL ?publish ?archive ?endTime'''
                     },
            'wikidata': { 
                         'step':  '''SELECT (GROUP_CONCAT(DISTINCT(?msc); SEPARATOR=" / ") AS ?mscID)
                                            (GROUP_CONCAT(DISTINCT CONCAT(?input, " | ", ?inputl, " | ", ?inputd); separator=" / ") AS ?inputDataSet)
                                            (GROUP_CONCAT(DISTINCT CONCAT(?output, " | ", ?outputl, " | ", ?outputd); separator=" / ") AS ?outputDataSet)
                                            (GROUP_CONCAT(DISTINCT CONCAT(?method, " | ", ?methodl, " | ", ?methodd); separator=" / ") AS ?uses)
                                            (GROUP_CONCAT(DISTINCT CONCAT(?platformsoftware, " | ", ?platformsoftwarel, " | ", ?platformsoftwared); separator=" / ") AS ?platformSoftware)
                                            (GROUP_CONCAT(DISTINCT CONCAT(?platforminstrument, " | ", ?platforminstrumentl, " | ", ?platforminstrumentd); separator=" / ") AS ?platformInstrument)
                                            (GROUP_CONCAT(DISTINCT CONCAT(?field, " | ", ?fieldl, " | ", ?fieldd); separator=" / ") AS ?fieldOfWork)

                                      WHERE {{

                                              VALUES ?step {{ wd:{0} }}

                                              OPTIONAL {{
                                                         ?step wdt:P ?inputraw
                                                         BIND(replace( xsd:string(?inputraw),'http://www.wikidata.org/entity/','wikidata:') as ?input) 

                                                         OPTIONAL {{
                                                                    ?inputraw rdfs:label ?inputlraw
                                                                    FILTER (lang(?inputlraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?inputlraw, "No Label Provided!") AS ?inputl)

                                                         OPTIONAL {{
                                                                    ?inputraw schema:description ?inputdraw
                                                                    FILTER (lang(?inputdraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?inputdraw, "No Description Provided!") AS ?inputd)
                                                       }}

                                              OPTIONAL {{
                                                         ?step wdt:P ?outputraw
                                                         BIND(replace( xsd:string(?outputraw),'http://www.wikidata.org/entity/','wikidata:') as ?output) 

                                                         OPTIONAL {{
                                                                    ?outputraw rdfs:label ?outputlraw
                                                                    FILTER (lang(?outputlraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?outputlraw, "No Label Provided!") AS ?outputl)

                                                         OPTIONAL {{
                                                                    ?outputraw schema:description ?outputdraw
                                                                    FILTER (lang(?outputdraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?outputdraw, "No Description Provided!") AS ?outputd)
                                                       }}

                                              OPTIONAL {{
                                                         ?step wdt:P2283 ?methodraw
                                                         BIND(replace( xsd:string(?methodraw),'http://www.wikidata.org/entity/','wikidata:') as ?method) 

                                                         OPTIONAL {{
                                                                    ?methodraw rdfs:label ?methodlraw
                                                                    FILTER (lang(?methodlraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?methodlraw, "No Label Provided!") AS ?methodl)

                                                         OPTIONAL {{
                                                                    ?methodraw schema:description ?methoddraw
                                                                    FILTER (lang(?methoddraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?methoddraw, "No Description Provided!") AS ?methodd)
                                                       }}

                                              OPTIONAL {{
                                                         ?step p:P400 ?statement0.
                                                         ?statement0 ps:P400 ?platformsoftwareraw.


                                                         ?statement pq:P3831 ?platformsoftwaretyperaw.
                                                         BIND(replace( xsd:string(?platformsoftwaretyperaw),'http://www.wikidata.org/entity/','') as ?platformsoftwaretype)
                                                         FILTER (?platformsoftwaretype = "Q7397")


                                                         BIND(replace( xsd:string(?platformsoftwareraw),'http://www.wikidata.org/entity/','wikidata:') as ?platformsoftware) 

                                                         OPTIONAL {{
                                                                    ?platformsoftwareraw rdfs:label ?platformsoftwarelraw
                                                                    FILTER (lang(?platformsoftwarelraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?platformsoftwarelraw, "No Label Provided!") AS ?platformsoftwarel)

                                                         OPTIONAL {{
                                                                    ?platformsoftwareraw schema:description ?platformsoftwaredraw
                                                                    FILTER (lang(?platformsoftwaredraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?platformsoftwaredraw, "No Description Provided!") AS ?platformsoftwared)
                                                       }}

                                              OPTIONAL {{
                                                         ?step p:P400 ?statement1.
                                                         ?statement1 ps:P400 ?platforminstrumentraw.


                                                         ?statement pq:P3831 ?platforminstrumenttyperaw.
                                                         BIND(replace( xsd:string(?platforminstrumenttyperaw),'http://www.wikidata.org/entity/','') as ?platforminstrumenttype)
                                                         FILTER (?platforminstrumenttype = "")


                                                         BIND(replace( xsd:string(?platforminstrumentraw),'http://www.wikidata.org/entity/','wikidata:') as ?platforminstrument) 

                                                         OPTIONAL {{
                                                                    ?platforminstrumentraw rdfs:label ?platforminstrumentlraw
                                                                    FILTER (lang(?platforminstrumentlraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?platforminstrumentlraw, "No Label Provided!") AS ?platforminstrumentl)

                                                         OPTIONAL {{
                                                                    ?platforminstrumentraw schema:description ?platforminstrumentdraw
                                                                    FILTER (lang(?platforminstrumentdraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?platforminstrumentdraw, "No Description Provided!") AS ?platforminstrumentd)
                                                       }}

                                              OPTIONAL {{
                                                         ?step wdt:P101 ?fieldraw.
                                                         BIND(replace( xsd:string(?fieldraw),'http://www.wikidata.org/entity/','wikidata:') as ?field)

                                                         OPTIONAL {{
                                                                    ?fieldraw rdfs:label ?fieldlraw
                                                                    FILTER (lang(?fieldlraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?fieldlraw, "No Label Provided!") AS ?fieldl)

                                                         OPTIONAL {{
                                                                    ?fieldraw schema:description ?fielddraw
                                                                    FILTER (lang(?fielddraw) = 'en')
                                                                  }}

                                                         BIND(COALESCE(?fielddraw, "No Description Provided!") AS ?fieldd)
                                                       }}

                                              OPTIONAL {{
                                                         ?step wdt:P3285 ?msc.
                                                       }}

                                  }}''',

                           'method':  '''SELECT (GROUP_CONCAT(DISTINCT CONCAT(?impSoft, " | ", ?impSoftl, " | ", ?impSoftd); separator=" / ") AS ?implementedBySoftware)
                                                (GROUP_CONCAT(DISTINCT CONCAT(?impInst, " | ", ?impInstl, " | ", ?impInstd); separator=" / ") AS ?implementedByInstrument)
                                                
                                         WHERE {{
                                                 VALUES ?method {{ wd:{0} }}
                                                 OPTIONAL {{
                                                            ?method wdt:P ?impSoftraw.
                                                            ?impSoftraw wdt:P31 wd:Q7397.
  
                                                            BIND(replace( xsd:string(?impSoftraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?impSoft) 
                                                            
                                                            OPTIONAL {{
                                                                       ?impSoftraw rdfs:label ?impSoftlraw
                                                                       FILTER (lang(?impSoftlraw) = 'en')
                                                                     }}
                                                            
                                                            BIND(COALESCE(?impSoftlraw, "No Label Provided!") AS ?impSoftl)
                                                            
                                                            OPTIONAL {{
                                                                       ?impSoftraw schema:description ?impSoftdraw
                                                                       FILTER (lang(?impSoftdraw) = 'en')
                                                                     }}
                                                            
                                                            BIND(COALESCE(?impSoftdraw, "No Description Provided!") AS ?impSoftd)
                                                          }}
                                                          
                                                OPTIONAL {{
                                                            ?method wdt:P ?impInstraw.
                                                            ?impInstraw wdt:P31 wd:Q110994345.
                                                            
                                                            BIND(replace( xsd:string(?impInstraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?impInst) 
                                                            
                                                            OPTIONAL {{
                                                                       ?impInstraw rdfs:label ?impInstlraw
                                                                       FILTER (lang(?impInstlraw) = 'en')
                                                                     }}
                                                            
                                                            BIND(COALESCE(?impInstlraw, "No Label Provided!") AS ?impInstl)
                                                            
                                                            OPTIONAL {{
                                                                       ?impInstraw schema:description ?impInstdraw
                                                                       FILTER (lang(?impInstdraw) = 'en')
                                                                     }}
                                                            
                                                            BIND(COALESCE(?impInstdraw, "No Description Provided!") AS ?impInstd)
                                                          }}
                                               }}''',

                           'software':  '''SELECT ?sourceCodeRepository ?userManualURL ?reference
                                                  (GROUP_CONCAT(DISTINCT CONCAT(?pl, " | ", ?pll, " | ", ?pld); separator=" / ") AS ?programmedIn)
                                                  (GROUP_CONCAT(DISTINCT CONCAT(?dp, " | ", ?dpl, " | ", ?dpd); separator=" / ") AS ?dependsOnSoftware)
                                       
                                           WHERE {{

                                             VALUES ?software {{ wd:{0} }}
           
                                             # Get Programming Language
                                             OPTIONAL {{
                                                        ?software wdt:P277 ?plraw.
                                                        BIND(replace( xsd:string(?plraw),'http://www.wikidata.org/entity/','wikidata:') as ?pl) 
                                                        
                                                        OPTIONAL {{
                                                                   ?plraw rdfs:label ?pllraw
                                                                   FILTER (lang(?pllraw) = 'en')
                                                                 }}
                                                        
                                                        BIND(COALESCE(?pllraw, "No Label Provided!") AS ?pll)
                                                        
                                                        OPTIONAL {{
                                                                   ?plraw schema:description ?pldraw
                                                                   FILTER (lang(?pldraw) = 'en')
                                                                 }}
                                                        
                                                        BIND(COALESCE(?pldraw, "No Description Provided!") AS ?pld)
                                                      }}  
                                             
                                             # Get Dependencies
                                             OPTIONAL {{
                                                        ?software wdt:P1547 ?dpraw.
                                                        BIND(replace( xsd:string(?dpraw),'http://www.wikidata.org/entity/','wikidata:') as ?dp) 
                                                        
                                                        OPTIONAL {{
                                                                   ?dpraw rdfs:label ?dplraw
                                                                   FILTER (lang(?dplraw) = 'en')
                                                                 }}
                                                        
                                                        BIND(COALESCE(?dplraw, "No Label Provided!") AS ?dpl)
                                                        
                                                        OPTIONAL {{
                                                                   ?dpraw schema:description ?dpdraw
                                                                   FILTER (lang(?dpdraw) = 'en')
                                                                 }}
                                                        
                                                        BIND(COALESCE(?dpdraw, "No Description Provided!") AS ?dpd)
                                                      }}
           
                                             # Source Code Published
                                             OPTIONAL {{
                                                        ?software wdt:P1324 ?published.
                                                      }}
           
                                             # User Manual Documented
                                             OPTIONAL {{
                                                        ?software wdt:P2078 ?documented.
                                                      }}
                                             # DOI
                                             OPTIONAL {{
                                                        ?software wdt:P356 ?doi.
                                                      }}
                                             
                                             # SWMATH
                                             OPTIONAL {{
                                                        ?software wdt:P6830 ?swmath.
                                                      }}

                                             # URL
                                             OPTIONAL {{
                                                        ?software wdt:P2699 ?url.
                                                      }}

                                             BIND(
                                              CONCAT(
                                                  IF(BOUND(?doi), CONCAT("doi:", STR(?doi), " | "), ""),
                                                  IF(BOUND(?swmath), CONCAT("swmath:", STR(?swmath), " | "), ""),
                                                  IF(BOUND(?url), STR(?url), "")
                                              ) AS ?referenceraw
                                             )
                                          
                                             BIND(IF(STRENDS(?referenceraw, " | "), STRBEFORE(?referenceraw, " | "), ?referenceraw) AS ?reference)
           
                                            }}
                                           GROUP BY ?sourceCodeRepository ?userManualURL ?reference''',

                           'hardware': '''SELECT ?nodes ?cores
                                          (GROUP_CONCAT(DISTINCT CONCAT(?cpu, " | ", ?cpul, " | ", ?cpud); separator=" / ") AS ?CPU)
       
                                          WHERE {{

                                            VALUES ?hardware {{ wd:{0} }}

                                            # Get CPU
                                            OPTIONAL {{
                                                       ?hardware p:P880 ?statement.
                                                       ?statement ps:P880 ?cpuraw.
                                                       BIND(replace( xsd:string(?cpuraw),'http://www.wikidata.org/entity/','wikidata:') as ?cpu) 

                                                       OPTIONAL {{
                                                                  ?cpuraw rdfs:label ?cpulraw
                                                                  FILTER (lang(?cpulraw) = 'en')
                                                                }}

                                                       BIND(COALESCE(?cpulraw, "No Label Provided!") AS ?cpul)

                                                       OPTIONAL {{
                                                                  ?cpuraw schema:description ?cpudraw
                                                                  FILTER (lang(?cpudraw) = 'en')
                                                                }}

                                                       BIND(COALESCE(?cpudraw, "No Description Provided!") AS ?cpud)

                                                       OPTIONAL {{
                                                                  ?cpuraw wdt:P1141 ?cores.
                                                                }}

                                                       OPTIONAL {{
                                                                  ?statement pq:P1114 ?nodes.
                                                                }}
                                                     }}
                                                }}
                                                GROUP BY ?nodes ?cores ''',

                           'data-set':'''SELECT ?sizeValue ?sizeUnit ?sizeRecord ?fileFormat ?binaryOrText ?proprietary
                                                ?DOI ?URL ?publish ?archive ?endTime
                                                (GROUP_CONCAT(DISTINCT CONCAT(?datatype, " | ", ?datatypel, " | ", ?datatyped); separator=" / ") AS ?dataType)
                                                (GROUP_CONCAT(DISTINCT CONCAT(?representationformat, " | ", ?representationformatl, " | ", ?representationformatd); separator=" / ") AS ?representationFormat)
       
                                         WHERE {{

                                           VALUES ?dataset {{ wd:{0} }}
         
                                           # Get Size (bytes)
                                           OPTIONAL {{
                                                      ?dataset p:P3575 ?statementNode.          
                                                      ?statementNode psv:P3575 ?valueNode.      
                                                      ?valueNode wikibase:quantityAmount ?sizeValue; 
                                                                 wikibase:quantityUnit ?unit.
                                                      ?unit rdfs:label ?sizeUnit.
                                                      FILTER (lang(?sizeUnit) = 'en')
                                                    }}

                                           # Get Size (number of items)
                                           OPTIONAL {{
                                                      ?dataset wdt:P4876 ?sizeRecord
                                                    }}
         
                                           # Data Type
                                           OPTIONAL {{
                                                      ?dataset p:P2283 ?statement_dt.
                                                      ?statement_dt ps:P2283 ?datatyperaw. 
                                                      ?statement_dt pq:P3831 ?qualifier.
                                                      FILTER (?qualifier = wd:Q190087)
         
                                                      BIND(replace( xsd:string(?datatyperaw),'http://www.wikidata.org/entity/','wikidata:') as ?datatype)
                                                      
                                                      OPTIONAL {{
                                                                 ?datatyperaw rdfs:label ?datatypelraw
                                                                 FILTER (lang(?datatypelraw) = 'en')
                                                               }}
                                                      
                                                      BIND(COALESCE(?datatypelraw, "No Label Provided!") AS ?datatypel)
                                                      
                                                      OPTIONAL {{
                                                                 ?datatyperaw schema:description ?datatypedraw
                                                                 FILTER (lang(?datatypedraw) = 'en')
                                                               }}
                                                      
                                                      BIND(COALESCE(?datatypedraw, "No Description Provided!") AS ?datatyped)
                                                    }}  
           
                                           #Representation Format
                                           OPTIONAL {{
                                                      ?dataset p:P2283 ?statement_dt2.
                                                      ?statement_dt2 ps:P2283 ?representationformatraw. 
                                                      ?statement_dt2 pq:P3831 ?qualifier2.
                                                      FILTER (?qualifier2 = wd:)
         
                                                      BIND(replace( xsd:string(?representationformatraw),'http://www.wikidata.org/entity/','wikidata:') as ?representationformat)
                                                      
                                                      OPTIONAL {{
                                                                 ?representationformatraw rdfs:label ?representationformatlraw
                                                                 FILTER (lang(?representationformatlraw) = 'en')
                                                               }}
                                                      
                                                      BIND(COALESCE(?representationformatlraw, "No Label Provided!") AS ?representationformatl)
                                                      
                                                      OPTIONAL {{
                                                                 ?representationformatraw schema:description ?representationformatdraw
                                                                 FILTER (lang(?representationformatdraw) = 'en')
                                                               }}
                                                      
                                                      BIND(COALESCE(?representationformatdraw, "No Description Provided!") AS ?representationformatd)
                                                    }}
         
                                           # Get file extension
                                           OPTIONAL {{
                                                      ?dataset wdt:P1195 ?fileFormat
                                                    }}
                                               
                                           # Binary or Text
                                           BIND(IF(EXISTS {{ ?dataset wdt:P31 wd:Q4913888 }}, "binary", IF(EXISTS {{ ?dataset wdt:P31 wd:Q60476328 }}, "text", "" )) AS ?binaryOrText)
         
                                           # Proprietary
                                           BIND(IF(EXISTS {{ ?dataset wdt:P31 wd:Q123684347 }}, "Yes", IF(EXISTS {{ ?dataset wdt:P31 wd:Q309901 }}, "No", "" )) AS ?proprietary)
                                           
                                           # Bind DOI and URL if they exist
                                           OPTIONAL {{ ?dataset wdt:P356 ?DOI. }}
                                           OPTIONAL {{ ?dataset wdt:P2699 ?URL. }}
         
                                           # Data Publishing
                                           BIND(IF(EXISTS {{ ?dataset wdt:P4424 wd:Q17051824 }}, "Yes", "No") AS ?publish)
         
                                           # Data Archiving
                                           BIND(IF(EXISTS {{ ?dataset wdt:P4424 wd:Q17155735 }}, "YesText", "NoText") AS ?archive)
         
                                           OPTIONAL {{ ?dataset p:P4424 ?statementNode2.
                                                       ?statementNode2 ps:P4424 wd:Q17155735.
                                                       OPTIONAL {{
                                                                   ?statementNode2 pq:P582 ?endTime.
                                                                }}
                                                    }}
                                           }}    
                                           GROUP BY ?sizeValue ?sizeUnit ?sizeRecord ?fileFormat ?binaryOrText ?proprietary ?DOI ?URL ?publish ?archive ?endTime'''
            },
            'mathalgodb': {
                           'method': '''PREFIX prop: <https://mardi4nfdi.de/mathalgodb/0.1#>
                                        PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1/algorithm#>
                                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                          
                                        
                                        SELECT DISTINCT (GROUP_CONCAT(DISTINCT CONCAT(?imple, " | ", ?implel, " | ", ?impled); separator=" / ") AS ?implementedBySoftware)
                                                        
                                        WHERE {{
                                                VALUES ?idraw {{ :{0} }}
         
                                                OPTIONAL {{
                                                           ?idraw prop:implementedBy ?impleraw.
                                                           BIND(CONCAT("mathalgodb:", STRAFTER(STR(?impleraw), "#")) AS ?imple)
                                                           OPTIONAL {{ ?impleraw rdfs:label ?implelraw}}
                                                           BIND(COALESCE(?implelraw, "No Label Provided!") AS ?implel)
                                                           OPTIONAL {{ ?impleraw rdfs:comment ?impledraw}}
                                                           BIND(COALESCE(?impledraw, "No Description Provided!") AS ?impled)
                                                         }}
                                              }}''',

                           'software': '''PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1/software#>
                                          PREFIX dc: <http://purl.org/spar/datacite/>   
                                          
                                          SELECT DISTINCT (GROUP_CONCAT(DISTINCT ?referenceraw; separator=" | ") AS ?reference)
                                                          
                                          WHERE {{
                                                  VALUES ?idraw {{ :{0} }}
           
                                                  OPTIONAL {{ ?idraw dc:hasIdentifier ?referenceraw }}
           
                                                }}
                                          GROUP BY ?reference''' 
            }

}

queryProvider = {
                 'RT': '''SELECT DISTINCT (GROUP_CONCAT(DISTINCT CONCAT(?ta, " | ", ?tal, " | ", ?tad); separator=" / ") AS ?usedBy)
                                                       
                                       WHERE {{
                                         
                                          VALUES ?id {{wd:{0}}}

                                          OPTIONAL {{
                                                         ?id wdt:{used by} ?taraw.
                                                         BIND(replace( xsd:string(?taraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?ta)

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
                                            }}'''
}

queryPreview = {'basic': '''SELECT DISTINCT ?isSpaceContinuous ?isSpaceDiscrete
                                            ?isTimeContinuous ?isTimeDiscrete
                                                                 
                            WHERE {{
                              
                               VALUES ?id {{wd:{0}}}
                               
                               BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-space model} }}, "True", "False" ) AS ?isSpaceContinuous)
                               BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-space model} }}, "True", "False" ) AS ?isSpaceDiscrete)
                               
                               BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{continuous-time model} }}, "True", "False" ) AS ?isTimeContinuous)
                               BIND(IF(EXISTS {{ ?id wdt:{instance of} wd:{discrete-time model} }}, "True", "False" ) AS ?isTimeDiscrete)
                
                            }}
                            GROUP BY ?isSpaceContinuous ?isTimeContinuous ?isSpaceDiscrete ?isTimeDiscrete''',
                
                'variables': '''SELECT ?ID ?Name ?Unit ?Symbol ?label ?Type

                                WHERE {{ 

                                VALUES ?task {{{0}}}

                                OPTIONAL {{ ?task rdfs:label ?labelraw .
                                            FILTER (lang(?labelraw) = 'en') }}
                                BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)

                                # Define type based on connection type (Input or Output)
                                {{
                                    ?task p:{contains} ?statement.
                                    ?statement ps:{contains} ?idraw.
                                    ?statement pq:{object has role} ?role.
                                    FILTER (?role = wd:{input})
                                    BIND(replace( xsd:string(?idraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?ID)
                                    OPTIONAL {{ ?idraw rdfs:label ?Nameraw .
                                                FILTER (lang(?Nameraw) = 'en') }}
                                    BIND(COALESCE(?Nameraw, "No Label Provided!") AS ?Name)
                                    BIND("independent" AS ?Type)
                                }}
                                UNION
                                {{
                                    ?task p:{contains} ?statement.
                                    ?statement ps:{contains} ?idraw.
                                    ?statement pq:{object has role} ?role.
                                    FILTER (?role = wd:{output})
                                    BIND(replace( xsd:string(?idraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?ID)
                                    OPTIONAL {{ ?idraw rdfs:label ?Nameraw .
                                                FILTER (lang(?Nameraw) = 'en') }}
                                    BIND(COALESCE(?Nameraw, "No Label Provided!") AS ?Name)
                                    BIND("dependent" AS ?Type)
                                }}

                                # Filter results to only show defining statements that match the current quantity label
                                OPTIONAL {{
                                    ?task wdt:{contains} ?formulation.
                                    ?formulation wdt:{instance of} wd:{mathematical expression}.
                                    ?formulation p:{in defining formula} ?statement2.
                                    ?statement2 ps:{in defining formula} ?Symbol.
                                    ?statement2 pq:{symbol represents} ?quantityraw.
                                    BIND(replace( xsd:string(?quantityraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?quantity)
                                }}
                                
                                FILTER(?ID = ?quantity)       

                            # Initialize the Unit variable as empty
                            BIND("" AS ?Unit)
                            }}
                            ORDER BY ?label ?Type''',

                'parameters': '''SELECT ?Name ?Unit ?Symbol ?label

                                WHERE {{ 

                                VALUES ?task {{{0}}}

                                OPTIONAL {{ ?task rdfs:label ?labelraw .
                                            FILTER (lang(?labelraw) = 'en') }}
                                BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)

                                # Define type based on connection type (Input or Output)
                                
                                    ?task p:{contains} ?statement.
                                    ?statement ps:{contains} ?idraw.
                                    ?statement pq:{object has role} ?role.
                                    FILTER (?role = wd:{parameter})
                                    BIND(replace( xsd:string(?idraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?ID)
                                    OPTIONAL {{ ?idraw rdfs:label ?Nameraw .
                                                FILTER (lang(?Nameraw) = 'en') }}
                                    BIND(COALESCE(?Nameraw, "No Label Provided!") AS ?Name)
                                
                                
                                # Filter results to only show defining statements that match the current quantity label
                                OPTIONAL {{
                                    ?task wdt:{contains} ?formulation.
                                    ?formulation wdt:{instance of} wd:{mathematical expression}.
                                    ?formulation p:{in defining formula} ?statement2.
                                    ?statement2 ps:{in defining formula} ?Symbol.
                                    ?statement2 pq:{symbol represents} ?quantityraw.
                                    BIND(replace( xsd:string(?quantityraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?quantity)
                                }}
                                
                                FILTER(?ID = ?quantity)       

                            # Initialize the Unit variable as empty
                            BIND("" AS ?Unit)
                            }}
                            ORDER BY ?label'''
}