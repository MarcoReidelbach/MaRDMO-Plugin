from .id import *
from .config import *

BASE_URI='http://example.com/terms/domain/MaRDI/'

# Raw Math Template

math_temp=''' 

PID (if applicable): '''+BASE_URI+'''Section_2/Set_1/Question_02_0

## Problem Statement

'''+BASE_URI+'''Section_2/Set_1/Question_01_0

### Object of Research and Objective

'''+BASE_URI+'''Section_2/Set_2/Question_01_0

### Procedure

'''+BASE_URI+'''Section_2/Set_2/Question_02_0

### Involved Disciplines

DISCIPLINES

### Data Streams

'''+BASE_URI+'''Section_2/Set_3/Question_02_0

## Model

ID: '''+BASE_URI+'''Section_3/Set_1/Wiki_01_0

'''+BASE_URI+'''Section_3/Set_1/Question_01_0 

'''+BASE_URI+'''Section_3/Set_1/Wiki_02_0

### Discretization

* Time: '''+BASE_URI+'''Section_3/Set_1/Question_02_0
* Space: '''+BASE_URI+'''Section_3/Set_1/Question_03_0

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

'''+BASE_URI+'''Section_5/Set_1/Question_01_0

### Runtime Reproducibility 

'''+BASE_URI+'''Section_5/Set_1/Question_02_0

### Reproducibility of Results

'''+BASE_URI+'''Section_5/Set_1/Question_03_0

### Reproducibility on original Hardware

'''+BASE_URI+'''Section_5/Set_1/Question_04_0

### Reproducibility on other Hardware

'''+BASE_URI+'''Section_5/Set_1/Question_05_0

### Transferability to

'''+BASE_URI+'''Section_5/Set_1/Question_06_0

## Legend

The following abbreviations are used in the document to indicate/resolve IDs:

doi: DOI / https://dx.doi.org/

sw: swMATH / https://swmath.org/software/

wikidata: https://www.wikidata.org/wiki/

mardi: https://portal.mardi4nfdi.de/wiki/'''

# Raw Exp Template

exp_temp='''

PID (if applicable): '''+BASE_URI+'''Section_2/Set_1/Question_02_0

## Problem Statement

'''+BASE_URI+'''Section_2/Set_1/Question_01_0

### Object of Research and Objective

'''+BASE_URI+'''Section_2/Set_2/Question_01_0

### Procedure

'''+BASE_URI+'''Section_2/Set_2/Question_02_0

### Involved Disciplines

'''+BASE_URI+'''Section_2/Set_3/Question_01_0

### Data Streams

'''+BASE_URI+'''Section_2/Set_3/Question_02_0

## Model

ID: '''+BASE_URI+'''Section_3/Set_1/Wiki_01_0

'''+BASE_URI+'''Section_3/Set_1/Question_01_0

'''+BASE_URI+'''Section_3/Set_1/Wiki_02_0

### Discretization
(if applicable)

* Time: '''+BASE_URI+'''Section_3/Set_1/Question_02_0
* Space: '''+BASE_URI+'''Section_3/Set_1/Question_03_0

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

'''+BASE_URI+'''Section_5/Set_2/Question_01_0

### Reproducibility of the Experiments on other Devices/Instruments/Hardware

'''+BASE_URI+'''Section_5/Set_2/Question_02_0

### Transferability of the  Experiments to

'''+BASE_URI+'''Section_5/Set_2/Question_03_0

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

math_ids=[[BASE_URI+'Section_3/Set_2/Question_01',BASE_URI+'Section_3/Set_2/Question_02',BASE_URI+'Section_3/Set_2/Question_03'],
          [BASE_URI+'Section_3/Set_3/Question_01',BASE_URI+'Section_3/Set_3/Question_02',BASE_URI+'Section_3/Set_3/Question_03'],
          [BASE_URI+'Section_4/Set_1/Question_01',BASE_URI+'Section_4/Set_1/Question_02',BASE_URI+'Section_4/Set_1/Question_03',
           BASE_URI+'Section_4/Set_1/Question_04',BASE_URI+'Section_4/Set_1/Question_05',BASE_URI+'Section_4/Set_1/Question_06',
           BASE_URI+'Section_4/Set_1/Question_07',BASE_URI+'Section_4/Set_1/Question_08'],
          [BASE_URI+'Section_4/Set_2/Question_01',BASE_URI+'Section_4/Set_2/Question_02',BASE_URI+'Section_4/Set_2/Question_03',
           BASE_URI+'Section_4/Set_2/Question_04',BASE_URI+'Section_4/Set_2/Question_05'],
          [BASE_URI+'Section_4/Set_3/Question_01',BASE_URI+'Section_4/Set_3/Question_02',BASE_URI+'Section_4/Set_3/Question_03',
           BASE_URI+'Section_4/Set_3/Question_04',BASE_URI+'Section_4/Set_3/Question_05',BASE_URI+'Section_4/Set_3/Question_06',
           BASE_URI+'Section_4/Set_3/Question_07',BASE_URI+'Section_4/Set_3/Question_08',BASE_URI+'Section_4/Set_3/Question_09'],
          [BASE_URI+'Section_4/Set_4/Question_01',BASE_URI+'Section_4/Set_4/Question_02',BASE_URI+'Section_4/Set_4/Question_03',
           BASE_URI+'Section_4/Set_4/Question_04',BASE_URI+'Section_4/Set_4/Question_05',BASE_URI+'Section_4/Set_4/Question_05'],
          [BASE_URI+'Section_4/Set_6/Question_00',BASE_URI+'Section_4/Set_6/Question_01',BASE_URI+'Section_4/Set_6/Question_02',
           BASE_URI+'Section_4/Set_6/Question_03',BASE_URI+'Section_4/Set_6/Question_04',BASE_URI+'Section_4/Set_6/Question_05',
           BASE_URI+'Section_4/Set_6/Question_06',BASE_URI+'Section_4/Set_6/Question_07',BASE_URI+'Section_4/Set_6/Question_08',
           BASE_URI+'Section_4/Set_6/Question_09'],
          [BASE_URI+'Section_4/Set_7/Question_00',BASE_URI+'Section_4/Set_7/Question_01',BASE_URI+'Section_4/Set_7/Question_02',
           BASE_URI+'Section_4/Set_7/Question_03',BASE_URI+'Section_4/Set_7/Question_04',BASE_URI+'Section_4/Set_7/Question_05',
           BASE_URI+'Section_4/Set_7/Question_06',BASE_URI+'Section_4/Set_7/Question_07',BASE_URI+'Section_4/Set_7/Question_08',
           BASE_URI+'Section_4/Set_7/Question_09']]

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

exp_ids=[[BASE_URI+'Section_3/Set_2/Question_01',BASE_URI+'Section_3/Set_2/Question_02',BASE_URI+'Section_3/Set_2/Question_03', BASE_URI+'Section_3/Set_2/Question_04'],
         [BASE_URI+'Section_3/Set_3/Question_01',BASE_URI+'Section_3/Set_3/Question_02',BASE_URI+'Section_3/Set_3/Question_03'],
         [BASE_URI+'Section_4/Set_1/Question_01',BASE_URI+'Section_4/Set_1/Question_02',BASE_URI+'Section_4/Set_1/Question_03',
          BASE_URI+'Section_4/Set_1/Question_04',BASE_URI+'Section_4/Set_1/Question_05',BASE_URI+'Section_4/Set_1/Question_06',
          BASE_URI+'Section_4/Set_1/Question_07',BASE_URI+'Section_4/Set_1/Question_08'],
         [BASE_URI+'Section_4/Set_2/Question_01',BASE_URI+'Section_4/Set_2/Question_02',BASE_URI+'Section_4/Set_2/Question_03',
          BASE_URI+'Section_4/Set_2/Question_04',BASE_URI+'Section_4/Set_2/Question_05'],
         [BASE_URI+'Section_4/Set_3/Question_01',BASE_URI+'Section_4/Set_3/Question_02',BASE_URI+'Section_4/Set_3/Question_03',
          BASE_URI+'Section_4/Set_3/Question_04',BASE_URI+'Section_4/Set_3/Question_05',BASE_URI+'Section_4/Set_3/Question_06',
          BASE_URI+'Section_4/Set_3/Question_07',BASE_URI+'Section_4/Set_3/Question_08',BASE_URI+'Section_4/Set_3/Question_09'],
         [BASE_URI+'Section_4/Set_5/Question_01',BASE_URI+'Section_4/Set_5/Question_02',BASE_URI+'Section_4/Set_5/Question_03',
          BASE_URI+'Section_4/Set_5/Question_04',BASE_URI+'Section_4/Set_5/Question_05',BASE_URI+'Section_4/Set_5/Question_06',
          BASE_URI+'Section_4/Set_5/Question_07',BASE_URI+'Section_4/Set_5/Question_08'],
         [BASE_URI+'Section_4/Set_6/Question_00',BASE_URI+'Section_4/Set_6/Question_01',BASE_URI+'Section_4/Set_6/Question_02',
          BASE_URI+'Section_4/Set_6/Question_03',BASE_URI+'Section_4/Set_6/Question_04',BASE_URI+'Section_4/Set_6/Question_05',
          BASE_URI+'Section_4/Set_6/Question_06',BASE_URI+'Section_4/Set_6/Question_07',BASE_URI+'Section_4/Set_6/Question_08',
          BASE_URI+'Section_4/Set_6/Question_09'],
         [BASE_URI+'Section_4/Set_7/Question_00',BASE_URI+'Section_4/Set_7/Question_01',BASE_URI+'Section_4/Set_7/Question_02',
          BASE_URI+'Section_4/Set_7/Question_03',BASE_URI+'Section_4/Set_7/Question_04',BASE_URI+'Section_4/Set_7/Question_05',
          BASE_URI+'Section_4/Set_7/Question_06',BASE_URI+'Section_4/Set_7/Question_07',BASE_URI+'Section_4/Set_7/Question_08',
          BASE_URI+'Section_4/Set_7/Question_09']]

# Stuff for Decisions

dec=[[BASE_URI+'Section_0/Set_1/Question_01_0', 'Workflow Documentation', 'Workflow Dokumentation', 'Workflow Search', 'Workflow Suche'],
     [BASE_URI+'Section_2/Set_1/Question_03_0', 'Theoretical Workflow', 'Theoretischer Workflow', 'Experimental Workflow', 'Experimenteller Workflow'],
     [BASE_URI+'Section_6/Set_1/Question_01_0', 'Markdown File', 'MaRDI Portal'],
     [BASE_URI+'Section_6/Set_1/Question_02_0', 'No', 'Nein'],
     [BASE_URI+'Section_1/Set_1/Question_00_0', 'Yes', 'Ja'],
     [BASE_URI+'Section_1/Set_1/Question_02_0', 'Yes', 'Ja'],
     [BASE_URI+'Section_1/Set_1/Question_04_0', 'Yes', 'Ja']]

# Question IDs required for data integration into MaRDI KG

ws = {'doi': [BASE_URI+'Section_2/Set_1/Question_02_0'],    # Question for cited paper
      'mod': [BASE_URI+'Section_3/Set_1/Wiki_01',           # Questions for applied model
              BASE_URI+'Section_3/Set_1/Question_01',
              BASE_URI+'Section_3/Set_1/Wiki_02',
              BASE_URI+'Section_3/Set_1/Wiki_03',
              BASE_URI+'Section_3/Set_1/Wiki_04',
              BASE_URI+'Section_3/Set_1/Question_00'],
      'met': [BASE_URI+'Section_4/Set_2/Question_01',       # Questions for applied methods
              BASE_URI+'Section_4/Set_2/Question_02',
              BASE_URI+'Section_4/Set_2/Wiki_02',
              BASE_URI+'Section_4/Set_2/Wiki_03',
              BASE_URI+'Section_4/Set_2/Wiki_04',
              BASE_URI+'Section_4/Set_2/Question_00'],
      'sof': [BASE_URI+'Section_4/Set_3/Question_01',       # Questions for applied softwares
              BASE_URI+'Section_4/Set_3/Question_02',
              BASE_URI+'Section_4/Set_3/Question_03',
              BASE_URI+'Section_4/Set_3/Question_05',
              BASE_URI+'Section_4/Set_3/Question_00'],
      'dis': [BASE_URI+'Section_2/Set_3/Question_01_0'],    # Question for related disciplines
      'obj': [BASE_URI+'Section_2/Set_2/Question_01_0'],    # Question for related research objective
      'inp': [BASE_URI+'Section_4/Set_6/Question_00',       # Questions for related input data sets
              BASE_URI+'Section_4/Set_6/Question_01',
              BASE_URI+'Section_4/Set_6/Question_10'],
      'out': [BASE_URI+'Section_4/Set_7/Question_00',       # Questions for related output data sets
              BASE_URI+'Section_4/Set_7/Question_01',
              BASE_URI+'Section_4/Set_7/Question_10'],
      'sea': [BASE_URI+'Section_1/Set_1/Question_01_0',       # Questions for Workflow search
              BASE_URI+'Section_1/Set_1/Question_03_0',
              BASE_URI+'Section_1/Set_1/Question_05_0']}

# Set IDs

sts=['Section_4/Set_2',
     'Section_4/Set_3',
     'Section_4/Set_6',
     'Section_4/Set_7']

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

# DEFAULT ANSWERS

defs=[['<N/A>', '<N/A>'],
      ['<NAME>','<NAME>'],
      ['<DESCRIPTION>','<BESCHREIBUNG>'],
      ['<EXTERNAL ID>','<EXTERNE ID>'],
      ['<KEY WORD>','<SCHLAGWORT>'],
      ['<RESEARCH OBJECTIVE>','<FORSCHUNGSGEGENSTAND>']]

# Refine Stuff

refine_strs=[BASE_URI+"Section_\d{1}/Set_\d{1}/Question_\d{2}_\d",
             BASE_URI+"Section_\d{1}/Set_\d{1}/Question_\d{2}",
             BASE_URI+"Section_\d{1}/Set_\d{1}/Wiki_\d{2}_\d",
             BASE_URI+"Section_\d{1}/Set_\d{1}/Wiki_\d{2}"]

# Link Stuff

linkers = [['mardi:','[Q0-9]+',mardi_wiki+'Item:'],
           ['wikidata:','[Q0-9]+','https://www.wikidata.org/wiki/Item:'],
           ['sw:','[0-9]+','https://swmath.org/software/'],
           ['doi:','10.\d{4,9}/[-._;()/:a-z0-9A-Z]+','https://dx.doi.org/']]

