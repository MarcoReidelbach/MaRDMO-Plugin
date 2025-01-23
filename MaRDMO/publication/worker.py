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
                        print(data)
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
            
            #if answers['publication'][key].get('reference'):
#
            #    # If MaRDI Portal ID available
            #    if answers['publication'][key]['reference'].get(2):
            #        query = queryPublication['All_MaRDILabel'].format(P16, f"wd:{answers['publication'][key]['reference'][2][1]}", P8, P22, P4, P12, P10, P7, P9, P11, P13, P14, P15, P2, P23, wdt, wd)
            #        result = query_sparql(query,mardi_endpoint)
            #        if result:
            #            data = Publication.from_query(result)
            #            answers['publication'][key]['Title'] = generate_label(data)
            #            value_editor(instance, f'{BASE_URI}domain/publication/id', f"mardi:{answers['publication'][key]['reference'][2][1]}", f"mardi:{answers['publication'][key]['reference'][2][1]}", None, None, key)
            #            value_editor(instance, f'{BASE_URI}domain/publication/name', data.label, None, None, None, key)
            #            value_editor(instance, f'{BASE_URI}domain/publication/description', data.description, None, None, None, key)
            #            if not answers['publication'][key]['reference'].get(0) and data.doi:
            #                # If no DOI provided add queried DOI to answers and Questionnaire
            #                answers['publication'][key]['reference'].update({0:[options['DOI'],data.doi]})
            #                value_editor(instance, f'{BASE_URI}domain/publication/reference', data.doi, None, Option.objects.get(uri=options['DOI']), 0, key)       
#
            #    # If Wikidata ID available
            #    elif answers['publication'][key]['reference'].get(5):
            #        query = queryPublication['All_WikidataLabel'].format('356', f"wd:{answers['publication'][key]['reference'][5][1]}", '50', '496', '31', '1433', '407', '1476', '2093', '577', '478', '433', '304', '', '1556')
            #        result = query_sparql(query,wikidata_endpoint)
            #        if result:
            #            data = Publication.from_query(result)
            #            answers['publication'][key]['Title'] = generate_label(data)
            #            value_editor(instance, f'{BASE_URI}domain/publication/id', f"wikidata:{answers['publication'][key]['reference'][5][1]}", f"wikidata:{answers['publication'][key]['reference'][5][1]}", None, None, key)
            #            value_editor(instance, f'{BASE_URI}domain/publication/name', data.label, None, None, None, key)
            #            value_editor(instance, f'{BASE_URI}domain/publication/description', data.description, None, None, None, key)
            #            if not answers['publication'][key]['reference'].get(0) and data.doi:
            #                # If no DOI provided add queried DOI to answers and Questionnaire
            #                answers['publication'][key]['reference'].update({0:[options['DOI'],data.doi]})
            #                value_editor(instance, f'{BASE_URI}domain/publication/reference', data.doi, None, Option.objects.get(uri=options['DOI']), 0, key)
            #            if not answers['publication'][key]['reference'].get(2) and data.doi:
            #                query = queryPublication['All_MaRDI'].format(P16, data.doi, P8, P22, P4, P12, P10, P7, P9, P11, P13, P14, P15, P2, P23, wdt, wd)
            #                result = query_sparql(query,mardi_endpoint)
            #                if result:
            #                    data2 = Publication.from_query(result)
            #                    answers['publication'][key]['reference'].update({2:[options['MaRDIPortalID'],data2.id.split(':')[-1]]})
            #                    value_editor(instance, f'{BASE_URI}domain/publication/id', data2.id, data2.id, None, None, key)
            #                    value_editor(instance, f'{BASE_URI}domain/publication/name', data2.label, None, None, None, key)
            #                    value_editor(instance, f'{BASE_URI}domain/publication/description', data2.description, None, None, None, key)
            #                    value_editor(instance, f'{BASE_URI}domain/publication/reference', data2.id.split(':')[-1], None, Option.objects.get(uri=options['MaRDIPortalID']), 2, key)
            #                
            #    # If MathModDB ID available
            #    elif answers['publication'][key]['reference'].get(4):
            #        query = queryPublication['PublicationMathModDBLabel'].format(f":{answers['publication'][key]['reference'][4][1]}")
            #        result = query_sparql(query,mathmoddb_endpoint)
            #        if result:
            #            data = Publication.from_query(result)
            #            answers['publication'][key]['Title'] = data.label
            #            value_editor(instance, f'{BASE_URI}domain/publication/id', f"mathmoddb:{answers['publication'][key]['reference'][4][1]}", f"mathmoddb:{answers['publication'][key]['reference'][4][1]}", None, None, key)
            #            value_editor(instance, f'{BASE_URI}domain/publication/name', data.label, None, None, None, key)
            #            if data.doi:
            #                data2 = get_citation(data.doi)
            #                ID_added = False
            #                if data2.get('mardi'):
            #                    if not answers['publication'][key].get('Title'):
            #                        answers['publication'][key]['Title'] = generate_label(data2['mardi'])
            #                    if not answers['publication'][key]['reference'].get(2):
            #                        # If DOI provided add MaRDI Portal ID
            #                        answers['publication'][key]['reference'].update({2:[options['MaRDIPortalID'],data2['mardi'].id.split(':')[-1]]})
            #                        value_editor(instance, f'{BASE_URI}domain/publication/reference', data2['mardi'].id.split(':')[-1], None, Option.objects.get(uri=options['MaRDIPortalID']), 2, key)
            #                        if not ID_added:
            #                            value_editor(instance, f'{BASE_URI}domain/publication/id', data2['mardi'].id, data2['mardi'].id, None, None, key)
            #                            value_editor(instance, f'{BASE_URI}domain/publication/name', data2['mardi'].label, None, None, None, key)
            #                            ID_added = True
            #                if data2.get('wikidata'):
            #                    if not answers['publication'][key].get('Title'):
            #                        answers['publication'][key]['Title'] = generate_label(data2['wikidata'])
            #                    if not answers['publication'][key]['reference'].get(5):
            #                        # If DOI provided add Wikidata ID
            #                        answers['publication'][key]['reference'].update({5:[options['WikidataID'],data2['wikidata'].id.split(':')[-1]]})
            #                        value_editor(instance, f'{BASE_URI}domain/publication/reference', data2['wikidata'].id.split(':')[-1], None, Option.objects.get(uri=options['WikidataID']), 5, key)
            #                        if not ID_added:
            #                            print('YES!!!')
            #                            value_editor(instance, f'{BASE_URI}domain/publication/id', data2['wikidata'].id, data2['wikidata'].id, None, None, key)
            #                            value_editor(instance, f'{BASE_URI}domain/publication/name', data2['wikidata'].label, None, None, None, key)
            #                            ID_added = True
            #                if data2.get('crossref'):
            #                    if not answers['publication'][key].get('Title'):
            #                        answers['publication'][key]['Title'] = generate_label(data2['crossref'])
            #                        if not ID_added:
            #                            value_editor(instance, f'{BASE_URI}domain/publication/id', f"doi:{answers['publication'][key]['reference'][0][1]}", f"doi:{answers['publication'][key]['reference'][0][1]}", None, None, key)
            #                            value_editor(instance, f'{BASE_URI}domain/publication/name', generate_label(data2['crossref']), None, None, None, key)
            #                            ID_added = True
            #                if data2.get('datacite'):
            #                    if not answers['publication'][key].get('Title'):
            #                        answers['publication'][key]['Title'] = generate_label(data2['datacite'])
            #                        if not ID_added:
            #                            value_editor(instance, f'{BASE_URI}domain/publication/id', f"doi:{answers['publication'][key]['reference'][0][1]}", f"doi:{answers['publication'][key]['reference'][0][1]}", None, None, key)
            #                            value_editor(instance, f'{BASE_URI}domain/publication/name', generate_label(data2['datacite']), None, None, None, key)
            #                            ID_added = True
            #                if data2.get('doi'):
            #                    if not answers['publication'][key].get('Title'):
            #                        answers['publication'][key]['Title'] = generate_label(data2['doi'])
            #                        if not ID_added:
            #                            value_editor(instance, f'{BASE_URI}domain/publication/id', f"doi:{answers['publication'][key]['reference'][0][1]}", f"doi:{answers['publication'][key]['reference'][0][1]}", None, None, key)
            #                            value_editor(instance, f'{BASE_URI}domain/publication/name', generate_label(data2['doi']), None, None, None, key)
            #                            ID_added = True
            #                if data2.get('zbmath'):
            #                    if not answers['publication'][key].get('Title'):
            #                        answers['publication'][key]['Title'] = generate_label(data2['zbmath'])
            #                        if not ID_added:
            #                            value_editor(instance, f'{BASE_URI}domain/publication/id', f"doi:{answers['publication'][key]['reference'][0][1]}", f"doi:{answers['publication'][key]['reference'][0][1]}", None, None, key)
            #                            value_editor(instance, f'{BASE_URI}domain/publication/name', generate_label(data2['zbmath']), None, None, None, key)
            #                            ID_added = True
            #            if not answers['publication'][key]['reference'].get(0) and data.doi:
            #                # If no DOI provided add queried DOI to answers and Questionnaire
            #                answers['publication'][key]['reference'].update({0:[options['DOI'],data.doi]})
            #                value_editor(instance, f'{BASE_URI}domain/publication/reference', data.doi, None, Option.objects.get(uri=options['DOI']), 0, key)
                          

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
                    

