'''Module containing Providers for the Publication Documentation'''

from rdmo.options.providers import Provider
from ..queries import query_sources

class Publication(Provider):
    '''Publication Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MaRDI Portal, Wikidata, MathAlgoDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        query_id = 'algorithm/queries/provider_publication.sparql'
        sources = ['mathalgodb', 'mardi', 'wikidata']

        return query_sources(search, query_id, sources)
