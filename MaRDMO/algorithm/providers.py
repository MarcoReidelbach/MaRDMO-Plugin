from rdmo.options.providers import Provider

from ..utils import query_sources, query_sources_with_user_additions

class Algorithm(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'AL'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, queryID, sources)
    
class RelatedAlgorithm(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'AL'
        queryAttribute = 'algorithm'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, ['mathalgodb'])
    
class AlgorithmicProblem(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'AP'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, queryID, sources)
    
class RelatedAlgorithmicProblem(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'AP'
        queryAttribute = 'problem'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, ['mathalgodb'])
    
class Software(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'SO'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, queryID, sources)
    
class RelatedSoftware(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'SO'
        queryAttribute = 'software'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, ['mathalgodb'])
    
class Benchmark(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'BE'
        sources = ['mathalgodb','mardi','wikidata']

        return query_sources(search, queryID, sources)
    
class RelatedBenchmark(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'BE'
        queryAttribute = 'benchmark'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, ['mathalgodb'])
    
