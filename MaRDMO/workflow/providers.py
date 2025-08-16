from rdmo.options.providers import Provider
from rdmo.domain.models import Attribute

from .sparql import queryProvider

from ..config import BASE_URI, endpoint
from ..getters import get_items, get_data, get_properties, get_questions_workflow
from ..queries import query_sources, query_sources_with_user_additions, query_sparql

class MaRDIAndWikidataSearch(Provider):

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class MainMathematicalModel(Provider):

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'MM'
        sources = ['mardi']

        return query_sources(search, queryID, sources)
    
class Method(Provider):

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
    
class RelatedMethod(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        if not search:
            return []
        
        # Define the query parameter
        queryID = 'AL'
        sources = ['mathalgodb', 'mardi', 'wikidata']
        queryAttributes = ['method']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 queryID = queryID,
                                                 creation = True,
                                                 sources = sources)
    
class WorkflowTask(Provider):

    def get_options(self, project, search=None, user=None, site=None):
        '''Queries MaRDI Portak for Task related to chosen Model'''

        questions = get_questions_workflow()
        options = []
        model_id = ''

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}{questions["Model"]["ID"]["uri"]}'))        
        for value in values:
            model_id = value.external_id

        if model_id:
            _, id_value = model_id.split(':')
            results = query_sparql(queryProvider['RT'].format(id_value, **get_items(), **get_properties()), endpoint['mardi']['sparql'])
            if results:
                if results[0].get('usedBy', {}).get('value'):
                    tasks = results[0]['usedBy']['value'].split(' / ')
                    for task in tasks:
                        id, label, description = task.split(' | ')
                        options.append({'id': id, 'text': f'{label} ({description}) [mardi]'})

        return options
    
class Software(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = 'SO'
        sources = ['mathalgodb', 'mardi', 'wikidata']

        return query_sources(search, queryID, sources)

class RelatedSoftware(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
    
        if not search:
            return []
        
        # Define the query parameter
        queryID = 'SO'
        sources = ['mathalgodb', 'mardi', 'wikidata']
        queryAttributes = ['software']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 queryID = queryID,
                                                 creation = True,
                                                 sources = sources)

class Hardware(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)
    
class Instrument(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)
    
class DataSet(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)
    
class RelatedInstrument(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
    
        if not search:
            return []
        
        # Define the query parameter
        queryAttributes = ['instrument']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes,
                                                 creation = True)
    
class RelatedDataSet(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):
    
        if not search:
            return []
        
        # Define the query parameter
        queryAttributes = ['data-set']

        return query_sources_with_user_additions(search = search, 
                                                 project = project, 
                                                 queryAttributes = queryAttributes, 
                                                 creation = True)
            
class ProcessStep(Provider):

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        return query_sources(search, queryID, sources)
    
class Discipline(Provider):

    msc = get_data('data/msc2020.json')

    search = True
    refresh = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MaRDI Portal and Wikidata for user input'''
        if not search or len(search) < 3:
            return []

        # Define the query parameter
        queryID = ''
        sources = ['mardi', 'wikidata']

        # Discipline from Knowledge Graphs
        options = query_sources(search, queryID, sources, False)

        # Mathematical Subjects
        options.extend([{'id': f"msc:{self.msc[key]['id']}", 'text': f"{key} ({self.msc[key]['quote']}) [msc]"} for key in self.msc if search.lower() in key.lower()])

        return sorted(options, key=lambda option: option['text'].lower())[:30]
