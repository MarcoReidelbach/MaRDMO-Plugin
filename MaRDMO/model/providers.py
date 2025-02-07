from rdmo.options.providers import Provider

from ..utils import query_sources, query_sources_with_user_additions

class ResearchField(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = 'RF'
        sources = ['mathmoddb', 'mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class RelatedResearchField(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'RF'
        queryAttribute = 'field'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute)
    
class ResearchProblem(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'RP'
        sources = ['mathmoddb', 'mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class RelatedResearchProblem(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'RP'
        queryAttribute = 'problem'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute)
    
class MathematicalModel(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'MM'
        sources = ['mathmoddb','mardi','wikidata']

        return query_sources(search, queryID, sources)

class RelatedMathematicalModel(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'MM'
        queryAttribute = 'model'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute)
    
class QuantityOrQuantityKind(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'QQK'
        sources = ['mathmoddb', 'mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class RelatedQuantity(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'Q'
        queryAttribute = 'quantity'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute)

class RelatedQuantityKind(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'QK'
        queryAttribute = 'quantity'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute)
    
class RelatedQuantityOrQuantityKind(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'QQK'
        queryAttribute = 'quantity'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute)
    
class MathematicalFormulation(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'MF'
        sources = ['mathmoddb','mardi','wikidata']

        return query_sources(search, queryID, sources)
    
class RelatedMathematicalFormulation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'MF'
        queryAttribute = 'formulation'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute)
    
class Task(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'T'
        sources = ['mathmoddb','mardi','wikidata']

        return query_sources(search, queryID, sources)

class RelatedTask(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'T'
        queryAttribute = 'task'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute)
