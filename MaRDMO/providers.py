from django.utils.translation import gettext_lazy as _

import requests
import os
import json

from rdmo.options.providers import Provider
from rdmo.domain.models import Attribute
from rdmo.options.models import Option

from multiprocessing.pool import ThreadPool

from .config import wikidata_api, mardi_api, BASE_URI
from .sparql import queryProvider
from .utils import query_api, query_sparql, extract_parts

class MaRDIAndWikidataSearch(Provider):
    
    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Function which queries Wikidata and MaRDI KG for user input.'''
        if not search or len(search) < 3:
            return []
    
        # Use a ThreadPool to make concurrent API requests
        pool = ThreadPool(processes=2)
        wikidata_results, mardi_results = pool.map(lambda api_url: query_api(api_url, search), [wikidata_api, mardi_api])

        # Process Results to fit RDMO Provider Output Requirements
        options = [
            process_result(result, 'wikidata') for result in wikidata_results[:10]
        ]
        options += [ 
            process_result(result, 'mardi') for result in mardi_results[:10]
        ]

        # Return unique options (if similar Results returned from MaRDI KG and Wikidata, only keep the MaRDI KG result)
        options = list({option['text']:option for option in options}.values())
        
        return options

class AvailableSoftware(Provider):

    search = True

    SUBJECT_ATTRIBUTES = [
        f'{BASE_URI}domain/SoftwareName',
        f'{BASE_URI}domain/SoftwareDescription'
    ]

    def get_options(self, project, search, user=None, site=None):
        '''Function which queries Wikidata and MaRDI KG for user input.'''
        if not search or len(search) < 3:
            return []

        options = []

        values1 = get_attribute_values(project, get_attribute(self.SUBJECT_ATTRIBUTES[0]))
        values2 = get_attribute_values(project, get_attribute(self.SUBJECT_ATTRIBUTES[1]))

        for v1, v2 in zip(values1, values2):
            if v1.text or v2.text:
                options.append({'id': 'no ID <|> ' + v1.text + ' <|> ' + v2.text, 'text': v1.text + ' (' + v2.text + ')'})

        # Use a ThreadPool to make concurrent API requests
        pool = ThreadPool(processes=2)
        wikidata_results, mardi_results = pool.map(lambda api_url: query_api(api_url, search), [wikidata_api, mardi_api])

        # Process Results to fit RDMO Provider Output Requirements
        options += [
            process_result(result, 'wikidata') for result in wikidata_results[:10]
        ]
        options += [
            process_result(result, 'mardi') for result in mardi_results[:10]
        ]

        # Return unique options (if similar Results returned from MaRDI KG and Wikidata, only keep the MaRDI KG result)
        options = list({option['text']:option for option in options}.values())

        return options

class MaRDISearch(Provider):

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Function which queries MaRDI KG for user input.'''
        if not search or len(search) < 3:
            return []

        mardi_results = query_api(mardi_api, search)

        options = [
            process_result(result, 'mardi') for result in mardi_results[:20]
        ]

        return options

class MSCProvider(Provider):

    path = os.path.join(os.path.dirname(__file__), 'data', 'msc2020.json')

    with open(path, "r") as json_file:
        msc = json.load(json_file)

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Function which get MSC Classification.'''
        if not search or len(search) < 3:
            return []

        options = []

        options = [{'id': self.msc[key]['id'] + ' - ' + key , 'text': f"{key} ({self.msc[key]['id']})"} for key in self.msc if search.lower() in key.lower()]

        return options[:20]

class ProcessorProvider(Provider):

    search = True
    api_url = 'https://en.wikichip.org/w/api.php?' 

    def get_options(self, project, search, user=None, site=None):
        '''Function which get MSC Classification.'''
        if not search or len(search) < 3:
            return []
        
        response = requests.get(self.api_url, params={
            'action': 'opensearch',
            'search': search
            }, headers={'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()
        
        if response[1]:
            options = [{'id': wikichipId + ' <|> ' + wikichipLabel + ' <|> processor', 'text': wikichipLabel} for wikichipId, wikichipLabel in zip(response[-1],response[1])]
        else:
            options = []
    
        return options[:20]


class MathAreaProvider(Provider):
    
    SUBJECT_ATTRIBUTE = f'{BASE_URI}domain/MathematicalSubject'

    def get_options(self, project, search=None, user=None, site=None):
        """
        Function providing the user-defined mathematical areas.
        """
        subject_attribute = get_attribute(self.SUBJECT_ATTRIBUTE)
        if not subject_attribute:
            return []

        options = []
        values = get_attribute_values(project, subject_attribute)

        options = add_options(options, values, 0)

        return options

class EnvironmentProvider(Provider):
    
    SUBJECT_ATTRIBUTES = [
        f'{BASE_URI}domain/SoftwareQID',
        f'{BASE_URI}domain/SoftwareName',
        f'{BASE_URI}domain/InstrumentName'
    ]

    def get_options(self, project, search=None, user=None, site=None):
        """
        Function providing the user-defined environments.
        """
        options = []

        for index, attribute_uri in enumerate(self.SUBJECT_ATTRIBUTES):
            subject_attribute = get_attribute(attribute_uri)
            if not subject_attribute:
                continue

            values = get_attribute_values(project, subject_attribute)

            # Define a lambda function for text processing
            process_text_fn = lambda text: text.split(' <|> ')[1] if ' <|> ' in text else text

            options = add_options(options, values, len(options), process_text_fn=process_text_fn)

        return options

class MethodProvider(Provider):
    
    SUBJECT_ATTRIBUTES = [
        f'{BASE_URI}domain/MethodQID',
        f'{BASE_URI}domain/MethodName'
    ]

    def get_options(self, project, search=None, user=None, site=None):
        """
        Function providing the user-defined methods.
        """
        options = []

        for index, attribute_uri in enumerate(self.SUBJECT_ATTRIBUTES):
            subject_attribute = get_attribute(attribute_uri)
            if not subject_attribute:
                continue

            values = get_attribute_values(project, subject_attribute)

            # Process text differently for each subject_attribute
            if index == 0:
                process_text_fn = lambda text: text.split(' <|> ')[1] if ' <|> ' in text else text
            else:
                process_text_fn = lambda text: text

            options = add_options(options, values, len(options), process_text_fn=process_text_fn)

        return options

class DataProvider(Provider):
    
    SUBJECT_ATTRIBUTES = [
        f'{BASE_URI}domain/DataSetQID',
        f'{BASE_URI}domain/DataSetName',
    ]

    def get_options(self, project, search=None, user=None, site=None):
        """
        Function providing the user-defined input and output data sets.
        """
        options = []

        for index, attribute_uri in enumerate(self.SUBJECT_ATTRIBUTES):
            subject_attribute = get_attribute(attribute_uri)
            if not subject_attribute:
                continue

            values = get_attribute_values(project, subject_attribute)

            if index in (0, 2):  # Split text for zeroth and second attributes
                process_text_fn = lambda text: text.split(' <|> ')[1] if ' <|> ' in text else text
            else:
                process_text_fn = lambda text: text
            options = add_options(options, values, len(options)+10*index, process_text_fn=process_text_fn)
        return options

class SoftwareProvider(Provider):
    
    SUBJECT_ATTRIBUTES = [
        f'{BASE_URI}domain/SoftwareQID',
        f'{BASE_URI}domain/SoftwareName'
    ]

    def get_options(self, project, search=None, user=None, site=None):
        """
        Function providing the user-defined software.
        """
        options = []

        for index, attribute_uri in enumerate(self.SUBJECT_ATTRIBUTES):
            subject_attribute = get_attribute(attribute_uri)
            if not subject_attribute:
                continue

            values = get_attribute_values(project, subject_attribute)

            # Process text differently for each subject_attribute
            if index == 0:
                process_text_fn = lambda text: text.split(' <|> ')[1] if ' <|> ' in text else text
            else:
                process_text_fn = lambda text: text

            options = add_options(options, values, len(options), process_text_fn=process_text_fn)
        return options

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

class MainMathematicalModel(Provider):

    search = True

    def get_options(self, project, search, user=None, site=None):
        '''Queries MathModDB for user input'''
        if not search or len(search) < 3:
            return []

        # Define the sources to query
        queryID = 'MM'
        sources = ['mathmoddb']

        return query_sources(search, queryID, sources)
    
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

class Publication(Provider):

    search = True

    def get_options(self, project, search=None, user=None, site=None):

        options = MathModDBProvider(search,queryProvider['P'])
        
        return options

class GetDetails(Provider):

    search = False
    refresh = True

    def get_options(self, project, search=None, user=None, site=None):

        options = [{'id': '0', 'text': 'MathModDB Knowledge Graph'}, 
                   {'id': '1', 'text': 'MathAlgoDB Knowledge Graph'}, 
                   {'id': '2', 'text': 'MaRDI Portal or Wikidata'},
                   {'id': '3', 'text': 'all available Resources'}]  

        return options      

class WorkflowTask(Provider):

    def get_options(self, project, search=None, user=None, site=None):

        options = []

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/TaskMathModDBID'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/TaskQID'))
        values3 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/TaskName'))

        for value1 in values1:
            if value1.text and value1.text != 'not in MathModDB':
                options.extend([{'id': value1.external_id, 'text': value1.text}])

        for value2 in values2:
            if value2.text:
                Id,label,quote = value2.external_id.split(' <|> ')
                options.extend([{'id': f"{Id} <|> {label}", 'text': f"{label}"}])

        for idx, value3 in enumerate(values3):
            if value3.text:
                options.extend([{'id': f"{idx} <|> {value3.text}", 'text': f"{value3.text}"}])

        return options

class AllEntities(Provider):

    path = os.path.join(os.path.dirname(__file__), 'data', 'mathmoddb.json')

    with open(path, "r") as json_file:
        mathmoddb = json.load(json_file)

    def get_options(self, project, search=None, user=None, site=None):
        options =[]

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/field/id'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/field/name'))
        values3 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/field/description'))
        values4 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/problem/id'))
        values5 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/problem/name'))
        values6 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/problem/description'))
        values7 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/model/id'))
        values8 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/model/name'))
        values9 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/model/description'))
        values10 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/quantity/id'))
        values11 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/quantity/name'))
        values12 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/quantity/description'))
        values13 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/formulation/id'))
        values14 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/formulation/name'))
        values15 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/formulation/description'))
        values16 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/task/id'))
        values17 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/task/name'))
        values18 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/task/description'))
        
        
        for idx, (value1, value2, value3) in enumerate(zip(values1, values2, values3)):
            if value1.text and value1.text != 'not found':
                options.append({'id': value1.external_id, 'text': value1.text})
            else:
                options.append({'id': f"RF{str(idx+1)}",'text': f"{value2.text} ({value3.text}) [user-defined]"})
        
        for idx, (value4, value5, value6) in enumerate(zip(values4, values5, values6)):
            if value4.text and value4.text != 'not found':
                options.append({'id': value4.external_id, 'text': value4.text})
            else:
                options.append({'id': f"RP{str(idx+1)}",'text': f"{value5.text} ({value6.text}) [user-defined]"})
        
        for idx, (value7, value8, value9) in enumerate(zip(values7, values8, values9)):
            if value7.text and value7.text != 'not found':
                options.append({'id': value7.external_id, 'text': value7.text})
            else:
                options.append({'id': f"MM{str(idx+1)}",'text': f"{value8.text} ({value9.text}) [user-defined]"})

        for idx, (value10, value11, value12) in enumerate(zip(values10, values11, values12)):
            if value10.text and value10.text != 'not found':
                options.append({'id': value10.external_id, 'text': value10.text})
            else:
                options.append({'id': f"QQK{str(idx+1)}",'text': f"{value11.text} ({value12.text}) [user-defined]"})

        for idx, (value13, value14, value15) in enumerate(zip(values13, values14, values15)):
            if value13.text and value13.text != 'not found':
                options.append({'id': value13.external_id, 'text': value13.text})
            else:
                options.append({'id': f"MF{str(idx+1)}",'text': f"{value14.text} ({value15.text}) [user-defined]"})

        for idx, (value16, value17, value18) in enumerate(zip(values16, values17, values18)):
            if value16.text and value16.text != 'not found':
                options.append({'id': value16.external_id, 'text': value16.text})
            else:
                options.append({'id': f"T{str(idx+1)}",'text': f"{value17.text} ({value18.text}) [user-defined]"})

        return options

def process_result(result, location):
    '''Function to process the result and return a dictionary with id, text, and description.'''
    return {
         'id': f"{location}:{result['id']}",
         'text': f"{result['display']['label']['value']} ({result['display'].get('description', {}).get('value', 'No Description Provided!')}) [{location}]"
    }

def get_attribute(uri):
    """
    Retrieve attribute object based on URI.
    """
    try:
        return Attribute.objects.get(uri=uri)
    except Attribute.DoesNotExist:
        return None

def get_attribute_values(project, attribute):
    """
    Retrieve values for a given attribute in a project.
    """
    if attribute:
        return project.values.filter(snapshot=None, attribute=attribute)
    return []

def add_options(options, values, start_index, process_text_fn=None):
    """
    Add options to the list based on values.
    """
    for index, value in enumerate(values, start=start_index):
        if value.text or value.external_id:
            if value.external_id:
                text = value.external_id
            else:
                text = value.text
            if process_text_fn:
                text = process_text_fn(text)
            options.append({'id': f'Environment{index}', 'text': text})
    return options

def MathModDBProvider(search, query, notFound=True):
    """
    Dynamic query of MathModDB, results as options for Provider.
    """
    if not search:
        return []

    # Fetch results from the MathModDB knowledge graph
    results = query_sparql(query)
    dic = {}
    options = []

    # Store results in dict
    for result in results:
        if result.get('class',{}).get('value'):
            if result['class']['value'].split('#')[1] == 'Quantity':
                dic.update({f"{result['label']['value']} (Quantity)":{'id':f"{result['answer']['value']} <|> {result['label']['value']} <|> Quantity"}})
            elif result['class']['value'].split('#')[1] == 'QuantityKind':
                dic.update({f"{result['label']['value']} (Quantity Kind)":{'id':f"{result['answer']['value']} <|> {result['label']['value']} <|> QuantityKind"}})
        else:
            dic.update({result['label']['value']:{'id':result['id']['value'], 'quote':result['quote']['value']}})

    # Filter results by user-defined search
    options.extend([{'id': f"mathmoddb:{dic[key]['id']}", 'text': f'{key} ({dic[key]["quote"]}) [mathmoddb]'} for key in dic if search.lower() in key.lower()])

    # Add 'not in MathModDB' option
    if notFound:
        options = [{'id': 'not found', 'text': 'not found'}] + sorted(options, key=lambda option: option['text'])

    return options


def query_sources(search, queryID, sources, notFound=True):
        '''Helper function to query specified sources and process results.'''
        
        source_functions = {
            'wikidata': lambda s: query_api(wikidata_api, s),
            'mardi': lambda s: query_api(mardi_api, s),
            'mathmoddb': lambda s: MathModDBProvider(s, queryProvider[queryID], notFound)
        }

        # Filter only specified sources
        queries = [source_functions[source] for source in sources if source in source_functions]

        # Use ThreadPool to make concurrent API requests
        pool = ThreadPool(processes=len(queries))
        results = pool.map(lambda func: func(search), queries)

        # Unpack results based on available sources
        results_dict = dict(zip(sources, results))

        # Process results to fit RDMO Provider Output Requirements
        options = []
        
        if 'mathmoddb' in results_dict:
            options += results_dict['mathmoddb'][:10]

        if 'mardi' in results_dict:
            options += [process_result(result, 'mardi') for result in results_dict['mardi'][:10]]

        if 'wikidata' in results_dict:
            options += [process_result(result, 'wikidata') for result in results_dict['wikidata'][:10]]

        return options

def query_sources_with_user_additions(search, project, queryID, queryAttribute):
    '''Fetch options from MathModDB, user-defined fields, and other sources.'''

    # Query sources and get the results directly in options
    options = query_sources(search, queryID, ['mathmoddb'], False)

    # Fetch user-defined research fields from the project
    values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{queryAttribute}/id'))
    values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{queryAttribute}/name'))
    values3 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri=f'{BASE_URI}domain/{queryAttribute}/description'))
    
    # Process user-defined research fields
    dic = {}
    for idx, (value1, value2, value3) in enumerate(zip(values1, values2, values3)):
        source = label = description = None
        if value1.text:
            if value1.text == 'not found':
                # User-Defined Cases
                label = value2.text or "No Label Provided!"
                description = value3.text or "No Description Provided!"
                source = 'user-defined'
            elif 'mathmoddb' not in value1.text:
                # ID Cases
                label, description, source = extract_parts(value1.text)
        if source and source != 'mathmoddb':
            dic[f"{label} ({description}) [{source}]"] = {'id': f"user:{idx}"}
            

    # Add the user-defined options to the list, filtered by search
    options.extend([{'id': f"{dic[key]['id']}", 'text': key} for key in dic if search.lower() in key.lower()])

    # Return combined, sorted options
    return sorted(options, key=lambda option: option['text'])

