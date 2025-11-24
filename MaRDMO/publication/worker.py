'''Worker Module to collect Publication Metadata'''

from rdmo.projects.models import Value
from rdmo.domain.models import Attribute

from .constants import PUBLICATIONS, JOURNALS, AUTHORS, LANGUAGES
from .utils import generate_label, get_citation
from .sparql import queryPublication
from .models import Publication

from ..constants import BASE_URI
from ..getters import get_questions, get_properties, get_url
from ..queries import query_sparql
from ..helpers import value_editor

class PublicationRetriever:
    '''Retrieve Metadata from MaRDI Portal, Wikidata, MathAlgoDB and other
       sources like Crossref, DataCite, zbMath, DOI, and ORCid for Workflow,
       Model, and Algorithm documentation.'''

    # Get Publication-related Questions
    questions = get_questions('publication')

    def workflow_or_model(self, project, snapshot, answers, options):
        '''Function retrieving Publication Information for workflow and model documentation'''

        for key in answers.get('publication', {}):

            if str(project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):
                # Ignore references for individual triple in workflow catalog
                if answers['publication'][key]['workflow'] != options['Yes']:
                    continue

            # If ID is missing (not answered or deleted)
            if not answers['publication'][key].get('ID'):
                continue

            #If User selected Publication from Wikidata...
            if answers['publication'][key]['ID'].startswith('wikidata'):
                #...use the DOI...
                doi = answers['publication'][key].get('reference', {}).get(0, ['',''])[1]
                #...to query MaRDI Portal.
                query = queryPublication['MaRDI']['DOI'].format(doi, **get_properties())
                results = query_sparql(
                    query,
                    get_url(
                        'mardi',
                        'sparql'
                    )
                )
                if results:
                    #If Publication found in MaRDI Portal...
                    data = Publication.from_query(results)
                    #...add data to Questionnaire and...
                    value_editor(
                        project = project,
                        uri = f'{BASE_URI}{self.questions["Publication"]["ID"]["uri"]}',
                        info = {
                            'text': f"{data.label} ({data.description}) [mardi]" , 
                            'external_id': data.id, 
                            'set_index': key
                        }
                    )
                    #...ouput dictionary.
                    answers['publication'][key]['ID'] = data.id
                    answers['publication'][key]['Name'] = data.label
                    answers['publication'][key]['Description'] = data.description

            #If User selected a Publication from MathAlgoDB or did not find it...
            elif answers['publication'][key]['ID'].startswith(('mathalgodb', 'not found')):
                #...but provided a DOI.
                if answers['publication'][key].get('reference', {}).get(0, ['',''])[1]:
                    #Clean potential old data...
                    for question in PUBLICATIONS | LANGUAGES | JOURNALS | AUTHORS:
                        Value.objects.filter(
                            project = project,
                            snapshot = snapshot,
                            attribute_id = Attribute.objects.get(
                                uri = f'{BASE_URI}{self.questions["Publication"][question]["uri"]}'
                            ),
                            set_index = key
                        ).delete()
                    #Get the Citation of several ressource.
                    data_all = get_citation(answers['publication'][key]['reference'][0][1].upper())

                    #If Publication available at MaRDI Portal or Wikidata...
                    if data_all.get('mardi') or data_all.get('wikidata'):
                        data = data_all['mardi'] or data_all['wikidata']
                        #...and add data to Questionnaire and...
                        value_editor(
                            project = project,
                            uri = f'{BASE_URI}{self.questions["Publication"]["ID"]["uri"]}',
                            info = {
                                'text':
                                    f"{data.label} ({data.description}) [{data.id.split(':')[0]}]",
                                'external_id': data.id, 
                                'set_index': key
                            }
                        )
                        #...ouput dictionary.
                        answers['publication'][key]['ID'] = data.id
                        answers['publication'][key]['Name'] = data.label
                        answers['publication'][key]['Description'] = data.description

                    #If Publication available at Crossref, Datacite, zbMath or DOI...
                    elif any(data_all.get(k) for k in ("crossref", "datacite", "zbmath", "doi")):
                        data = (
                            data_all.get("crossref")
                            or data_all.get("datacite")
                            or data_all.get("zbmath")
                            or data_all.get("doi")
                        )
                        #...add data to Questionnaire and...
                        for uri, data_key in PUBLICATIONS.items():
                            value_editor(
                                project = project,
                                uri = f'{BASE_URI}{self.questions["Publication"][uri]["uri"]}',
                                info = {
                                    'text': getattr(data, data_key), 
                                    'set_index': key
                                }
                            )

                        for idx, language in enumerate(data.language):
                            for uri, data_key in LANGUAGES.items():
                                value_editor(
                                    project = project,
                                    uri = f'{BASE_URI}{self.questions["Publication"][uri]["uri"]}',
                                    info = {
                                        'text': getattr(language, data_key), 
                                        'collection_index': idx, 
                                        'set_index': key
                                    }
                                )

                        for idx, journal in enumerate(data.journal):
                            for uri, data_key in JOURNALS.items():
                                value_editor(
                                    project = project,
                                    uri = f'{BASE_URI}{self.questions["Publication"][uri]["uri"]}',
                                    info = {
                                        'text': getattr(journal, data_key), 
                                        'collection_index': idx, 
                                        'set_index': key
                                    }
                                )

                        for idx, author in enumerate(data.authors):
                            for uri, data_key in AUTHORS.items():
                                value_editor(
                                    project = project,
                                    uri = f'{BASE_URI}{self.questions["Publication"][uri]["uri"]}',
                                    info = {
                                        'text': getattr(author, data_key), 
                                        'collection_index': idx, 
                                        'set_index': key
                                    }
                                )

                        #...output dictionary.
                        answers['publication'][key]['Name'] = data.title
                        answers['publication'][key]['Description'] = data.description

        return answers

    def algorithm(self, project, answers):
        '''Function retrieving Publication Information for algorithm documentation'''

        # Go through all Publications
        for key in answers['publication']:
            # If ID is missing (not answered or deleted)
            if not answers['publication'][key].get('ID'):
                continue
            # If User selected Publication from MaRDI Portal or Wikidata...
            if answers['publication'][key]['ID'].startswith(('mardi', 'wikidata')):
                #...check if ressource returned a DOI and...
                if answers['publication'][key].get('reference', {}).get(0, ['',''])[1]:
                    #... use the DOI to query MathAlgoDB.
                    query = queryPublication['PublicationMathAlgoDBDOI'].format(
                        answers['publication'][key]['reference'][0][1]
                    )
                    results = query_sparql(
                        query,
                        get_url(
                            'mathalgodb',
                            'sparql'
                        )
                    )
                    if results:
                        # If Publication found on MathAlgoDB...
                        data = Publication.from_query(results)
                        #...add data to Questionnaire and...
                        value_editor(
                            project = project,
                            uri = f'{BASE_URI}{self.questions["Publication"]["ID"]["uri"]}',
                            info = {
                                'text': f"{data.label} ({data.description}) [mathalgodb]" , 
                                'external_id': data.id, 
                                'set_index': key
                            }
                        )
                        #...ouput dictionary.
                        answers['publication'][key]['ID'] = data.id
                        answers['publication'][key]['Name'] = data.label
                        answers['publication'][key]['Description'] = data.description

            #If User did not find its publication...
            elif answers['publication'][key]['ID'].startswith('not found'):
                #...but provided a DOI.
                if answers['publication'][key]['reference'].get(0, ['',''])[1]:
                    #Get the Citation of several ressource.
                    data_all = get_citation(answers['publication'][key]['reference'][0][1])
                    #If Publication available at MathAlgoDB...
                    if data_all['mathalgodb']:
                        #...add data to Questionnaire and...
                        value_editor(
                            project = project,
                            uri = f'{BASE_URI}{self.questions["Publication"]["ID"]["uri"]}',
                            info = {
                                'text': 
                                    f"{data_all['mathalgodb'].label} ({data_all['mathalgodb'].description}) [mathalgodb]",
                                'external_id': data_all['mathalgodb'].id,
                                'set_index': key
                            }
                        )
                        #...ouput dictionary or...
                        answers['publication'][key]['ID'] = data_all['mathalgodb'].id
                        answers['publication'][key]['Name'] = data_all['mathalgodb'].label
                        answers['publication'][key]['Description'] = data_all['mathalgodb'].description
                    #if Publication available at MaRDI/Wikidata/Crossref/DataCite/zbMath/DOI.
                    elif any(data_all.get(k) for k in (
                        "mardi", "wikidata", "crossref",
                        "datacite", "zbmath", "doi")
                    ):
                        data = (
                            data_all.get("mardi")
                            or data_all.get("wikidata")
                            or data_all.get("crossref")
                            or data_all.get("datacite")
                            or data_all.get("zbmath")
                            or data_all.get("doi")
                        )
                        #...add data to Questionnaire and...
                        value_editor(
                            project = project,
                            uri =
                                f'{BASE_URI}{self.questions["Publication"]["Name"]["uri"]}',
                            info = {
                                'text': generate_label(data), 
                                'set_index': key
                            }
                        )
                        value_editor(
                            project = project,
                            uri = 
                                f'{BASE_URI}{self.questions["Publication"]["Description"]["uri"]}',
                            info = {
                                'text': data.description, 
                                'set_index': key
                            }
                        )
                        #...output dictionary.
                        answers['publication'][key]['Name'] = generate_label(data)
                        answers['publication'][key]['Description'] = data.description

        return answers
