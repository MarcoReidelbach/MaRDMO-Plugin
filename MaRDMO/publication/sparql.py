#Queries to MaRDI KG and Wikidata for Publication Handler

queryPublication = {

        'MaRDIDOI': '''PREFIX wdt:<https://portal.mardi4nfdi.de/prop/direct/> 
                       PREFIX wd:<https://portal.mardi4nfdi.de/entity/>
                        
                       SELECT ?id ?label ?description         
                        
                 WHERE {{?idraw wdt:P27 "{0}".
                        BIND(CONCAT("mardi:", STRAFTER(STR(?idraw), STR(wd:))) AS ?id)
                        
                        OPTIONAL {{?idraw rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?idraw schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                       }}''',
    
       'All_MaRDILabel': '''PREFIX wdt:<https://portal.mardi4nfdi.de/prop/direct/> 
                            PREFIX wd:<https://portal.mardi4nfdi.de/entity/>
                        
                            SELECT ?label ?description ?doi         
                            (GROUP_CONCAT(DISTINCT(?authorInfo); separator=" | ") AS ?authorInfos) 
                            (GROUP_CONCAT(DISTINCT CONCAT(?inv, " | ", ?invl, " | ", ?invd); separator=" / ") AS ?invents)    
                            (GROUP_CONCAT(DISTINCT CONCAT(?doc, " | ", ?docl, " | ", ?docd); separator=" / ") AS ?documents)
                            (GROUP_CONCAT(DISTINCT CONCAT(?rev, " | ", ?revl, " | ", ?revd); separator=" / ") AS ?surveys)
                            (GROUP_CONCAT(DISTINCT CONCAT(?use, " | ", ?usel, " | ", ?used); separator=" / ") AS ?uses)                                                   
                            ?entrytypelabel ?journalInfo ?languagelabel                               
                            ?title ?date ?volume ?issue ?page          

                 WHERE {{ VALUES ?publication {{ wd:{} }}

                        OPTIONAL {{
                                       ?invraw p:P286 ?statement1.
                                       ?statement1 ps:P286 ?publication.

                                       BIND(replace( xsd:string(?invraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?inv)
                                       
                                       OPTIONAL {{
                                                  ?invraw rdfs:label ?invlraw.
                                                  FILTER (lang(?invlraw) = 'en')
                                               }}
                                      BIND(COALESCE(?invlraw, "No Label Provided!") AS ?invl)
                                      
                                      OPTIONAL {{
                                                 ?invraw schema:description ?invdraw
                                                 FILTER (lang(?invdraw) = 'en')
                                               }}
                                      BIND(COALESCE(?invdraw, "No Description Provided!") AS ?invd)
                                      
                                      ?statement1 pq:P560 wd:Q6672344.
                                   }}

                        OPTIONAL {{
                                       ?docraw p:P286 ?statement2.
                                       ?statement2 ps:P286 ?publication.

                                       BIND(replace( xsd:string(?docraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?doc)
                                       
                                       OPTIONAL {{
                                                  ?docraw rdfs:label ?doclraw.
                                                  FILTER (lang(?doclraw) = 'en')
                                               }}
                                      BIND(COALESCE(?doclraw, "No Label Provided!") AS ?docl)
                                      
                                      OPTIONAL {{
                                                 ?docraw schema:description ?docdraw
                                                 FILTER (lang(?docdraw) = 'en')
                                               }}
                                      BIND(COALESCE(?docdraw, "No Description Provided!") AS ?docd)
                                      
                                      ?statement2 pq:P560 wd:Q6672349.
                                   }}

                        OPTIONAL {{
                                       ?revraw p:P286 ?statement3.
                                       ?statement3 ps:P286 ?publication.

                                       BIND(replace( xsd:string(?revraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?rev)
                                       
                                       OPTIONAL {{
                                                  ?revraw rdfs:label ?revlraw.
                                                  FILTER (lang(?revlraw) = 'en')
                                               }}
                                      BIND(COALESCE(?revlraw, "No Label Provided!") AS ?revl)
                                      
                                      OPTIONAL {{
                                                 ?revraw schema:description ?revdraw
                                                 FILTER (lang(?revdraw) = 'en')
                                               }}
                                      BIND(COALESCE(?revdraw, "No Description Provided!") AS ?revd)
                                      
                                      ?statement3 pq:P560 wd:Q6672366.
                                   }}

                        OPTIONAL {{
                                       ?useraw p:P286 ?statement4.
                                       ?statement4 ps:P286 ?publication.

                                       BIND(replace( xsd:string(?useraw),'https://portal.mardi4nfdi.de/entity/','mardi:') as ?use)
                                       
                                       OPTIONAL {{
                                                  ?useraw rdfs:label ?uselraw.
                                                  FILTER (lang(?uselraw) = 'en')
                                               }}
                                      BIND(COALESCE(?uselraw, "No Label Provided!") AS ?usel)
                                      
                                      OPTIONAL {{
                                                 ?useraw schema:description ?usedraw
                                                 FILTER (lang(?usedraw) = 'en')
                                               }}
                                      BIND(COALESCE(?usedraw, "No Description Provided!") AS ?used)
                                      
                                      ?statement4 pq:P560 wd:Q6480405.
                                   }}
                 
                        OPTIONAL {{ ?publication wdt:P27 ?doi. }}
                        
                        OPTIONAL {{?publication rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?publication schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                        
                        OPTIONAL {{?publication (wdt:P16 | wdt:P43) ?authorraw.
                                  BIND(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("mardi:", STRAFTER(STR(?authorraw), STR(wd:))), "") AS ?author)
     
                                  OPTIONAL {{?authorraw rdfs:label ?authorlabelraw.
                                            FILTER (lang(?authorlabelraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorlabelraw, ?authorraw), "") AS ?authorlabel)
   
                                  OPTIONAL {{?authorraw schema:description ?authordescriptionraw.
                                            FILTER (lang(?authordescriptionraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authordescriptionraw, ""), "") AS ?authordescription)
   
                                  OPTIONAL {{?authorraw wdt:P20 ?authororcidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authororcidraw, ""), "") AS ?authororcid)
                          
                                  OPTIONAL {{?authorraw wdt:P12 ?authorwikidataidraw}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorwikidataidraw), STR(wd:))), ""), "") AS ?authorwikidataid)
   
                                  OPTIONAL {{?authorraw wdt:P676 ?authorzbmathidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorzbmathidraw, ""), "") AS ?authorzbmathid)
     
                                  BIND(CONCAT(?author, " <|> ", ?authorlabel, " <|> ", ?authordescription, " <|> ", ?authororcid, " <|> ", ?authorzbmathid, " <|> ", ?authorwikidataid) AS ?authorInfo)}}
   
                        OPTIONAL {{?publication wdt:P31 ?entrytyperaw.
                                  
                                   OPTIONAL {{?entrytyperaw rdfs:label ?entrytypelabelraw.
                                            FILTER (lang(?entrytypelabelraw) = 'en')}}
                                   BIND(COALESCE(?entrytypelabelraw, "No Label Provided!") As ?entrytypelabel)
                                  }}
                        
                        OPTIONAL {{?publication wdt:P200 ?journalraw.
                                  BIND(CONCAT("mardi:", STRAFTER(STR(?journalraw), STR(wd:))) AS ?journal)
                                  
                                  OPTIONAL {{?journalraw rdfs:label ?journallabelraw.
                                            FILTER (lang(?journallabelraw) = 'en')}}
                                  BIND(COALESCE(?journallabelraw, "No Label Provided!") As ?journallabel)
                                  
                                  OPTIONAL {{?journalraw schema:description ?journaldescriptionraw.
                                            FILTER (lang(?journaldescriptionraw) = 'en')}}
                                  BIND(COALESCE(?journaldescriptionraw, "No Description Provided!") As ?journaldescription)
                                  
                                  BIND(concat(?journal, " <|> ", ?journallabel, " <|> ", ?journaldescription) AS ?journalInfo)}}
                        
                        OPTIONAL {{?publication wdt:P34 ?languageraw.
                                   
                                   OPTIONAL {{?languageraw rdfs:label ?languagelabelraw.
                                              FILTER (lang(?languagelabelraw) = 'en')}}
                                   BIND(COALESCE(?languagelabelraw, "No Label Provided!") As ?languagelabel)}}
                        
                        OPTIONAL {{?publication wdt:P159 ?titleraw.
                                   BIND(COALESCE(?titleraw, "No Title Provided!") As ?title)}}
                        
                        OPTIONAL {{?publication wdt:P28 ?dateraw.
                                   BIND(COALESCE(?dateraw, "No Publication Date Provided!") As ?date)}}
                        
                        OPTIONAL {{?publication wdt:P26 ?volumeraw.
                                   BIND(COALESCE(?volumeraw, "No Volume Provided!") As ?volume)}}
                        
                        OPTIONAL {{?publication wdt:P25 ?issueraw.
                                   BIND(COALESCE(?issueraw, "No Issue Provided!") As ?issue)}}
                        
                        OPTIONAL {{?publication wdt:P128 ?pageraw.
                                   BIND(COALESCE(?pageraw, "No Pages Provided!") As ?page)}}
                        }}
   
                 GROUP BY ?doi ?label ?description ?entrytypelabel ?journalInfo ?languagelabel ?title ?date ?volume ?issue ?page ''',
    
       'All_MaRDI': '''PREFIX wdt:<https://portal.mardi4nfdi.de/prop/direct/> 
                       PREFIX wd:<https://portal.mardi4nfdi.de/entity/>
                       
                         SELECT ?id ?label ?description         
                        (GROUP_CONCAT(DISTINCT(?authorInfo); separator=" | ") AS ?authorInfos)                                                        
                        ?entrytypelabel ?journalInfo ?languagelabel                               
                        ?title ?date ?volume ?issue ?page          

                 WHERE {{?idraw wdt:P27 "{0}".
                        BIND(CONCAT("mardi:", STRAFTER(STR(?idraw), STR(wd:))) AS ?id)
                        
                        OPTIONAL {{?idraw rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?idraw schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                        
                        OPTIONAL {{?idraw (wdt:P16 | wdt:P43) ?authorraw.
                                  BIND(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("mardi:", STRAFTER(STR(?authorraw), STR(wd:))), "") AS ?author)
     
                                  OPTIONAL {{?authorraw rdfs:label ?authorlabelraw.
                                            FILTER (lang(?authorlabelraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorlabelraw, ?authorraw), "") AS ?authorlabel)
   
                                  OPTIONAL {{?authorraw schema:description ?authordescriptionraw.
                                            FILTER (lang(?authordescriptionraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authordescriptionraw, ""), "") AS ?authordescription)
   
                                  OPTIONAL {{?authorraw wdt:P20 ?authororcidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authororcidraw, ""), "") AS ?authororcid)
                          
                                  OPTIONAL {{?authorraw wdt:P12 ?authorwikidataidraw}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorwikidataidraw), STR(wd:))), ""), "") AS ?authorwikidataid)
   
                                  OPTIONAL {{?authorraw wdt:P676 ?authorzbmathidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorzbmathidraw, ""), "") AS ?authorzbmathid)
     
                                  BIND(CONCAT(?author, " <|> ", ?authorlabel, " <|> ", ?authordescription, " <|> ", ?authororcid, " <|> ", ?authorzbmathid, " <|> ", ?authorwikidataid) AS ?authorInfo)}}
   
                        OPTIONAL {{?idraw wdt:P31 ?entrytyperaw.
                                  
                                   OPTIONAL {{?entrytyperaw rdfs:label ?entrytypelabelraw.
                                            FILTER (lang(?entrytypelabelraw) = 'en')}}
                                   BIND(COALESCE(?entrytypelabelraw, "No Label Provided!") As ?entrytypelabel)
                                  }}
                        
                        OPTIONAL {{?idraw wdt:P200 ?journalraw.
                                  BIND(CONCAT("mardi:", STRAFTER(STR(?journalraw), STR(wd:))) AS ?journal)
                                  
                                  OPTIONAL {{?journalraw rdfs:label ?journallabelraw.
                                            FILTER (lang(?journallabelraw) = 'en')}}
                                  BIND(COALESCE(?journallabelraw, "No Label Provided!") As ?journallabel)
                                  
                                  OPTIONAL {{?journalraw schema:description ?journaldescriptionraw.
                                            FILTER (lang(?journaldescriptionraw) = 'en')}}
                                  BIND(COALESCE(?journaldescriptionraw, "No Description Provided!") As ?journaldescription)
                                  
                                  BIND(concat(?journal, " <|> ", ?journallabel, " <|> ", ?journaldescription) AS ?journalInfo)}}
                        
                        OPTIONAL {{?idraw wdt:P34 ?languageraw.
                                   
                                   OPTIONAL {{?languageraw rdfs:label ?languagelabelraw.
                                              FILTER (lang(?languagelabelraw) = 'en')}}
                                   BIND(COALESCE(?languagelabelraw, "No Label Provided!") As ?languagelabel)}}
                        
                        OPTIONAL {{?idraw wdt:P159 ?titleraw.
                                   BIND(COALESCE(?titleraw, "No Title Provided!") As ?title)}}
                        
                        OPTIONAL {{?idraw wdt:P28 ?dateraw.
                                   BIND(COALESCE(?dateraw, "No Publication Date Provided!") As ?date)}}
                        
                        OPTIONAL {{?idraw wdt:P26 ?volumeraw.
                                   BIND(COALESCE(?volumeraw, "No Volume Provided!") As ?volume)}}
                        
                        OPTIONAL {{?idraw wdt:P25 ?issueraw.
                                   BIND(COALESCE(?issueraw, "No Issue Provided!") As ?issue)}}
                        
                        OPTIONAL {{?idraw wdt:P128 ?pageraw.
                                   BIND(COALESCE(?pageraw, "No Pages Provided!") As ?page)}}
                        }}
   
                 GROUP BY ?id ?label ?description ?entrytypelabel ?journalInfo ?languagelabel ?title ?date ?volume ?issue ?page ''',

       'WikidataDOI': '''SELECT ?doi         
                        
                 WHERE {{ 
                         OPTIONAL {{ {1} wdt:P{0} ?doi. }}
                       }}''',
       
       'All_WikidataLabel': '''SELECT ?label ?description ?doi         
                        (GROUP_CONCAT(DISTINCT(?authorInfo); separator=" | ") AS ?authorInfos)                                                        
                        ?entrytypelabel ?journalInfo ?languagelabel                               
                        ?title ?date ?volume ?issue ?page          

                 WHERE {{ VALUES ?publication {{ wd:{0} }}
                 
                        OPTIONAL {{ ?publication wdt:P356 ?doi. }}

                        OPTIONAL {{?publication rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?publication schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                        
                        OPTIONAL {{?publication (wdt:P50 | wdt:P2093) ?authorraw.
                                  BIND(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorraw), STR(wd:))), "") AS ?author)
     
                                  OPTIONAL {{?authorraw rdfs:label ?authorlabelraw.
                                            FILTER (lang(?authorlabelraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorlabelraw, ?authorraw), "") AS ?authorlabel)
   
                                  OPTIONAL {{?authorraw schema:description ?authordescriptionraw.
                                            FILTER (lang(?authordescriptionraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authordescriptionraw, ""), "") AS ?authordescription)
   
                                  OPTIONAL {{?authorraw wdt:P496 ?authororcidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authororcidraw, ""), "") AS ?authororcid)
                          
                                  OPTIONAL {{?authorraw wdt:P ?authorwikidataidraw}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorwikidataidraw), STR(wd:))), ""), "") AS ?authorwikidataid)
   
                                  OPTIONAL {{?authorraw wdt:P1556 ?authorzbmathidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorzbmathidraw, ""), "") AS ?authorzbmathid)
     
                                  BIND(CONCAT(?author, " <|> ", ?authorlabel, " <|> ", ?authordescription, " <|> ", ?authororcid, " <|> ", ?authorzbmathid, " <|> ", ?authorwikidataid) AS ?authorInfo)}}
   
                        OPTIONAL {{?publication wdt:P31 ?entrytyperaw.
                                  
                                   OPTIONAL {{?entrytyperaw rdfs:label ?entrytypelabelraw.
                                            FILTER (lang(?entrytypelabelraw) = 'en')}}
                                   BIND(COALESCE(?entrytypelabelraw, "No Label Provided!") As ?entrytypelabel)
                                  }}
                        
                        OPTIONAL {{?publication wdt:P1433 ?journalraw.
                                  BIND(CONCAT("wikidata:", STRAFTER(STR(?journalraw), STR(wd:))) AS ?journal)
                                  
                                  OPTIONAL {{?journalraw rdfs:label ?journallabelraw.
                                            FILTER (lang(?journallabelraw) = 'en')}}
                                  BIND(COALESCE(?journallabelraw, "No Label Provided!") As ?journallabel)
                                  
                                  OPTIONAL {{?journalraw schema:description ?journaldescriptionraw.
                                            FILTER (lang(?journaldescriptionraw) = 'en')}}
                                  BIND(COALESCE(?journaldescriptionraw, "No Description Provided!") As ?journaldescription)
                                  
                                  BIND(concat(?journal, " <|> ", ?journallabel, " <|> ", ?journaldescription) AS ?journalInfo)}}
                        
                        OPTIONAL {{?publication wdt:P407 ?languageraw.
                                   
                                   OPTIONAL {{?languageraw rdfs:label ?languagelabelraw.
                                              FILTER (lang(?languagelabelraw) = 'en')}}
                                   BIND(COALESCE(?languagelabelraw, "No Label Provided!") As ?languagelabel)}}
                        
                        OPTIONAL {{?publication wdt:P1476 ?titleraw.
                                   BIND(COALESCE(?titleraw, "No Title Provided!") As ?title)}}
                        
                        OPTIONAL {{?publication wdt:P577 ?dateraw.
                                   BIND(COALESCE(?dateraw, "No Publication Date Provided!") As ?date)}}
                        
                        OPTIONAL {{?publication wdt:P478 ?volumeraw.
                                   BIND(COALESCE(?volumeraw, "No Volume Provided!") As ?volume)}}
                        
                        OPTIONAL {{?publication wdt:P433 ?issueraw.
                                   BIND(COALESCE(?issueraw, "No Issue Provided!") As ?issue)}}
                        
                        OPTIONAL {{?publication wdt:P304 ?pageraw.
                                   BIND(COALESCE(?pageraw, "No Pages Provided!") As ?page)}}
                        }}
   
                 GROUP BY ?doi ?label ?description ?entrytypelabel ?journalInfo ?languagelabel ?title ?date ?volume ?issue ?page ''',

       'All_Wikidata': '''SELECT ?id ?label ?description         
                        (GROUP_CONCAT(DISTINCT(?authorInfo); separator=" | ") AS ?authorInfos)                                                        
                        ?entrytypelabel ?journalInfo ?languagelabel                               
                        ?title ?date ?volume ?issue ?page          

                 WHERE {{?idraw wdt:P356 "{0}".
                        BIND(CONCAT("wikidata:", STRAFTER(STR(?idraw), STR(wd:))) AS ?id)

                        OPTIONAL {{?idraw rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?idraw schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                        
                        OPTIONAL {{?idraw (wdt:P50 | wdt:P2093) ?authorraw.
                                  BIND(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorraw), STR(wd:))), "") AS ?author)
     
                                  OPTIONAL {{?authorraw rdfs:label ?authorlabelraw.
                                            FILTER (lang(?authorlabelraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorlabelraw, ?authorraw), "") AS ?authorlabel)
   
                                  OPTIONAL {{?authorraw schema:description ?authordescriptionraw.
                                            FILTER (lang(?authordescriptionraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authordescriptionraw, ""), "") AS ?authordescription)
   
                                  OPTIONAL {{?authorraw wdt:P496 ?authororcidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authororcidraw, ""), "") AS ?authororcid)
                          
                                  OPTIONAL {{?authorraw wdt:P ?authorwikidataidraw}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorwikidataidraw), STR(wd:))), ""), "") AS ?authorwikidataid)
   
                                  OPTIONAL {{?authorraw wdt:P1556 ?authorzbmathidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorzbmathidraw, ""), "") AS ?authorzbmathid)
     
                                  BIND(CONCAT(?author, " <|> ", ?authorlabel, " <|> ", ?authordescription, " <|> ", ?authororcid, " <|> ", ?authorzbmathid, " <|> ", ?authorwikidataid) AS ?authorInfo)}}
   
                        OPTIONAL {{?idraw wdt:P31 ?entrytyperaw.
                                  
                                   OPTIONAL {{?entrytyperaw rdfs:label ?entrytypelabelraw.
                                            FILTER (lang(?entrytypelabelraw) = 'en')}}
                                   BIND(COALESCE(?entrytypelabelraw, "No Label Provided!") As ?entrytypelabel)
                                  }}
                        
                        OPTIONAL {{?idraw wdt:P1433 ?journalraw.
                                  BIND(CONCAT("wikidata:", STRAFTER(STR(?journalraw), STR(wd:))) AS ?journal)
                                  
                                  OPTIONAL {{?journalraw rdfs:label ?journallabelraw.
                                            FILTER (lang(?journallabelraw) = 'en')}}
                                  BIND(COALESCE(?journallabelraw, "No Label Provided!") As ?journallabel)
                                  
                                  OPTIONAL {{?journalraw schema:description ?journaldescriptionraw.
                                            FILTER (lang(?journaldescriptionraw) = 'en')}}
                                  BIND(COALESCE(?journaldescriptionraw, "No Description Provided!") As ?journaldescription)
                                  
                                  BIND(concat(?journal, " <|> ", ?journallabel, " <|> ", ?journaldescription) AS ?journalInfo)}}
                        
                        OPTIONAL {{?idraw wdt:P407 ?languageraw.
                                   
                                   OPTIONAL {{?languageraw rdfs:label ?languagelabelraw.
                                              FILTER (lang(?languagelabelraw) = 'en')}}
                                   BIND(COALESCE(?languagelabelraw, "No Label Provided!") As ?languagelabel)}}
                        
                        OPTIONAL {{?idraw wdt:P1476 ?titleraw.
                                   BIND(COALESCE(?titleraw, "No Title Provided!") As ?title)}}
                        
                        OPTIONAL {{?idraw wdt:P577 ?dateraw.
                                   BIND(COALESCE(?dateraw, "No Publication Date Provided!") As ?date)}}
                        
                        OPTIONAL {{?idraw wdt:P478 ?volumeraw.
                                   BIND(COALESCE(?volumeraw, "No Volume Provided!") As ?volume)}}
                        
                        OPTIONAL {{?idraw wdt:P433 ?issueraw.
                                   BIND(COALESCE(?issueraw, "No Issue Provided!") As ?issue)}}
                        
                        OPTIONAL {{?idraw wdt:P304 ?pageraw.
                                   BIND(COALESCE(?pageraw, "No Pages Provided!") As ?page)}}
                        }}
   
                 GROUP BY ?id ?label ?description ?entrytypelabel ?journalInfo ?languagelabel ?title ?date ?volume ?issue ?page ''',

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


       'authors': '''SELECT (GROUP_CONCAT(DISTINCT(?authorInfo); separator=" | ") AS ?authorInfos)
                          WHERE {{
                            {{
                              ?authorraw wdt:P{2} ?orcid .
                              BIND(STRAFTER(STR(?authorraw), STR(wd:)) AS ?author)
                              VALUES ?orcid {{{0}}}
                            }}
                            UNION
                            {{
                              ?authorraw wdt:P{3} ?zbmathid .
                              BIND(STRAFTER(STR(?authorraw), STR(wd:)) AS ?author)
                              VALUES ?zbmathid {{{1}}}
                            }}

                            OPTIONAL {{?authorraw rdfs:label ?labelraw.
                                       FILTER (lang(?labelraw) = 'en')}}
                            BIND(COALESCE(?labelraw, "") AS ?label)

                            OPTIONAL {{?authorraw schema:description ?descriptionraw.
                                       FILTER (lang(?descriptionraw) = 'en')}}
                            BIND(COALESCE(?descriptionraw, "") AS ?description)

                            OPTIONAL {{?authorraw wdt:P{4} ?wikidataidraw}}
                            BIND(COALESCE(?wikidataidraw, "") AS ?wikidataid)
                            
                            OPTIONAL {{?authorraw wdt:P{2} ?ORCIDRAW}}
                            BIND(COALESCE(?ORCIDRAW, "") AS ?ORCID)
                            
                            OPTIONAL {{?authorraw wdt:P{3} ?ZBMATHIDRAW}}
                            BIND(COALESCE(?ZBMATHIDRAW, "") AS ?ZBMATHID)

                            BIND(CONCAT(?author, " <|> ", ?label, " <|> ", ?description, " <|> ", ?ORCID, " <|> ", ?ZBMATHID, " <|> ", ?wikidataid) AS ?authorInfo)

                            }}''',

       'journal': '''SELECT ?journalInfos
                           WHERE {{
                               
                               ?journalraw wdt:P{1} "{0}".
                               BIND(STRAFTER(STR(?journalraw),STR(wd:)) AS ?journal).
                               
                               OPTIONAL {{?journalraw rdfs:label ?journallabelraw.
                                         FILTER (lang(?journallabelraw) = 'en')}}
                               BIND(COALESCE(?journallabelraw, "No Label Provided!") As ?journallabel)
                               
                               OPTIONAL {{?journalraw schema:description ?journaldescriptionraw.
                                         FILTER (lang(?journaldescriptionraw) = 'en')}}
                               BIND(COALESCE(?journaldescriptionraw, "No Description Provided!") As ?journaldescription)
                               
                               BIND(concat(?journal, " <|> ", ?journallabel, " <|> ", ?journaldescription) AS ?journalInfos)
 
                             }}''',

      'PublicationMathAlgoDBLabel': '''PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1/publication#>
                                   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                   PREFIX dc: <http://purl.org/spar/datacite/>
                                   
                                   SELECT DISTINCT ?label ?doi
                                   WHERE {{
                                           OPTIONAL {{ {0} rdfs:label ?labelraw. }}
                                           BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                                           OPTIONAL {{ {0} dc:hasIdentifier ?doiraw 
                                                        BIND(STRAFTER(STR(?doiraw), ":") AS ?doi) }}
                                           
                                   }}''',
       
       'PublicationMathAlgoDB': '''PREFIX pb: <https://mardi4nfdi.de/mathalgodb/0.1/publication#>
                                   PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1#>
                                   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                   PREFIX dc: <http://purl.org/spar/datacite/>

                                  SELECT DISTINCT ?id ?label ?description ?doi
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?appliesentity, " | ", ?appliesentitylabel, " | ", ?appliesentitydescription)); SEPARATOR=" / ") AS ?applies)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?analyzesentity, " | ", ?analyzesentitylabel, " | ", ?analyzesentitydescription)); SEPARATOR=" / ") AS ?analyzes)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?documentsentity, " | ", ?documentsentitylabel, " | ", ?documentsentitydescription, " | ", ?documentsentityclass)); SEPARATOR=" / ") AS ?documents)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?inventsentity, " | ", ?inventsentitylabel, " | ", ?inventsentitydescription)); SEPARATOR=" / ") AS ?invents)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?studiesentity, " | ", ?studiesentitylabel, " | ", ?studiesentitydescription)); SEPARATOR=" / ") AS ?studies)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?surveysentity, " | ", ?surveysentitylabel, " | ", ?surveysentitydescription)); SEPARATOR=" / ") AS ?surveys)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?usesentity, " | ", ?usesentitylabel, " | ", ?usesentitydescription, " | ", ?usesentityclass)); SEPARATOR=" / ") AS ?uses)
                                                                                    
                                  WHERE {{
                                          VALUES ?idraw {{ pb:{0} }}

                                          ?idraw a :publication.
                                          BIND(CONCAT("mathalgodb:", STRAFTER(STR(?idraw), "#")) AS ?id)
    
                                          OPTIONAL {{?idraw dc:hasIdentifier ?doiraw 
                                                        BIND(STRAFTER(STR(?doiraw), ":") AS ?doi) }}

                                          OPTIONAL {{?idraw rdfs:label ?labelraw.}}
                                          BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)

                                          OPTIONAL {{?idraw rdfs:comment ?descriptionraw.}}
                                          BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)

                                          OPTIONAL {{?idraw :applies ?appliesentityraw.
                                                     BIND(CONCAT("mathalgodb:", STRAFTER(STR(?appliesentityraw), "#")) AS ?appliesentity)

                                                     OPTIONAL {{?appliesentityraw rdfs:label ?appliesentitylabelraw.}}
                                                     BIND(COALESCE(?appliesentitylabelraw, "No Label Provided!") As ?appliesentitylabel)

                                                     OPTIONAL {{?appliesentityraw rdfs:comment ?appliesentitydescriptionraw.}}
                                                     BIND(COALESCE(?appliesentitydescriptionraw, "No Description Provided!") As ?appliesentitydescription)
                                                   }}

                                          OPTIONAL {{?idraw :analyzes ?analyzesentityraw.
                                                     BIND(CONCAT("mathalgodb:", STRAFTER(STR(?analyzesentityraw), "#")) AS ?analyzesentity)

                                                     OPTIONAL {{?analyzesentityraw rdfs:label ?analyzesentitylabelraw.}}
                                                     BIND(COALESCE(?analyzesentitylabelraw, "No Label Provided!") As ?analyzesentitylabel)

                                                     OPTIONAL {{?analyzesentityraw rdfs:comment ?analyzesentitydescriptionraw.}}
                                                     BIND(COALESCE(?analyzesentitydescriptionraw, "No Description Provided!") As ?analyzesentitydescription)
                                                   }}

                                          OPTIONAL {{?idraw :documents ?documentsentityraw.
                                                     BIND(CONCAT("mathalgodb:", STRAFTER(STR(?documentsentityraw), "#")) AS ?documentsentity)

                                                     ?documentsentityraw a ?documentsentityclassraw.
                                                     BIND(STRAFTER(STR(?documentsentityclassraw), "#") AS ?documentsentityclass)
                                                     FILTER (?documentsentityclassraw IN (:benchmark, :software))

                                                     OPTIONAL {{?documentsentityraw rdfs:label ?documentsentitylabelraw.}}
                                                     BIND(COALESCE(?documentsentitylabelraw, "No Label Provided!") As ?documentsentitylabel)

                                                     OPTIONAL {{?documentsentityraw rdfs:comment ?documentsentitydescriptionraw.}}
                                                     BIND(COALESCE(?documentsentitydescriptionraw, "No Description Provided!") As ?documentsentitydescription)
                                                   }}

                                          OPTIONAL {{?idraw :invents ?inventsentityraw.
                                                     BIND(CONCAT("mathalgodb:", STRAFTER(STR(?inventsentityraw), "#")) AS ?inventsentity)

                                                     OPTIONAL {{?inventsentityraw rdfs:label ?inventsentitylabelraw.}}
                                                     BIND(COALESCE(?inventsentitylabelraw, "No Label Provided!") As ?inventsentitylabel)

                                                     OPTIONAL {{?inventsentityraw rdfs:comment ?inventsentitydescriptionraw.}}
                                                     BIND(COALESCE(?inventsentitydescriptionraw, "No Description Provided!") As ?inventsentitydescription)
                                                   }}

                                          OPTIONAL {{?idraw :studies ?studiesentityraw.
                                                     BIND(CONCAT("mathalgodb:", STRAFTER(STR(?studiesentityraw), "#")) AS ?studiesentity)

                                                     OPTIONAL {{?studiesentityraw rdfs:label ?studiesentitylabelraw.}}
                                                     BIND(COALESCE(?studiesentitylabelraw, "No Label Provided!") As ?studiesentitylabel)

                                                     OPTIONAL {{?studiesentityraw rdfs:comment ?studiesentitydescriptionraw.}}
                                                     BIND(COALESCE(?studiesentitydescriptionraw, "No Description Provided!") As ?studiesentitydescription)
                                                   }}

                                          OPTIONAL {{?idraw :reviews ?surveysentityraw.
                                                     BIND(CONCAT("mathalgodb:", STRAFTER(STR(?surveysentityraw), "#")) AS ?surveysentity)

                                                     OPTIONAL {{?surveysentityraw rdfs:label ?surveysentitylabelraw.}}
                                                     BIND(COALESCE(?surveysentitylabelraw, "No Label Provided!") As ?surveysentitylabel)

                                                     OPTIONAL {{?surveysentityraw rdfs:comment ?surveysentitydescriptionraw.}}
                                                     BIND(COALESCE(?surveysentitydescriptionraw, "No Description Provided!") As ?surveysentitydescription)
                                                   }}

                                          OPTIONAL {{?idraw :uses ?usesentityraw.
                                                     BIND(CONCAT("mathalgodb:", STRAFTER(STR(?usesentityraw), "#")) AS ?usesentity)

                                                     ?usesentityraw a ?usesentityclassraw.
                                                     BIND(STRAFTER(STR(?usesentityclassraw), "#") AS ?usesentityclass)
                                                     FILTER (?usesentityclass IN (:benchmark, :software))

                                                     OPTIONAL {{?usesentityraw rdfs:label ?usesentitylabelraw.}}
                                                     BIND(COALESCE(?usesentitylabelraw, "No Label Provided!") As ?usesentitylabel)

                                                     OPTIONAL {{?usesentityraw rdfs:comment ?usesentitydescriptionraw.}}
                                                     BIND(COALESCE(?usesentitydescriptionraw, "No Description Provided!") As ?usesentitydescription)
                                                   }}
                                        }}
                                  GROUP BY ?id ?label ?description ?doi''',

                'PublicationMathAlgoDBDOI': '''PREFIX pb: <https://mardi4nfdi.de/mathalgodb/0.1/publication#>
                                   PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1#>
                                   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                                   PREFIX dc: <http://purl.org/spar/datacite/>

                                  SELECT DISTINCT ?id ?label ?description
                                                                                    
                                  WHERE {{
                                          ?idraw a :publication.
                                          ?idraw dc:hasIdentifier ?doi
                                          FILTER(LCASE(STR(?doi)) = LCASE("doi:{0}"))

                                          BIND(CONCAT("mathalgodb:", STRAFTER(STR(?idraw), "#")) AS ?id)
    
                                          OPTIONAL {{?idraw rdfs:label ?labelraw.}}
                                          BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)

                                          OPTIONAL {{?idraw rdfs:comment ?descriptionraw.}}
                                          BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)


                                        }}
                                  GROUP BY ?id ?label ?description'''
                                          }