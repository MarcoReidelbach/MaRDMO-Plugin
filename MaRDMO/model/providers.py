from rdmo.options.providers import Provider

from .. helpers import define_setup
from ..queries import query_sources, query_sources_with_user_additions


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
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['field'],
            creation = True
        )
 
        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
    
class RelatedResearchFieldWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['field'],
            sources = ['mardi']
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
    
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
    
class RelatedResearchProblemWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

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
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['model'],
            sources = ['mardi']
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
    
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
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['quantity'],
            sources = ['mardi']
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )

class RelatedQuantityKindWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['quantity'],
            sources = ['mardi']
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
    
class RelatedQuantityOrQuantityKindWithCreation(Provider):

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['quantity'],
            creation = True
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
    
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
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['formulation'],
            creation = True
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
    
class RelatedMathematicalFormulationWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['formulation'],
            sources = ['mardi']
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )

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
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['task'],
            creation = True
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
    
class RelatedTaskWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []
        
        # Define the query_setup
        setup = define_setup(
            query_attributes = ['task'],
            sources = ['mardi']
        )

        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
    
class RelatedModelEntityWithoutCreation(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search or len(search) < 3:
            return []

        # Define the query_setup
        setup = define_setup(
            query_attributes = ['field', 'problem', 'model', 'quantity', 'formulation', 'task'],
            sources = ['mardi']
        )
        
        return query_sources_with_user_additions(
            search = search, 
            project = project, 
            setup = setup
        )
