# MaRDMO

This repository contains a questionnaire and an Export/Query Plugin for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) (RDMO) developed within Task Area 4 "Interdisciplinary Mathematics" of the [Mathematical Research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). 

The questionnaire allows a standardized documentation of interdisciplinary workflows related to mathematics, where the connection to "real" experiments or theoretical approaches, like simulations, is possible and desired.

The Export/Query Plugin allows the user to export documented workflows into a standardized template, which could be stored locally as Markdown File (depreciated) or shared with others as Wiki Page on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal). Furthermore, integral aspects of the workflows are integrated into the MaRDI Knowledge Graph thus enabling specific workflow queries. 

The functionality of the Export/Query Plugin is captured in the questionnaire, such that a single button controls everything. 

MaRDMO connects individual RDMO instances with the MaRDI Portal and its underlying Knowledge Graph. To use MaRDMO with any other [wikibase](https://www.mediawiki.org/wiki/Wikibase/Installation) a script is provided to prepare the wikibase for MaRDMO. 

## Structure of MaRDMO directory in rdmo-app

```bash
. 
├── catalog - RDMO Questionnaire Files 
│   ├── conditions.xml - individual conditions of RDMO Questionnaire 
│   ├── domains.xml - individual domains of RDMO Questionnaire 
│   ├── options.xml - individual options of RDMO Questionnaire 
│   └── questions.xml - individual questions for RDMO Questionnaire 
│ 
├── requirements.txt - File to set up virtual environment 
│ 
├── func - Export/Query Plugin Files
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
  
## Installation

### RDMO and MaRDMO Plugin

Check if you meet the [prerequisites](https://rdmo.readthedocs.io/en/latest/installation/prerequisites.html) of RDMO. Install them, if required.

Clone the MaRDMO directory:

```bash
git clone https://github.com/MarcoReidelbach/MaRDMO.git
```

**Note:** So far MaRDMO is provided for test operation with an old `rdmo-app directory` to ensure compatibility to `RDMO 1.9.0`. In the future MaRDMO will be implemented as an extension of `RDMO 2.0`. 

Once cloned, setup a virtual environment in the `rdmo-app directory` containing `bibtexparser`, `langdetect`, `pylatexenc`, `pypandoc_binary` and `wikibaseintegrator`:

```bash
cd MaRDMO/rdmo-app
python3 -m venv env 
source env/bin/activate
pip install --upgrade pip setuptools 
pip install -r MaRDMO/requirements.txt
```

**Note:** So far `RDMO 1.9.0` is also installed through `requirements.txt`. In the future MaRDMO should be added to an existing RDMO instance.

Setup the RDMO application:

```bash
cp config/settings/sample.local.py config/settings/local.py
python manage.py migrate                
python manage.py setup_groups           
python manage.py createsuperuser
```

Your RDMO instance is now ready. To install the Export/Query Plugin add the following lines to `config/settings/local.py` and set **Debug = True**:

```python
from django.utils.translation import ugettext_lazy as _  
from . import BASE_DIR, INSTALLED_APPS, PROJECT_EXPORTS
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

Thereby, the Export/Query Plugin is installed and a "MaRDI Export/Query" Button is added in the Project View. The option set provider allows direct Wikidata / MaRDI KG queries. 

To connect MaRDMO with the MaRDI portal do

```bash
mv MaRDMO/func/config_empty.py MaRDMO/func/config.py
```

and add the bot credeantials to the file. 

If you want to use MaRDMO with a different wikibase adjust the URLs of the portal Wiki, API and SPARQL endpoint as well as the SPARQL prefixes in `MaRDMO/func/config.py`. As before, add the bot credentials.

Now, run RDMO and log in via your browser:

```bash
python manage.py runserver
```

To actually use RDMO, a questionnaire (or more than one) needs to be added. To do this, click on "Management", choose "Domain" and import `domains.xml` from `MaRDMO/catalog`. Do the same for `options.xml`, `conditions.xml` and `questions.xml` by choosing "Options", "Conditions" and "Questions", respectively. Ensure, that `questions.xml` is added last.

## Usage of RDMO and Export/Query Plugin

Once you completed the installation, the MaRDMO Questionnaire can be used to document and query workflows. Therefore, select "Create New Project" in RDMO and choose a proper name for your project (this name will be used as wokflow name and label in the wikibase), assign the "MaRDI Workflow Documentation" catalog and click on "Create Project". Your project is now created. On the right hand side in the "Export" category you may notice the "MaRDI Export/Query" button.      

Choose "Answer Questions" to start the interview. With the first question the Operation Modus of the Export/Query Plugin is determined:

1) If you choose **"Workflow Documentation"** and click on "Save and proceed", you have to decide in a next step if you want to do the documentation locally (as Markdown File) or if you want to publish the documentation as Wiki Page. If you choose Wiki Page publication, you can get an HTML preview before the actual export. Please, use the HTML preview to check if your documentation is rendered correctly (e.g. Latex Math Equations). Once again click "Save and proceed". Now, you will be guided through a series of questions (the individual questions are listed below) in order to document your workflow. For some of these questions you have to add sets, e.g. each variable of your workflow gets his own question set. Make sure to use integer numbers starting from 0 for the individual question set names. Once you have answered all questions return to the project page and choose "MaRDI Export/Query" to add your workflow documentation to the knowledge graph or download it. 

2) If you choose **"Workflow Finding"** and click on "Save and proceed", you will be directed to a page where you have to choose by which component you would like to search existing workflow documentations and describe your needs. Once described, click on "Save", return to the project page and choose "MaRDI Export/Query". If MaRDMO detects workflows in the wikibase which could be interesting for you, you will receive the URIs of the corresponding Wiki pages.

