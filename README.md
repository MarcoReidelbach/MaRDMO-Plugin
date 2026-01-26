<div align='center' style="margin-top: 50px; font-size: 14px; color: grey;">
  <img src="https://github.com/user-attachments/assets/98c92c58-9d31-41ca-a3ca-189bbfb92101" />
  <p>MaRDMO Logo by <a href="https://www.mardi4nfdi.de/about/mission" target="_blank" style="color: grey;">MaRDI</a>, licensed under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank" style="color: grey;">CC BY-NC-ND 4.0</a>.</p>
</div>


# MaRDMO Plugin

This repository contains the MaRDMO Plugin for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) (RDMO) developed within the [Mathematical Research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). 

The plugin allows a standardized documentation of:

<ol>
  <li>Mathematical Models</li>
  <li>Interdisciplinary Workflows</li>
  <li>Algorithms</li>
</ol>

Model documentation in MaRDMO is based on the [MathModDB ontology](https://portal.mardi4nfdi.de/wiki/MathModDB). Within the plugin, users can record a model, related expressions, computational tasks, quantities or quantity kinds, research problems, academic disciplines, and publications. These inputs are gathered in a guided interview, enabling MaRDMO to produce metadata that is directly compatible with the MaRDI knowledge graph for mathematical models. A demo video showing the documentation process for a mathematical model in MaRDMO is available [here](https://www.youtube.com/watch?v=UmbBNUZJ994&list=PLgoPZ7uPWbo-jqDXzx4fSm_4JyAYEMPjn).

Workflow documentation follows a [standardized scheme](https://portal.mardi4nfdi.de/wiki/MD_UseCases) developed in MaRDI. Within the plugin, users can record a workflow, related models, methods, software, hardware, experimentall devices, data sets, and publications. These inputs are gathered in a guided interview, enabling MaRDMO to produce metadata that is directly compatible with the MaRDI knowledge graph for interdisciplinary workflows.

Algorithm documentation in MaRDMO follows the [MathAlgoDB ontology](https://portal.mardi4nfdi.de/wiki/Service:6534228). Within the plugin, users can record an algorithm, related algorithmic tasks, implementing software, benchmarks, and publications. These inputs are gathered in a guided interview, enabling MaRDMO to produce metadata that is directly compatible with the MaRDI knowledge graph for algorithms.

<div align="center" style="margin-top: 20px; font-size: 14px; color: grey;">
  <img src="https://github.com/user-attachments/assets/fb22ea44-8648-44e8-8a1e-51f31564d23c" width="800" />
  <p><em>Figure 1: MaRDMO Data Model containing Classes and Relations for the Documentation of Mathematical Models (blue), Algorithms (red), and Interdisciplinary Workflows (green).</em></p>
</div>

Completed documentations in MaRDMO can be exported directly from RDMO to the respective MaRDI knowledge graph via the **MaRDMO Button**. This feature generates a concise summary of the documented model, algorithm, or workflow, and—after user authentication—submits the metadata to the corresponding knowledge graphs. This streamlines the publication process and ensures the documentation becomes immediately discoverable within the MaRDI ecosystem. 

In addition to documentation, MaRDMO provides a dedicated interview for searching existing workflows, algorithms, and models. Users can specify individual search parameters, and the MaRDI Button will generate the corresponding SPARQL query based on the input. The query results are displayed directly in RDMO, enabling researchers to discover and reuse existing knowledge—thus closing the knowledge transfer loop within the MaRDI ecosystem.
  
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
        ('wikibase', _('Export to MaRDI Portal'), 'MaRDMO.main.MaRDMOExportProvider'),
        ]

OPTIONSET_PROVIDERS = [
    # Search
    ('MaRDISearch', _('Options for MaRDI Search'), 'MaRDMO.search.providers.MaRDISearch'),
    ('SoftwareSearch', _('Options for Software Search'), 'MaRDMO.search.providers.SoftwareSearch'),
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
    ('Formula', _('Options for Formulas'), 'MaRDMO.model.providers.Formula'),
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

In addition add the following urlpattern to `config/urls.py`:

```python
path('services/', include("MaRDMO.urls")),
```

Thereby, the MaRDMO Plugin is installed and a "MaRDI Button" button is added in the project view.

## MaRDI Portal, MathAlgoDB, and MathModDB Connection

Add the following lines to `config/settings/local.py` to connect MaRDMO with the individual databases.

```python
MARDMO_PROVIDER = {
    'mardi': {
        'items': 'data/items.json',
        'properties': 'data/properties.json',
        'api': 'https://portal.mardi4nfdi.de/w/api.php',
        'sparql': 'https://query.portal.mardi4nfdi.de/sparql',
        'uri': 'https://portal.mardi4nfdi.de',
        'oauth2_client_id': '',
        'oauth2_client_secret': '',
    },
    'mathalgodb': {
        'uri': 'https://cordi2025.m1.mardi.ovh/',
        'sparql': 'https://sparql.cordi2025.m1.mardi.ovh/mathalgodb/query',
        'update': 'https://sparql.cordi2025.m1.mardi.ovh/mathalgodb/update',
        'mathalgodb_id': '',
        'mathalgodb_secret': ''
    },
    'wikidata': {
        'uri': 'https://www.wikidata.org',
        'api': 'https://www.wikidata.org/w/api.php',
        'sparql': 'https://query-main.wikidata.org/sparql',
        'uri': 'https://www.wikidata.org'
    },
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

