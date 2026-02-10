'''Module containing Providers for the Algorithm Documentation'''

from rdmo.options.providers import Provider

from ..helpers import define_setup
from ..queries import query_sources, query_sources_with_user_additions

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

        return query_sources(search)

class RelatedAlgorithmWithoutCreation(Provider):
    '''Algorithm Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            query_attributes = ['algorithm'],
            sources = ['mardi']
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

        return query_sources(search)

class RelatedAlgorithmicProblemWithCreation(Provider):
    '''Algorithmic Problem Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            query_attributes = ['problem'],
            creation = True
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

        # Define the query_setup
        setup = define_setup(
            query_attributes = ['problem'],
            sources = ['mardi']
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

        return query_sources(search)

class RelatedBenchmarkWithCreation(Provider):
    '''Benchmark Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            query_attributes = ['benchmark'],
            creation = True
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

        # Define the query_setup
        setup = define_setup(
            query_attributes = ['benchmark', 'software'],
            sources = ['mardi']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )
