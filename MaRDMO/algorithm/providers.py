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
    
class RelatedAlgorithmWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query parameter
        queryID = 'AL'
        queryAttributes = ['algorithm']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryID = queryID,
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mathalgodb'])
    
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
    
class RelatedAlgorithmicProblemWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query parameter
        queryID = 'AP'
        queryAttributes = ['problem']

        return query_sources_with_user_additions(search = search, 
                                                 project = project,
                                                 queryID = queryID, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mathalgodb','mardi','wikidata'],
                                                 creation = True)
    
class RelatedAlgorithmicProblemWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query parameter
        queryID = 'AP'
        queryAttributes = ['problem']

        return query_sources_with_user_additions(search = search, 
                                                 project = project,
                                                 queryID = queryID, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mathalgodb'])
    
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
    
class RelatedSoftwareWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query parameter
        queryID = 'SO'
        queryAttributes = ['software']

        return query_sources_with_user_additions(search = search, 
                                                 project = project,
                                                 queryID = queryID, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mathalgodb','mardi','wikidata'],
                                                 creation = True)
        
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
    
class RelatedBenchmarkWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query parameter
        queryID = 'BE'
        queryAttributes = ['benchmark']

        return query_sources_with_user_additions(search = search, 
                                                 project = project,
                                                 queryID = queryID, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mathalgodb','mardi','wikidata'],
                                                 creation = True)
    