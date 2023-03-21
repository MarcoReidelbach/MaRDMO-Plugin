# MaRDMO

This repository contains a questionnaire and an Export/Query Plugin for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) developed within Task Area 4 "Interdisciplinary Mathematics" of the [Mathematical Research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). 

The questionnaire allows a standardized documentation of interdisciplinary workflows related to mathematics, where the connection to "real" experiments or theoretical approaches, like simulations, is possible and desired.

The Export/Query Plugin allows the user to export documented workflows into a standardized template, which could be stored locally as Markdown File (depreciated) or shared with others as Wiki Page on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal). Furthermore, integral aspects of the workflows are integrated into the MaRDI Knowledge Graph thus enabling specific workflow queries. 

The functionality of the Export/Query Plugin is captured in the questionnaire, such that a single button controls everything. 

So far, there is no connection to the *real* MaRDI Portal / Knowledge Graph. To test MaRDMO a local [instance of the MaRDI Portal](https://github.com/MaRDI4NFDI/portal-compose) or any other [wikibase](https://www.mediawiki.org/wiki/Wikibase/Installation) needs to be installed/uesd. 

## Repository structure

```bash
. 
├── catalog - Files necessary for RDMO Questionnaire 
│   ├── conditions.xml - individual conditions of RDMO Questionnaire 
│   ├── domains.xml - individual domains of RDMO Questionnaire 
│   ├── options.xml - individual options of RDMO Questionnaire 
│   └── questions.xml - individual questions for RDMO Questionnaire 
│ 
├── environment.yml - File to set up MaRDMO conda environment 
│ 
├── func - Files necessary for Export/Query Plugin 
│   ├─ citation.py - get citation from DOI and ORCID API 
│   ├── config_empty.py - wikibase information 
│   ├── export.py - Export/Query Function 
│   ├── id.py - wikibase item and property ids 
│   └── para.py - Export/Query parameters
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

Thereby, a virtual environment "MaRDMO" is created in which the RDMO package and further packages, e.g. `PyPandoc`, `WikibaseIntegrator`, and `SPARQLWrapper`, for the Export/Query Plugin are installed.  

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

Now, run your application and log in via your browser:

```bash
python manage.py runserver
```

To actually use RDMO, a questionnaire (or more than one) needs to be added. To do this, click on "Management", choose "Domain" and import `domains.xml` from `MaRDMO/catalog`. Do the same for `options.xml`, `conditions.xml` and `questions.xml` by choosing "Options", "Conditions" and "Questions", respectively. Ensure, that `questions.xml` is added last.

### Wikibase Installation, Setup, and MaRDMO Coupling

You may test MaRDMO with a local wikibase, e.g. a [local MaRDI Portal instance](https://github.com/MaRDI4NFDI/portal-compose) or any other [wikibase](https://www.mediawiki.org/wiki/Wikibase/Installation). Follow the individual installation guides. If you do not use the local MaRDI Portal instance make sure that all MaRDI requirements, e.g. [Math Extension](https://www.mediawiki.org/wiki/Extension:Math/de) are met.

Once the local wikibase instance is set up, define a bot for creating and editing. Store the bot name (`lgname`) and bot password (`lgpassword`) in `MaRDMO/func/config_empty.py`. If you do not use the local MaRDI Portal instance adjust the URIs of the Wiki (`mardi_wiki`), the API (` mardi_api`), and the SPARQL endpoint (`mardi_endpoint`). Rename `config_empty.py` to `config.py`.

To add workflows to the wikibase several Items and Properties need to be present in your wikibase instance. A complete list can be found in `MaRDMO/func/id.py`. Add the required Items and Properties to your wikibase and adjust `id.py` if your QIDs and PIDs differ. (Will be automated soon...)   


## Usage of RDMO and Export/Query Plugin

Once you completed the installation, the MaRDMO Questionnaire can be used to document (loacal or wikibase) and query workflows. Therefore, select "Create New Project" in RDMO and choose a proper name for your project (this name will be used as wokflow name and label in the wikibase), assign the "MaRDI Workflow Documentation" catalog and click on "Create Project". Your project is now created. On the right hand side in the "Export" category you may notice the "MaRDI Export/Query" button.      

Choose "Answer Questions" to start the interview. With the first question the Operation Modus of the Export/Query Plugin is determined:

1) If you choose **"Workflow Documentation"** and click on "Save and proceed", you have to decide in a next step if you want to do the documentation locally (as Markdown File) or if you want to publish the documentation as Wiki Page. If you choose Wiki Page publication, you can get an HTML preview before the actual export. Please, use the HTML preview to check if your documentation is rendered correctly (e.g. Latex Math Equations). Once again click "Save and proceed". Now, you will be guided through a series of questions (the individual questions are listed below) in order to document your workflow. For some of these questions you have to add sets, e.g. each variable of your workflow gets his own question set. Make sure to use integer numbers starting from 0 for the individual question set names. Once you have answered all questions return to the project page and choose "MaRDI Export/Query" to add your workflow documentation to the knowledge graph or download it. 

2) If you choose **"Workflow Finding"** and click on "Save and proceed", you will be directed to a page where you have to choose by which component you would like to search existing workflow documentations and describe your needs. Once described, click on "Save", return to the project page and choose "MaRDI Export/Query". If MaRDMO detects workflows in the wikibase which could be interesting for you, you will receive the URIs of the corresponding Wiki pages.

## Questionnaire

**Operation Modus**

0.0 Do you want to document or find a workflow?

**Workflow Finding**

1.0 Please choose to search existing workflow documentation by research objective, used mathematical model, methods and software, field of research, or input data. <br>
1.1 Please state what to search. 

**Workflow Documentation**

**Documentation**

2.0 Do you want to save your workflow documentation locally or export it to the MaRDI portal? <br>
2.1 Get an HTML preview before exporting to the MaRDI portal to correct errors?

**General**

**Publication and Problem Statement**

3.0.0 Name the Problem of the underlying Workflow. <br>
3.0.1 Is your workflow experimental or theoretical? <br>
3.0.2 Has the workflow been published?

**Research Objective and Procedure**

3.1.0 Name the research object of the underlying workflow. <br>
3.1.1 Describe the procedure of your workflow.

**Involved Disciplines and Data Streams**

3.2.0 Which disciplines can your workflow be assigned to? <br>
3.2.1 Data streams between the disciplines 

**Model, Variables and Parameter**

**Model**

4.0.0 Is the mathematical model already deposited in MaRDI Knowledge Graph or wikidata? <br>
4.0.1 Provide the name of the mathematical model. <br>
4.0.2 Provide a short description of the mathematical model. <br>
4.0.3 Please state the main subject of the mathematical model. <br>
4.0.4 State the defining mathematical formulas of the method.

**Discretization**

4.1.0 Is time discretized? <br>
4.1.1 Is space discretized?

**Involved Variables**

4.2.0 Name of the Variable <br>
4.2.1 Unit of the Variable <br>
4.2.2 Symbol of the Variable <br>
4.2.3 Is the variable dependent or independent? (*Experimental Workflow only*)

**Involved Parameters** (*Experimental Workflow only*)

4.3.0 Name of the Paramter <br>
4.3.1 Unit of the Parameter <br>
4.3.2 Symbol of the Parameter

**Process Information**

**Describe the individual process steps of your workflow**

5.0.0 Name of the Process Step <br>
5.0.1 Description of the Process Step <br> 
5.0.2 Input of the Process Step <br>
5.0.3 Output of the Process Step <br>
5.0.4 Method of the Process Step <br>
5.0.5 Parameter of the Process Step <br>
5.0.6 Environment of the Process Step <br>
5.0.7 Mathematical Area of the Process Step 

**Describe the methods applied in your Workflow**

5.1.0 Provide an ID for the Method. <br>
5.1.1 Name of the Method <br>
5.1.2 Provide a short description of the method. <br>
5.1.3 State the main subject of the method. <br>
5.1.4 State the defining mathematical formulas of the method. <br>
5.1.5 Process Step in which Method is used. <br> 
5.1.6 Parameter of the Method <br>
5.1.7 Method realized or implemented by

**Describe the Software used in your Workflow**

5.2.0 Provide a Software ID <br>
5.2.1 Name of the Software <br>
5.2.2 Description of the Software <br>
5.2.3 Version of the Software <br>
5.2.4 Programming Language of the Software <br>
5.2.5 Dependencies of the Software <br>
5.2.6 Is the sofware versioned? <br>
5.2.7 Is the sofware published? <br>
5.2.8 Is the software documented? 

**Describe the hardware used in the Workflow** (*Mathematical Workflow only*)

5.3.0 ID of the Hardware <br>
5.3.1 Name of the Hardware <br>
5.3.2 Name of the Processor <br>
5.3.3 Existing Compiler <br>
5.3.4 Number of Nodes <br>
5.3.5 Number of Cores <br>

**Describe the experimental Devices, Instruments and Computer Hardware used in your Workflow** (*Experimental Workflow only*)

5.4.0 ID of the experimental device or hardware <br>
5.4.1 Name of the experimental device or hardware <br>
5.4.2 Description of the experimental device or the hardware <br>
5.4.3 Version of the experimental device or the hardware <br>
5.4.4 Part Number of the experimental device or the hardware <br>
5.4.5 Serial Number of the experimental device or hardware <br>
5.4.6 Location of the experimental device or hardware <br>
5.4.7 Software of the experimental device or hardware 

**Input Data**

5.5.0 Provide an ID for your input data.
5.5.1 Provide a name for your input data. <br>
5.5.2 Provide the size of your input data. <br>
5.5.3 Provide the data structure of your input data. <br>
5.5.4 Provide the representation format of your input data. <br> 
5.5.5 Provide the exchange format of your input data. <br>
5.5.6 Is your input data binary or text? <br>
5.5.7 Is the input data prorietary? <br>
5.5.8 Is it necessary to publish the input data? <br> 
5.5.9 Is it necessary to archive the input data? 

**Output Data** 

5.6.0 Provide an ID for your output data. <br>
5.6.1 Provide a name for your output data. <br>
5.6.2 Provide the size of your output data. <br>
5.6.3 Provide the data structure of your output data. <br> 
5.6.4 Provide the representation format of your output data. <br> 
5.6.5 Provide the exchange format of your output data. <br>
5.6.6 Is your output data binary or text? <br>
5.6.7 Is the output data prorietary? <br>
5.6.8 Is it necessary to publish the output data? <br> 
5.6.9 Is it necessary to archive the output data? 

**Reproducibility**

**Mathematical reproducibility and transferability?** (*Mathematical Workflow only*)

6.0.0 Mathematical Reproducibility? <br>
6.0.1 Runtime reproducibility? <br>
6.0.2 Reproducibility of Results? <br>
6.0.3 Reproducibilty on original hardware? <br>
6.0.4 Reproducibility on other hardware? <br>
6.0.5 Transferability to 

**Reproducibility and Transferability of the Experiments** (*Experimental Workflow only*)

6.1.0 Are the experiments reproducible on the original devices/instruments/hardware? <br>
6.1.1 Are the experiments reproducible on other devices/instruments/hardware? <br>
6.1.1 Transferability of the experiments to 

