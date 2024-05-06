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
       
        options = [ 
            process_result(result, 'mardi') for result in mardi_results[:10]
        ]
        options += [
            process_result(result, 'wikidata') for result in wikidata_results[:10]
        ]
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
   
    def get_options(self, project, search=None):
        """
        Function providing Research Fields from MathModDB.
        """

        responses = MathModDB_request(wd, wdt, 'Q266')

        options=[{'id':'default','text':'not in MathModDB'}]

        for response in responses:
            options.append({'id': response['qid']['value'],
                            'text': response['label']['value']+f" (mardi:{response['qid']['value']})"})

        return options

class ResearchField2(Provider):

    SUBJECT_ATTRIBUTE = 'http://example.com/terms/domain/MaRDI/Section_3a/Set_0/Question_0'

    def get_options(self, project, search=None):
        """
        Function providing Research Fields from MathModDB and User.
        """

        options =[]

        responses = MathModDB_request(wd, wdt, 'Q266')

        for response in responses:
            options.append({'id':response['qid']['value'],
                            'text':response['label']['value']+f" (mardi:{response['qid']['value']})"})

        subject_attribute = get_attribute(self.SUBJECT_ATTRIBUTE)
        values = get_attribute_values(project, subject_attribute)

        options = add_options(options, values, len(options), process_text_fn=lambda text: text)
        
        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

        return options

class ResearchProblem(Provider):

    def get_options(self, project, search=None):
        """
        Function providing Research Problem from MathModDB.
        """

        responses = MathModDB_request(wd, wdt, 'Q268')

        options=[{'id':'default','text':'not in MathModDB'}]

        for response in responses:
            options.append({'id':response['qid']['value'],
                            'text':response['label']['value']+f" (mardi:{response['qid']['value']})"})

        return options

class ResearchProblem2(Provider):

    SUBJECT_ATTRIBUTE = 'http://example.com/terms/domain/MaRDI/Section_3a/Set_1/Question_0'

    def get_options(self, project, search=None):
        """
        Function providing Research Problem from MathModDB and User.
        """

        options =[]

        responses = MathModDB_request(wd, wdt, 'Q268')

        for response in responses:
            options.append({'id':response['qid']['value'],
                            'text':response['label']['value']+f" (mardi:{response['qid']['value']})"})

        subject_attribute = get_attribute(self.SUBJECT_ATTRIBUTE)
        values = get_attribute_values(project, subject_attribute)

        options = add_options(options, values, len(options), process_text_fn=lambda text: text)

        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

        return options

class MathematicalModel(Provider):

    def get_options(self, project, search=None):

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label ?quote
                 WHERE {
                        ?id wdt:P4 wd:Q270;
                            rdfs:label ?label;
                            schema:description ?quote.

                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        options=[{'id':'default','text':'not in MathModDB'}]

        for r in req:
            options.append({'id':r['qid']['value'],'text':'mardi:'+r['qid']['value'] + ' <|> ' + r['label']['value'] + ' <|> ' + r['quote']['value']})
        
        return options

class MathematicalModel2(Provider):

    def get_options(self, project, search=None):
        options =[]

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q270;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0a'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':str(idx),'text':value.text})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_01'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':str(idx),'text':value.text})

        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

        return options

class Quantity(Provider):

    def get_options(self, project, search=None):

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q272;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        options=[{'id':'default','text':'not in MathModDB'}]

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        return options

class Quantity2(Provider):

    def get_options(self, project, search=None):
        options =[]

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q272;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':str(idx),'text':value.text})

        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

        return options

class QuantityKind(Provider):

    def get_options(self, project, search=None):

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q274;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        options=[{'id':'default','text':'not in MathModDB'}]

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        return options

class QuantityKind2(Provider):

    def get_options(self, project, search=None):
        options =[]

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q274;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_4/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':str(idx),'text':value.text})

        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

        return options

class MathematicalFormulation(Provider):

    def get_options(self, project, search=None):

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q276;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        options=[{'id':'default','text':'not in MathModDB'}]

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        return options

class MathematicalFormulation2(Provider):

    def get_options(self, project, search=None):
        options =[]

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q276;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})


        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_5/Question_0'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_5/Question_0a'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':str(idx),'text':value.text})

        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

        return options

class QuantityAndQuantityKind(Provider):

    def get_options(self, project, search=None):
        options = []

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_07'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'Q'+str(idx),'text':value.text})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_09'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_4/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'QK'+str(idx),'text':value.text})

        return options

class MathematicalTask(Provider):

    def get_options(self, project, search=None):

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q278;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        options=[{'id':'default','text':'not in MathModDB'}]

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        return options

class MathematicalTask2(Provider):

    def get_options(self, project, search=None):
        options =[]

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q278;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_6/Question_0'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_6/Question_0a'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':str(idx),'text':value.text})

        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

        return options

class AllEntities(Provider):

    def get_options(self, project, search=None):
        options =[]

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_04'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text + ' (Research Field)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_0/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'RF'+str(idx),'text':value.text + ' (Research Field)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_05'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text + ' (Research Problem)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_1/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'RP'+str(idx),'text':value.text + ' (Research Problem)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Wiki_01'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text + ' (Mathematical Model)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_01'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'MMa'+str(idx),'text':value.text + ' (Mathematical Model)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text + ' (Mathematical Model)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_2/Question_0a'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'MMb'+str(idx),'text':value.text + ' (Mathematical Model)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_07'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text + ' (Quantity)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_3/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'Q'+str(idx),'text':value.text + ' (Quantity)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3/Set_0/Set_0/Question_09'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text + ' (Quantity Kind)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_4/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'QK'+str(idx),'text':value.text + ' (Quantity Kind)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_5/Question_0'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text + ' (Mathematical Formulation)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_5/Question_0a'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'MF'+str(idx),'text':value.text + ' (Mathematical Formulation)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_6/Question_0'))
        for idx, value in enumerate(values):
            if value.text and value.text != 'not in MathModDB':
                options.append({'id':re.search('\(mardi:(.*)\)',value.text).group(1),'text':value.text + ' (Mathematical Task)'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_6/Question_0a'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'MT'+str(idx),'text':value.text + ' (Mathematical Task)'})

        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

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
        'id': f"{result['id']}",
        'text': f"{location}:{result['id']} <|> {result['display']['label']['value']} <|> {description}"
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
        if value.text:
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
