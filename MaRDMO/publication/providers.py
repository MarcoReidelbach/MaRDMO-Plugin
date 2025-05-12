from rdmo.options.providers import Provider
from ..utils import query_sources

class Publication(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = 'PU'
        sources = ['mathalgodb', 'mardi', 'wikidata']

        return query_sources(search, queryID, sources)