from rdmo.options.providers import Provider

from ..utils import query_sources, query_sources_with_user_additions


class ResearchField(Provider):

    search = True
    refresh =True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedResearchFieldWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['field']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 creation = True)
    
class RelatedResearchFieldWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['field']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mardi'])
    
class ResearchProblem(Provider):

    search = True
    refresh =True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedResearchProblemWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['problem']
        
        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 creation = True)
    
class RelatedResearchProblemWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['problem']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mardi'])
    
class MathematicalModel(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []
        
        return query_sources(search)

class RelatedMathematicalModelWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['model']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mardi'])
    
class QuantityOrQuantityKind(Provider):

    search = True
    refresh =True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedQuantityWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['quantity']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mardi'])

class RelatedQuantityKindWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['quantity']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mardi'])
    
class RelatedQuantityOrQuantityKindWithCreation(Provider):

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['quantity']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 creation = True)
    
class MathematicalFormulation(Provider):

    search = True
    refresh =True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)
    
class RelatedMathematicalFormulationWithCreation(Provider):

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['formulation']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 creation = True)
    
class RelatedMathematicalFormulationWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['formulation']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mardi'])

class Task(Provider):

    search = True
    refresh =True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedTaskWithCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['task']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 creation = True)
    
class RelatedTaskWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the queryAttributes
        queryAttributes = ['task']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mardi'])
    
class RelatedModelEntityWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query parameter
        queryAttributes = ['field', 'problem', 'model', 'quantity', 'formulation', 'task']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 sources = ['mardi'])
