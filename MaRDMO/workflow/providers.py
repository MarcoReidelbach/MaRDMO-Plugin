from rdmo.options.providers import Provider
from rdmo.domain.models import Attribute

from .sparql import queryProvider

from ..config import BASE_URI
from ..utils import get_data, query_sources, query_sources_with_user_additions, query_sparql

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
        sources = ['mathmoddb']

        return query_sources(search, queryID, sources)
    
class MainAlgorithm(Provider):

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathAlgoDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'AL'
        sources = ['mathalgodb']

        return query_sources(search, queryID, sources)
    
class WorkflowTask(Provider):

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for Task related to chosen Model'''

        options = []

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/main-model/id'))        
        for value in values:
            id = value.external_id

        results = query_sparql(queryProvider['RT'].format(f':{id.split(":")[-1]}'))
        if results:
            for result in results:
                options.append({'id': f'mathmoddb:{result.get("id", {}).get("value")}', 'text': f'{result.get("label", {}).get("value")} ({result.get("quote", {}).get("value")}) [mathmoddb]'})

        return options
    
class Software(Provider):

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
    
class RelatedSoftware(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
    
        if not search:
            return []
        
        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']
        queryAttribute = 'software'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources)
    
class RelatedInstrument(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
    
        if not search:
            return []
        
        # Define the query parameter
        queryID = ''
        sources = []
        queryAttribute = 'instrument'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources)
    
class RelatedDataSet(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
    
        if not search:
            return []
        
        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']
        queryAttribute = 'data-set'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources)
            
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
        options.extend([{'id': f"msc:{self.msc[key]['id']}" + ' - ' + key , 'text': f"{key} ({self.msc[key]['id']}) [msc]"} for key in self.msc if search.lower() in key.lower()])

        return sorted(options, key=lambda option: option['text'].lower())[:30]
