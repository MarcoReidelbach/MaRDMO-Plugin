from rdmo.options.providers import Provider
from ..utils import query_sources

class MaRDISearch(Provider):

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi']

        return query_sources(search, queryID, sources)
    
class ModelEntitySearch(Provider):

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = 'EN'
        sources = ['mathmoddb']

        return query_sources(search, queryID, sources)