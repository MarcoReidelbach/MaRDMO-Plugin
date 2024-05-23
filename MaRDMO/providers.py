import requests
import itertools
import re, os
import json

from rdmo.options.providers import Provider
from rdmo.domain.models import Attribute
from multiprocessing.pool import ThreadPool

from .config import *

class WikidataSearch(Provider):
    
    search = True

    def get_options(self, project, search):
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
        'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_02',
        'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_03'
    ]

    def get_options(self, project, search):
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

class ComponentSearch(Provider):

    search = True

    def get_options(self, project, search):
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

    def get_options(self, project, search):
        '''Function which get MSC Classification.'''
        if not search or len(search) < 3:
            return []

        options = []

        options = [{'id': self.msc[key]['id'] + ' - ' + key , 'text': key} for key in self.msc if search.lower() in key.lower()]

        return options[:20]

class ProcessorProvider(Provider):

    search = True
    api_url = 'https://en.wikichip.org/w/api.php?' 

    def get_options(self, project, search):
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
    
    SUBJECT_ATTRIBUTE = 'http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_00'

    def get_options(self, project, search=None):
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
        'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_01',
        'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_02',
        'http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_02'
    ]

    def get_options(self, project, search=None):
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
        'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_01',
        'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_02'
    ]

    def get_options(self, project, search=None):
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
        'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_00',
        'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_01',
    ]

    def get_options(self, project, search=None):
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

            options = add_options(options, values, len(options), process_text_fn=process_text_fn)

        return options

class SoftwareProvider(Provider):
    
    SUBJECT_ATTRIBUTES = [
        'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_01',
        'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_02'
    ]

    def get_options(self, project, search=None):
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

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#ResearchField> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        options = [{'id':'not in MathModDB','text':'not in MathModDB'}]

        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options

class Publication(Provider):

    search = True

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#Publication> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        options = [{'id':'not in MathModDB','text':'not in MathModDB'}]

        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options

class ResearchFieldRelations(Provider):

    search = True

    def get_options(self, project, search=None):
        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#ResearchField> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                          params = {'format': 'json', 'query': query},
                          headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']


        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_0/Question_3'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_0/Question_0'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':value1.external_id}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':str(idx)}})

        
        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])
        
        return options

class ResearchProblem(Provider):

    search = True

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#ResearchProblem> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        options = [{'id':'not in MathModDB','text':'not in MathModDB'}]

        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options

class ResearchProblemRelations(Provider):

    search = True

    def get_options(self, project, search=None):
        if not search or len(search) < 3:
            return []
        
        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#ResearchProblem> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                          params = {'format': 'json', 'query': query},
                          headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']


        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_1/Question_5'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_1/Question_0'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':value1.external_id}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':str(idx)}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options

class ResearchProblemRelations2(Provider):

    def get_options(self, project, search=None):

        dic = {}

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_1/Question_5'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_1/Question_0'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':value1.external_id}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':str(idx)}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic])

        return options


class ResearchFieldUser(Provider):

        def get_options(self, project, search=None):
        
            dic = {}
    
            values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_0/Question_3'))
            values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_0/Question_0'))

            for idx, value1 in enumerate(values1):
                if value1.text:
                    dic.update({value1.text:{'id':value1.external_id}})
            for idx, value2 in enumerate(values2):
                if value2.text:
                    dic.update({value2.text:{'id':str(idx)}})

            options = []
            options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key} for key in dic])

            return options

class MathematicalModel(Provider):

    search = True

    def get_options(self, project, search):
        
        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#MathematicalModel> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        options = [{'id':'not in MathModDB','text':'not in MathModDB'}]

        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])
        
        return options

class MathematicalModelAdditional(Provider):

    search = True

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#MathematicalModel> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options


class MathematicalModelRelation(Provider):

    search = True

    def get_options(self, project, search=None):
        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#MathematicalModel> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                          params = {'format': 'json', 'query': query},
                          headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']


        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0a'))
        values3 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_01'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':value1.external_id}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':str(idx)}})
        for idx, value3 in enumerate(values3):
            if value3.text:
                dic.update({value3.text:{'id':str(idx)}})


        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options

class MathematicalModelRelation2(Provider):

    def get_options(self, project, search=None):

        dic = {}

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0a'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_01'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':str(idx)}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':str(idx)}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic])

        return options


class Quantity(Provider):

    search = True

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#Quantity> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req = requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                          params = {'format': 'json', 'query': query},
                          headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        options = [{'id':'not in MathModDB','text':'not in MathModDB'}]

        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options

class QuantityKind(Provider):

    search = True

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#QuantityKind> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req = requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                          params = {'format': 'json', 'query': query},
                          headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_6'))

        for idx, value in enumerate(values):
            if value.text:
                dic.update({value.text:{'id':str(idx)}})

        options = [{'id':'not in MathModDB','text':'not in MathModDB'}]

        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options


class QuantityRelations(Provider):

    search = True

    def get_options(self, project, search=None):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#Quantity> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                          params = {'format': 'json', 'query': query},
                          headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        
        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_5'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':value1.external_id}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':str(idx)}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options

class QuantityKindRelations(Provider):

    search = True

    def get_options(self, project, search=None):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#QuantityKind> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                          params = {'format': 'json', 'query': query},
                          headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']


        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_6'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_7'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':value1.external_id}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':str(idx)}})
        
        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options


class MathematicalFormulation(Provider):

    search = True

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#MathematicalFormulation> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options


class MathematicalFormulation2(Provider):

    search = True

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>  
                        SELECT DISTINCT ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)  
                        WHERE { 
                               ?answer a <https://mardi4nfdi.de/mathmoddb#MathematicalFormulation> .
                               ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                               FILTER (lang(?l) = 'en')
                               }
                        GROUP BY ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value']}})

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_5/Question_0a'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':str(idx)}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options

class MathematicalFormulation3(Provider):

    def get_options(self, project, search=None):

        dic = {}

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_5/Question_0a'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_5/Question_0'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':str(idx)}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':value2.external_id}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic])

        return options

class QuantityAll(Provider):

    def get_options(self, project, search=None):

        dic = {}

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_07'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_5'))
        values3 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_0'))

        for idx, value1 in enumerate(values1):
            if value1.text and value1.text != 'not in MathModDB':
                dic.update({value1.text:{'id':value1.external_id}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':value2.external_id}})
        for idx, value3 in enumerate(values3):
            if value3.text:
                dic.update({value2.text:{'id':str(idx)}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key} for key in dic])

        return options

class MathematicalTask(Provider):

    search = True

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>
                   SELECT DISTINCT ?subclass ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)
                   WHERE {
                          ?subclass <http://www.w3.org/2000/01/rdf-schema#subClassOf> <https://mardi4nfdi.de/mathmoddb#Task> .
                          ?answer a ?subclass .
                          ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                          FILTER (lang(?l) = 'en')
                         }
                   GROUP BY ?subclass ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value'] + ' <ID|SU> ' + r['subclass']['value']}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])
    
        return options

class MathematicalTask2(Provider):

    search = True

    def get_options(self, project, search):

        if not search or len(search) < 3:
            return []

        query = '''PREFIX : <https://mardi4nfdi.de/mathmoddb>
                   SELECT DISTINCT ?subclass ?answer (GROUP_CONCAT(DISTINCT(?l); SEPARATOR=" / ") AS ?label)
                   WHERE {
                          ?subclass <http://www.w3.org/2000/01/rdf-schema#subClassOf> <https://mardi4nfdi.de/mathmoddb#Task> .
                          ?answer a ?subclass .
                          ?answer <http://www.w3.org/2000/01/rdf-schema#label> ?l .
                          FILTER (lang(?l) = 'en')
                         }
                   GROUP BY ?subclass ?answer ?label'''

        req=requests.get('https://sparql.ta4.m1.mardi.ovh/mathalgodb/query',
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        dic = {}

        for r in req:
            dic.update({r['label']['value']:{'id':r['answer']['value'] + ' <ID|SU> ' + r['subclass']['value']}})

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_6/Question_0a'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_6/Question_0'))

        for idx, value1 in enumerate(values1):
            if value1.text:
                dic.update({value1.text:{'id':str(idx)}})
        for idx, value2 in enumerate(values2):
            if value2.text:
                dic.update({value2.text:{'id':value2.external_id}})

        options = []
        options.extend([{'id': dic[key]['id'] + ' <|> ' + key, 'text': key } for key in dic if search.lower() in key.lower()])

        return options

class AllEntities(Provider):

    def get_options(self, project, search=None):
        options =[]

        values1 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_04'))
        values2 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_0/Question_3'))
        values3 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_0/Question_0'))
        values4 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_05'))
        values5 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_1/Question_5'))
        values6 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_1/Question_0'))
        values7 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_01'))
        values8 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0'))
        values9 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0a'))
        values10 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_07'))
        values11 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_5'))
        values12 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_0'))
        values13 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_4'))
        values14 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_6'))
        values15 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_7'))
        values16 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_5/Question_0'))
        values17 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_5/Question_0a'))
        values18 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_6/Question_0'))
        values19 = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_6/Question_0a'))

        for idx, value1 in enumerate(values1):
            if value1.text and value1.text != 'not in MathModDB':
                options.append({'id':value1.external_id,'text':value1.text + ' (Research Field)'})
        for idx, value2 in enumerate(values2):
            if value2.text:
                options.append({'id':value2.external_id,'text':value2.text + ' (Research Field)'})
        for idx, value3 in enumerate(values3):
            if value3.text:
                options.append({'id':'RF'+str(idx),'text':value3.text + ' (Research Field)'})
        for idx, value4 in enumerate(values4):
            if value4.text and value4.text != 'not in MathModDB':
                options.append({'id':value4.external_id,'text':value4.text + ' (Research Problem)'})
        for idx, value5 in enumerate(values5):
            if value5.text:
                options.append({'id':value5.external_id,'text':value5.text + ' (Research Problem)'})
        for idx, value6 in enumerate(values6):
            if value6.text:
                options.append({'id':'RP'+str(idx),'text':value6.text + ' (Research Problem)'})
        for idx, value7 in enumerate(values7):
            if value7.text:
                options.append({'id':'MMa'+str(idx),'text':value7.text + ' (Mathematical Model)'})
        for idx, value8 in enumerate(values8):
            if value8.text:
                options.append({'id':value8.external_id,'text':value8.text + ' (Mathematical Model)'})
        for idx, value9 in enumerate(values9):
            if value9.text:
                options.append({'id':'MMb'+str(idx),'text':value9.text + ' (Mathematical Model)'})
        for idx, value10 in enumerate(values10):
            if value10.text and value10.text != 'not in MathModDB':
                options.append({'id':value10.external_id,'text':value10.text + ' (Quantity)'})
        for idx, value11 in enumerate(values11):
            if value11.text:
                options.append({'id':value11.external_id,'text':value11.text + ' (Quantity)'})
        for idx, value12 in enumerate(values12):
            if value12.text:
                options.append({'id':'Q'+str(idx),'text':value12.text + ' (Quantity)'})
        for idx, value13 in enumerate(values13):
            if value13.text and value13.text != 'not in MathModDB':
                options.append({'id':value13.external_id,'text':value13.text + ' (Quantity Kind)'})
        for idx, value14 in enumerate(values14):
            if value14.text:
                options.append({'id':value14.external_id,'text':value14.text + ' (Quantity Kind)'})
        for idx, value15 in enumerate(values15):
            if value15.text:
                options.append({'id':'QK'+str(idx),'text':value15.text + ' (Quantity Kind)'})
        for idx, value16 in enumerate(values16):
            if value16.text:
                options.append({'id':value16.external_id,'text':value16.text + ' (Mathematical Formulation)'})
        for idx, value17 in enumerate(values17):
            if value17.text:
                options.append({'id':'MF'+str(idx),'text':value17.text + ' (Mathematical Formulation)'})
        for idx, value18 in enumerate(values18):
            if value18.text:
                options.append({'id':value18.external_id,'text':value18.text + ' (Task)'})
        for idx, value19 in enumerate(values19):
            if value19.text:
                options.append({'id':'MF'+str(idx),'text':value19.text + ' (Task)'})

        return options


def query_api(api_url, search_term):
    '''Function to query an API and return the JSON response.'''
    response = requests.get(api_url, params={
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'en',
        'type': 'item',
        'limit': 10,
        'search': search_term
    }, headers={'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'})
    return response.json().get('search', [])

def process_result(result, location):
    '''Function to process the result and return a dictionary with id, text, and description.'''
    try:
        description = result['display']['description']['value']
    except (KeyError, TypeError):
        description = 'No Description Provided!'
    return {
         'id': f"{location}:{result['id']} <|> {result['display']['label']['value']} <|> {description}",
         'text': f"{result['display']['label']['value']} ({description})"
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

def MathModDB_request(item_pref, prop_pref, item):
    """
    Retrieve Entity from MathModDB Classes.
    """
    query=f'''PREFIX wdt:{prop_pref} 
              PREFIX wd:{item_pref} 
              SELECT ?qid ?label 
              WHERE {{?id wdt:P4 wd:{item};
                          rdfs:label ?label.
              BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).}}'''

    responses = requests.get(mardi_endpoint,
                             params = {'format': 'json', 'query': query},
                             headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json().get('results', {}).get('bindings', '')

    return responses
