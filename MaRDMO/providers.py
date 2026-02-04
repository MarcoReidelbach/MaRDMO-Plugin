'''Module containing general Providers for the Documentation'''

from rdmo.options.providers import Provider

from .helpers import define_setup
from .queries import query_sources, query_sources_with_user_additions

class Software(Provider):
    '''Software Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)
    
class RelatedSoftwareWithCreation(Provider):
    '''Software Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            query_attributes = ['software'],
            creation = True
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )
