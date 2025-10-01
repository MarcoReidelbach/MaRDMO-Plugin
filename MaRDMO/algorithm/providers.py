from rdmo.options.providers import Provider

from ..helpers import define_setup
from ..queries import query_sources, query_sources_with_user_additions

class Algorithm(Provider):

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        query_id = 'AL'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, query_id, sources)
    
class RelatedAlgorithmWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            query_attributes = ['algorithm'],
            query_id = 'AL',
            sources = ['mathalgodb']
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
    
class AlgorithmicProblem(Provider):

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        query_id = 'AP'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, query_id, sources)
    
class RelatedAlgorithmicProblemWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query_setup
        setup = define_setup(
            creation = True,
            query_attributes = ['problem'],
            query_id = 'AP',
            sources = ['mathalgodb','mardi','wikidata']
        )
        
        return query_sources_with_user_additions(
            search = search, 
            project = project,
            setup = setup
        )
    
class RelatedAlgorithmicProblemWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        setup = define_setup(
            query_attributes = ['problem'],
            query_id = 'AP',
            sources = ['mathalgodb']
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project,
            setup = setup
        )
    
class Software(Provider):

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        query_id = 'SO'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, query_id, sources)
    
class RelatedSoftwareWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query_setup
        setup = define_setup(
            creation = True,
            query_attributes = ['software'],
            query_id = 'SO',
            sources = ['mathalgodb','mardi','wikidata']
        )
        
        return query_sources_with_user_additions(
            search = search, 
            project = project,
            setup = setup
        )
        
class Benchmark(Provider):

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        query_id = 'BE'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, query_id, sources)
    
class RelatedBenchmarkWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query_setup
        setup = define_setup(
            creation = True,
            query_attributes = ['benchmark'],
            query_id = 'BE',
            sources = ['mathalgodb','mardi','wikidata']
        )
        
        return query_sources_with_user_additions(
            search = search, 
            project = project,
            setup = setup
        )
