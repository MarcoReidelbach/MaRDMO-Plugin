from .constants import PUBLICATIONS, JOURNALS, AUTHORS, LANGUAGES
from .utils import generate_label, get_citation
from .sparql import queryPublication
from .models import Publication

from ..utils import query_sparql, get_questionsPU, value_editor
from ..config import BASE_URI, endpoint

class PublicationRetriever:

    def Workflow(project, answers, options):
        '''Function retrieving Publication Information for model documentation'''

        # Get Questions of Workflow Catalog
        questions = get_questionsPU()

        for key in answers['publication']:

            #If Workflow is published in Publication...
            if answers['publication'][key]['workflow'] == options['Yes']:

                #If User selected Publication from Wikidata...
                if answers['publication'][key]['ID'].startswith('wikidata'):
                    #...use the DOI to query MaRDI Portal. 
                    query = queryPublication['MaRDIDOI'].format(answers['publication'][key]['reference'][0][1])
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
    
                #If User selected a Publication from MathAlgoDB, MathModDB or did not find it...
                elif answers['publication'][key]['ID'].startswith('mathalgodb') or answers['publication'][key]['ID'].startswith('mathmoddb') or answers['publication'][key]['ID'].startswith('not found'):
                    #...and exported for the first time...
                    if answers['publication'][key].get('Name'):
                        return answers
                    #...but provided a DOI.
                    if answers['publication'][key].get('reference', {}).get(0, ['',''])[1]:
                        #Get the Citation of several ressource.
                        data = get_citation(answers['publication'][key]['reference'][0][1])
                        #If Publication available at MaRDI Portal or Wikidata...
                        if data['mardi'] or data['wikidata']:
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
                        elif data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']:
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
            
    def Model(project, answers):
        '''Function retrieving Publication Information for model documentation'''

        # Get Questions of Workflow Catalog
        questions = get_questionsPU()

        # Go through all Publications
        for key in answers['publication']:
            
            # If User selected Publication from MathAlgoDB, MaRDI Portal or Wikidata...
            if answers['publication'][key]['ID'].startswith('mathalgodb') or answers['publication'][key]['ID'].startswith('mardi') or answers['publication'][key]['ID'].startswith('wikidata'):
                #...check if ressource returned a DOI and...
                if answers['publication'][key].get('reference', {}).get(0, ['',''])[1]:
                    #... use the DOI to query MathModDB. 
                    query = queryPublication['PublicationMathModDBDOI'].format(answers['publication'][key]['reference'][0][1])
                    results = query_sparql(query, endpoint['mathmoddb']['sparql'])
                    if results:
                        # If Publication found on MathModDB...
                        data = Publication.from_query(results)
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                     text = f"{data.label} ({data.description}) [mathmoddb]" , 
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
                    #If Publication available at MathModDB...
                    if data['mathmoddb']:
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                     text = f"{data['mathmoddb'].label} ({data['mathmoddb'].description}) [mathmoddb]", 
                                     external_id = data['mathmoddb'].id, 
                                     set_index = key)
                        #...ouput dictionary or...
                        answers['publication'][key]['ID'] = data['mathmoddb'].id
                        answers['publication'][key]['Name'] = data['mathmoddb'].label
                        answers['publication'][key]['Description'] = data['mathmoddb'].description
                    #if Publication available at MathAlgoDB...
                    elif data['mathalgodb']:
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                     text = f"{data['mathalgodb'].label} ({data['mathalgodb'].description}) [mathalgodb]", 
                                     external_id = data['mathalgodb'].id, 
                                     set_index = key)
                        #...ouput dictionary...
                        answers['publication'][key]['ID'] = data['mathalgodb'].id
                        answers['publication'][key]['Name'] = data['mathalgodb'].label
                        answers['publication'][key]['Description'] = data['mathalgodb'].description
                    #if Publication available at MaRDI Portal...
                    elif data['mardi']:
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                     text = f"{data['mardi'].label} ({data['mardi'].description}) [mardi]", 
                                     external_id = data['mardi'].id, 
                                     set_index = key)
                        #...ouput dictionary...
                        answers['publication'][key]['ID'] = data['mardi'].id
                        answers['publication'][key]['Name'] = generate_label(data['mardi'])
                        answers['publication'][key]['Description'] = data['mardi'].description
                    #if Publication available at Wikidata...
                    elif data['wikidata']:
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                     text = f"{data['wikidata'].label} ({data['wikidata'].description}) [wikidata]", 
                                     external_id = data['wikidata'].id, 
                                     set_index = key)
                        #...ouput dictionary...
                        answers['publication'][key]['ID'] = data['wikidata'].id
                        answers['publication'][key]['Name'] = generate_label(data['wikidata'])
                        answers['publication'][key]['Description'] = data['wikidata'].description
                    #if Publication available at Crossref, DataCite, ZBMath or DOI...
                    elif data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']:
                        DATA = data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']
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
    
    def Algorithm(project, answers):
        '''Function retrieving Publication Information for algorithm documentation'''

        # Get Questions of Workflow Catalog
        questions = get_questionsPU()

        # Go through all Publications
        for key in answers['publication']:
            # If User selected Publication from MathModDB, MaRDI Portal or Wikidata...
            if answers['publication'][key]['ID'].startswith('mathmoddb') or answers['publication'][key]['ID'].startswith('mardi') or answers['publication'][key]['ID'].startswith('wikidata'):
                #...check if ressource returned a DOI and...
                if answers['publication'][key].get('reference', {}).get(0, ['',''])[1]:
                    #... use the DOI to query MathAlgoDB. 
                    query = queryPublication['PublicationMathAlgoDBDOI'].format(answers['publication'][key]['reference'][0][1])
                    results = query_sparql(query, endpoint['mathalgodb']['sparql'])
                    if results:
                        # If Publication found on MathModDB...
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
                    #If Publication available at MathModDB...
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
                    #if Publication available at MathModDB...
                    elif data['mathmoddb']:
                        #...add data to Questionnaire and...
                        value_editor(project = project, 
                                     uri = f'{BASE_URI}{questions["Publication ID"]["uri"]}', 
                                     text = f"{data['mathmoddb'].label} ({data['mathmoddb'].description}) [mathmoddb]", 
                                     external_id = data['mathmoddb'].id, 
                                     set_index = key)
                        #...ouput dictionary...
                        answers['publication'][key]['ID'] = data['mathmoddb'].id
                        answers['publication'][key]['Name'] = data['mathmoddb'].label
                        answers['publication'][key]['Description'] = data['mathmoddb'].description
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
                    

