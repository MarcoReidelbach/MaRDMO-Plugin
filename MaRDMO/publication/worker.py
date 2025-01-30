from rdmo.options.models import Option

from .utils import generate_label, get_citation
from .sparql import queryPublication
from .models import Publication

from ..utils import query_sparql, value_editor
from ..config import BASE_URI, mardi_endpoint, mathmoddb_endpoint, mathalgodb_endpoint, wdt, wd, wikidata_endpoint
from ..id import *

class PublicationRetriever:

    def Workflow(instance, answers, options):
        '''Function retrieving Publication Information for model documentation'''

        for key in answers['publication']:

            #If Workflow is published in Publication...
            if answers['publication'][key]['workflow'] == options['Yes']:

                #If User selected Publication from Wikidata...
                if answers['publication'][key]['ID'].startswith('wikidata'):
                    #...use the DOI to query MaRDI Portal. 
                    query = queryPublication['MaRDIDOI'].format(P16, answers['publication'][key]['reference'][0][1].upper(), wdt, wd)
                    results = query_sparql(query,mardi_endpoint)
                    if results:
                        #If Publication found on MathModDB...
                        data = Publication.from_query(results)
                        #...add data to Questionnaire and...
                        value_editor(instance, f'{BASE_URI}domain/publication/id', f"{data.label} ({data.description}) [mardi]" , data.id, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/name', data.label , None, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/description', data.description, None, None, None, key)
                        #...ouput dictionary.
                        answers['publication'][key]['ID'] = data.id
                        answers['publication'][key]['Name'] = data.label
                        answers['publication'][key]['Description'] = data.description
    
                #If User selected a Publication from MathAlgoDB, MathModDB or did not find it...
                elif answers['publication'][key]['ID'].startswith('mathalgodb') or answers['publication'][key]['ID'].startswith('mathmoddb') or answers['publication'][key]['ID'].startswith('not found'):
                    #...but provided a DOI.
                    if answers['publication'][key]['reference'].get(0, ['',''])[1]:
                        #Get the Citation of several ressource.
                        data = get_citation(answers['publication'][key]['reference'][0][1])
                        #If Publication available at MaRDI Portal or Wikidata...
                        if data['mardi'] or data['wikidata']:
                            DATA = data['mardi'] or data['wikidata']
                            #...add data to Questionnaire and...
                            value_editor(instance, f'{BASE_URI}domain/publication/id', f"{DATA.label} ({DATA.description}) [{DATA.id.split(':')[0]}]" , DATA.id, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/name', DATA.label , None, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/description', DATA.description, None, None, None, key)
                            #...ouput dictionary.
                            answers['publication'][key]['ID'] = DATA.id
                            answers['publication'][key]['Name'] = DATA.label
                            answers['publication'][key]['Description'] = DATA.description
                        #If Publication available at Crossref, Datacite, zbMath or DOI...
                        elif data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']:
                            DATA = data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']
                            #...add data to Questionnaire and...
                            value_editor(instance, f'{BASE_URI}domain/publication/name', DATA.title, None, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/description', DATA.entrytype, None, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/entry-type', DATA.entrytype, None, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/language', DATA.language, None, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/title', DATA.title, None, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/date', DATA.date, None, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/volume', DATA.volume, None, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/issue', DATA.issue, None, None, None, key)
                            value_editor(instance, f'{BASE_URI}domain/publication/page', DATA.page, None, None, None, key)
                            for idx, journal in enumerate(DATA.journal):
                                value_editor(instance, f'{BASE_URI}domain/publication/journal/id', journal.id, None, None, idx, key)
                                value_editor(instance, f'{BASE_URI}domain/publication/journal/issn', journal.issn, None, None, idx, key)
                                value_editor(instance, f'{BASE_URI}domain/publication/journal/name', journal.label, None, None, idx, key)
                                value_editor(instance, f'{BASE_URI}domain/publication/journal/description', journal.description, None, None, idx, key)
                            for idx, author in enumerate(DATA.authors):
                                value_editor(instance, f'{BASE_URI}domain/publication/author/id', author.id, None, None, idx, key)
                                value_editor(instance, f'{BASE_URI}domain/publication/author/orcid', author.orcid_id, None, None, idx, key)
                                value_editor(instance, f'{BASE_URI}domain/publication/author/zbmath', author.zbmath_id, None, None, idx, key)
                                value_editor(instance, f'{BASE_URI}domain/publication/author/wikidata', author.wikidata_id, None, None, idx, key)                            
                                value_editor(instance, f'{BASE_URI}domain/publication/author/name', author.label, None, None, idx, key)
                                value_editor(instance, f'{BASE_URI}domain/publication/author/description', author.description, None, None, idx, key)
                            #...output dictionary.
                            answers['publication'][key]['Name'] = DATA.title
                            answers['publication'][key]['Description'] = DATA.entrytype

        return answers
            
    def Model(instance, answers, options):
        '''Function retrieving Publication Information for model documentation'''

        # Go through all Publications
        for key in answers['publication']:
            
            # If User selected Publication from MathAlgoDB, MaRDI Portal or Wikidata...
            if answers['publication'][key]['ID'].startswith('mathalgodb') or answers['publication'][key]['ID'].startswith('mardi') or answers['publication'][key]['ID'].startswith('wikidata'):
                #...check if ressource returned a DOI and...
                if answers['publication'][key]['reference'].get(0, ['',''])[1]:
                    #... use the DOI to query MathModDB. 
                    query = queryPublication['PublicationMathModDBDOI'].format(answers['publication'][key]['reference'][0][1])
                    results = query_sparql(query,mathmoddb_endpoint)
                    if results:
                        # If Publication found on MathModDB...
                        data = Publication.from_query(results)
                        #...add data to Questionnaire and...
                        value_editor(instance, f'{BASE_URI}domain/publication/id', f"{data.label} ({data.description}) [mathmoddb]" , data.id, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/name', data.label , None, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/description', data.description, None, None, None, key)
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
                        value_editor(instance, f'{BASE_URI}domain/publication/id', f"{data['mathmoddb'].label} ({data['mathmoddb'].description}) [mathmoddb]" , data['mathmoddb'].id, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/name', data['mathmoddb'].label , None, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/description', data['mathmoddb'].description, None, None, None, key)
                        #...ouput dictionary or...
                        answers['publication'][key]['ID'] = data['mathmoddb'].id
                        answers['publication'][key]['Name'] = data['mathmoddb'].label
                        answers['publication'][key]['Description'] = data['mathmoddb'].description
                    #if Publication available at MathAlgoDB...
                    elif data['mathalgodb']:
                        #...add data to Questionnaire and...
                        value_editor(instance, f'{BASE_URI}domain/publication/id', f"{data['mathalgodb'].label} ({data['mathalgodb'].description}) [mathalgodb]" , data['mathalgodb'].id, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/name', data['mathalgodb'].label , None, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/description', data['mathalgodb'].description, None, None, None, key)
                        #...ouput dictionary...
                        answers['publication'][key]['ID'] = data['mathalgodb'].id
                        answers['publication'][key]['Name'] = data['mathalgodb'].label
                        answers['publication'][key]['Description'] = data['mathalgodb'].description
                    #if Publication available at MaRDI Portal, Wikidata, Crossref, DataCite, ZBMath or DOI...
                    elif data['mardi'] or data['wikidata'] or data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']:
                        DATA = data['mardi'] or data['wikidata'] or data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']
                        #...add data to Questionnaire and...
                        value_editor(instance, f'{BASE_URI}domain/publication/name', generate_label(DATA), None, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/description', DATA.description, None, None, None, key)
                        #...output dictionary.
                        answers['publication'][key]['Name'] = generate_label(DATA)
                        answers['publication'][key]['Description'] = DATA.description

        return answers
    
    def Algorithm(instance, answers, options):
        '''Function retrieving Publication Information for algorithm documentation'''

        # Go through all Publications
        for key in answers['publication']:
            # If User selected Publication from MathModDB, MaRDI Portal or Wikidata...
            if answers['publication'][key]['ID'].startswith('mathmoddb') or answers['publication'][key]['ID'].startswith('mardi') or answers['publication'][key]['ID'].startswith('wikidata'):
                #...check if ressource returned a DOI and...
                if answers['publication'][key]['reference'].get(0, ['',''])[1]:
                    #... use the DOI to query MathAlgoDB. 
                    query = queryPublication['PublicationMathAlgoDBDOI'].format(answers['publication'][key]['reference'][0][1])
                    results = query_sparql(query,mathalgodb_endpoint)
                    if results:
                        # If Publication found on MathModDB...
                        data = Publication.from_query(results)
                        #...add data to Questionnaire and...
                        value_editor(instance, f'{BASE_URI}domain/publication/id', f"{data.label} ({data.description}) [mathalgodb]" , data.id, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/name', data.label , None, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/description', data.description, None, None, None, key)
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
                        value_editor(instance, f'{BASE_URI}domain/publication/id', f"{data['mathalgodb'].label} ({data['mathalgodb'].description}) [mathalgodb]" , data['mathalgodb'].id, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/name', data['mathalgodb'].label , None, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/description', data['mathalgodb'].description, None, None, None, key)
                        #...ouput dictionary or...
                        answers['publication'][key]['ID'] = data['mathalgodb'].id
                        answers['publication'][key]['Name'] = data['mathalgodb'].label
                        answers['publication'][key]['Description'] = data['mathalgodb'].description
                    #if Publication available at MathModDB...
                    elif data['mathmoddb']:
                        #...add data to Questionnaire and...
                        value_editor(instance, f'{BASE_URI}domain/publication/id', f"{data['mathmoddb'].label} ({data['mathmoddb'].description}) [mathmoddb]" , data['mathmoddb'].id, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/name', data['mathmoddb'].label , None, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/description', data['mathmoddb'].description, None, None, None, key)
                        #...ouput dictionary...
                        answers['publication'][key]['ID'] = data['mathmoddb'].id
                        answers['publication'][key]['Name'] = data['mathmoddb'].label
                        answers['publication'][key]['Description'] = data['mathmoddb'].description
                    #if Publication available at MaRDI Portal, Wikidata, Crossref, DataCite, ZBMath or DOI...
                    elif data['mardi'] or data['wikidata'] or data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']:
                        DATA = data['mardi'] or data['wikidata'] or data['crossref'] or data['datacite'] or data['zbmath'] or data['doi']
                        #...add data to Questionnaire and...
                        value_editor(instance, f'{BASE_URI}domain/publication/name', generate_label(DATA), None, None, None, key)
                        value_editor(instance, f'{BASE_URI}domain/publication/description', DATA.description, None, None, None, key)
                        #...output dictionary.
                        answers['publication'][key]['Name'] = generate_label(DATA)
                        answers['publication'][key]['Description'] = DATA.description

        return answers
                    

