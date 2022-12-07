# MaRDI_RDMO

This repository contains a questionnaire and an Export/Query app for the [Research Datamanagement Organizer](https://rdmorganiser.github.io/) developed within Task Area 4 "Interdisciplinary Mathematics" of the [Mathematical research Data Initiative](https://www.mardi4nfdi.de/about/mission) (MaRDI). 

The questionnaire allows a standardized documentation of interdisciplinary workflows related to mathematics, where the connection to "real" experiments as well as to computational simulations is possible and also desired.

The Export/Query App allows the user to export his documented workflow into a standardized Markdown template. It also offers the possibility to publish the documented workflow directly on the [MaRDI Portal](https://portal.mardi4nfdi.de/wiki/Portal)* and to integrate it into the knowledge graph there. The Query App in turn allows the user to search the workflows stored in the portal based on individual components. 

The functionality of the Export/Query App as well as the export method are captured in the question catalog, so that a single button controls everything. 

*For the time being, there is no connection to the MaRDI Knowledge Graph, so a local Knowledge Graph will be used for testing.

## Repository structure

  catalog &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; all files necessary for RDMO questionnaire <br>
  --questions.xml &emsp;&emsp; question-/help-text, relation to domain, options, condition <br>
  --domains.xml &emsp;&emsp; individual domains <br>
  --options.xml &emsp;&emsp; individual options <br>
  --conditions.xml &emsp;&emsp; individual conditions
  
  func &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; all files necessary for the Export/Query app <br>
  --export.py &emsp;&emsp; contains Export/Query function (based on RDMO's csv export) <br>
  --para.py &emsp;&emsp; contains question IDs for proper export and query
  
  kg &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; all files necessary for the local knowledge graph
  --MaRDI_RDMO.owl &emsp;&emsp; owl based knowledge graph for local workflow exports and queries
  
  requirements.txt &emsp;&emsp; all package requirements to set up a proper conda environment

