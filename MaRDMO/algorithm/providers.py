'''Module containing Providers for the Algorithm Documentation'''

from rdmo.options.providers import Provider

from ..helpers import define_setup
from ..queries import query_sources, query_sources_with_user_additions

class Algorithm(Provider):
    '''Algorithm Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        query_id = 'algorithm/queries/provider_algorithm.sparql'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, query_id, sources)

class RelatedAlgorithmWithoutCreation(Provider):
    '''Algorithm Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            query_attributes = ['algorithm'],
            query_id = 'algorithm/queries/provider_algorithm.sparql',
            sources = ['mathalgodb']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class AlgorithmicProblem(Provider):
    '''Algorithmic Problem Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        query_id = 'algorithm/queries/provider_problem.sparql'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, query_id, sources)

class RelatedAlgorithmicProblemWithCreation(Provider):
    '''Algorithmic Problem Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            creation = True,
            query_attributes = ['problem'],
            query_id = 'algorithm/queries/provider_problem.sparql',
            sources = ['mathalgodb','mardi','wikidata']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class RelatedAlgorithmicProblemWithoutCreation(Provider):
    '''Algorithmic Problem Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []

        setup = define_setup(
            query_attributes = ['problem'],
            query_id = 'algorithm/queries/provider_problem.sparql',
            sources = ['mathalgodb']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class Software(Provider):
    '''Software Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        query_id = 'algorithm/queries/provider_software.sparql'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, query_id, sources)

class RelatedSoftwareWithCreation(Provider):
    '''Software Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            creation = True,
            query_attributes = ['software'],
            query_id = 'algorithm/queries/provider_software.sparql',
            sources = ['mathalgodb','mardi','wikidata']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class Benchmark(Provider):
    '''Benchmark Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        query_id = 'algorithm/queries/provider_benchmark.sparql'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, query_id, sources)

class RelatedBenchmarkWithCreation(Provider):
    '''Benchmark Provider (MaRDI Portal / Wikidata / MathAlgoDB),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            creation = True,
            query_attributes = ['benchmark'],
            query_id = 'algorithm/queries/provider_benchmark.sparql',
            sources = ['mathalgodb','mardi','wikidata']
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )
