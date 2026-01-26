'''Module containing Providers for the Model Documentation'''

from rdmo.options.providers import Provider

from ..helpers import define_setup
from ..queries import query_sources, query_sources_with_user_additions

class Formula(Provider):
    '''Formula Provider for all sorts of Latex Math.
       Future Potential:
          - render Latex Math while entered
          - definitive safe to automatically extract elements
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Returns user input'''
        return [{'id': 'formula', 'text': search}]

class ResearchField(Provider):
    '''Research Field Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedResearchFieldWithCreation(Provider):
    '''Research Field Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
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
    '''Research Field Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
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
    '''Research Problem Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedResearchProblemWithCreation(Provider):
    '''Research Problem Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
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
    '''Research Problem Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
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
    '''Mathematical Model Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedMathematicalModelWithoutCreation(Provider):
    '''Mathematical Model Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
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
    '''Quantity [Kind] Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedQuantityWithoutCreation(Provider):
    '''Quantity Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
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
    '''Quantity Kind Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
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
    '''Quantity [Kind] Provider (MaRDI Portal / Wikidata),
       User Creation, Refresh Upon Selection
    '''

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
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
    '''Mathematical Formulation Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedMathematicalFormulationWithCreation(Provider):
    '''Mathematical Formulation Provider (MaRDI Portal / Wikidata),
       User Creation, Refresh Upon Selection
    '''

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
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
    '''Mathematical Formulation Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
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
    '''Task Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh =True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(search)

class RelatedTaskWithCreation(Provider):
    '''Task Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
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
    '''Task Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
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
    '''Research Field, Research Problem, Mathematical Model,
       Mathematical Formulation, Quantity [Kind], Task Provider 
       (MaRDI Portal / Wikidata), No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MathModDB for user input'''
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
