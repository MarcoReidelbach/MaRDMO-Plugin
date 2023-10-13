# MaRDMO

This repository contains a questionnaire and an Export/Query Plugin for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) (RDMO) developed within Task Area 4 "Interdisciplinary Mathematics" of the [Mathematical Research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). 

The questionnaire allows a standardized documentation of interdisciplinary workflows related to mathematics, where the connection to "real" experiments or theoretical approaches, like simulations, is possible and desired.

The Export/Query Plugin allows the user to export documented workflows into a standardized template, which could be stored locally as Markdown File (depreciated) or shared with others as Wiki Page on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal). Furthermore, integral aspects of the workflows are integrated into the MaRDI Knowledge Graph thus enabling specific workflow queries. 

The functionality of the Export/Query Plugin is captured in the questionnaire, such that a single button controls everything. 

MaRDMO connects individual RDMO instances with the MaRDI Portal and its underlying Knowledge Graph. To use MaRDMO with any other [wikibase](https://www.mediawiki.org/wiki/Wikibase/Installation) a setup script (`func/export.py`) is provided to prepare the wikibase for MaRDMO. 

## Structure of MaRDMO directory

```bash
. 
├── catalog - Questionnaire Files 
│   ├── conditions.xml - individual conditions of Questionnaire 
│   ├── domains.xml - individual domains of Questionnaire 
│   ├── options.xml - individual options of Questionnaire 
│   └── questions.xml - individual questions for Questionnaire 
│ 
├── requirements.txt - File to set up virtual environment 
│ 
├── func - Plugin Files
│   ├── citation.py - get citation from DOI and ORCID API 
│   ├── config_empty.py - wikibase information (API,SPARQL endpoint, bot credentials)
│   ├── export.py - Export/Query Function 
│   ├── display.py - HTTPResponse display information
│   ├── id.py - wikibase item and property ids 
│   ├── para.py - Export/Query Parameters
│   ├── providers.py - Dynamic Option Sets via Wikidata / MaRDI KG
│   ├── sparql.py - SPARQL query selection
│   └── setup.py - Setup File for other wikibases
│ 
└── LICENSE.md 
```
  
## MaRDMO Installation

To use the MaRDMO Plugin at least `RDMO v2.0.0` is required. Follow the installation / update instructions of [RDMO](https://rdmo.readthedocs.io/en/latest/installation) if required. 

Go to the `rdmo-app` directory of your RDMO installation and clone the MaRDMO Plugin directory:

```bash
git clone https://github.com/MarcoReidelbach/MaRDMO.git
```

In the virtual environment of the RDMO installation install the requirements of the MaRDMO Plugin:

```bash
pip install --upgrade pip setuptools 
pip install -r MaRDMO/requirements.txt
```

To connect the MaRDMO Plugin with the RDMO installation add the following lines to `config/settings/local.py` (if not already present):

```python
from django.utils.translation import ugettext_lazy as _ 
``` 

```python
INSTALLED_APPS = ['MaRDMO'] + INSTALLED_APPS

PROJECT_EXPORTS += [
        ('mde', _('MaRDI Export/Query'), 'MaRDMO.func.export.MaRDIExport'),
        ]

OPTIONSET_PROVIDERS = [
    ('WikidataSearch', _('Options for Wikidata Search'), 'MaRDMO.func.providers.WikidataSearch')
    ]
```

Thereby, the MaRDMO Plugin is installed and a "MaRDI Export/Query" Button is added in the Project View. The optionset provider allows direct Wikidata / MaRDI KG queries while answering the questionnaire. 
## MaRDI Portal Connection

To connect the MaRDMO Plugin with the MaRDI Portal adjust the config file:

```bash
mv MaRDMO/func/config_empty.py MaRDMO/func/config.py
```

The config file holds important information for MaRDMO, namely, URIs of the Wiki, API and SPARQL endpoint of the MaRDI Portal, the SPARQL endpoint of Wikidata and prefixes for MaRDI Portal SPARQL queries. If MaRDMO should be used with a Wikibase other than the MaRDI Portal, the Wikibase information need to be adjusted. 

Until now, edits on the MaRDI Portal require a login. In MaRDMO this is facilitated using a bot. To set up the bot visit the MaRDI Portal, log in with your user credentials, choose `Special Pages` and `Bot passwords`. Provide a name for the new bot, select `Create`, grant the bot permission for `High-volume (bot) access`, `Edit existing pages` and `Create, edit, and move pages` and seelct again `Create`. Thereby, a bot is created. Add the name of the bot `username@botname` (lgname) and the password (lgpassword) to the config file of the MaRDMO Plugin. Non-MaRDI users may contact the owner of the repository.

## MaRDMO Questionnaire        

The MaRDMO Plugin requires the MaRDMO Questionnaire. To use the Questionnaire visit the web interface of the RDMO installation, select `Management` and import the `domains.xml`, `options.xml`, `conditions.xml` and `questions.xml` from the `MaRDMO/catalog` directory othe MaRDMO Plugin.

## Usage of MaRDMO

Once MaRDMO is set up, the Questionnaire can be used to document and query interdisciplinary workflows. Therefore, select "Create New Project" in RDMO, choose a proper project name (project name will be used as wokflow name and label in the wikibase), assign the "MaRDI Workflow Documentation" catalog and select "Create Project". The project is created. On the right hand side in the "Export" category the "MaRDI Export/Query" button is located to process the completed Questionnaire.     

Choose "Answer Questions" to start the interview. With the first question the Operation Modus of the MaRDMO Plugin is determined:

1) Choose **"Workflow Documentation"** and click on "Save and proceed". Next, decide whether the completed Questionnaire should be exported locally or publicly on the MaRDI Portal. If a public export is desired a preview of the rendered Wiki Page could be displayed. Please, check the preview before publishing the workflow on the MaRDI Portal. Once the general settings are completed the workflow will be documented by providing general information, model information, process information and reproducibility information. Upon completion return to the project page and choose "MaRDI Export/Query" to compile the answers and return it in the desired format. 

2) Choose **"Workflow Search"** and click on "Save and proceed". Next, choose by which component existing workflow documentations should be searched and specify the component. Once completed, return to the project page and choose "MaRDI Export/Query". If appropriate workflow documentations are located on the MaRDI Portal, the corresponding URIs are displayed. 

