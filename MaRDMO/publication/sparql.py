#Queries to MaRDI KG and Wikidata for Publication Handler

queryPublication = {

        'MaRDIDOI': '''PREFIX wdt:{2} PREFIX wd:{3}
                        SELECT ?id ?label ?description         
                        
                 WHERE {{?idraw wdt:P{0} "{1}";
                        BIND(CONCAT("mardi:", STRAFTER(STR(?idraw), STR(wd:))) AS ?id)
                        
                        OPTIONAL {{?idraw rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?idraw schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                       }}''',
    
       'All_MaRDILabel': '''PREFIX wdt:{15} PREFIX wd:{16}
                        SELECT ?label ?description ?doi         
                        (GROUP_CONCAT(DISTINCT(?authorInfo); separator=" | ") AS ?authorInfos)                                                        
                        ?entrytypelabel ?journalInfo ?languagelabel                               
                        ?title ?date ?volume ?issue ?page          

                 WHERE {{ VALUES ?publication {{ wd:{1} }}
                 
                        OPTIONAL {{ ?publication wdt:P{0} ?doi. }}
                        
                        OPTIONAL {{?publication rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?publication schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                        
                        OPTIONAL {{?publication (wdt:P{2} | wdt:P{8}) ?authorraw.
                                  BIND(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("mardi:", STRAFTER(STR(?authorraw), STR(wd:))), "") AS ?author)
     
                                  OPTIONAL {{?authorraw rdfs:label ?authorlabelraw.
                                            FILTER (lang(?authorlabelraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorlabelraw, ?authorraw), "") AS ?authorlabel)
   
                                  OPTIONAL {{?authorraw schema:description ?authordescriptionraw.
                                            FILTER (lang(?authordescriptionraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authordescriptionraw, ""), "") AS ?authordescription)
   
                                  OPTIONAL {{?authorraw wdt:P{3} ?authororcidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authororcidraw, ""), "") AS ?authororcid)
                          
                                  OPTIONAL {{?authorraw wdt:P{13} ?authorwikidataidraw}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorwikidataidraw), STR(wd:))), ""), "") AS ?authorwikidataid)
   
                                  OPTIONAL {{?authorraw wdt:P{14} ?authorzbmathidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorzbmathidraw, ""), "") AS ?authorzbmathid)
     
                                  BIND(CONCAT(?author, " <|> ", ?authorlabel, " <|> ", ?authordescription, " <|> ", ?authororcid, " <|> ", ?authorzbmathid, " <|> ", ?authorwikidataid) AS ?authorInfo)}}
   
                        OPTIONAL {{?publication wdt:P{4} ?entrytyperaw.
                                  
                                   OPTIONAL {{?entrytyperaw rdfs:label ?entrytypelabelraw.
                                            FILTER (lang(?entrytypelabelraw) = 'en')}}
                                   BIND(COALESCE(?entrytypelabelraw, "No Label Provided!") As ?entrytypelabel)
                                  }}
                        
                        OPTIONAL {{?publication wdt:P{5} ?journalraw.
                                  BIND(CONCAT("mardi:", STRAFTER(STR(?journalraw), STR(wd:))) AS ?journal)
                                  
                                  OPTIONAL {{?journalraw rdfs:label ?journallabelraw.
                                            FILTER (lang(?journallabelraw) = 'en')}}
                                  BIND(COALESCE(?journallabelraw, "No Label Provided!") As ?journallabel)
                                  
                                  OPTIONAL {{?journalraw schema:description ?journaldescriptionraw.
                                            FILTER (lang(?journaldescriptionraw) = 'en')}}
                                  BIND(COALESCE(?journaldescriptionraw, "No Description Provided!") As ?journaldescription)
                                  
                                  BIND(concat(?journal, " <|> ", ?journallabel, " <|> ", ?journaldescription) AS ?journalInfo)}}
                        
                        OPTIONAL {{?publication wdt:P{6} ?languageraw.
                                   
                                   OPTIONAL {{?languageraw rdfs:label ?languagelabelraw.
                                              FILTER (lang(?languagelabelraw) = 'en')}}
                                   BIND(COALESCE(?languagelabelraw, "No Label Provided!") As ?languagelabel)}}
                        
                        OPTIONAL {{?publication wdt:P{7} ?titleraw.
                                   BIND(COALESCE(?titleraw, "No Title Provided!") As ?title)}}
                        
                        OPTIONAL {{?publication wdt:P{9} ?dateraw.
                                   BIND(COALESCE(?dateraw, "No Publication Date Provided!") As ?date)}}
                        
                        OPTIONAL {{?publication wdt:P{10} ?volumeraw.
                                   BIND(COALESCE(?volumeraw, "No Volume Provided!") As ?volume)}}
                        
                        OPTIONAL {{?publication wdt:P{11} ?issueraw.
                                   BIND(COALESCE(?issueraw, "No Issue Provided!") As ?issue)}}
                        
                        OPTIONAL {{?publication wdt:P{12} ?pageraw.
                                   BIND(COALESCE(?pageraw, "No Pages Provided!") As ?page)}}
                        }}
   
                 GROUP BY ?doi ?label ?description ?entrytypelabel ?journalInfo ?languagelabel ?title ?date ?volume ?issue ?page ''',
    
       'All_MaRDI': '''PREFIX wdt:{15} PREFIX wd:{16}
                        SELECT ?id ?label ?description         
                        (GROUP_CONCAT(DISTINCT(?authorInfo); separator=" | ") AS ?authorInfos)                                                        
                        ?entrytypelabel ?journalInfo ?languagelabel                               
                        ?title ?date ?volume ?issue ?page          

                 WHERE {{?idraw wdt:P{0} "{1}";
                        BIND(CONCAT("mardi:", STRAFTER(STR(?idraw), STR(wd:))) AS ?id)
                        
                        OPTIONAL {{?idraw rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?idraw schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                        
                        OPTIONAL {{?idraw (wdt:P{2} | wdt:P{8}) ?authorraw.
                                  BIND(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("mardi:", STRAFTER(STR(?authorraw), STR(wd:))), "") AS ?author)
     
                                  OPTIONAL {{?authorraw rdfs:label ?authorlabelraw.
                                            FILTER (lang(?authorlabelraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorlabelraw, ?authorraw), "") AS ?authorlabel)
   
                                  OPTIONAL {{?authorraw schema:description ?authordescriptionraw.
                                            FILTER (lang(?authordescriptionraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authordescriptionraw, ""), "") AS ?authordescription)
   
                                  OPTIONAL {{?authorraw wdt:P{3} ?authororcidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authororcidraw, ""), "") AS ?authororcid)
                          
                                  OPTIONAL {{?authorraw wdt:P{13} ?authorwikidataidraw}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorwikidataidraw), STR(wd:))), ""), "") AS ?authorwikidataid)
   
                                  OPTIONAL {{?authorraw wdt:P{14} ?authorzbmathidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorzbmathidraw, ""), "") AS ?authorzbmathid)
     
                                  BIND(CONCAT(?author, " <|> ", ?authorlabel, " <|> ", ?authordescription, " <|> ", ?authororcid, " <|> ", ?authorzbmathid, " <|> ", ?authorwikidataid) AS ?authorInfo)}}
   
                        OPTIONAL {{?idraw wdt:P{4} ?entrytyperaw.
                                  
                                   OPTIONAL {{?entrytyperaw rdfs:label ?entrytypelabelraw.
                                            FILTER (lang(?entrytypelabelraw) = 'en')}}
                                   BIND(COALESCE(?entrytypelabelraw, "No Label Provided!") As ?entrytypelabel)
                                  }}
                        
                        OPTIONAL {{?idraw wdt:P{5} ?journalraw.
                                  BIND(CONCAT("mardi:", STRAFTER(STR(?journalraw), STR(wd:))) AS ?journal)
                                  
                                  OPTIONAL {{?journalraw rdfs:label ?journallabelraw.
                                            FILTER (lang(?journallabelraw) = 'en')}}
                                  BIND(COALESCE(?journallabelraw, "No Label Provided!") As ?journallabel)
                                  
                                  OPTIONAL {{?journalraw schema:description ?journaldescriptionraw.
                                            FILTER (lang(?journaldescriptionraw) = 'en')}}
                                  BIND(COALESCE(?journaldescriptionraw, "No Description Provided!") As ?journaldescription)
                                  
                                  BIND(concat(?journal, " <|> ", ?journallabel, " <|> ", ?journaldescription) AS ?journalInfo)}}
                        
                        OPTIONAL {{?idraw wdt:P{6} ?languageraw.
                                   
                                   OPTIONAL {{?languageraw rdfs:label ?languagelabelraw.
                                              FILTER (lang(?languagelabelraw) = 'en')}}
                                   BIND(COALESCE(?languagelabelraw, "No Label Provided!") As ?languagelabel)}}
                        
                        OPTIONAL {{?idraw wdt:P{7} ?titleraw.
                                   BIND(COALESCE(?titleraw, "No Title Provided!") As ?title)}}
                        
                        OPTIONAL {{?idraw wdt:P{9} ?dateraw.
                                   BIND(COALESCE(?dateraw, "No Publication Date Provided!") As ?date)}}
                        
                        OPTIONAL {{?idraw wdt:P{10} ?volumeraw.
                                   BIND(COALESCE(?volumeraw, "No Volume Provided!") As ?volume)}}
                        
                        OPTIONAL {{?idraw wdt:P{11} ?issueraw.
                                   BIND(COALESCE(?issueraw, "No Issue Provided!") As ?issue)}}
                        
                        OPTIONAL {{?idraw wdt:P{12} ?pageraw.
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

                 WHERE {{ VALUES ?publication {{ wd:{1} }}
                 
                        OPTIONAL {{ ?publication wdt:P{0} ?doi. }}

                        OPTIONAL {{?publication rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?publication schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                        
                        OPTIONAL {{?publication (wdt:P{2} | wdt:P{8}) ?authorraw.
                                  BIND(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorraw), STR(wd:))), "") AS ?author)
     
                                  OPTIONAL {{?authorraw rdfs:label ?authorlabelraw.
                                            FILTER (lang(?authorlabelraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorlabelraw, ?authorraw), "") AS ?authorlabel)
   
                                  OPTIONAL {{?authorraw schema:description ?authordescriptionraw.
                                            FILTER (lang(?authordescriptionraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authordescriptionraw, ""), "") AS ?authordescription)
   
                                  OPTIONAL {{?authorraw wdt:P{3} ?authororcidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authororcidraw, ""), "") AS ?authororcid)
                          
                                  OPTIONAL {{?authorraw wdt:P{13} ?authorwikidataidraw}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorwikidataidraw), STR(wd:))), ""), "") AS ?authorwikidataid)
   
                                  OPTIONAL {{?authorraw wdt:P{14} ?authorzbmathidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorzbmathidraw, ""), "") AS ?authorzbmathid)
     
                                  BIND(CONCAT(?author, " <|> ", ?authorlabel, " <|> ", ?authordescription, " <|> ", ?authororcid, " <|> ", ?authorzbmathid, " <|> ", ?authorwikidataid) AS ?authorInfo)}}
   
                        OPTIONAL {{?publication wdt:P{4} ?entrytyperaw.
                                  
                                   OPTIONAL {{?entrytyperaw rdfs:label ?entrytypelabelraw.
                                            FILTER (lang(?entrytypelabelraw) = 'en')}}
                                   BIND(COALESCE(?entrytypelabelraw, "No Label Provided!") As ?entrytypelabel)
                                  }}
                        
                        OPTIONAL {{?publication wdt:P{5} ?journalraw.
                                  BIND(CONCAT("wikidata:", STRAFTER(STR(?journalraw), STR(wd:))) AS ?journal)
                                  
                                  OPTIONAL {{?journalraw rdfs:label ?journallabelraw.
                                            FILTER (lang(?journallabelraw) = 'en')}}
                                  BIND(COALESCE(?journallabelraw, "No Label Provided!") As ?journallabel)
                                  
                                  OPTIONAL {{?journalraw schema:description ?journaldescriptionraw.
                                            FILTER (lang(?journaldescriptionraw) = 'en')}}
                                  BIND(COALESCE(?journaldescriptionraw, "No Description Provided!") As ?journaldescription)
                                  
                                  BIND(concat(?journal, " <|> ", ?journallabel, " <|> ", ?journaldescription) AS ?journalInfo)}}
                        
                        OPTIONAL {{?publication wdt:P{6} ?languageraw.
                                   
                                   OPTIONAL {{?languageraw rdfs:label ?languagelabelraw.
                                              FILTER (lang(?languagelabelraw) = 'en')}}
                                   BIND(COALESCE(?languagelabelraw, "No Label Provided!") As ?languagelabel)}}
                        
                        OPTIONAL {{?publication wdt:P{7} ?titleraw.
                                   BIND(COALESCE(?titleraw, "No Title Provided!") As ?title)}}
                        
                        OPTIONAL {{?publication wdt:P{9} ?dateraw.
                                   BIND(COALESCE(?dateraw, "No Publication Date Provided!") As ?date)}}
                        
                        OPTIONAL {{?publication wdt:P{10} ?volumeraw.
                                   BIND(COALESCE(?volumeraw, "No Volume Provided!") As ?volume)}}
                        
                        OPTIONAL {{?publication wdt:P{11} ?issueraw.
                                   BIND(COALESCE(?issueraw, "No Issue Provided!") As ?issue)}}
                        
                        OPTIONAL {{?publication wdt:P{12} ?pageraw.
                                   BIND(COALESCE(?pageraw, "No Pages Provided!") As ?page)}}
                        }}
   
                 GROUP BY ?doi ?label ?description ?entrytypelabel ?journalInfo ?languagelabel ?title ?date ?volume ?issue ?page ''',

       'All_Wikidata': '''SELECT ?id ?label ?description         
                        (GROUP_CONCAT(DISTINCT(?authorInfo); separator=" | ") AS ?authorInfos)                                                        
                        ?entrytypelabel ?journalInfo ?languagelabel                               
                        ?title ?date ?volume ?issue ?page          

                 WHERE {{?idraw wdt:P{0} "{1}";
                        BIND(CONCAT("wikidata:", STRAFTER(STR(?idraw), STR(wd:))) AS ?id)

                        OPTIONAL {{?idraw rdfs:label ?labelraw.
                                  FILTER (lang(?labelraw) = 'en')}}
                        BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)
                        
                        OPTIONAL {{?idraw schema:description ?descriptionraw.
                                  FILTER (lang(?descriptionraw) = 'en')}}
                        BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                        
                        OPTIONAL {{?idraw (wdt:P{2} | wdt:P{8}) ?authorraw.
                                  BIND(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorraw), STR(wd:))), "") AS ?author)
     
                                  OPTIONAL {{?authorraw rdfs:label ?authorlabelraw.
                                            FILTER (lang(?authorlabelraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorlabelraw, ?authorraw), "") AS ?authorlabel)
   
                                  OPTIONAL {{?authorraw schema:description ?authordescriptionraw.
                                            FILTER (lang(?authordescriptionraw) = 'en')}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authordescriptionraw, ""), "") AS ?authordescription)
   
                                  OPTIONAL {{?authorraw wdt:P{3} ?authororcidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authororcidraw, ""), "") AS ?authororcid)
                          
                                  OPTIONAL {{?authorraw wdt:P{13} ?authorwikidataidraw}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), CONCAT("wikidata:", STRAFTER(STR(?authorwikidataidraw), STR(wd:))), ""), "") AS ?authorwikidataid)
   
                                  OPTIONAL {{?authorraw wdt:P{14} ?authorzbmathidraw.}}
                                  BIND(COALESCE(IF(CONTAINS(STR(?authorraw), STR(wd:)), ?authorzbmathidraw, ""), "") AS ?authorzbmathid)
     
                                  BIND(CONCAT(?author, " <|> ", ?authorlabel, " <|> ", ?authordescription, " <|> ", ?authororcid, " <|> ", ?authorzbmathid, " <|> ", ?authorwikidataid) AS ?authorInfo)}}
   
                        OPTIONAL {{?idraw wdt:P{4} ?entrytyperaw.
                                  
                                   OPTIONAL {{?entrytyperaw rdfs:label ?entrytypelabelraw.
                                            FILTER (lang(?entrytypelabelraw) = 'en')}}
                                   BIND(COALESCE(?entrytypelabelraw, "No Label Provided!") As ?entrytypelabel)
                                  }}
                        
                        OPTIONAL {{?idraw wdt:P{5} ?journalraw.
                                  BIND(CONCAT("wikidata:", STRAFTER(STR(?journalraw), STR(wd:))) AS ?journal)
                                  
                                  OPTIONAL {{?journalraw rdfs:label ?journallabelraw.
                                            FILTER (lang(?journallabelraw) = 'en')}}
                                  BIND(COALESCE(?journallabelraw, "No Label Provided!") As ?journallabel)
                                  
                                  OPTIONAL {{?journalraw schema:description ?journaldescriptionraw.
                                            FILTER (lang(?journaldescriptionraw) = 'en')}}
                                  BIND(COALESCE(?journaldescriptionraw, "No Description Provided!") As ?journaldescription)
                                  
                                  BIND(concat(?journal, " <|> ", ?journallabel, " <|> ", ?journaldescription) AS ?journalInfo)}}
                        
                        OPTIONAL {{?idraw wdt:P{6} ?languageraw.
                                   
                                   OPTIONAL {{?languageraw rdfs:label ?languagelabelraw.
                                              FILTER (lang(?languagelabelraw) = 'en')}}
                                   BIND(COALESCE(?languagelabelraw, "No Label Provided!") As ?languagelabel)}}
                        
                        OPTIONAL {{?idraw wdt:P{7} ?titleraw.
                                   BIND(COALESCE(?titleraw, "No Title Provided!") As ?title)}}
                        
                        OPTIONAL {{?idraw wdt:P{9} ?dateraw.
                                   BIND(COALESCE(?dateraw, "No Publication Date Provided!") As ?date)}}
                        
                        OPTIONAL {{?idraw wdt:P{10} ?volumeraw.
                                   BIND(COALESCE(?volumeraw, "No Volume Provided!") As ?volume)}}
                        
                        OPTIONAL {{?idraw wdt:P{11} ?issueraw.
                                   BIND(COALESCE(?issueraw, "No Issue Provided!") As ?issue)}}
                        
                        OPTIONAL {{?idraw wdt:P{12} ?pageraw.
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

       'PublicationMathModDBLabel': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                       PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                                       SELECT ?label ?description ?doi

                                       WHERE {{
                                               OPTIONAL {{{0} rdfs:label ?labelraw.
                                                     FILTER (lang(?labelraw) = 'en')}}
                                               BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)

                                               OPTIONAL {{?idraw rdfs:comment ?descriptionraw.
                                                     FILTER (lang(?descriptionraw) = 'en')}}
                                          BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)

                                               OPTIONAL {{ {0} :doiID ?doiraw.
                                                           BIND(REPLACE(STR(?doiraw), "https://doi.org/", "") AS ?doi)}}
                                             }}''',

       'PublicationMathModDB': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                                  SELECT DISTINCT ?id ?label ?description ?doi
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?documentsentity, " | ", ?documentsentitylabel, " | ", ?documentsentitydescription)); SEPARATOR=" / ") AS ?documents)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?inventsentity, " | ", ?inventsentitylabel, " | ", ?inventsentitydescription)); SEPARATOR=" / ") AS ?invents)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?studiesentity, " | ", ?studiesentitylabel, " | ", ?studiesentitydescription)); SEPARATOR=" / ") AS ?studies)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?surveysentity, " | ", ?surveysentitylabel, " | ", ?surveysentitydescription)); SEPARATOR=" / ") AS ?surveys)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?usesentity, " | ", ?usesentitylabel, " | ", ?usesentitydescription)); SEPARATOR=" / ") AS ?uses)
                                                                                    
                                  WHERE {{
                                          VALUES ?idraw {{ :{0} }}

                                          ?idraw a :Publication.
                                          BIND(CONCAT("mathmoddb:", STRAFTER(STR(?idraw), "#")) AS ?id)
    
                                          OPTIONAL {{?idraw :doiID ?doiraw
                                                     BIND(REPLACE(STR(?doiraw), "https://doi.org/", "") AS ?doi)}}

                                          OPTIONAL {{?idraw rdfs:label ?labelraw.
                                                     FILTER (lang(?labelraw) = 'en')}}
                                          BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)

                                          OPTIONAL {{?idraw rdfs:comment ?descriptionraw.
                                                     FILTER (lang(?descriptionraw) = 'en')}}
                                          BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)

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
                                  GROUP BY ?id ?label ?description ?doi''',

        'PublicationMathModDBDOI': '''PREFIX : <https://mardi4nfdi.de/mathmoddb#>
                                  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                                  SELECT DISTINCT ?id ?label ?description
                                                                                    
                                  WHERE {{
                                          ?idraw a :Publication.
                                          ?idraw :doiID ?doi .
                                          FILTER(LCASE(STR(?doi)) = LCASE("https://doi.org/{0}"))

                                          BIND(CONCAT("mathmoddb:", STRAFTER(STR(?idraw), "#")) AS ?id)
                                          
                                          OPTIONAL {{?idraw rdfs:label ?labelraw.
                                                     FILTER (lang(?labelraw) = 'en')}}
                                          BIND(COALESCE(?labelraw, "No Label Provided!") As ?label)

                                          OPTIONAL {{?idraw rdfs:comment ?descriptionraw.
                                                     FILTER (lang(?descriptionraw) = 'en')}}
                                          BIND(COALESCE(?descriptionraw, "No Description Provided!") As ?description)
                                        }}
                                  GROUP BY ?id ?label ?description''',

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
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?documentsentity, " | ", ?documentsentitylabel, " | ", ?documentsentitydescription)); SEPARATOR=" / ") AS ?documents)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?inventsentity, " | ", ?inventsentitylabel, " | ", ?inventsentitydescription)); SEPARATOR=" / ") AS ?invents)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?studiesentity, " | ", ?studiesentitylabel, " | ", ?studiesentitydescription)); SEPARATOR=" / ") AS ?studies)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?surveysentity, " | ", ?surveysentitylabel, " | ", ?surveysentitydescription)); SEPARATOR=" / ") AS ?surveys)
                                                  (GROUP_CONCAT(DISTINCT(CONCAT(?usesentity, " | ", ?usesentitylabel, " | ", ?usesentitydescription)); SEPARATOR=" / ") AS ?uses)
                                                                                    
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

                                          OPTIONAL {{?idraw :surveys ?surveysentityraw.
                                                     BIND(CONCAT("mathalgodb:", STRAFTER(STR(?surveysentityraw), "#")) AS ?surveysentity)

                                                     OPTIONAL {{?surveysentityraw rdfs:label ?surveysentitylabelraw.}}
                                                     BIND(COALESCE(?surveysentitylabelraw, "No Label Provided!") As ?surveysentitylabel)

                                                     OPTIONAL {{?surveysentityraw rdfs:comment ?surveysentitydescriptionraw.}}
                                                     BIND(COALESCE(?surveysentitydescriptionraw, "No Description Provided!") As ?surveysentitydescription)
                                                   }}

                                          OPTIONAL {{?idraw :uses ?usesentityraw.
                                                     BIND(CONCAT("mathalgodb:", STRAFTER(STR(?usesentityraw), "#")) AS ?usesentity)

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