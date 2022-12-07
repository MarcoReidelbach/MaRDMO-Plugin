# MaRDI_RDMO

This repository contains a questionnaire and an Export/Query app for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) developed within Task Area 4 "Interdisciplinary Mathematics" of the [Mathematical research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). 

The questionnaire allows a standardized documentation of interdisciplinary workflows related to mathematics, where the connection to "real" experiments as well as to computational simulations is possible and also desired.

The Export/Query App allows the user to export his documented workflow into a standardized Markdown template. It also offers the possibility to publish the documented workflow directly on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal)* and to integrate it into the knowledge graph there. The Query App in turn allows the user to search the workflows stored in the portal based on individual components. 

The functionality of the Export/Query App as well as the export method are captured in the question catalog, so that a single button controls everything. 

*For the time being, there is no connection to the MaRDI Knowledge Graph, so a local Knowledge Graph will be used for testing.

## Repository structure

  catalog                 all files necessary for RDMO questionnaire 
  
  --questions.xml         question-/help-text, relation to domain, options, condition
  
  --domains.xml           individual domains
  
  --options.xml           individual options
  
  --conditions.xml        individual conditions
  
  func
  
  --export.py             contains Export/Query function (based on RDMO's csv export) 
  
  --para.py               contains question IDs for proper export and query
  
  kg
  
  --MaRDI_RDMO.owl        owl based knowledge graph for local workflow exports and queries
  
  requirements.txt        all package requirements to set up a proper conda environment

