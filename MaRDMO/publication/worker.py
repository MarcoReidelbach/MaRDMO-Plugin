from .constants import PUBLICATIONS, JOURNALS, AUTHORS, LANGUAGES
from .utils import generate_label, get_citation
from .sparql import queryPublication
from .models import Publication

from ..config import BASE_URI, endpoint
from ..getters import get_items, get_questions_publication, get_properties
from ..queries import query_sparql
from ..helpers import value_editor

class PublicationRetriever:

    def WorkflowOrModel(project, answers, options):
        '''Function retrieving Publication Information for workflow and model documentation'''

        # Get Questions of Workflow Catalog
        questions = get_questions_publication()

        for key in answers['publication']:

            if str(project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':
                # Ignore references for individual triple in workflow catalog
                if answers['publication'][key]['workflow'] != options['Yes']:
                    continue

            #If User selected Publication from Wikidata...
            if answers['publication'][key]['ID'].startswith('wikidata'):
                #...use the DOI... 
                doi = answers['publication'][key].get('reference', {}).get(0, ['',''])[1]
                #...to query MaRDI Portal.
                query = queryPublication['MaRDI']['DOI'].format(doi, **get_properties())
                results = query_sparql(query, endpoint['mardi']['sparql'])
                if results:
                    #If Publication found in MaRDI Portal...
                    data = Publication.from_query(results)
                    #...add data to Questionnaire and...
                    value_editor(project = project, 
                                 uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                 text = f"{data.label} ({data.description}) [mardi]" , 
                                 external_id = data.id, 
                                 set_index = key)
                    #...ouput dictionary.
                    answers['publication'][key]['ID'] = data.id
                    answers['publication'][key]['Name'] = data.label
                    answers['publication'][key]['Description'] = data.description
    
            #If User selected a Publication from MathAlgoDB or did not find it...
            elif answers['publication'][key]['ID'].startswith('mathalgodb') or answers['publication'][key]['ID'].startswith('not found'):
                #...and exported for the first time...
                if answers['publication'][key].get('Name'):
                    return answers
                #...but provided a DOI.
                if answers['publication'][key].get('reference', {}).get(0, ['',''])[1]:
                    #Get the Citation of several ressource.
                    data = get_citation(answers['publication'][key]['reference'][0][1])
                    #If Publication available at MaRDI Portal or Wikidata...
                    if data.get('mardi') or data.get('wikidata'):
                        DATA = data['mardi'] or data['wikidata']
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                     text = f"{DATA.label} ({DATA.description}) [{DATA.id.split(':')[0]}]" , 
                                     external_id = DATA.id, 
                                     set_index = key)
                        #...ouput dictionary.
                        answers['publication'][key]['ID'] = DATA.id
                        answers['publication'][key]['Name'] = DATA.label
                        answers['publication'][key]['Description'] = DATA.description
                    #If Publication available at Crossref, Datacite, zbMath or DOI...
                    elif data.get('crossref') or data.get('datacite') or data.get('zbmath') or data.get('doi'):
                        DATA = data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']
                        #...add data to Questionnaire and...
                        for uri, data_key in PUBLICATIONS.items():
                            value_editor(project = project, 
                                         uri = f'{BASE_URI}{questions[uri]["uri"]}', 
                                         text = getattr(DATA, data_key), 
                                         set_index = key)
                            
                        for idx, language in enumerate(DATA.language):
                            for uri, data_key in LANGUAGES.items():
                                value_editor(project = project, 
                                             uri = f'{BASE_URI}{questions[uri]["uri"]}', 
                                             text = getattr(language, data_key), 
                                             collection_index = idx, 
                                             set_index = key)

                        for idx, journal in enumerate(DATA.journal):
                            for uri, data_key in JOURNALS.items():
                                value_editor(project = project, 
                                             uri = f'{BASE_URI}{questions[uri]["uri"]}', 
                                             text = getattr(journal, data_key), 
                                             collection_index = idx, 
                                             set_index = key)

                        for idx, author in enumerate(DATA.authors):
                            for uri, data_key in AUTHORS.items():
                                value_editor(project = project, 
                                             uri = f'{BASE_URI}{questions[uri]["uri"]}', 
                                             text = getattr(author, data_key), 
                                             collection_index = idx, 
                                             set_index = key)

                        #...output dictionary.
                        answers['publication'][key]['Name'] = DATA.title
                        answers['publication'][key]['Description'] = DATA.description

        return answers

    def Algorithm(project, answers):
        '''Function retrieving Publication Information for algorithm documentation'''

        # Get Questions of Workflow Catalog
        questions = get_questions_publication()

        # Go through all Publications
        for key in answers['publication']:
            # If User selected Publication from MaRDI Portal or Wikidata...
            if answers['publication'][key]['ID'].startswith('mardi') or answers['publication'][key]['ID'].startswith('wikidata'):
                #...check if ressource returned a DOI and...
                if answers['publication'][key].get('reference', {}).get(0, ['',''])[1]:
                    #... use the DOI to query MathAlgoDB. 
                    query = queryPublication['PublicationMathAlgoDBDOI'].format(answers['publication'][key]['reference'][0][1])
                    results = query_sparql(query, endpoint['mathalgodb']['sparql'])
                    if results:
                        # If Publication found on MathAlgoDB...
                        data = Publication.from_query(results)
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                     text = f"{data.label} ({data.description}) [mathalgodb]" , 
                                     external_id = data.id, 
                                     set_index = key)
                        #...ouput dictionary.
                        answers['publication'][key]['ID'] = data.id
                        answers['publication'][key]['Name'] = data.label
                        answers['publication'][key]['Description'] = data.description
                
            #If User did not find its publication...
            elif answers['publication'][key]['ID'].startswith('not found'):
                #...but provided a DOI.
                if answers['publication'][key]['reference'].get(0, ['',''])[1]:
                    #Get the Citation of several ressource.
                    data = get_citation(answers['publication'][key]['reference'][0][1])
                    #If Publication available at MathAlgoDB...
                    if data['mathalgodb']:
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                     text = f"{data['mathalgodb'].label} ({data['mathalgodb'].description}) [mathalgodb]" , 
                                     external_id = data['mathalgodb'].id, 
                                     set_index = key)
                        #...ouput dictionary or...
                        answers['publication'][key]['ID'] = data['mathalgodb'].id
                        answers['publication'][key]['Name'] = data['mathalgodb'].label
                        answers['publication'][key]['Description'] = data['mathalgodb'].description
                    #if Publication available at MaRDI Portal, Wikidata, Crossref, DataCite, ZBMath or DOI...
                    elif data['mardi'] or data['wikidata'] or data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']:
                        DATA = data['mardi'] or data['wikidata'] or data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication Name"]["uri"]}', 
                                     text = generate_label(DATA), 
                                     set_index = key)
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication Description"]["uri"]}', 
                                     text = DATA.description, 
                                     set_index = key)
                        #...output dictionary.
                        answers['publication'][key]['Name'] = generate_label(DATA)
                        answers['publication'][key]['Description'] = DATA.description

        return answers
                    

