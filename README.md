<div align='center' style="margin-top: 50px; font-size: 14px; color: grey;">
  <img src="https://github.com/user-attachments/assets/98c92c58-9d31-41ca-a3ca-189bbfb92101" />
  <p>MaRDMO Logo by <a href="https://www.mardi4nfdi.de/about/mission" target="_blank" style="color: grey;">MaRDI</a>, licensed under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank" style="color: grey;">CC BY-NC-ND 4.0</a>.</p>
</div>


# MaRDMO Plugin

This repository contains the MaRDMO Plugin for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) (RDMO) developed within the [Mathematical Research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). The plugin allows a standardized documentation of interdisciplinary workflows, where the connection to experiments or computational approaches, like simulations, is possible and desired. Documented workflows can be stored locally (depreciated) or shared with other scientists on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal). In the latter case a Wiki Page is created for the documented workflow and integral aspects of the workflow are integrated into the MaRDI Knowledge Graph. Integration into the MaRDI Knowledge Graph allows specific workflow queries which are also possible through the MaRDMO Plugin.

To document the underlying mathematical model(s) MaRDMO relies on the [MathModDB](https://portal.mardi4nfdi.de/wiki/MathModDB) ontology developed within Task Area 4 of MaRDI. Existing model documentations are retrieved from the MathModDB Knowledge Graph, direct publication of documented models into the MathModDB Knowledge Graph will be enabled in the near future. So far, documented models can only be exported into a Model Documentation Template. Upon request these documentations will be reviewed and integrated into the Knowledge Graph. Model documentations are possible as part of the workflow documentation and individually. 
  
## MaRDMO Plugin Installation

To use the MaRDMO Plugin at least `RDMO v2.0.0` is required. Follow the installation / update instructions of [RDMO](https://rdmo.readthedocs.io/en/latest/installation) if required. 

Go to the `rdmo-app` directory of your RDMO installation. In the virtual environment of the RDMO installation install the MaRDMO Plugin:

```bash
pip install git+https://github.com/MarcoReidelbach/MaRDMO-Plugin
```

To connect the MaRDMO Plugin with the RDMO installation add the following lines to `config/settings/local.py` (if not already present):

```python
from django.utils.translation import gettext_lazy as _ 
``` 

```python
INSTALLED_APPS = ['MaRDMO'] + INSTALLED_APPS

PROJECT_EXPORTS += [
        ('mde', _('MaRDI Export/Query'), 'MaRDMO.export.MaRDIExport'),
        ]

OPTIONSET_PROVIDERS = [
    ('MaRDIAndWikidataSearch', _('Options for MaRDI and Wikidata Search'), 'MaRDMO.providers.MaRDIAndWikidataSearch'),
    ('MaRDISearch', _('Options for MaRDI Search'), 'MaRDMO.providers.MaRDISearch'),
    ('MSCProvider', _('Options for Mathematical Subject Classification Search'), 'MaRDMO.providers.MSCProvider'),
    ('ProcessorProvider', _('Options for Processor Search'), 'MaRDMO.providers.ProcessorProvider'),
    ('AvailableSoftware', _('Options for Available Software'), 'MaRDMO.providers.AvailableSoftware'),
    ('MathAreaProvider', _('Options for Math Areas'), 'MaRDMO.providers.MathAreaProvider'),
    ('EnvironmentProvider', _('Options for Environments'), 'MaRDMO.providers.EnvironmentProvider'),
    ('MethodProvider', _('Options for Methods'), 'MaRDMO.providers.MethodProvider'),
    ('DataProvider', _('Options for Data Sets'), 'MaRDMO.providers.DataProvider'),
    ('SoftwareProvider', _('Options for Software'), 'MaRDMO.providers.SoftwareProvider'),
    ('ResearchField', _('Options for Research Fields'), 'MaRDMO.providers.ResearchField'),
    ('RelatedResearchField', _('Options for Related Research Fields'), 'MaRDMO.providers.RelatedResearchField'),
    ('ResearchProblem', _('Options for Research Problems'), 'MaRDMO.providers.ResearchProblem'),
    ('ResearchFieldWithUserAddition', _('Options for Research Fields with User Additions'), 'MaRDMO.providers.ResearchFieldWithUserAddition'),
    ('RelatedResearchProblem', _('Options for Related Research Problems'), 'MaRDMO.providers.RelatedResearchProblem'),
    ('MathematicalModel', _('Options for Mathematical Models'), 'MaRDMO.providers.MathematicalModel'),
    ('RelatedMathematicalModel', _('Options for related Mathematical Model'), 'MaRDMO.providers.RelatedMathematicalModel'),
    ('MathematicalModelWithUserAddition', _('Options for Mathematical Models with User Additions'), 'MaRDMO.providers.MathematicalModelWithUserAddition'),
    ('QuantityOrQuantityKind', _('Options for Quantities and Quantity Kinds'), 'MaRDMO.providers.QuantityOrQuantityKind'),
    ('RelatedQuantity', _('Options for related Quantities'), 'MaRDMO.providers.RelatedQuantity'),
    ('RelatedQuantityKind', _('Options for related Quantity Kinds'), 'MaRDMO.providers.RelatedQuantityKind'),
    ('MathematicalFormulation', _('Options for Mathematical Formulation'), 'MaRDMO.providers.MathematicalFormulation'),
    ('MathematicalFormulationWithUserAddition', _('Options for Mathematical Formulations with User Additions '), 'MaRDMO.providers.MathematicalFormulationWithUserAddition'),
    ('QuantityOrQuantityKindWithUserAddition', _('Options for Quantities and Quantity Kinds with User Additions'), 'MaRDMO.providers.QuantityOrQuantityKindWithUserAddition'),
    ('WorkflowTask', _('Options for Workflow Task'), 'MaRDMO.providers.WorkflowTask'),
    ('Task', _('Options for Task'), 'MaRDMO.providers.Task'),
    ('RelatedTask', _('Options for related Tasks'), 'MaRDMO.providers.RelatedTask'),
    ('Publication', _('Options for Publications'), 'MaRDMO.providers.Publication'),
    ('AllEntities', _('Options for All Entities'), 'MaRDMO.providers.AllEntities')
    ]

```

Thereby, the MaRDMO Plugin is installed and a "MaRDI Export/Query" button is added in the project view.

## MaRDI Portal Connection

To add data to the MaRDI Portal, so far, a login is required. In the MaRDMO Plugin this is facilitated using a bot. To set up the bot visit the MaRDI Portal, log in with your user credentials, choose `Special Pages` and `Bot passwords`. Provide a name for the new bot, select `Create`, grant the bot permission for `High-volume (bot) access`, `Edit existing pages` and `Create, edit, and move pages` and select again `Create`. Thereby, a bot is created. Add its credentials to `config/settigs/local.py`:

```python
lgname = 'username@botname'
lgpassword = 'password'
```

Workflow search and local documentations are possible without login credentials. Non-MaRDI users may contact the owner of the repository to facilitate the login for MaRDI portal publication.

## MaRDMO-Questionnaire        

The MaRDMO Plugin requires the [MaRDMO-Questionnaire](https://github.com/MarcoReidelbach/MaRDMO-Questionnaire). To get the Questionnaire clone the repository to an appropriate location: 

```bash
git clone https://github.com/MarcoReidelbach/MaRDMO-Questionnaire.git
```

Integrate the MaRDMO Questionnaire into your RDMO instance through the user interface of your RDMO instance (`Management -> Import -> attributes.xml/optionsets.xml/conditions.xml/catalogs.xml`) or via 

```bash
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/attributes.xml
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/optionsets.xml
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/conditions.xml
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/catalogs.xml
```

## Usage of MaRDMO Plugin

Once the MaRDMO Plugin is set up, the Questionnaire can be used to document and query interdisciplinary workflows and/or mathematical models. Therefore, select "Create New Project" in RDMO, choose a proper project name (project name will be used as wokflow name and label in the MaRDI portal), assign the "MaRDI Workflow Documentation" catalog and select "Create Project". The project is created. On the right hand side in the "Export" category the "MaRDI Export/Query" button is located to process the completed Questionnaire.     

Choose "Answer Questions" to start the interview. The first questions define the Operation Modus of the MaRDMO Plugin. Following an Identification, question for the Workflow and/or Mathematical model documentation are provided. Once all questions are answered, return to the project overview page, choose 'MaRDI Export/Query' and your Workflow and/or Mathematical Model will be exported as selected during the interview.  

