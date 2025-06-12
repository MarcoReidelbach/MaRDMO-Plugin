<div align='center' style="margin-top: 50px; font-size: 14px; color: grey;">
  <img src="https://github.com/user-attachments/assets/98c92c58-9d31-41ca-a3ca-189bbfb92101" />
  <p>MaRDMO Logo by <a href="https://www.mardi4nfdi.de/about/mission" target="_blank" style="color: grey;">MaRDI</a>, licensed under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank" style="color: grey;">CC BY-NC-ND 4.0</a>.</p>
</div>


# MaRDMO Plugin

This repository contains the MaRDMO Plugin for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) (RDMO) developed within the [Mathematical Research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). The plugin allows a standardized documentation of interdisciplinary workflows, where the connection to experiments or computational approaches, like simulations, is possible and desired. Documented workflows can be stored locally (depreciated) or shared with other scientists on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal). In the latter case a Wiki Page is created for the documented workflow and integral aspects of the workflow are integrated into the MaRDI Knowledge Graph. Integration into the MaRDI Knowledge Graph allows specific workflow queries which are also possible through the MaRDMO Plugin.

To document the underlying mathematical model(s) MaRDMO relies on the [MathModDB](https://portal.mardi4nfdi.de/wiki/MathModDB) ontology developed within Task Area 4 of MaRDI. Existing model documentations are retrieved from the MathModDB Knowledge Graph. Export into the MathModDB KG is possible upon authentification. If credentials are missing, it is possible to export the documented model into a standardized model documentation template and share it with the MaRDI TA4 Team for integration.    
  
## MaRDMO Plugin Installation

To use the MaRDMO Plugin at least `RDMO v2.3.0` is required. Follow the installation / update instructions of [RDMO](https://rdmo.readthedocs.io/en/latest/installation) if required. 

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
    ('RelatedResearchFieldWithCreation', _('Options for related Research Fields with Creation'), 'MaRDMO.model.providers.RelatedResearchFieldWithCreation'),
    ('RelatedResearchFieldWithoutCreation', _('Options for related Research Fields without Creation'), 'MaRDMO.model.providers.RelatedResearchFieldWithoutCreation'),
    ('ResearchProblem', _('Options for Research Problems'), 'MaRDMO.model.providers.ResearchProblem'),
    ('RelatedResearchProblemWithCreation', _('Options for related Research Problems with Creation'), 'MaRDMO.model.providers.RelatedResearchProblemWithCreation'),
    ('RelatedResearchProblemWithoutCreation', _('Options for related Research Problems without Creation'), 'MaRDMO.model.providers.RelatedResearchProblemWithoutCreation'),
    ('MathematicalModel', _('Options for Mathematical Model'), 'MaRDMO.model.providers.MathematicalModel'),
    ('RelatedMathematicalModelWithoutCreation', _('Options for related Mathematical Model without Creation'), 'MaRDMO.model.providers.RelatedMathematicalModelWithoutCreation'),
    ('QuantityOrQuantityKind', _('Options for Quantities and Quantity Kinds'), 'MaRDMO.model.providers.QuantityOrQuantityKind'),
    ('RelatedQuantityWithoutCreation', _('Options for related Quantities without Creation'), 'MaRDMO.model.providers.RelatedQuantityWithoutCreation'),
    ('RelatedQuantityKindWithoutCreation', _('Options for related Quantity Kinds without Creation'), 'MaRDMO.model.providers.RelatedQuantityKindWithoutCreation'),
    ('RelatedQuantityOrQuantityKindWithCreation', _('Options for related Quantites or Quantity Kinds with Creation'), 'MaRDMO.model.providers.RelatedQuantityOrQuantityKindWithCreation'),
    ('MathematicalFormulation', _('Options for Mathematical Formulation'), 'MaRDMO.model.providers.MathematicalFormulation'),
    ('RelatedMathematicalFormulationWithCreation', _('Options for related Mathematical Formulations with Creation'), 'MaRDMO.model.providers.RelatedMathematicalFormulationWithCreation'),
    ('RelatedMathematicalFormulationWithoutCreation', _('Options for related Mathematical Formulations without Creation'), 'MaRDMO.model.providers.RelatedMathematicalFormulationWithoutCreation'),
    ('AllEntities', _('Options for All Entities'), 'MaRDMO.model.providers.AllEntities'),
    ('Task', _('Options for Task'), 'MaRDMO.model.providers.Task'),
    ('RelatedTaskWithCreation', _('Options for related Tasks with Creation'), 'MaRDMO.model.providers.RelatedTaskWithCreation'),
    ('RelatedTaskWithoutCreation', _('Options for related Tasks without Creation'), 'MaRDMO.model.providers.RelatedTaskWithoutCreation'),
    ('RelatedModelEntityWithoutCreation', _('Options for related Model Entities without Creation'), 'MaRDMO.model.providers.RelatedModelEntityWithoutCreation'),
    # Publication
    ('Publication', _('Options for Publication'), 'MaRDMO.publication.providers.Publication'),
    # Algorithm
    ('Algorithm', _('Options for Algorithms'), 'MaRDMO.algorithm.providers.Algorithm'),
    ('RelatedAlgorithmWithoutCreation', _('Options for related Algorithms without Creation'), 'MaRDMO.algorithm.providers.RelatedAlgorithmWithoutCreation'),
    ('AlgorithmicProblem', _('Options for Algorithmic Problems'), 'MaRDMO.algorithm.providers.AlgorithmicProblem'),
    ('RelatedAlgorithmicProblemWithCreation', _('Options for related Algorithmic Problems with Creation'), 'MaRDMO.algorithm.providers.RelatedAlgorithmicProblemWithCreation'),
    ('RelatedAlgorithmicProblemWithoutCreation', _('Options for related Algorithmic Problems without Creation'), 'MaRDMO.algorithm.providers.RelatedAlgorithmicProblemWithoutCreation'),
    ('SoftwareAL', _('Options for Software (Algorithm)'), 'MaRDMO.algorithm.providers.Software'),
    ('RelatedSoftwareALWithCreation', _('Options for related Software (Algorithm) with Creation'), 'MaRDMO.algorithm.providers.RelatedSoftwareWithCreation'),
    ('Benchmark', _('Options for Benchmarks'), 'MaRDMO.algorithm.providers.Benchmark'),
    ('RelatedBenchmarkWithCreation', _('Options for related Benchmarks with Creation'), 'MaRDMO.algorithm.providers.RelatedBenchmarkWithCreation')
    ]

```

Thereby, the MaRDMO Plugin is installed and a "MaRDI Button" button is added in the project view.

## MaRDI Portal, MathAlgoDB, and MathModDB Connection

Add the following lines to `config/settings/local.py` to connect MaRDMO with the individual databases.

```python
MARDMO_PROVIDER = {
    'oauth2_client_id': '',
    'oauth2_client_secret': '',
    'mathalgodb_id': '',
    'mathalgodb_secret': ''
    }
``` 
Contact the MaRDI consortium for the individual credentials.

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

Once the MaRDMO Plugin is set up, the Questionnaires can be used to document and query interdisciplinary workflows, mathematical models, and algorithms. Therefore, select "Create New Project" in RDMO, choose a proper project name (for interdisciplinary workflow the project name will the workflow name), assign one of the the MaRDMO Catalogs and select "Create Project". The project is created. On the right hand side in the "Export" category the "MaRDMO Button" button is located to process the completed Questionnaires. Choose "Answer Questions" to start the interview.     

