queryProviderAL = {
                 'AL': '''PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                             
                          
                          SELECT DISTINCT ?id ?label ?quote
                          WHERE {
                                 ?idraw a :algorithm .
                                 BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                 OPTIONAL {?idraw rdfs:label ?labelraw .}
                                 BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                 OPTIONAL {?idraw rdfs:comment ?quoteraw.}
                                 BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                }
                          GROUP BY ?id ?label ?quote''',

                 'AP': '''PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                             
                          
                          SELECT DISTINCT ?id ?label ?quote
                          WHERE {
                                 ?idraw a :problem .
                                 BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                 OPTIONAL {?idraw rdfs:label ?labelraw .}
                                 BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                 OPTIONAL {?idraw rdfs:comment ?quoteraw.}
                                 BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                }
                          GROUP BY ?id ?label ?quote''',

                 'SO': '''PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                             
                          
                          SELECT DISTINCT ?id ?label ?quote
                          WHERE {
                                 ?idraw a :software .
                                 BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                 OPTIONAL {?idraw rdfs:label ?labelraw .}
                                 BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                 OPTIONAL {?idraw rdfs:comment ?quoteraw.}
                                 BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                }
                          GROUP BY ?id ?label ?quote''',

                 'BE': '''PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                             
                          
                          SELECT DISTINCT ?id ?label ?quote
                          WHERE {
                                 ?idraw a :benchmark .
                                 BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                 OPTIONAL {?idraw rdfs:label ?labelraw .}
                                 BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                 OPTIONAL {?idraw rdfs:comment ?quoteraw.}
                                 BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                }
                          GROUP BY ?id ?label ?quote''',

                 'PU': '''PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                             
                          
                          SELECT DISTINCT ?id ?label ?quote
                          WHERE {
                                 ?idraw a :publication .
                                 BIND(STRAFTER(STR(?idraw), "#") AS ?id)
                                 OPTIONAL {?idraw rdfs:label ?labelraw .}
                                 BIND(COALESCE(?labelraw, "No Label Provided!") AS ?label)
                                 OPTIONAL {?idraw rdfs:comment ?quoteraw.}
                                 BIND(COALESCE(?quoteraw, "No Description Provided!") AS ?quote)
                                }
                          GROUP BY ?id ?label ?quote'''

}

queryHandlerAL = {
    
    'benchmarkInformation': '''PREFIX prop: <https://mardi4nfdi.de/mathalgodb/0.1#>
                               PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1/benchmark#>
                               PREFIX dc: <http://purl.org/spar/datacite/>   
                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                          
                               
                               SELECT DISTINCT ?reference
                                               (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)
                               WHERE {{
                                       VALUES ?idraw {{ :{0} }}

                                       OPTIONAL {{ ?idraw dc:hasIdentifier ?reference }}
                                     
                                       OPTIONAL {{
                                                  ?idraw (prop:documentedIn | prop:usedIn) ?pubraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?pubraw), "#")) AS ?pub)
                                                  OPTIONAL {{ ?pubraw rdfs:label ?publraw}}
                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)
                                                  OPTIONAL {{ ?pubraw rdfs:comment ?pubdraw}}
                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                }}

                                     }}
                               GROUP BY ?reference''',

      'softwareInformation': '''PREFIX prop: <https://mardi4nfdi.de/mathalgodb/0.1#>
                               PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1/software#>
                               PREFIX dc: <http://purl.org/spar/datacite/>   
                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                          
                               
                               SELECT DISTINCT ?reference
                                               (GROUP_CONCAT(DISTINCT CONCAT(?bench, " | ", ?benchl, " | ", ?benchd); separator=" / ") AS ?benchmark)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)
                               WHERE {{
                                       VALUES ?idraw {{ :{0} }}

                                       OPTIONAL {{ ?idraw dc:hasIdentifier ?reference }}

                                       OPTIONAL {{
                                                  ?idraw prop:tests ?benchraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?benchraw), "#")) AS ?bench)
                                                  OPTIONAL {{ ?benchraw rdfs:label ?benchlraw}}
                                                  BIND(COALESCE(?benchlraw, "No Label Provided!") AS ?benchl)
                                                  OPTIONAL {{ ?benchraw rdfs:comment ?benchdraw}}
                                                  BIND(COALESCE(?benchdraw, "No Description Provided!") AS ?benchd)
                                                }}
                                     
                                       OPTIONAL {{
                                                  ?idraw (prop:documentedIn | prop:usedIn) ?pubraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?pubraw), "#")) AS ?pub)
                                                  OPTIONAL {{ ?pubraw rdfs:label ?publraw}}
                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)
                                                  OPTIONAL {{ ?pubraw rdfs:comment ?pubdraw}}
                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                }}

                                     }}
                               GROUP BY ?reference''',
      
      'problemInformation': '''PREFIX prop: <https://mardi4nfdi.de/mathalgodb/0.1#>
                               PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1/problem#>
                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                          
                               
                               SELECT DISTINCT (GROUP_CONCAT(DISTINCT CONCAT(?bench, " | ", ?benchl, " | ", ?benchd); separator=" / ") AS ?benchmark)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?spec, " | ", ?specl, " | ", ?specd); separator=" / ") AS ?specializes)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?specby, " | ", ?specbyl, " | ", ?specbyd); separator=" / ") AS ?specializedBy)
                               WHERE {{
                                       VALUES ?idraw {{ :{0} }}

                                       OPTIONAL {{
                                                  ?idraw prop:instantiates ?benchraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?benchraw), "#")) AS ?bench)
                                                  OPTIONAL {{ ?benchraw rdfs:label ?benchlraw}}
                                                  BIND(COALESCE(?benchlraw, "No Label Provided!") AS ?benchl)
                                                  OPTIONAL {{ ?benchraw rdfs:comment ?benchdraw}}
                                                  BIND(COALESCE(?benchdraw, "No Description Provided!") AS ?benchd)
                                                }}
                                     
                                       OPTIONAL {{
                                                  ?idraw prop:specializes ?specraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?specraw), "#")) AS ?spec)
                                                  OPTIONAL {{ ?specraw rdfs:label ?speclraw}}
                                                  BIND(COALESCE(?speclraw, "No Label Provided!") AS ?specl)
                                                  OPTIONAL {{ ?specraw rdfs:comment ?specdraw}}
                                                  BIND(COALESCE(?specdraw, "No Description Provided!") AS ?specd)
                                                }}

                                       OPTIONAL {{
                                                  ?idraw prop:specializedBy ?specbyraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?specbyraw), "#")) AS ?specby)
                                                  OPTIONAL {{ ?specbyraw rdfs:label ?specbylraw}}
                                                  BIND(COALESCE(?specbylraw, "No Label Provided!") AS ?specbyl)
                                                  OPTIONAL {{ ?specbyraw rdfs:comment ?specbydraw}}
                                                  BIND(COALESCE(?specbydraw, "No Description Provided!") AS ?specbyd)
                                                }}

                                     }}''',

      'algorithmInformation': '''PREFIX prop: <https://mardi4nfdi.de/mathalgodb/0.1#>
                               PREFIX : <https://mardi4nfdi.de/mathalgodb/0.1/algorithm#>
                               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>                          
                               
                               SELECT DISTINCT (GROUP_CONCAT(DISTINCT CONCAT(?prob, " | ", ?probl, " | ", ?probd); separator=" / ") AS ?problem)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?imple, " | ", ?implel, " | ", ?impled); separator=" / ") AS ?software)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?hascomp, " | ", ?hascompl, " | ", ?hascompd); separator=" / ") AS ?hasComponent)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?comp, " | ", ?compl, " | ", ?compd); separator=" / ") AS ?componentOf)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?hassub, " | ", ?hassubl, " | ", ?hassubd); separator=" / ") AS ?hasSubclass)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?sub, " | ", ?subl, " | ", ?subd); separator=" / ") AS ?subclassOf)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?rel, " | ", ?rell, " | ", ?reld); separator=" / ") AS ?relatedTo)
                                               (GROUP_CONCAT(DISTINCT CONCAT(?pub, " | ", ?publ, " | ", ?pubd); separator=" / ") AS ?publication)
                               WHERE {{
                                       VALUES ?idraw {{ :{0} }}

                                       OPTIONAL {{
                                                  ?idraw prop:solves ?probraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?probraw), "#")) AS ?prob)
                                                  OPTIONAL {{ ?probraw rdfs:label ?problraw}}
                                                  BIND(COALESCE(?problraw, "No Label Provided!") AS ?probl)
                                                  OPTIONAL {{ ?probraw rdfs:comment ?probdraw}}
                                                  BIND(COALESCE(?probdraw, "No Description Provided!") AS ?probd)
                                                }}

                                       OPTIONAL {{
                                                  ?idraw prop:implementedBy ?impleraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?impleraw), "#")) AS ?imple)
                                                  OPTIONAL {{ ?impleraw rdfs:label ?implellraw}}
                                                  BIND(COALESCE(?implelraw, "No Label Provided!") AS ?implel)
                                                  OPTIONAL {{ ?impleraw rdfs:comment ?impledraw}}
                                                  BIND(COALESCE(?impledraw, "No Description Provided!") AS ?impled)
                                                }}
                                     
                                       OPTIONAL {{
                                                  ?idraw prop:hasComponent ?hascompraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?hascompraw), "#")) AS ?hascomp)
                                                  OPTIONAL {{ ?hascompraw rdfs:label ?hascomplraw}}
                                                  BIND(COALESCE(?hascomplraw, "No Label Provided!") AS ?hascompl)
                                                  OPTIONAL {{ ?hascompraw rdfs:comment ?hascompdraw}}
                                                  BIND(COALESCE(?hascompdraw, "No Description Provided!") AS ?hascompd)
                                                }}

                                       OPTIONAL {{
                                                  ?idraw prop:componentOf ?compraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?compraw), "#")) AS ?comp)
                                                  OPTIONAL {{ ?compraw rdfs:label ?complraw}}
                                                  BIND(COALESCE(?complraw, "No Label Provided!") AS ?compl)
                                                  OPTIONAL {{ ?compraw rdfs:comment ?compdraw}}
                                                  BIND(COALESCE(?compdraw, "No Description Provided!") AS ?compd)
                                                }}

                                    OPTIONAL {{
                                                  ?idraw prop:hasSubclass ?hassubraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?hassubraw), "#")) AS ?hassub)
                                                  OPTIONAL {{ ?hassubraw rdfs:label ?hassublraw}}
                                                  BIND(COALESCE(?hassublraw, "No Label Provided!") AS ?hassubl)
                                                  OPTIONAL {{ ?hassubraw rdfs:comment ?hassubdraw}}
                                                  BIND(COALESCE(?hassubdraw, "No Description Provided!") AS ?hassubd)
                                                }}

                                       OPTIONAL {{
                                                  ?idraw prop:subclassOf ?subraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?subraw), "#")) AS ?sub)
                                                  OPTIONAL {{ ?subraw rdfs:label ?sublraw}}
                                                  BIND(COALESCE(?sublraw, "No Label Provided!") AS ?subl)
                                                  OPTIONAL {{ ?subraw rdfs:comment ?subdraw}}
                                                  BIND(COALESCE(?subdraw, "No Description Provided!") AS ?subd)
                                                }}

                                       OPTIONAL {{
                                                  ?idraw prop:relatedTo ?relraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?relraw), "#")) AS ?rel)
                                                  OPTIONAL {{ ?relraw rdfs:label ?rellraw}}
                                                  BIND(COALESCE(?rellraw, "No Label Provided!") AS ?rell)
                                                  OPTIONAL {{ ?relraw rdfs:comment ?reldraw}}
                                                  BIND(COALESCE(?reldraw, "No Description Provided!") AS ?reld)
                                                }}

                                       OPTIONAL {{
                                                  ?idraw (prop:documentedIn | prop:usedIn) ?pubraw.
                                                  BIND(CONCAT("mathalgodb:", STRAFTER(STR(?pubraw), "#")) AS ?pub)
                                                  OPTIONAL {{ ?pubraw rdfs:label ?publraw}}
                                                  BIND(COALESCE(?publraw, "No Label Provided!") AS ?publ)
                                                  OPTIONAL {{ ?pubraw rdfs:comment ?pubdraw}}
                                                  BIND(COALESCE(?pubdraw, "No Description Provided!") AS ?pubd)
                                                }}
                                     }}''',
    
}