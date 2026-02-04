'''Module containing Providers for the Algorithm, Model, Workflow Search'''

from rdmo.options.providers import Provider
from ..queries import query_sources

class MaRDISearch(Provider):
    '''General Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query sources
        sources = ['mardi']

        return query_sources(search, sources)
    