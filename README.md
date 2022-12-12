# MaRDI_RDMO

This repository contains a questionnaire and an Export/Query Plugin for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) developed within Task Area 4 "Interdisciplinary Mathematics" of the [Mathematical research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). 

The questionnaire allows a standardized documentation of interdisciplinary workflows related to mathematics, where the connection to "real" experiments or theoretical approaches, like simulations, is possible and desired.

The Export/Query Plugin allows the user to export documented workflows into a standardized Markdown template. It also offers the possibility to publish the documented workflow directly on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal)* and to integrate it into the MaRDI knowledge graph. The query functionality in turn allows the user to search the stored workflows based on individual components. 

The functionality of the Export/Query Plugin is captured in the questionnaire, such that a single button controls everything. 

*For the time being, there is no connection to the MaRDI knowledge graph and portal, hence a local knowledge graph is used for testing. The three searchable components are Research Objective, Methods and Input Data.

## Repository structure

 -catalog - all files necessary for RDMO questionnaire <br>
  --questions.xml - question-/help-text, relation to domain, options, condition <br>
  --domains.xml - individual domains <br>
  --options.xml - individual options <br>
  --conditions.xml - individual conditions
  
 -func - all files necessary for the Export/Query Plugin <br>
  --export.py - contains Export/Query function (based on RDMO's csv export) <br>
  --para.py - contains question IDs for proper export and query
  
 -kg - all files necessary for the local knowledge graph <br>
  --MaRDI_RDMO.owl - owl based knowledge graph for local workflow exports and queries

 -templates - all files for rendering  
  -- export.html - successfull export to local knowledge graph <br>
  -- error1/2/3/4.html - error message for different reasons

 -environment.yml - set up virtual conda environment 
 
  
## Installation and Export/Query Plugin Setup

To install RDMO check if you meet their [prerequisites](https://rdmo.readthedocs.io/en/latest/installation/prerequisites.html). If so, obtain the app directory by cloning the corresponding repository:

`git clone https://github.com/rdmorganiser/rdmo-app`

Likewise clone the MaRDI_RDMO directory:

`cd rdmo-app`

`git clone git@github.com:MarcoReidelbach/MaRDI_RDMO` (adjust once repo public)

Once cloned, setup a virtual conda environment:

`conda env create -f MaRDI_RDMO/environment.yml`

Thereby, a virtual environment "MaRDI_RDMO" is created in which the RDMO package and further packages, namely `Numpy`, `scikit-learn`, `owlready` and `nltk` (packages might change with the connection to the MaRDI knowledge graph), for the Export/Query Plugin are installed.  

Setup the RDMO application:

`conda activate MaRDI_RDMO`

`cp config/settings/sample.local.py config/settings/local.py`

`python manage.py migrate`                
`python manage.py setup_groups`           
`python manage.py createsuperuser`

Your RDMO instance is now ready. To install the Export/Query Plugin add the following lines to `local.py` and set **Debug = True**:

```python
from django.utils.translation import ugettext_lazy as _  
from . import BASE_DIR, INSTALLED_APPS, PROJECT_EXPORTS
```

```python
INSTALLED_APPS = ['MaRDI_RDMO'] + INSTALLED_APPS

PROJECT_EXPORTS += [
        ('mde', _('MaRDI Export/Query'), 'MaRDI_RDMO.func.export.MaRDIExport'),
        ]
```

Thereby, the Export/Query Plugin is installed and a "MaRDI Export/Query" Button is added.

Now, run your application and log in via your browser:

`python manage.py runserver`

To actually use RDMO, a questionnaire (or more than one) needs to be added. To do this, click on "Management", choose "Domain" and import `domains.xml` from `MaRDI_RDMO/catalog`. Do the same for `options.xml`, `conditions.xml` and `questions.xml` by choosing "Options", "Conditions" and "Questions", respectively. Ensure, that `questions.xml` is added last.

Your RDMO instance is now ready to be used with the "MaRDI Workflow Documentation" questionnaire and the Export/Query Plugin.

## Usage of RDMO and Export/Query Plugin

Choose "Create New Project". Choose a proper name for your project (this name will be later on used to identify your documented workflow), assign the "MaRDI Workflow Documentation" catalog and click on "Create Project". Your project is now created. On the right hand side in the "Export" category you may notice the "MaRDI Export/Query" button.      

Choose "Answer Questions" to start the interview. With the first question the Operation Modus of the Export/Query Plugin is determined:

1) If you choose **"Workflow Documentation"** and click on "Save and proceed", you will be guided through a series of questions (the individual questions are listed below) in order to document your workflow. For some of these questions you have to add sets, e.g. each variable of your workflow gets his own question set. Make sure to use integer numbers starting from 0 for the individual question set names. With the final question you decide if your workflow documentation is added to the MaRDI portal (choose "MaRDI Portal") or downloaded (choose "Markdown File"). Once you have answered all questions return to the project page and choose "MaRDI Export/Query" to add your workflow documentation to the knowledge graph or download it. 

**Note:** Not all questions have to be answered, hence if you cannot answer a specific question you can leave the field free. Beside the question about the operation modus, the questions about the workflow and export type are necessary. If one of those is not answered, the export will stop.

2) If you choose **"Workflow Finding"** and click on "Save and proceed", you will be directed to a page where you have to choose by which component you would like to search existing workflow documentations and describe your needs, e.g. if you would like to know how to determine intermediate states and reaction kinetics from time-resolved raman spectroscopy choose "Research Objective" and write something like "Intermediate States Kinetics Time-resolved Raman Spectroscopy". Click on "Save", return to the project page and choose "MaRDI Export/Query" and you will (hopefully) get a workflow suggestion that is interesting to you.

**Note:** If you do not choose a component to search for, the query will stop.      

## Questionnaire

Operation Modus:

0.0 Do you want to document or find a workflow?

Workflow Finding:

1.0 Please choose to search existing workflow documentation by research objective, methods used, or input data. <br>
1.1 Please state the research objective, methods or input data to be searched for. 

Workflow Documentation:

General

2.0 Name the Problem of the underlying Workflow. <br>
2.1 Has the workflow been published? <br>
2.2 Is your workflow experimental or theoretical? <br>
2.3 Name the research object of the underlying workflow. <br>
2.4 Describe the procedure of your workflow. <br>
2.5 Which disciplines can your workflow be assigned to? <br>
2.6 Data streams between the disciplines 

Model

3.0 Describe the model on which the workflow is based, in particular the theoretical foundations. <br>
3.1 Is time discretized? <br>
3.2 Is space discretized?

Variables

3.3.0 Name of the Variable <br>
3.3.1 Unit of the Variable <br>
3.3.2 Symbol of the Variable <br>
3.3.3 Is the variable dependent or independent? (*Experimental Workflow only*)

Parameters: (*Experimental Workflow only*)

3.4.0 Name of the Paramter <br>
3.4.1 Unit of the Parameter <br>
3.4.2 Symbol of the Parameter

Process Steps

4.0.0 Name of the Process Step <br>
4.0.1 Description of the Process Step <br> 
4.0.2 Input of the Process Step <br>
4.0.3 Output of the Process Step <br>
4.0.4 Method of the Process Step <br>
4.0.5 Parameter of the Process Step <br>
4.0.6 Environment of the Process Step <br>
4.0.7 Mathematical Area of the Process Step 

Methods:

4.1.0 Provide an ID for the Method. <br>
4.1.1 Name of the Method <br>
4.1.2 Process Step in which Method is used. <br> 
4.1.3 Parameter of the Method <br>
4.1.4 Method realized or implemented by

Software:

4.2.0 Provide a Software ID <br>
4.2.1 Name of the Software <br>
4.2.2 Description of the Software <br>
4.2.3 Version of the Software <br>
4.2.4 Programming Language of the Software <br>
4.2.5 Dependencies of the Software <br>
4.2.6 Is the sofware versioned? <br>
4.2.7 Is the sofware published? <br>
4.2.8 Is the software documented? 

Hardware: (*Mathematical Workflow only*)

4.3.0 ID of the Hardware <br>
4.3.1 Name of the hardware <br>
4.3.2 Name of the Processor <br>
4.3.3 Existing Compiler <br>
4.3.4 Number of Nodes <br>
4.3.5 Number of Cores <br>

Experimental Devices, Instruments and Computer Hardware: (*Experimental Workflow only*)

4.4.0 ID of the experimental device or hardware <br>
4.4.1 Name of the experimental device or hardware <br>
4.4.2 Description of the experimental device or the hardware <br>
4.4.3 Version of the experimental device or the hardware <br>
4.4.4 Part Number of the experimental device or the hardware <br>
4.4.5 Serial Number of the experimental device or hardware <br>
4.4.6 Location of the experimental device or hardware <br>
4.4.7 Software of the experimental device or hardware 

Input Data:

4.5.0 Provide an ID for your input data.
4.5.1 Provide a name for your input data. <br>
4.5.2 Provide the size of your input data. <br>
4.5.3 Provide the data structure of your input data. <br>
4.5.4 Provide the representation format of your input data. <br> 
4.5.5 Provide the exchange format of your input data. <br>
4.5.6 Is your input data binary or text? <br>
4.5.7 Is the input data prorietary? <br>
4.5.8 Is it necessary to publish the input data? <br> 
4.5.9 Is it necessary to archive the input data? 

Output Data: 

4.6.0 Provide an ID for your output data. <br>
4.6.1 Provide a name for your output data. <br>
4.6.2 Provide the size of your output data. <br>
4.6.3 Provide the data structure of your output data. <br> 
4.6.4 Provide the representation format of your output data. <br> 
4.6.5 Provide the exchange format of your output data. <br>
4.6.6 Is your output data binary or text? <br>
4.6.7 Is the output data prorietary? <br>
4.6.8 Is it necessary to publish the output data? <br> 
4.6.9 Is it necessary to archive the output data? 

Mathematical Reproducibility and Transferability: (*Mathematical Workflow only*)

5.1 Mathematical Reproducibility? <br>
5.2 Runtime reproducibility? <br>
5.3 Reproducibility of Results? <br>
5.4 Reproducibilty on original hardware? <br>
5.5 Reproducibility on other hardware? <br>
5.6 Transferability to 

Reproducibility and Transferability of the Experiments: (*Experimental Workflow only*)

6.1 Are the experiments reproducible on the original devices/instruments/hardware? <br>
6.2 Are the experiments reproducible on other devices/instruments/hardware? <br>
6.3 Transferability of the experiments to 

Export Type:

7.0 How should the workflow documentation be published? 



