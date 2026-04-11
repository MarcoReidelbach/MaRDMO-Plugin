'''Module containing Providers for the Algorithm Documentation'''
# pylint: disable=too-few-public-methods  # Provider subclasses only need get_options

from rdmo.options.providers import Provider

from ..getters import get_items
from ..helpers import define_setup
from ..queries import query_sources, query_sources_with_user_additions

_ITEMS = get_items()


class Algorithm(Provider):
    '''Algorithm Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search,
            item_class = _ITEMS['algorithm']
        )

class RelatedAlgorithmWithoutCreation(Provider):
    '''Algorithm Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        setup = define_setup(
            query_attributes = ['algorithm'],
            sources = ['mardi'],
            item_class = _ITEMS['algorithm']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class AlgorithmicProblem(Provider):
    '''Algorithmic Problem Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search,
            item_class = _ITEMS['algorithmic task']
        )

class RelatedAlgorithmicProblemWithCreation(Provider):
    '''Algorithmic Problem Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        setup = define_setup(
            query_attributes = ['problem'],
            creation = True,
            item_class = _ITEMS['algorithmic task']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class RelatedAlgorithmicProblemWithoutCreation(Provider):
    '''Algorithmic Problem Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        setup = define_setup(
            query_attributes = ['problem'],
            sources = ['mardi'],
            item_class = _ITEMS['algorithmic task']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class Benchmark(Provider):
    '''Benchmark Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search,
            item_class = _ITEMS['benchmark']
        )

class RelatedBenchmarkWithCreation(Provider):
    '''Benchmark Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        setup = define_setup(
            query_attributes = ['benchmark'],
            creation = True,
            item_class = _ITEMS['benchmark']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class RelatedBenchmarkOrSoftwareWithoutCreation(Provider):
    '''Benchmark, Software Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        setup = define_setup(
            query_attributes = ['benchmark', 'software'],
            sources = ['mardi'],
            item_class = [
                _ITEMS['benchmark'],
                _ITEMS['software']
            ]
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )
