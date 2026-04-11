'''Module containing Providers for the Publication Documentation'''
# pylint: disable=too-few-public-methods  # Provider subclasses only need get_options

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

        return query_sources(search)
