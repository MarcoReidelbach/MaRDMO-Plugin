'''Worker Module to collect Publication Metadata'''

from .constants import ITEMINFOS, CITATIONINFOS, JOURNALS, AUTHORS, LANGUAGES
from .utils import clean_background_data, get_citation

from ..constants import BASE_URI
from ..getters import get_items, get_properties, get_questions
from ..helpers import date_precision, value_editor

class PublicationRetriever:
    '''Retrieve Metadata from MaRDI Portal, Wikidata, and other
       sources like Crossref, DataCite, zbMath, DOI, and ORCid for Workflow,
       Model, and Algorithm documentation.'''

    # Get Publication-related Questions
    questions = get_questions('publication')

    def get_information(self, project, snapshot, answers, options):
        '''Function retrieving Publication Information for algorithm,
           workflow and model documentation.
        '''

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
            if answers['publication'][key]['ID'].startswith(('wikidata','not found')):

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

class PublicationExport:
    '''Collect Metadata for Author, Journal, and Publication Export'''

    def __init__(self):
        self.properties = get_properties()
        self.items = get_items()

    def _export_journals(self, payload, publications: dict):
        for publication in publications.values():
            for entry in publication.get('journal', {}).values():
                if not entry.get("ID") or entry.get("ID") == 'no journal found':
                    continue

                payload.get_item_key(
                value = entry
                )

                payload.add_answer(
                    verb = self.properties["instance of"],
                    object_and_type = [self.items["scientific journal"], "wikibase-item"],
                )

                if entry.get('issn'):
                    payload.add_answer(
                        verb = self.properties["ISSN"],
                        object_and_type = [entry["issn"], "external-id"],
                    )

    def _export_authors(self, payload, publications: dict):
        for publication in publications.values():
            for entry in publication.get('author', {}).values():
                if not entry.get("ID") or entry.get("ID") == 'no author found':
                    continue

                payload.get_item_key(
                value = entry
                )

                payload.add_answer(
                    verb = self.properties["instance of"],
                    object_and_type = [self.items["human"], "wikibase-item"],
                )

                payload.add_answer(
                    verb = self.properties["MaRDI profile type"],
                    object_and_type = [self.items["Person"], "wikibase-item"],
                )

                if entry.get('orcid'):
                    payload.add_answer(
                        verb = self.properties["ORCID iD"],
                        object_and_type = [
                            entry['orcid'],
                            "external-id"
                        ],
                    )

                if entry.get('zbmath'):
                    payload.add_answer(
                        verb = self.properties["zbMATH author ID"],
                        object_and_type = [
                            entry['zbmath'],
                            "external-id"
                        ],
                    )

    def _export_publications(self, payload, publications: dict, relations: list):
        for entry in publications.values():
            if not entry.get("ID"):
                continue

            payload.get_item_key(
                value = entry
            )

            # Only add class, profile, and DOI for non-MaRDI items
            if "mardi" not in entry["ID"]:

                 # Set and add Publication Class
                if entry.get("entrytype") == "scholarly article":
                    pclass = self.items["scholarly article"]
                else:
                    pclass = self.items["publication"]

                payload.add_answer(
                    verb = self.properties["instance of"],
                    object_and_type = [pclass, "wikibase-item"],
                )

                # Add Publication Profile
                payload.add_answer(
                        verb = self.properties["MaRDI profile type"],
                        object_and_type = [
                            self.items["MaRDI publication profile"],
                            "wikibase-item"
                        ],
                    )

                # Add DOI
                if entry.get("reference", {}).get(0):
                    payload.add_answer(
                        verb = self.properties["DOI"],
                        object_and_type = [
                            entry["reference"][0][1].upper(),
                            "external-id"
                        ],
                    )

                # bibliographic data
                if entry.get("title"):
                    payload.add_answer(
                        verb = self.properties["title"],
                        object_and_type = [
                            {"text": entry["title"], "language": "en"},
                            "monolingualtext",
                        ],
                    )

                if entry.get("volume"):
                    payload.add_answer(
                        verb = self.properties["volume"],
                        object_and_type = [entry["volume"], "string"],
                    )

                if entry.get("issue"):
                    payload.add_answer(
                        verb = self.properties["issue"],
                        object_and_type = [entry["issue"], "string"],
                    )

                if entry.get("page"):
                    payload.add_answer(
                        verb = self.properties["page(s)"],
                        object_and_type = [entry["page"], "string"],
                    )

                if entry.get("date"):
                    payload.add_answer(
                        verb = self.properties["publication date"],
                        object_and_type = [
                            {
                                "time": f"+{entry['date']}",
                                "precision": date_precision(
                                    date_str = entry['date']
                                ),
                                "calendarmodel": (
                                    "http://www.wikidata.org/entity/Q1985727"
                                ),
                            },
                            "time",
                        ],
                    )

                # Add Language
                payload.add_single_relation(
                    statement = {
                        'relation': self.properties["language of work or name"],
                        'relatant': "language"
                    }
                )
                # Add Journal
                payload.add_single_relation(
                    statement = {
                        'relation': self.properties["published in"],
                        'relatant': "journal"
                    }
                )
                # Add Authors
                payload.add_single_relation(
                    statement = {
                        'relation': self.properties["author"],
                        'relatant': "author"
                    },
                    alt_statement = {
                        "relation": self.properties["author name string"],
                        "relatant": "Name",
                    },
                )

            # Add caller-supplied relations (P2E, P2A/P2BS, etc.)
            for relation, relatant in relations:
                payload.add_multiple_relation(
                    statement = {
                        'relation': relation,
                        'relatant': relatant
                    },
                    reverse = True,
                )
