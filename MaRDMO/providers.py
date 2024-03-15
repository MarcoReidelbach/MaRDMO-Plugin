import requests
import itertools
from rdmo.options.providers import Provider
from rdmo.domain.models import Attribute
from .config import *
import re

class WikidataSearch(Provider):
    
    search = True

    def get_options(self, project, search):
        '''Function which queries wikidata and mardi KG, for user input.''' 
        if not search or len(search)<3:
            return []

        qwiki=requests.get(wikidata_api+'?action=wbsearchentities&format=json&language=en&type=item&limit=10&search={0}'.format(search),
                           headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['search']

        qmard=requests.get(mardi_api+'?action=wbsearchentities&format=json&language=en&type=item&limit=10&search={0}'.format(search),
                           headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['search'] 
        options=[]

        for index in range(10):
            
            if index < len(qwiki):
                try:
                    options.append({'id':'W'+str(index),
                                    'text':'wikidata:'+qwiki[index]['id']+' <|> '+qwiki[index]['display']['label']['value']+' <|> '+qwiki[index]['display']['description']['value']})
                except:
                    options.append({'id':'W'+str(index),
                                    'text':'wikidata:'+qwiki[index]['id']+' <|> '+qwiki[index]['display']['label']['value']+' <|> No Description Provided!'})
            
            if index < len(qmard):
                try:
                    options.append({'id':'M'+str(index),
                                    'text':'mardi:'+qmard[index]['id']+' <|> '+qmard[index]['display']['label']['value']+' <|> '+qmard[index]['display']['description']['value']})
                except:
                    options.append({'id':'M'+str(index),
                                    'text':'mardi:'+qmard[index]['id']+' <|> '+qmard[index]['display']['label']['value']+' <|> No Description Provided!'})

        return options

class ComponentSearch(Provider):

    search = True

    def get_options(self, project, search):
        '''Function which queries mardi KG, for user input.'''
        if not search or len(search)<3:
            return []

        qmard=requests.get(mardi_api+'?action=wbsearchentities&format=json&language=en&type=item&limit=10&search={0}'.format(search),
                           headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['search']

        options=[]

        for index in range(20):

            if index < len(qmard):
                try:
                    options.append({'id':'M'+str(index),'text':'mardi:'+qmard[index]['id']+' <|> '+qmard[index]['display']['label']['value']+' <|> '+qmard[index]['display']['description']['value']})
                except:
                    options.append({'id':'M'+str(index),'text':'mardi:'+qmard[index]['id']+' <|> '+qmard[index]['display']['label']['value'][1:]+' <|> No Description Provided!'})
        return options

class MathAreaProvider(Provider):

    subject_attribute = 'http://example.com/terms/domain/MaRDI/Section_2/Set_3/Question_00'

    def get_options(self, project, search=None):    
        '''Function providing the user-defined mathematical areas.'''

        try:
            subject_attribute = Attribute.objects.get(uri=self.subject_attribute)
        except Attribute.DoesNotExist:
            return {}

        options=[]

        # get current values for the subject attribute
        values = project.values.filter(snapshot=None, attribute=subject_attribute)

        index = 0

        for value in values:
            if value.text:
                options.append({'id':'MathArea'+str(index),'text':value.text.split(' <|> ')[1]})
                index+=1

        return options

class EnvironmentProvider(Provider):

    #Software from MaRDI KG /Wikidata
    subject_attribute_1 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_01'
    #Software (self-defined) 
    subject_attribute_2 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_02'
    #Experimental Device (self-defined)
    subject_attribute_3 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_5/Question_02'

    def get_options(self, project, search=None):
        '''Function providing the user-defined environments.'''

        try:
            subject_attribute_1 = Attribute.objects.get(uri=self.subject_attribute_1)
        except Attribute.DoesNotExist:
            return {}

        try:
            subject_attribute_2 = Attribute.objects.get(uri=self.subject_attribute_2)
        except Attribute.DoesNotExist:
            return {}

        try:
            subject_attribute_3 = Attribute.objects.get(uri=self.subject_attribute_3)
        except Attribute.DoesNotExist:
            return {}

        options=[]

        # get current values for MaRDI KG /Wikidata Software
        values = project.values.filter(snapshot=None, attribute=subject_attribute_1)

        index = 0

        for value in values:
            if value.text:
                options.append({'id':'Environment'+str(index),'text':value.text.split(' <|> ')[1]})
                index+=1

        # get current values for Software (self-defined)
        values = project.values.filter(snapshot=None, attribute=subject_attribute_2)

        for value in values:
            if value.text:
                options.append({'id':'Environment'+str(index),'text':value.text})
                index+=1

        # get current values for Experimental Devices (self-defined)
        values = project.values.filter(snapshot=None, attribute=subject_attribute_3)

        for value in values:
            if value.text:
                options.append({'id':'Environment'+str(index),'text':value.text})
                index+=1

        return options

class MethodProvider(Provider):

    #Method from MaRDI KG /Wikidata
    subject_attribute_1 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_01'
    #Method (self-defined) 
    subject_attribute_2 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_2/Question_02'

    def get_options(self, project, search=None):
        '''Function providing the user-defined methods.'''

        try:
            subject_attribute_1 = Attribute.objects.get(uri=self.subject_attribute_1)
        except Attribute.DoesNotExist:
            return {}

        try:
            subject_attribute_2 = Attribute.objects.get(uri=self.subject_attribute_2)
        except Attribute.DoesNotExist:
            return {}

        options=[]

        # get current values for MaRDI KG /Wikidata Method
        values = project.values.filter(snapshot=None, attribute=subject_attribute_1)

        index = 0

        for value in values:
            if value.text:
                options.append({'id':'Method'+str(index),'text':value.text.split(' <|> ')[1]})
                index+=1

        # get current values for Method (self-defined)
        values = project.values.filter(snapshot=None, attribute=subject_attribute_2)

        for value in values:
            if value.text:
                options.append({'id':'Method'+str(index),'text':value.text})
                index+=1

        return options

class DataProvider(Provider):

    #Input Data from MaRDI KG /Wikidata
    subject_attribute_1 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_00'
    #Input Data (self-defined) 
    subject_attribute_2 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_01'

    #Output Data from MaRDI KG /Wikidata
    subject_attribute_3 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_00'
    #Output Data (self-defined) 
    subject_attribute_4 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_01'

    def get_options(self, project, search=None):
        '''Function providing the user-defined input data sets.'''

        try:
            subject_attribute_1 = Attribute.objects.get(uri=self.subject_attribute_1)
        except Attribute.DoesNotExist:
            try:
                subject_attribute_2 = Attribute.objects.get(uri=self.subject_attribute_2)
            except Attribute.DoesNotExist:
                try:
                    subject_attribute_3 = Attribute.objects.get(uri=self.subject_attribute_3)
                except Attribute.DoesNotExist:
                    try:
                        subject_attribute_4 = Attribute.objects.get(uri=self.subject_attribute_4)
                    except Attribute.DoesNotExist:
                        return {}

        subject_attribute_1 = Attribute.objects.get(uri=self.subject_attribute_1)
        subject_attribute_2 = Attribute.objects.get(uri=self.subject_attribute_2)
        subject_attribute_3 = Attribute.objects.get(uri=self.subject_attribute_3)
        subject_attribute_4 = Attribute.objects.get(uri=self.subject_attribute_4)

        options=[]

        # get current values for MaRDI KG /Wikidata Method
        values = project.values.filter(snapshot=None, attribute=subject_attribute_1)

        index = 0

        for value in values:
            if value.text:
                options.append({'id':'Input'+str(index),'text':value.text.split(' <|> ')[1]})
                index+=1

        # get current values for Method (self-defined)
        values = project.values.filter(snapshot=None, attribute=subject_attribute_2)

        for value in values:
            if value.text:
                options.append({'id':'Input'+str(index),'text':value.text})
                index+=1

        # get current values for MaRDI KG /Wikidata Method
        values = project.values.filter(snapshot=None, attribute=subject_attribute_3)

        index = 0

        for value in values:
            if value.text:
                options.append({'id':'Output'+str(index),'text':value.text.split(' <|> ')[1]})
                index+=1

        # get current values for Method (self-defined)
        values = project.values.filter(snapshot=None, attribute=subject_attribute_4)

        for value in values:
            if value.text:
                options.append({'id':'Output'+str(index),'text':value.text})
                index+=1

        return options

class SoftwareProvider(Provider):

    #Software from MaRDI KG /Wikidata
    subject_attribute_1 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_01'
    #Software (self-defined) 
    subject_attribute_2 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_3/Question_02'

    def get_options(self, project, search=None):
        '''Function providing the user-defined software.'''

        try:
            subject_attribute_1 = Attribute.objects.get(uri=self.subject_attribute_1)
        except Attribute.DoesNotExist:
            return {}

        try:
            subject_attribute_2 = Attribute.objects.get(uri=self.subject_attribute_2)
        except Attribute.DoesNotExist:
            return {}

        options=[]

        # get current values for MaRDI KG /Wikidata Method
        values = project.values.filter(snapshot=None, attribute=subject_attribute_1)

        index = 0

        for value in values:
            if value.text:
                options.append({'id':'Software'+str(index),'text':value.text.split(' <|> ')[1]})
                index+=1

        # get current values for Method (self-defined)
        values = project.values.filter(snapshot=None, attribute=subject_attribute_2)

        for value in values:
            if value.text:
                options.append({'id':'Software'+str(index),'text':value.text})
                index+=1

        return options

class ResearchField(Provider):

    def get_options(self, project, search=None):
        
        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q266;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query}, 
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        options=[{'id':'default','text':'not in MathModDB'}]

        for re in req:
            options.append({'id':re['qid']['value'],'text':re['label']['value']+' (mardi:'+re['qid']['value']+')'})

        return options

class ResearchField2(Provider):

    def get_options(self, project, search=None):
        options =[]

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q266;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_0/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'user_'+str(idx),'text':value.text})

        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

        return options

class ResearchProblem(Provider):

    def get_options(self, project, search=None):

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q268;
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

class ResearchProblem2(Provider):

    def get_options(self, project, search=None):
        options =[]

        query='''PREFIX wdt:'''+wdt+'''
                 PREFIX wd:'''+wd+'''
                 SELECT  ?qid ?label
                 WHERE {
                        ?id wdt:P4 wd:Q268;
                            rdfs:label ?label.
                        BIND(STRAFTER(STR(?id),STR(wd:)) AS ?qid).
                        }'''

        req=requests.get(mardi_endpoint,
                         params = {'format': 'json', 'query': query},
                         headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['results']['bindings']

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})

        values = project.values.filter(snapshot=None, attribute=Attribute.objects.get(uri='http://example.com/terms/domain/MaRDI/Section_3a/Set_1/Question_0'))
        for idx, value in enumerate(values):
            if value.text:
                options.append({'id':'user_'+str(idx),'text':value.text})

        options = [dict(entry) for entry in {tuple(dicts.items()) for dicts in options}]

        return options

class MathematicalModel(Provider):

    def get_options(self, project, search=None):

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

        options=[{'id':'default','text':'not in MathModDB'}]

        for r in req:
            options.append({'id':r['qid']['value'],'text':r['label']['value']+' (mardi:'+r['qid']['value']+')'})
        
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



