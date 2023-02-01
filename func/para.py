# Raw Math Template

math_temp='''# TEMPLATE_TITLE 

PID (if applicable): http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_2

## Problem Statement

http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_1

### Object of Research and Objective

http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_1

### Procedure

http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_2

### Involved Disciplines

http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_1

### Data Streams

http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_2

## Model

http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_1

### Discretization

* Time: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_2
* Space: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_3

### Variables

MATH_TAB_1 

## Process Informationen

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

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_1

### Runtime Reproducibility 

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_2

### Reproducibility of Results

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_3

### Reproducibility on original Hardware

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_4

### Reproducibility on other Hardware

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_5

### Transferability to

http://example.com/terms/domain/MaRDI/Section_5/Set_1/Question_6

# Legend

The following abbreviations are used in the document to indicate/resolve IDs:

doi: DOI / https://dx.doi.org/

sw: swMATH / https://swmath.org/software/

wikidata: https://www.wikidata.org/wiki/'''

# Raw Exp Template

exp_temp='''# TEMPLATE_TITLE

PID (if applicable): http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_2

## Problem Statement

http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_1

### Object of Research and Objective

http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_1

### Procedure

http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_2

### Involved Disciplines

http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_1

### Data Streams

http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_2

## Model

http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_1

### Discretization
(if applicable)

* Time: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_2
* Space: http://example.com/terms/domain/MaRDI/Section_3/Set_1/Question_3

### Variables

EXP_TAB_1

### Parameter

EXP_TAB_2

## Process Informationen

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

http://example.com/terms/domain/MaRDI/Section_5/Set_2/Question_1

### Reproducibility of the Experiments on other Devices/Instruments/Hardware

http://example.com/terms/domain/MaRDI/Section_5/Set_2/Question_2

### Transferability of the  Experiments to

http://example.com/terms/domain/MaRDI/Section_5/Set_2/Question_3

# Legend

The following abbreviations are used in the document to indicate/resolve IDs:

doi: DOI / https://dx.doi.org/

sw: swMATH / https://swmath.org/software/

wikidata: https://www.wikidata.org/wiki/'''

# Stuff to generate Tables for Math Template

math_tables=['MATH_TAB_1','MATH_TAB_2','MATH_TAB_3','MATH_TAB_4','MATH_TAB_5','MATH_TAB_6','MATH_TAB_7']

math_topics=[['Name','Unit','Symbol'],
             ['Name','Description','Input','Output','Method','Parameter','Environment','Mathematical Area'],
             ['ID','Name','Process Step','Parameter','implemented by'],
             ['ID','Name','Description','Version','Programming Language','Dependencies','versioned','published','documented'],
             ['ID','Name','Processor','Compiler','#Nodes','#Cores'],
             ['ID','Name','Size','Data Structure','Format Representation','Format Exchange','binary/text','proprietary','to publish','to archive'],
             ['ID','Name','Size','Data Structure','Format Representation','Format Exchange','binary/text','proprietary','to publish','to archive']]

math_ids=[['http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_1','http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_2','http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_3'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_2','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_3',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_5','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_6',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_7','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_8'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_2','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_3',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_5'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_2','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_3',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_5','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_6',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_7','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_8','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_9'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_2','http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_3',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_5','http://example.com/terms/domain/MaRDI/Section_4/Set_4/Question_5'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_0','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_2',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_3','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_5',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_6','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_7','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_8',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_9'],
          ['http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_0','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_2',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_3','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_5',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_6','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_7','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_8',
           'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_9']]

# Stuff to generate Tables for Esp Template

exp_tables=['EXP_TAB_1','EXP_TAB_2','EXP_TAB_3','EXP_TAB_4','EXP_TAB_5','EXP_TAB_6','EXP_TAB_7','EXP_TAB_8']

exp_topics=[['Name','Unit','Symbol','dependent (measured) / independent (controlled)'],
            ['Name','Unit','Symbol'],
            ['Name','Description','Input','Output','Method','Parameter','Environment','Mathematical Area'],
            ['ID','Name','Process Step','Parameter','realised / implemented by'],
            ['ID','Name','Description','Version','Programming Language','Dependencies','versioned','published','documented'],
            ['ID','Name','Description','Version','Part Nr','Serial Nr','Location','Software'],
            ['ID','Name','Size','Data Structure','Format Representation','Format Exchange','binary/text','proprietary','to publish','to archive'],
            ['ID','Name','Size','Data Structure','Format Representation','Format Exchange','binary/text','proprietary','to publish','to archive']]

exp_ids=[['http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_1','http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_2','http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_3',
          'http://example.com/terms/domain/MaRDI/Section_3/Set_2/Question_4'],
         ['http://example.com/terms/domain/MaRDI/Section_3/Set_3/Question_1','http://example.com/terms/domain/MaRDI/Section_3/Set_3/Question_2','http://example.com/terms/domain/MaRDI/Section_3/Set_3/Question_3'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_2','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_3',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_5','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_6',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_7','http://example.com/terms/domain/MaRDI/Section_4/Set_1/Question_8'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_2','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_3',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_5'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_2','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_3',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_5','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_6',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_7','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_8','http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_9'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_2','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_3',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_5','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_6',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_7','http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_8'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_0','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_2',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_3','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_5',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_6','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_7','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_8',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_9'],
         ['http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_0','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_2',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_3','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_4','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_5',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_6','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_7','http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_8',
          'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_9']]

# Stuff for KG export

KG_export=['http://example.com/terms/domain/MaRDI/Section_2/Set_2/Question_1','http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_2','http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_1']

# Stuff for Decisions

dec=[[['http://example.com/terms/domain/MaRDI/Section_0/Set_1/Question_1', 'Workflow Documentation'],['http://example.com/terms/domain/MaRDI/Section_0/Set_1/Question_1', 'Workflow Dokumentation']],
     [['http://example.com/terms/domain/MaRDI/Section_0/Set_1/Question_1', 'Workflow Finding'],['http://example.com/terms/domain/MaRDI/Section_0/Set_1/Question_1', 'Workflow Findung']],
     [['http://example.com/terms/domain/MaRDI/Section_6/Set_1/Question_1', 'Markdown File'],['http://example.com/terms/domain/MaRDI/Section_6/Set_1/Question_1', 'MaRDI Portal']],
     [['http://example.com/terms/domain/MaRDI/Section_1/Set_1/Question_0', 'Research Objective'],['http://example.com/terms/domain/MaRDI/Section_1/Set_1/Question_0', 'Forschungsziel']],
     [['http://example.com/terms/domain/MaRDI/Section_1/Set_1/Question_0', 'Methods'],['http://example.com/terms/domain/MaRDI/Section_1/Set_1/Question_0', 'Methoden']],
     [['http://example.com/terms/domain/MaRDI/Section_1/Set_1/Question_0', 'Input Data'],['http://example.com/terms/domain/MaRDI/Section_1/Set_1/Question_0', 'Eingabedaten']],
     [['http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_3', 'Mathematical Workflow'],['http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_3', 'Mathematischer Workflow']],
     [['http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_3', 'Experimental Workflow'],['http://example.com/terms/domain/MaRDI/Section_2/Set_1/Question_3', 'Experimenteller Workflow']],
     [['http://example.com/terms/domain/MaRDI/Section_6/Set_1/Question_2', 'No'],['http://example.com/terms/domain/MaRDI/Section_6/Set_1/Question_2','Nein']]]


