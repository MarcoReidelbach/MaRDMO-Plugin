from .id import *
from .config import *

# Raw Math Template

math_temp=''' 

PID (if applicable): http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_02

## Problem Statement

http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_01

### Object of Research and Objective

http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_01

### Procedure

http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_02

### Involved Disciplines

http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_01

### Data Streams

http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_02

## Model

ID: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Wiki_01

http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_01 

http://example.com/terms/domain/MaRDI/Section_3/Set_1/Wiki_02

### Discretization

* Time: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_02
* Space: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_03

### Variables

MATH_TAB_1

### Parameters

MATH_TAB_a1

## Process Information

### Process Steps

MATH_TAB_2

### Applied Methods 

MATH_TAB_3

### Software used

MATH_TAB_4

### Hardware

MATH_TAB_5

### Input Data

MATH_TAB_6

### Output Data

MATH_TAB_7

## Reproducibility

### Mathematical Reproducibility 

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_01

### Runtime Reproducibility 

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_02

### Reproducibility of Results

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_03

### Reproducibility on original Hardware

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_04

### Reproducibility on other Hardware

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_05

### Transferability to

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_06

## Legend

The following abbreviations are used in the document to indicate/resolve IDs:

doi: DOI / https://dx.doi.org/

sw: swMATH / https://swmath.org/software/

wikidata: https://www.wikidata.org/wiki/

mardi: https://portal.mardi4nfdi.de/wiki/'''

# Raw Exp Template

exp_temp='''

PID (if applicable): http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_02

## Problem Statement

http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_01

### Object of Research and Objective

http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_01

### Procedure

http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_02

### Involved Disciplines

http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_01

### Data Streams

http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_02

## Model

ID: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Wiki_01

http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_01

http://example.com/terms/domain/MaRDI/Section_3/Set_1/Wiki_02

### Discretization
(if applicable)

* Time: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_02
* Space: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_03

### Variables

EXP_TAB_1

### Parameter

EXP_TAB_2

## Process Information

### Process Steps

EXP_TAB_3


### Applied Methods 

EXP_TAB_4

### Software used

EXP_TAB_5

### Experimental Devices/Instruments and Computer-Hardware

EXP_TAB_6

### Input Data

EXP_TAB_7

### Output Data

EXP_TAB_8

## Reproducibility

### Reproducibility of the Experiments on the original Devices/Instruments/Hardware

http://example.com/terms/domain/MaRDI/Section_5/Set_2/Question_01

### Reproducibility of the Experiments on other Devices/Instruments/Hardware

http://example.com/terms/domain/MaRDI/Section_5/Set_2/Question_02

### Transferability of the  Experiments to

http://example.com/terms/domain/MaRDI/Section_5/Set_2/Question_03

## Legend

The following abbreviations are used in the document to indicate/resolve IDs:

doi: DOI / https://dx.doi.org/

sw: swMATH / https://swmath.org/software/

wikidata: https://www.wikidata.org/wiki/

mardi: https://portal.mardi4nfdi.de/wiki/'''

# Stuff to generate Tables for Math Template

math_tables=['MATH_TAB_1','MATH_TAB_a1','MATH_TAB_2','MATH_TAB_3','MATH_TAB_4','MATH_TAB_5','MATH_TAB_6','MATH_TAB_7']

math_topics=[['Name','Unit','Symbol'],
             ['Name','Unit','Symbol'],
             ['Name','Description','Input','Output','Method','Parameter','Environment','Mathematical Area'],
             ['ID','Name','Process Step','Parameter','implemented by'],
             ['ID','Name','Description','Version','Programming Language','Dependencies','versioned','published','documented'],
             ['ID','Name','Processor','Compiler','#Nodes','#Cores'],
             ['ID','Name','Size','Data Structure','Format Representation','Format Exchange','binary/text','proprietary','to publish','to archive'],
             ['ID','Name','Size','Data Structure','Format Representation','Format Exchange','binary/text','proprietary','to publish','to archive']]

math_ids=[['http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_01','http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_02','http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_03'],
          ['http://example.com/terms/domain/MaRDI/Section_3/Set_3/Question_01','http://example.com/terms/domain/MaRDI/Section_3/Set_3/Question_02','http://example.com/terms/domain/MaRDI/Section_3/Set_3/Question_03'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_02','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_03',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_05','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_06',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_07','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_08'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_02','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_03',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_05'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_02','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_03',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_05','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_06',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_07','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_08','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_09'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_02','http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_03',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_05','http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_05'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_00','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_02',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_03','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_05',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_06','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_07','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_08',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_09'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_00','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_02',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_03','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_05',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_06','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_07','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_08',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_09']]

# Stuff to generate Tables for Exp Template

exp_tables=['EXP_TAB_1','EXP_TAB_2','EXP_TAB_3','EXP_TAB_4','EXP_TAB_5','EXP_TAB_6','EXP_TAB_7','EXP_TAB_8']

exp_topics=[['Name','Unit','Symbol','dependent (measured) / independent (controlled)'],
            ['Name','Unit','Symbol'],
            ['Name','Description','Input','Output','Method','Parameter','Environment','Mathematical Area'],
            ['ID','Name','Process Step','Parameter','realised / implemented by'],
            ['ID','Name','Description','Version','Programming Language','Dependencies','versioned','published','documented'],
            ['ID','Name','Description','Version','Part Nr','Serial Nr','Location','Software'],
            ['ID','Name','Size','Data Structure','Format Representation','Format Exchange','binary/text','proprietary','to publish','to archive'],
            ['ID','Name','Size','Data Structure','Format Representation','Format Exchange','binary/text','proprietary','to publish','to archive']]

exp_ids=[['http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_01','http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_02','http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_03', 'http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_04'],
         ['http://example.com/terms/domain/MaRDI/Section_3/Set_3/Question_01','http://example.com/terms/domain/MaRDI/Section_3/Set_3/Question_02','http://example.com/terms/domain/MaRDI/Section_3/Set_3/Question_03'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_02','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_03',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_05','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_06',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_07','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_08'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_02','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_03',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_05'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_02','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_03',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_05','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_06',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_07','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_08','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_09'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_02','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_03',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_05','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_06',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_07','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_08'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_00','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_02',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_03','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_05',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_06','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_07','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_08',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_09'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_00','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_02',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_03','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_04','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_05',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_06','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_07','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_08',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_09']]

# Stuff for KG export

KG_export=['http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_01','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_02','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_01']

# Stuff for Decisions
dec=[['http://example.com/terms/domain/MaRDI/Section_0/Set_1/Question_01', 'Workflow Documentation', 'Workflow Dokumentation'],
     ['http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_03', 'Theoretical Workflow', 'Theoretischer Workflow', 'Experimental Workflow', 'Experimenteller Workflow'],
     ['http://example.com/terms/domain/MaRDI/Section_6/Set_1/Question_01', 'Markdown File', 'MaRDI Portal'],
     ['http://example.com/terms/domain/MaRDI/Section_6/Set_1/Question_02', 'No', 'Nein'],
     ['http://example.com/terms/domain/MaRDI/Section_0/Set_1/Question_01', 'Workflow Search', 'Workflow Suche'],
     ['http://example.com/terms/domain/MaRDI/Section_1/Set_1/Question_00', 'Research Objective', 'Forschungsziel',
                                                                           'Model, Methods, Software and Input/Output Data', 'Model, Methoden, Software und Eingabe-/Ausgabedaten', 
                                                                           'Field of Research', 'Forschungsfeld']]

# Stuff for Wikibase Export

w_no=['http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_01',
      'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_01',
      'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_01']

paper_doi=['http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_02']

ws2=['http://example.com/terms/domain/MaRDI/Section_3/Set_1/Wiki_01',
     'http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_01',
     'http://example.com/terms/domain/MaRDI/Section_3/Set_1/Wiki_02',
     'http://example.com/terms/domain/MaRDI/Section_3/Set_1/Wiki_03',
     'http://example.com/terms/domain/MaRDI/Section_3/Set_1/Wiki_04',
     'http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_00']

ws3=['http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_01',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_02',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Wiki_02',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Wiki_03',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Wiki_04',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_00']

ws4=['http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_01',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_02',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_03',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_05',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_00']

ws5=['http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_01']

ws6=['http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_01']

ws7=['http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_00',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_01',
     'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_10']

ws7a=['http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_00',
      'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_01',
      'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_10']

ws8=['http://example.com/terms/domain/MaRDI/Section_1/Set_1/Question_01']

# Language Dictionary

lang_dict={'af':'Afrikaans','ar':'Arabic','bg':'Bulgarian','bn':'Bengali',
           'ca':'Catalan','cs':'Czech','cy':'Welsh','da':'Danish','de':'German',
           'el':'Greek','en':'English','es':'Spanish','et':'Estonian','fa':'Persian',
           'fi':'Finnish','fr':'French','gu':'Gujarati','he':'Hebrew','hi':'Hindi',
           'hr':'Croatian','hu':'Hungarian','id':'Indonesian','it':'Italian',
           'ja':'Japanese','kn':'Kannada','ko':'Korean','lt':'Lithuanian','lv':'Latvian',
           'mk':'Macedonian','ml':'Malayalam','mr':'Marathi','ne':'Nepali',
           'nl':'Dutch','no':'Norwegian','pa':'Punjabi','pl':'Polish','pt':'Portuguese',
           'ro':'Romanian','ru':'Russian','sk':'Slovak','sl':'Slovenian','so':'Somali',
           'sq':'Albanian','sv':'Swedish','sw':'Swahili','ta':'Tamil','te':'Telugu',
           'th':'Thai','tl':'Tagalog','tr':'Turkish','uk':'Ukrainian','ur':'Urdu',
           'vi':'Vietnamese','zh-cn':'Putonghua','zh-tw':'Taiwanese Mandarin'}

# Stuff to preview Documentation as HTML

html_front="""
<head>
  <script type="text/javascript" id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3.0.0/es5/tex-mml-chtml.js">
  </script>
  <style>
    table {
      margin-left: 0;
      margin-right: auto;
      margin-bottom: 24px;
      border-spacing: 0;
      border-bottom: 2px solid black;
      border-top: 2px solid black;
    }
    table th {
      padding: 3px 10px;
      background-color: white;
      border-top: none;
      border-left: 1px solid black;
      border-right: 1px solid black;
      border-bottom: 1px solid black;
      text-align: center;
    }
    table td {
      padding: 3px 10px;
      border-top: 1px solid black;
      border-left: 1px solid black;
      border-bottom: 1px solid black;
      border-right: 1px solid black;
      text-align: center;
    }
  </style>
</head>
<body>
"""

html_end="""
</body>
</html>"""




