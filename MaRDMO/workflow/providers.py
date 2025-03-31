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
        queryAttribute = 'method'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, ['mathalgodb', 'mardi', 'wikidata'])
    
class WorkflowTask(Provider):

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for Task related to chosen Model'''

        options = []
        model_id = ''

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/main-model/id'))        
        for value in values:
            model_id = value.external_id

        if model_id:
            _, id_value = model_id.split(':')
            results = query_sparql(queryProvider['RT'].format(id_value))
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
        queryAttribute = 'software'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources)

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
        queryID = ''
        sources = ['mardi', 'wikidata']
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
        options.extend([{'id': f"msc:{self.msc[key]['id']}", 'text': f"{key} ({self.msc[key]['quote']}) [msc]"} for key in self.msc if search.lower() in key.lower()])

        return sorted(options, key=lambda option: option['text'].lower())[:30]
