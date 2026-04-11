'''Module containing Providers for the Model Documentation'''
# pylint: disable=too-few-public-methods  # Provider subclasses only need get_options

from rdmo.options.providers import Provider

from ..getters import get_items
from ..helpers import define_setup
from ..queries import query_sources, query_sources_with_user_additions

_ITEMS = get_items()

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

        return query_sources(
            search = search,
            item_class = [
                _ITEMS['academic discipline']
            ]
        )

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
            creation = True,
            item_class = _ITEMS['academic discipline']
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
            sources = ['mardi'],
            item_class = _ITEMS['academic discipline']
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

        return query_sources(
            search = search,
            item_class = _ITEMS['research problem']
        )

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
            creation = True,
            item_class = _ITEMS['research problem']
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
            sources = ['mardi'],
            item_class = _ITEMS['research problem']
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
        

        return query_sources(
            search = search,
            item_class = _ITEMS['mathematical model']
        )

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
            sources = ['mardi'],
            item_class = _ITEMS['mathematical model']
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


        return query_sources(
            search = search,
            item_class = [
                _ITEMS['quantity'],
                _ITEMS['kind of quantity']
            ]
        )

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
            sources = ['mardi'],
            item_class = _ITEMS['quantity']
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
            sources = ['mardi'],
            item_class = _ITEMS['kind of quantity']
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
            creation = True,
            item_class = [
                _ITEMS['quantity'],
                _ITEMS['kind of quantity']
            ]
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


        return query_sources(
            search = search,
            item_class = _ITEMS['mathematical expression']
        )

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
            creation = True,
            item_class = _ITEMS['mathematical expression']
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
            sources = ['mardi'],
            item_class = _ITEMS['mathematical expression']
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


        return query_sources(
            search = search,
            item_class = _ITEMS['computational task']
        )

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
            creation = True,
            item_class = _ITEMS['computational task']
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
            sources = ['mardi'],
            item_class = _ITEMS['computational task']
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
            sources = ['mardi'],
            item_class = [
                _ITEMS['academic discipline'],
                _ITEMS['research problem'],
                _ITEMS['mathematical model'],
                _ITEMS['quantity'],
                _ITEMS['kind of quantity'],
                _ITEMS['mathematical expression'],
                _ITEMS['computational task']
            ]
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )
