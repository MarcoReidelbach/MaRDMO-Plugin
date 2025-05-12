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
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class RelatedResearchFieldWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'RF'
        sources = ['mardi','wikidata']
        queryAttribute = 'field'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, True)
    
class RelatedResearchFieldWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'RF'
        sources = ['mardi','wikidata']
        queryAttribute = 'field'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, False)
    
class ResearchProblem(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = 'RP'
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class RelatedResearchProblemWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'RP'
        sources = ['mardi','wikidata']
        queryAttribute = 'problem'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, True)
    
class RelatedResearchProblemWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'RP'
        sources = ['mardi','wikidata']
        queryAttribute = 'problem'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, False)
    
class MathematicalModel(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'MM'
        sources = ['mardi','wikidata']

        return query_sources(search, queryID, sources)

class RelatedMathematicalModelWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'MM'
        sources = ['mardi','wikidata']
        queryAttribute = 'model'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, False)
    
class QuantityOrQuantityKind(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'QQK'
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class RelatedQuantityWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'Q'
        sources = ['mardi', 'wikidata']
        queryAttribute = 'quantity'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, False)

class RelatedQuantityKindWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'QK'
        sources = ['mardi', 'wikidata']
        queryAttribute = 'quantity'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, False)
    
class RelatedQuantityOrQuantityKindWithCreation(Provider):

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'QQK'
        sources = ['mardi','wikidata']
        queryAttribute = 'quantity'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, True)
    
class MathematicalFormulation(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'MF'
        sources = ['mardi','wikidata']

        return query_sources(search, queryID, sources)
    
class RelatedMathematicalFormulationWithCreation(Provider):

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'MF'
        sources = ['mardi','wikidata']
        queryAttribute = 'formulation'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, True)
    
class RelatedMathematicalFormulationWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'MF'
        sources = ['mardi','wikidata']
        queryAttribute = 'formulation'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, False)

class Task(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'T'
        sources = ['mardi','wikidata']

        return query_sources(search, queryID, sources)

class RelatedTaskWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'T'
        sources = ['mardi','wikidata']
        queryAttribute = 'task'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, True)
    
class RelatedTaskWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'T'
        sources = ['mardi','wikidata']
        queryAttribute = 'task'

        return query_sources_with_user_additions(search, project, queryID, queryAttribute, sources, False)
