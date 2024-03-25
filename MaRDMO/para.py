from .id import *
from .config import *

BASE_URI='http://example.com/terms/domain/MaRDI/'

# Raw Math Template

math_temp=''' 

PID (if applicable): '''+BASE_URI+'''Section_2/Set_1/Question_02_0

## Problem Statement

'''+BASE_URI+'''Section_2/Set_1/Question_01_0

### Object of Research and Objective

'''+BASE_URI+'''Section_2/Set_1/Question_04_0

### Procedure

'''+BASE_URI+'''Section_2/Set_1/Question_05_0

### Involved Disciplines

<b>Mathematical Areas:</b>

FIELDS

<b>Non-Mathematical Disciplines:</b>

DISCIPLINES

### Data Streams

'''+BASE_URI+'''Section_2/Set_3/Question_02_0

## Model

ID: '''+BASE_URI+'''Section_3/Set_0/Wiki_01_0

'''+BASE_URI+'''Section_3/Set_0/Set_0/Question_01_0 

'''+BASE_URI+'''Section_3/Set_0/Set_0/Wiki_02_0

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

'''+BASE_URI+'''Section_2/Set_1/Question_04_0

### Procedure

'''+BASE_URI+'''Section_2/Set_1/Question_05_0

### Involved Disciplines

<b>Mathematical Areas:</b>

FIELDS

<b>Non-Mathematical Disciplines:</b>

DISCIPLINES

### Data Streams

'''+BASE_URI+'''Section_2/Set_3/Question_02_0

## Model

ID: '''+BASE_URI+'''Section_3/Set_0/Wiki_01_0

'''+BASE_URI+'''Section_3/Set_0/Set_0/Question_01_0

'''+BASE_URI+'''Section_3/Set_0/Set_0/Wiki_02_0

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
           BASE_URI+'Section_4/Set_4/Question_04',BASE_URI+'Section_4/Set_4/Question_05',BASE_URI+'Section_4/Set_4/Question_06'],
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

# Question IDs required for data integration into MaRDI KG

ws = {'doi': [BASE_URI+'Section_2/Set_1/Question_02_0'],    # Question for cited paper
      'mod': [BASE_URI+'Section_3/Set_0/Wiki_01',           # Questions for applied model
              BASE_URI+'Section_3/Set_0/Set_0/Question_01',
              BASE_URI+'Section_3/Set_0/Set_0/Wiki_02',
              BASE_URI+'Section_3/Set_0/Wiki_03',
              BASE_URI+'Section_3/Set_0/Wiki_04',
              BASE_URI+'Section_3/Set_0/Question_00'],
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
      'fie': [BASE_URI+'Section_2/Set_3/Question_00_0'],    # Question for mathematical fields
      'dis': [BASE_URI+'Section_2/Set_3/Question_01_0'],    # Question for related disciplines
      'obj': [BASE_URI+'Section_2/Set_1/Question_04_0'],    # Question for related research objective
      'inp': [BASE_URI+'Section_4/Set_6/Question_00',       # Questions for related input data sets
              BASE_URI+'Section_4/Set_6/Question_01',
              BASE_URI+'Section_4/Set_6/Question_10'],
      'out': [BASE_URI+'Section_4/Set_7/Question_00',       # Questions for related output data sets
              BASE_URI+'Section_4/Set_7/Question_01',
              BASE_URI+'Section_4/Set_7/Question_10'],
      'sea': [BASE_URI+'Section_1/Set_1/Question_01_0',     # Questions for Workflow search
              BASE_URI+'Section_1/Set_1/Question_03_0',
              BASE_URI+'Section_1/Set_1/Question_05_0']}

# Set IDs

sts=['Section_4/Set_2',
     'Section_4/Set_3',
     'Section_4/Set_6',
     'Section_4/Set_7']

# Language Dictionary

lang_dict={'af':['wikidata:Q14196', 'Afrikaans', 'West Germanic language, spoken in South Africa and Namibia'],
           'ar':['wikidata:Q13955', 'Arabic', 'Semitic language and lingua franca of the Arab world'],
           'bg':['wikidata:Q7918', 'Bulgarian', 'South Slavic language'],
           'bn':['wikidata:Q9610', 'Bangla', 'Indo-Aryan language mostly spoken in Bangladesh and India'],
           'ca':['wikidata:Q7026', 'Catalan', 'Western Romance language'],
           'cs':['wikidata:Q9056', 'Czech', 'West Slavic language'],
           'cy':['wikidata:Q9309', 'Welsh', 'Brythonic language spoken natively in Wales'],
           'da':['wikidata:Q9035', 'Danish', 'North Germanic language spoken in Denmark'],
           'de':['wikidata:Q188', 'German', 'West Germanic language spoken mainly in Central Europe'],
           'el':['wikidata:Q9129', 'Greek', 'Indo-European language'],
           'en':['wikidata:Q1860', 'English', 'West Germanic language'],
           'es':['wikidata:Q1321', 'Spanish', 'Romanic language originating in the Iberian Peninsula'],
           'et':['wikidata:Q9072', 'Estonian', 'Uralic language'],
           'fa':['wikidata:Q9168', 'Persian', 'Southwestern Iranian dialect continuum spoken in the Caucasus, Central Asia, Iran, Kuwait, and Pakistan'],
           'fi':['wikidata:Q1412', 'Finnish', 'Finno-Ugric language mostly spoken in Finland'],
           'fr':['wikidata:Q150', 'French', 'Romance language'],
           'gu':['wikidata:Q5137', 'Gujarati', 'Indo-Aryan language that is spoken on the state of Gujarat'],
           'he':['wikidata:Q9288', 'Hebrew', 'Northwest Semitic language'],
           'hi':['wikidata:Q1568', 'Hindi', 'Indo-Aryan language spoken in India'],
           'hr':['wikidata:Q6654', 'Croatian', 'standardized variety of Serbo-Croatian language, used by Croats'],
           'hu':['wikidata:Q9067', 'Hungarian', 'Urlaic language'],
           'id':['wikidata:Q9240', 'Indonesian', 'official language of Indonesia'],
           'it':['wikidata:Q652', 'Italian', 'Romance language'],
           'ja':['wikidata:Q5287', 'Japanese', 'language spoken in East Asia'],
           'kn':['wikidata:Q33673', 'Kannada', 'Dravidian language'],
           'ko':['wikidata:Q9176', 'Korean', 'language spoken in Korean Peninsula and some part of North-eastern China'],
           'lt':['wikidata:Q9083', 'Lithuanian', 'Baltic language spoken in Lithuania'],
           'lv':['wikidata:Q9078', 'Latvian', 'Baltic language, official in Latvia and the European Union'],
           'mk':['wikidata:Q9296', 'Macedonian', 'South Slavic language mostly spoken in North Macedonia and its neighbouring countries'],
           'ml':['wikidata:Q36236', 'Malayalam', 'Dravidian language of India'],
           'mr':['wikidata:Q1571', 'Marathi', 'Indo-Aryan language'],
           'ne':['wikidata:Q33823', 'Nepali', 'official language of Nepal'],
           'nl':['wikidata:Q7411', 'Dutch', 'West Germanic language'],
           'no':['wikidata:Q9043', 'Norwegian', 'North Germanic language spoken in Norway'],
           'pa':['wikidata:Q58635', 'Punjabi', 'Indo-Aryan language spoken in the Punjab region of Pakistan and India'],
           'pl':['wikidata:Q809', 'Polish', 'West Slavic language'],
           'pt':['wikidata:Q5146', 'Portuguese', 'Western Romance language of the Indo-European language family'],
           'ro':['wikidata:Q7913', 'Romanian', 'Eastern Romance language, official of Romania'],
           'ru':['wikidata:Q7737', 'Russian', 'East Slavic language'],
           'sk':['wikidata:Q9058', 'Slovak', 'West Slavic language spoken in Slovakia'],
           'sl':['wikidata:Q9063', 'Slovene', 'South Slavic language spoken primarily in Slovenia'],
           'so':['wikidata:Q13275', 'Somali', 'Afroasiatic language belonging to the Cushitic branch'],
           'sq':['wikidata:Q8748', 'Albanian', 'Indo-European language, spoken in Albania, Kosovo, North Macedonia and Montenegro as well as Italy, Croatia, Romania and Sebia'],
           'sv':['wikidata:Q9027', 'Swedish', 'North Germanic language spoken in Sweden and Finland'],
           'sw':['wikidata:Q7838', 'Swahili', 'Bantu language spoken mainly in East Africa'],
           'ta':['wikidata:Q5885', 'Tamil', 'Dravidian language native to South India and Sri Lanka'],
           'te':['wikidata:Q8097', 'Telugu', 'Dravidian language native to South India'],
           'th':['wikidata:Q9217', 'Thai', 'Tai language'],
           'tl':['wikidata:Q34057', 'Tagalog', 'Austronesian language and the national language of the Philippines'],
           'tr':['wikidata:Q256', 'Turkish', 'Oghuz Turkic language of the Turkish people'],
           'uk':['wikidata:Q8798', 'Ukrainian', 'East Slavic language'],
           'ur':['wikidata:Q1617', 'Urdu', 'Indo-Aryan language spoken in South Asia'],
           'vi':['wikidata:Q9199', 'Vietnamese', 'Austroasiatic language originating in Vietnam'],
           'zh-cn':['wikidata:Q727694', 'Standard Mandarin', 'standard form of Chinese and the official language of China'],
           'zh-tw':['wikidata:Q262828', 'Standard Taiwanese Mandarin', 'variety of Mandarin serving as the official language of the Republic of China (Taiwan)']}

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

# Links for Version, Docs, Publish

VDP = [BASE_URI+'Section_4/Set_3/Question_07',
       BASE_URI+'Section_4/Set_3/Question_08',
       BASE_URI+'Section_4/Set_3/Question_09']

# IDs for Publication

pub_ids = [BASE_URI + 'Section_2/Set_1/Question_02',
           BASE_URI + 'Section_2/Set_2/Question_03',
           BASE_URI + 'Section_2/Set_2/Question_00_hidden',
           BASE_URI + 'Section_2/Set_2/Question_01_hidden',
           BASE_URI + 'Section_2/Set_2/Question_02_hidden',
           BASE_URI + 'Section_2/Set_2/Question_03_hidden',
           BASE_URI + 'Section_2/Set_2/Question_04_hidden',
           BASE_URI + 'Section_2/Set_2/Question_05_hidden',
           BASE_URI + 'Section_2/Set_2/Question_06_hidden',
           BASE_URI + 'Section_2/Set_2/Question_07_hidden',
           BASE_URI + 'Section_2/Set_2/Question_08_hidden',
           BASE_URI + 'Section_2/Set_2/Question_09_hidden']

# Keys for publication handler

keys = ['publicationQid', 'publicationLabel', 'publicationDescription1', 'authorInfo',
        'entrytypeQid', 'entrytypeLabel', 'entrytypeDescription1',
        'journalQid', 'journalLabel', 'journalDescription1',
        'languageQid', 'languageLabel', 'languageDescription1',
        'title', 'otherAuthor', 'publicationDate', 'volume', 'issue', 'page']

# Option Dictionary

option = {'YesText': 'https://rdmorganiser.github.io/terms/options/yes_with_text_no/yes',
          'Input': 'http://example.com/terms/options/QuantityAndQuantityKind_kind0',
          'Output': 'http://example.com/terms/options/QuantityAndQuantityKind_kind1',
          'Parameter': 'http://example.com/terms/options/QuantityAndQuantityKind_kind3',
          'TimeDiscrete': 'http://example.com/terms/options/MathematicalModel_proerpty6',
          'SpaceDiscrete': 'http://example.com/terms/options/MathematicalModel_proerpty5',
          'Documentation': 'http://example.com/terms/options/operation_modus/modus_0',
          'Search': 'http://example.com/terms/options/operation_modus/modus_1',
          'Local': 'http://example.com/terms/options/publication_type/type_1',
          'Public': 'http://example.com/terms/options/publication_type/type_0',
          'No': 'http://example.com/terms/options/yes_no/no',
          'Yes': 'http://example.com/terms/options/yes_no/yes',
          'Analysis': 'http://example.com/terms/options/workflow_type/type_0',
          'Computation': 'http://example.com/terms/options/workflow_type/type_1'}

# Answer Dictionary

answer = {'ResearchObjective': BASE_URI+'Section_2/Set_1/Question_04'}

