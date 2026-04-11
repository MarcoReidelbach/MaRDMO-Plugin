'''Module containing general Providers for the Documentation'''
# pylint: disable=too-few-public-methods  # Provider subclasses only need get_options

from rdmo.options.providers import Provider

from .getters import get_items
from .helpers import define_setup
from .queries import query_sources, query_sources_with_user_additions

_ITEMS = get_items()


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

        return query_sources(
            search = search,
            item_class = _ITEMS['software'],
        )

class RelatedSoftwareWithCreation(Provider):
    '''Software Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        setup = define_setup(
            query_attributes = ['software'],
            creation = True,
            item_class = _ITEMS['software'],
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )
