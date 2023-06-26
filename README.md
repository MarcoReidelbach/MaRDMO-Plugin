# MaRDMO

This repository contains a questionnaire and an Export/Query Plugin for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) (RDMO) developed within Task Area 4 "Interdisciplinary Mathematics" of the [Mathematical Research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). 

The questionnaire allows a standardized documentation of interdisciplinary workflows related to mathematics, where the connection to "real" experiments or theoretical approaches, like simulations, is possible and desired.

The Export/Query Plugin allows the user to export documented workflows into a standardized template, which could be stored locally as Markdown File (depreciated) or shared with others as Wiki Page on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal). Furthermore, integral aspects of the workflows are integrated into the MaRDI Knowledge Graph thus enabling specific workflow queries. 

The functionality of the Export/Query Plugin is captured in the questionnaire, such that a single button controls everything. 

MaRDMO connects individual RDMO instances with the MaRDI Portal and its underlying Knowledge Graph. To use MaRDMO with any other [wikibase](https://www.mediawiki.org/wiki/Wikibase/Installation) a script is provided to prepare the wikibase for MaRDMO. 

## Repository structure

```bash
. 
├── catalog - RDMO Questionnaire Files 
│   ├── conditions.xml - individual conditions of RDMO Questionnaire 
│   ├── domains.xml - individual domains of RDMO Questionnaire 
│   ├── options.xml - individual options of RDMO Questionnaire 
│   └── questions.xml - individual questions for RDMO Questionnaire 
│ 
├── environment.yml - File to set up MaRDMO conda environment 
│ 
├── func - Export/Query Plugin Files
│   ├── citation.py - get citation from DOI and ORCID API 
│   ├── config_empty.py - wikibase information 
│   ├── export.py - Export/Query Function 
│   ├── id.py - wikibase item and property ids 
│   ├── para.py - Export/Query Parameters
│   ├── sparql.py - SPARQL query selection
│   └── setup.py - Setup File for other wikibases
│ 
├── LICENSE.md
│ 
├── README.md 
│ 
└── templates - Files to render
    ├── errors.html 
    └── export.html 
```
  
## Installation

### RDMO and MaRDMO Plugin

To install RDMO check if you meet their [prerequisites](https://rdmo.readthedocs.io/en/latest/installation/prerequisites.html). If so, obtain the app directory by cloning the corresponding repository:

```bash
git clone https://github.com/rdmorganiser/rdmo-app
```

Likewise clone the MaRDMO directory:

```bash
cd rdmo-app
```

```bash
git clone https://github.com/MarcoReidelbach/MaRDMO.git
```

Once cloned, setup a virtual conda environment:

```bash
conda env create -f MaRDMO/environment.yml
```

Thereby, a virtual environment "MaRDMO" is created in which the RDMO package and further packages, e.g. `WikibaseIntegrator`, for the Export/Query Plugin are installed.  

Setup the RDMO application:

```bash
conda activate MaRDMO
```

```bash
cp config/settings/sample.local.py config/settings/local.py
```

```python
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
```

Thereby, the Export/Query Plugin is installed and a "MaRDI Export/Query" Button is added in the Project View.

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

