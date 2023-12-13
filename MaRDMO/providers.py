import requests
from rdmo.options.providers import Provider
from .config import *

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
        
        options=[{'id':'default','text':'<N/A>'}]

        for index in range(10):
            
            if index < len(qwiki):
                try:
                    options.append({'id':'W'+str(index),'text':'wikidata:'+qwiki[index]['id']+' <|> '+qwiki[index]['display']['label']['value']+' <|> '+qwiki[index]['display']['description']['value']})
                except:
                    options.append({'id':'W'+str(index),'text':'wikidata:'+qwiki[index]['id']+' <|> '+qwiki[index]['display']['label']['value']+' <|> No Description Provided!'})
            
            if index < len(qmard):
                try:
                    options.append({'id':'M'+str(index),'text':'mardi:'+qmard[index]['id']+' <|> '+qmard[index]['display']['label']['value']+' <|> '+qmard[index]['display']['description']['value']})
                except:
                    options.append({'id':'M'+str(index),'text':'mardi:'+qmard[index]['id']+' <|> '+qmard[index]['display']['label']['value'][1:]+' <|> No Description Provided!'})

        return options

class ComponentSearch(Provider):

    search = True

    def get_options(self, project, search):
        '''Function which queries mardi KG, for user input.'''
        if not search or len(search)<3:
            return []

        qmard=requests.get(mardi_api+'?action=wbsearchentities&format=json&language=en&type=item&limit=10&search={0}'.format(search),
                           headers = {'User-Agent': 'MaRDMO_0.1 (https://zib.de; reidelbach@zib.de)'}).json()['search']

        options=[{'id':'default','text':'<N/A>'}]

        for index in range(20):

            if index < len(qmard):
                try:
                    options.append({'id':'M'+str(index),'text':'mardi:'+qmard[index]['id']+' <|> '+qmard[index]['display']['label']['value']+' <|> '+qmard[index]['display']['description']['value']})
                except:
                    options.append({'id':'M'+str(index),'text':'mardi:'+qmard[index]['id']+' <|> '+qmard[index]['display']['label']['value'][1:]+' <|> No Description Provided!'})
        return options
