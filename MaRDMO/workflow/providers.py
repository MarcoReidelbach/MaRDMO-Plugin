from rdmo.options.providers import Provider
from rdmo.domain.models import Attribute

from .sparql import queryProvider

from ..config import BASE_URI, endpoint
from ..id import ITEMS, PROPERTIES
from ..utils import get_data, query_sources, query_sources_with_user_additions, query_sparql
import requests, time

# PLACEHOLDER PROVIDER FOR FUTURE CHANGES
#class WikibaseModelLoader:
#    _data_cache = None
#    _loaded = False
#    _last_load_time = 0
#
#    instance_qid = "Q486902"  # QID for "mathematical model"
#    sparql_endpoint = "https://query.wikidata.org/sparql"  # Your endpoint here
#
#    @classmethod
#    def _load_data(cls):
#        # Optional: Reload after 1 hour
#        if cls._loaded and (time.time() - cls._last_load_time < 3600):
#            return cls._data_cache
#
#        print("Fetching data via SPARQL GET...")
#
#        query = f"""
#        SELECT ?item ?itemLabel ?itemDescription WHERE {{
#          ?item wdt:P31 wd:{cls.instance_qid} .
#          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
#        }}
#        LIMIT 10000
#        """
#        params = {
#            "query": query,
#            "format": "json"
#        }
#
#        try:
#            response = requests.get(cls.sparql_endpoint, params=params, headers={"User-Agent": "ModelLoader/1.0"})
#            response.raise_for_status()
#            results = response.json()
#        except Exception as e:
#            print("SPARQL GET failed:", e)
#            cls._data_cache = []
#            cls._loaded = True
#            return cls._data_cache
#
#        data = []
#        for result in results["results"]["bindings"]:
#            qid = result["item"]["value"].split("/")[-1]
#            label = result.get("itemLabel", {}).get("value", "")
#            description = result.get("itemDescription", {}).get("value", "")
#            data.append({
#                "id": f"wikidata:{qid}",
#                "label": label,
#                "description": description
#            })
#
#        cls._data_cache = data
#        cls._loaded = True
#        cls._last_load_time = time.time()
#        print(f"Fetched {len(data)} items")
#        return cls._data_cache
#
#    @classmethod
#    def get_model_data(cls):
#        return cls._load_data()
#
#class TEST(WikibaseModelLoader, Provider):
#    search = True
#
#    def get_options(self, project, search, user=None, site=None):
#        if not search or len(search) < 2:
#            return []
#
#        data = self.get_model_data()
#        search_lower = search.lower()
#
#        return [
#            {
#                "id": model["id"],
#                "text": f'{model["label"]} ({model["description"]}) [wikidata]'
#            }
#            for model in data
#            if search_lower in model["label"].lower()
#        ]

class MaRDIAndWikidataSearch(Provider):

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class MainMathematicalModel(Provider):

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'MM'
        sources = ['mardi']

        return query_sources(search, queryID, sources)
    
class Method(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'AL'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, queryID, sources)
    
class RelatedMethod(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'AL'
        sources = ['mathalgodb', 'mardi', 'wikidata']
        queryAttributes = ['method']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 queryID = queryID,
                                                 creation = True,
                                                 sources = sources)
    
class WorkflowTask(Provider):

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MaRDI Portak for Task related to chosen Model'''

        options = []
        model_id = ''

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/main-model'))        
        for value in values:
            model_id = value.external_id

        if model_id:
            _, id_value = model_id.split(':')
            results = query_sparql(queryProvider['RT'].format(id_value, **ITEMS, **PROPERTIES), endpoint['mardi']['sparql'])
            if results:
                if results[0].get('usedBy', {}).get('value'):
                    tasks = results[0]['usedBy']['value'].split(' / ')
                    for task in tasks:
                        id, label, description = task.split(' | ')
                        options.append({'id': id, 'text': f'{label} ({description}) [mardi]'})

        return options
    
class Software(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = 'SO'
        sources = ['mathalgodb', 'mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class RelatedSoftware(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
    
        if not search:
            return []
        
        # Define the query parameter
        queryID = 'SO'
        sources = ['mathalgodb', 'mardi', 'wikidata']
        queryAttributes = ['software']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 queryID = queryID,
                                                 creation = True,
                                                 sources = sources)

class Hardware(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)
    
class Instrument(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)
    
class DataSet(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)
    
class RelatedInstrument(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
    
        if not search:
            return []
        
        # Define the query parameter
        queryAttributes = ['instrument']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 creation = True)
    
class RelatedDataSet(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
    
        if not search:
            return []
        
        # Define the query parameter
        queryAttributes = ['data-set']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 creation = True)
            
class ProcessStep(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)
    
class Discipline(Provider):

    msc = get_data('data/msc2020.json')

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        # Discipline from Knowledge Graphs
        options = query_sources(search, queryID, sources, False)

        # Mathematical Subjects
        options.extend([{'id': f"msc:{self.msc[key]['id']}", 'text': f"{key} ({self.msc[key]['quote']}) [msc]"} for key in self.msc if search.lower() in key.lower()])

        return sorted(options, key=lambda option: option['text'].lower())[:30]
