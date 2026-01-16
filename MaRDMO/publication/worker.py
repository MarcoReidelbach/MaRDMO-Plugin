'''Worker Module to collect Publication Metadata'''

from .constants import ITEMINFOS, CITATIONINFOS, JOURNALS, AUTHORS, LANGUAGES
from .utils import clean_background_data, generate_label, get_citation

from ..constants import BASE_URI
from ..getters import get_questions
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

            #Clean potential old data...
            clean_background_data(
                key_dict = CITATIONINFOS | LANGUAGES | JOURNALS | AUTHORS,
                questions = self.questions["Publication"],
                project = project,
                snapshot = snapshot,
                set_index = key
            )

            #If User selected a Publication from Wikidata, MathAlgoDB or did not find it...
            if answers['publication'][key]['ID'].startswith(('wikidata','mathalgodb','not found')):

                #...check if DOI is available.
                if not answers['publication'][key].get('reference', {}).get(0, ['',''])[1]:
                    continue

                #Get the Citation of several ressource.
                data_all = get_citation(answers['publication'][key]['reference'][0][1].upper())

                #If Publication available at MaRDI, Wikidata, Crossref, Datacite, zbMath or DOI...
                if any(
                    data_all.get(k)
                    for k in ("mardi", "wikidata", "crossref", "datacite", "zbmath", "doi")
                ):

                    data = (
                        data_all.get('mardi')
                        or data_all.get("wikidata")
                        or data_all.get("crossref")
                        or data_all.get("datacite")
                        or data_all.get("zbmath")
                        or data_all.get("doi")
                    )

                    #...add data to Questionnaire and...
                    if data_all.get('mardi') or data_all.get('wikidata'):
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

                    for uri, data_key in (ITEMINFOS|CITATIONINFOS).items():
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
                    if data_all.get('mardi') or data_all.get('wikidata'):
                        answers['publication'][key]['ID'] = data.id
                    answers['publication'][key]['Name'] = data.label
                    answers['publication'][key]['Description'] = data.description

        return answers

    def algorithm(self, project, snapshot, answers):
        '''Function retrieving Publication Information for algorithm documentation'''

        # Go through all Publications
        for key in answers['publication']:

            # If ID is missing (not answered or deleted)
            if not answers['publication'][key].get('ID'):
                continue

            # If User selected Publication from MaRDI Portal or Wikidata...
            if answers['publication'][key]['ID'].startswith(('mardi', 'wikidata', 'not found')):

                #...check if DOI is available.
                if not answers['publication'][key].get('reference', {}).get(0, ['',''])[1]:
                    continue

                #Clean potential old data...
                clean_background_data(
                    key_dict = CITATIONINFOS | LANGUAGES | JOURNALS | AUTHORS,
                    questions = self.questions["Publication"],
                    project = project,
                    snapshot = snapshot,
                    set_index = key
                )

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
                                f"{data_all['mathalgodb'].label} "
                                f"({data_all['mathalgodb'].description}) [mathalgodb]",
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
                    if data_all.get('mardi') or data_all.get('wikidata'):
                        answers['publication'][key]['ID'] = data.id
                    answers['publication'][key]['Name'] = generate_label(data)
                    answers['publication'][key]['Description'] = data.description

        return answers
