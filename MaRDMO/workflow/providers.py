'''Module containing Providers for the Documentation of Interdisciplinary Workflows'''
# pylint: disable=too-few-public-methods  # Provider subclasses only need get_options

from rdmo.options.providers import Provider
from rdmo.domain.models import Attribute

from ..constants import BASE_URI
from ..getters import get_items, get_data, get_properties, get_questions, get_sparql_query, get_url
from ..helpers import define_setup
from ..queries import query_sources, query_sources_with_user_additions, query_sparql

_ITEMS = get_items()


class MaRDIAndWikidataSearch(Provider):
    '''General Provider (MaRDI Portal / Wikidata),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search
        )


class MainMathematicalModel(Provider):
    '''Main Mathematical Model Provider (MaRDI Portal),
       No User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search,
            item_class = _ITEMS['mathematical model'],
            sources = ['mardi'],
        )

class Method(Provider):
    '''Method Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search,
            item_class = [
                _ITEMS['method'],
                _ITEMS['algorithm']
            ]
        )

class RelatedMethod(Provider):
    '''Method Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search:
            return []

        setup = define_setup(
            query_attributes = ['method'],
            creation = True,
            item_class = [
                _ITEMS['method'],
                _ITEMS['algorithm']
            ]
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class WorkflowTask(Provider):
    '''Task Provider (MaRDI Portal),
       User Creation, No Refresh Upon Selection
    '''

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MaRDI Portal for Task related to chosen Model'''

        questions = get_questions('workflow')
        options = []
        model_id = ''

        values = project.values.filter(
            snapshot = None,
            attribute = Attribute.objects.get(
                uri = f'{BASE_URI}{questions["Model"]["ID"]["uri"]}'
            )
        )

        for value in values:
            model_id = value.external_id

        if not model_id:
            return options

        _, id_value = model_id.split(':')

        query = get_sparql_query('workflow/queries/task_mardi.sparql').format(
            id_value,
            **get_items(),
            **get_properties()
        )

        results = query_sparql(
            query,
            get_url('mardi', 'sparql')
        )

        if not results:
            return options

        if results[0].get('usedBy', {}).get('value'):
            tasks = results[0]['usedBy']['value'].split(' <|> ')
            for task in tasks:
                identifier, label, description = task.split(' || ')
                options.append(
                    {
                        'id': identifier,
                        'text': f'{label} ({description}) [mardi]'
                    }
                )

        return options

class Hardware(Provider):
    '''Hardware Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search,
            item_class = _ITEMS['computer hardware'],
        )

class Instrument(Provider):
    '''Instrument Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search,
            item_class = _ITEMS['research tool'],
        )

class DataSet(Provider):
    '''Data Set Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search,
            item_class = _ITEMS['data set'],
        )

class RelatedInstrument(Provider):
    '''Instrument Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search:
            return []

        setup = define_setup(
            creation = True,
            query_attributes = ['instrument'],
            item_class = _ITEMS['research tool'],
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class RelatedDataSet(Provider):
    '''Data Set Provider (MaRDI Portal / Wikidata),
       User Creation, No Refresh Upon Selection
    '''

    search = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search:
            return []

        setup = define_setup(
            creation = True,
            query_attributes = ['data-set'],
            item_class = _ITEMS['data set'],
        )

        return query_sources_with_user_additions(
            search = search,
            project = project,
            setup = setup
        )

class ProcessStep(Provider):
    '''Process Step Provider (MaRDI Portal / Wikidata),
       No User Creation, Refresh Upon Selection
    '''

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external source for user input'''
        if not search or len(search) < 3:
            return []

        return query_sources(
            search = search,
            item_class = _ITEMS['process step'],
        )

class Discipline(Provider):
    '''Discipline Provider (MaRDI Portal / Wikidata / MSC),
       No User Creation, Refresh Upon Selection
    '''

    msc = get_data('data/msc2020.json')

    search = True
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries external sources for user input'''
        if not search or len(search) < 3:
            return []

        # Discipline from Knowledge Graphs
        options = query_sources(
            search = search,
            item_class = _ITEMS['academic discipline'],
            not_found = False,
        )

        # Mathematical Subjects
        options.extend(
            [
                {
                    'id': f"msc:{self.msc[key]['id']}",
                    'text': f"{key} ({self.msc[key]['quote']}) [msc]"
                }
                for key in self.msc if search.lower() in key.lower()
            ]
        )

        return sorted(options, key=lambda option: option['text'].lower())[:30]
