import requests
from rdmo.options.providers import Provider
from rdmo.domain.models import Attribute
from .config import *

class WikidataSearch(Provider):
    
    search = True
    refresh = True

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

class InputDataProvider(Provider):

    #Input Data from MaRDI KG /Wikidata
    subject_attribute_1 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_00'
    #Input Data (self-defined) 
    subject_attribute_2 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_6/Question_01'

    def get_options(self, project, search=None):
        '''Function providing the user-defined input data sets.'''

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
                options.append({'id':'Input'+str(index),'text':value.text.split(' <|> ')[1]})
                index+=1

        # get current values for Method (self-defined)
        values = project.values.filter(snapshot=None, attribute=subject_attribute_2)

        for value in values:
            if value.text:
                options.append({'id':'Input'+str(index),'text':value.text})
                index+=1

        return options

class OutputDataProvider(Provider):

    #Output Data from MaRDI KG /Wikidata
    subject_attribute_1 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_00'
    #Output Data (self-defined) 
    subject_attribute_2 = 'http://example.com/terms/domain/MaRDI/Section_4/Set_7/Question_01'

    def get_options(self, project, search=None):
        '''Function providing the user-defined output data sets.'''

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
                options.append({'id':'Output'+str(index),'text':value.text.split(' <|> ')[1]})
                index+=1

        # get current values for Method (self-defined)
        values = project.values.filter(snapshot=None, attribute=subject_attribute_2)

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


