<div align='center' style="margin-top: 50px; font-size: 14px; color: grey;">
  <img src="https://github.com/user-attachments/assets/98c92c58-9d31-41ca-a3ca-189bbfb92101" />
  <p>MaRDMO Logo by <a href="https://www.mardi4nfdi.de/about/mission" target="_blank" style="color: grey;">MaRDI</a>, licensed under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank" style="color: grey;">CC BY-NC-ND 4.0</a>.</p>
</div>


# MaRDMO Plugin

This repository contains the MaRDMO Plugin for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) (RDMO) developed within the [Mathematical Research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). The plugin allows a standardized documentation of interdisciplinary workflows, where the connection to experiments or computational approaches, like simulations, is possible and desired. Documented workflows can be stored locally (depreciated) or shared with other scientists on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal). In the latter case a Wiki Page is created for the documented workflow and integral aspects of the workflow are integrated into the MaRDI Knowledge Graph. Integration into the MaRDI Knowledge Graph allows specific workflow queries which are also possible through the MaRDMO Plugin.

To document the underlying mathematical model(s) MaRDMO relies on the [MathModDB](https://portal.mardi4nfdi.de/wiki/MathModDB) ontology developed within Task Area 4 of MaRDI. Existing model documentations are retrieved from the MathModDB Knowledge Graph. Export into the MathModDB KG is possible upon authentification. If credentials are missing, it is possible to export the documented model into a standardized model documentation template and share it with the MaRDI TA4 Team for integration.    
  
## MaRDMO Plugin Installation

To use the MaRDMO Plugin at least `RDMO v2.0.0` is required. Follow the installation / update instructions of [RDMO](https://rdmo.readthedocs.io/en/latest/installation) if required. 

Go to the `rdmo-app` directory of your RDMO installation. In the virtual environment of the RDMO installation install the MaRDMO Plugin:

```bash
pip install MaRDMO
```

To connect the MaRDMO Plugin with the RDMO installation add the following lines to `config/settings/local.py` (if not already present):

```python
from django.utils.translation import gettext_lazy as _ 
``` 

```python
INSTALLED_APPS = ['MaRDMO'] + INSTALLED_APPS

PROJECT_EXPORTS += [
        ('wikibase', _('MaRDMO Button'), 'MaRDMO.main.MaRDMOExportProvider'),
        ]

OPTIONSET_PROVIDERS = [
    # Search
    ('MaRDISearch', _('Options for MaRDI Search'), 'MaRDMO.search.providers.MaRDISearch'),
    # Workflow
    ('MaRDIAndWikidataSearch', _('Options for MaRDI and Wikidata Search'), 'MaRDMO.workflow.providers.MaRDIAndWikidataSearch'),
    ('MainMathematicalModel', _('Options for Main Mathematical Model'), 'MaRDMO.workflow.providers.MainMathematicalModel'),
    ('WorkflowTask', _('Options for Workflow Task'), 'MaRDMO.workflow.providers.WorkflowTask'),
    ('SoftwareW', _('Options for Software (Workflow)'), 'MaRDMO.workflow.providers.Software'),
    ('Hardware', _('Options for Hardware'), 'MaRDMO.workflow.providers.Hardware'),
    ('Instrument', _('Options for Instruments'), 'MaRDMO.workflow.providers.Instrument'),
    ('DataSet', _('Options for Data Sets'), 'MaRDMO.workflow.providers.DataSet'),
    ('RelatedDataSet', _('Options for related Data Sets'), 'MaRDMO.workflow.providers.RelatedDataSet'),
    ('RelatedSoftware', _('Options for related Software'), 'MaRDMO.workflow.providers.RelatedSoftware'),
    ('RelatedInstrument', _('Options for related Instruments'), 'MaRDMO.workflow.providers.RelatedInstrument'),
    ('Method', _('Options for Methods'), 'MaRDMO.workflow.providers.Method'),
    ('RelatedMethod', _('Options for related Methods'), 'MaRDMO.workflow.providers.RelatedMethod'),
    ('ProcessStep', _('Options for Process Step'), 'MaRDMO.workflow.providers.ProcessStep'),
    ('Discipline', _('Options for Disciplines'), 'MaRDMO.workflow.providers.Discipline'),
    # Model
    ('ResearchField', _('Options for Research Fields'), 'MaRDMO.model.providers.ResearchField'),
    ('RelatedResearchField', _('Options for Related Research Fields'), 'MaRDMO.model.providers.RelatedResearchField'),
    ('ResearchProblem', _('Options for Research Problems'), 'MaRDMO.model.providers.ResearchProblem'),
    ('RelatedResearchProblem', _('Options for Related Research Problems'), 'MaRDMO.model.providers.RelatedResearchProblem'),
    ('MathematicalModel', _('Options for Mathematical Model'), 'MaRDMO.model.providers.MathematicalModel'),
    ('RelatedMathematicalModel', _('Options for related Mathematical Model'), 'MaRDMO.model.providers.RelatedMathematicalModel'),
    ('QuantityOrQuantityKind', _('Options for Quantities and Quantity Kinds'), 'MaRDMO.model.providers.QuantityOrQuantityKind'),
    ('RelatedQuantity', _('Options for related Quantities'), 'MaRDMO.model.providers.RelatedQuantity'),
    ('RelatedQuantityKind', _('Options for related Quantity Kinds'), 'MaRDMO.model.providers.RelatedQuantityKind'),
    ('RelatedQuantityOrQuantityKind', _('Options for related Quantites or Quantity Kinds'), 'MaRDMO.model.providers.RelatedQuantityOrQuantityKind'),
    ('MathematicalFormulation', _('Options for Mathematical Formulation'), 'MaRDMO.model.providers.MathematicalFormulation'),
    ('RelatedMathematicalFormulation', _('Options for related Mathematical Formulations'), 'MaRDMO.model.providers.RelatedMathematicalFormulation'),
    ('AllEntities', _('Options for All Entities'), 'MaRDMO.model.providers.AllEntities'),
    ('Task', _('Options for Task'), 'MaRDMO.model.providers.Task'),
    ('RelatedTask', _('Options for related Tasks'), 'MaRDMO.model.providers.RelatedTask'),
    # Publication
    ('Publication', _('Options for Publication'), 'MaRDMO.publication.providers.Publication'),
    # Algorithm
    ('Algorithm', _('Options for Algorithms'), 'MaRDMO.algorithm.providers.Algorithm'),
    ('RelatedAlgorithm', _('Options for related Algorithms'), 'MaRDMO.algorithm.providers.RelatedAlgorithm'),
    ('AlgorithmicProblem', _('Options for Algorithmic Problems'), 'MaRDMO.algorithm.providers.AlgorithmicProblem'),
    ('RelatedAlgorithmicProblem', _('Options for related Algorithmic Problems'), 'MaRDMO.algorithm.providers.RelatedAlgorithmicProblem'),
    ('SoftwareAL', _('Options for Software (Algorithm)'), 'MaRDMO.algorithm.providers.Software'),
    ('RelatedSoftwareAL', _('Options for related Software (Algorithm)'), 'MaRDMO.algorithm.providers.RelatedSoftware'),
    ('Benchmark', _('Options for Benchmarks'), 'MaRDMO.algorithm.providers.Benchmark'),
    ('RelatedBenchmark', _('Options for related Benchmarks'), 'MaRDMO.algorithm.providers.RelatedBenchmark'),
    ]
```

Thereby, the MaRDMO Plugin is installed and a "MaRDI Button" button is added in the project view.

## MaRDI Portal and MathModDB Connection

To add data to the MaRDI Portal an OAuth2 login procedure will be integrated soon. No export to the MaRDI Portal is possible until. Login via Bots is not supported anymore.

To write to the MathModDB KG a login is required. Credentials might be obtained by contacting the MaRDI staff. Add them to `config/settigs/local.py`:

```python
mathmoddb_username = 'username'
mathmoddb_password = 'password'
``` 

Local workflow and model documentations and workflow searches are possible without login credentials. Non-MaRDI users may contact the owner of the repository to facilitate the login for MaRDI portal and MathModDB publication.

## MaRDMO-Questionnaire        

The MaRDMO Plugin requires the [MaRDMO-Questionnaire](https://github.com/MarcoReidelbach/MaRDMO-Questionnaire), download its latest release [![Latest Release](https://img.shields.io/github/v/release/MarcoReidelbach/MaRDMO-Questionnaire)](https://github.com/MarcoReidelbach/MaRDMO-Questionnaire/releases/latest).

Integrate the MaRDMO Questionnaire into your RDMO instance through the user interface of your RDMO instance (`Management -> Import -> attributes.xml/optionsets.xml/conditions.xml/catalogs.xml`) or via 

```bash
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/attributes.xml
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/optionsets.xml
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/conditions.xml
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/mardmo-search-catalog.xml
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/mardmo-model-catalog.xml
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/mardmo-interdisciplinary-workflow-catalog.xml
python manage.py import /path/to/MaRDMO-Questionnaire/catalog/mardmo-algorithm-catalog.xml
```

## Usage of MaRDMO Plugin

Once the MaRDMO Plugin is set up, the Questionnaire can be used to document and query interdisciplinary workflows and/or mathematical models. Therefore, select "Create New Project" in RDMO, choose a proper project name (project name will be used as wokflow name and label in the MaRDI portal), assign the "MaRDMO Catalog" and select "Create Project". The project is created. On the right hand side in the "Export" category the "MaRDI Export/Query" button is located to process the completed Questionnaire.     

Choose "Answer Questions" to start the interview. The first questions define the operation modus of the MaRDMO Plugin. Following an identification, questions for the workflow and/or mathematical model documentation are provided. Once all questions are answered, return to the project overview page, choose 'MaRDI Export/Query' and your Workflow and/or Mathematical Model will be exported as selected during the interview.  

