from rdmo.options.providers import Provider

from ..config import BASE_URI
from ..utils import get_data, query_sources, query_sources_with_user_additions

class Algorithm(Provider):

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
    
class AlgorithmicProblem(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'AP'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, queryID, sources)
    
class Software(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'SO'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, queryID, sources)
    
class Benchmark(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'BE'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, queryID, sources)