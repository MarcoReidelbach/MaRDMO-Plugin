import logging
import requests

from dataclasses import asdict

from django import forms
from django.conf import settings
from django.shortcuts import redirect, render, reverse
from django.utils.translation import gettext_lazy as _

from rdmo.projects.exports import Export
from rdmo.services.providers import OauthProviderMixin

from .oauth2 import OauthProviderMixin

from .utils import get_answer, get_data, get_new_ids, query_sparql
from .model.worker import model_relations
from .algorithm.worker import algorithm_relations
from .search.worker import search
from .config import mathmoddb_update, mardi_uri, mathalgodb_uri, mathmoddb_uri, wikidata_uri

from .model.sparql import queryModelDocumentation
from .model.utils import get_answer_model, merge_dicts_with_unique_keys, dict_to_triples, generate_sparql_insert_with_new_ids

from .algorithm.utils import get_answer_algorithm

from .workflow.sparql import queryPreview
from .workflow.utils import get_answer_workflow, get_discipline
from .workflow.models import ModelProperties, Variables, Parameters

from .publication.worker import PublicationRetriever

logger = logging.getLogger(__name__)

try:
    # Get login credentials if available 
    from config.settings import mathmoddb_username, mathmoddb_password
except:
    mathmoddb_username=''; mathmoddb_password=''


class BaseMaRDMOExportProvider(OauthProviderMixin, Export):

    @property
    def client_id(self):
        return settings.MaRDMO_PROVIDER['client_id']

    @property
    def client_secret(self):
        return settings.MaRDMO_PROVIDER['client_secret']

    @property
    def wikibase_url(self):
        return 'https://test.wikidata.org'

    @property
    def authorize_url(self):
        return f'{self.wikibase_url}/w/rest.php/oauth2/authorize'

    @property
    def token_url(self):
        return f'{self.wikibase_url}/w/rest.php/oauth2/access_token'

    @property
    def deposit_url(self):
        return f'{self.wikibase_url}/w/rest.php/wikibase/v1/entities/items'

    @property
    def redirect_path(self):
        return reverse('oauth_callback', args=['zenodo'])

    def get_authorize_params(self, request, state):
        return {
            'response_type': 'code',
            'client_id': self.client_id,
            'state': state
        }

    def get_callback_data(self, request):
        return {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': request.GET.get('code')
        }

    def get_error_message(self, response):
        return response.json().get('errors')


class MaRDMOExportProvider(BaseMaRDMOExportProvider):

    class ExportForm(forms.Form):
        pass

    def render(self):

        # MaRDMO: Mathematical Model Documentation
        if str(self.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
            
            data = self.get_post_data()
            
            return render(self.request, 
                          'MaRDMO/mardmoPreview.html', 
                          {'form': self.ExportForm(), 'include_file': 
                                'MaRDMO/modelTemplate.html',
                                'include_params': {'title': self.project.title},
                                                   'answers': data[0],
                                                   'option': data[1]|data[2]}, 
                           status=200)
        
        # MaRDMO: Algorithm Documentation
        if str(self.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':
            
            data = self.get_post_data()
            
            return render(self.request, 
                          'MaRDMO/mardmoPreview.html', 
                          {'form': self.ExportForm(), 'include_file': 
                                'MaRDMO/algorithmTemplate.html',
                                'include_params': {'title': self.project.title},
                                                   'answers': data[0],
                                                   'option': data[1]|data[2]}, 
                           status=200)


        # MaRDMO: Search Interdisciplinary Workflows, Mathematical Models or Algorithms
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-search-catalog':

            data = self.get_post_data()

            return render(self.request, 
                          'MaRDMO/mardmoPreview.html', 
                          {'form': self.ExportForm(), 'include_file': 
                           'MaRDMO/searchTemplate.html',
                           'include_params': {'title': self.project.title},
                                              'answers': data[0],
                                              'option': data[1]}, 
                           status=200)
        
        # MaRDMO: Interdisciplinary Workflow Documentation
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':

            data = self.get_post_data()
            
            # Update Model Properties via MathModDB
            if data[0].get('model',{}).get('ID'):
                basic = query_sparql(queryPreview['basic'].format(data[0]['model']['ID']))
                if basic:
                    data[0].get('model', {}).update(asdict(ModelProperties.from_query(basic)))
            
            # Update Model Variables and Parameters via MathModDB
            if data[0].get('specifictask'):
                variables = query_sparql(queryPreview['variables'].format(' '.join(value.get('ID', '') for _, value in data[0]['specifictask'].items())))
                if variables:
                    for idx, variable in enumerate(variables):
                        data[0].setdefault('variables', {}).update({idx: asdict(Variables.from_query(variable))})
                        
                parameters = query_sparql(queryPreview['parameters'].format(' '.join(value.get('ID', '') for _, value in data[0]['specifictask'].items())))
                if parameters:
                    for idx, parameter in enumerate(parameters):
                        data[0].setdefault('parameters', {}).update({idx: asdict(Parameters.from_query(parameter))})
            
            return render(self.request, 
                          'MaRDMO/mardmoPreview.html', 
                          {'form': self.ExportForm(), 'include_file': 
                           'MaRDMO/workflowTemplate.html',
                           'include_params': {'title': self.project.title},
                                              'answers': data[0],
                                              'option': data[1],
                                              'mathmoddbURI': mathmoddb_uri,
                                              'mathalgodbURI': mathalgodb_uri,
                                              'mardiURI': mardi_uri,
                                              'wikidataURI': wikidata_uri}, 
                           status=200)


    def submit(self):
        if 'cancel' in self.request.POST:
            return redirect('project', self.project.id)
        else:
            # MaRDMO: Mathematical Model Documentation
            if str(self.project.catalog).split('/')[-1] == 'mardmo-model-catalog':
                
                data = self.get_post_data()
                
                # Merge answers related to mathematical model
                merged_dict = merge_dicts_with_unique_keys(data[0])         
                # Generate list of triples
                triple_list, ids = dict_to_triples(merged_dict) 
                # Generate query for MathModDB KG
                query = generate_sparql_insert_with_new_ids(triple_list)
                
                # Add Model Documentation to MathModDB
                response = requests.post(mathmoddb_update, data=query, headers={
                                        "Content-Type": "application/sparql-update",
                                        "Accept": "text/turtle"},
                                        auth=(mathmoddb_username, mathmoddb_password),
                                        verify = False
                                    )
                
                if response.status_code == 204:
                    ids = get_new_ids(self.project, ids, queryModelDocumentation['IDCheck'])
                    # Links to newly created Entities
                    return render(self.request,
                                  'MaRDMO/modelExport.html', 
                                  {'ids': ids,
                                   'mathmoddb_uri': mathmoddb_uri}, 
                                  status=200)
                else:
                    return render(self.request,
                                  'MaRDMO/workflowError.html', 
                                  {'error': 'The mathematical model could not be integrated into the MathodDB!'}, 
                                  status=200)

            # MaRDMO: Algorithm Documentation
            if str(self.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':

                return render(self.request,
                              'MaRDMO/Export_soon.html',        
                              status=200)

            # MaRDMO: Search Interdisciplinary Workflow, Mathematical Models or Algorithms    
            elif str(self.project.catalog).split('/')[-1] == 'mardmo-search-catalog':

                data = self.get_post_data()

                return render(self.request,
                              'MaRDMO/workflowSearch.html', 
                              {'noResults': data[0]['no_results'],
                               'links': data[0]['links']}, 
                              status=200)
            
            # MaRDMO: Interdisciplinary Workflow Documentation
            elif str(self.project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':

                #data = self.get_post_data()
                
                #url = self.get_post_url()

                #payload = [{
                #           "item": {
                #               "labels": {
                #                   "en": "Item5"
                #               },
                #               "descriptions": {
                #                   "en": "item6"
                #               }
                #           },
                #           "comment": "Creating Item 5"
                #       },
                #       {
                #           "item": {
                #               "labels": {
                #                   "en": "Item6"
                #               },
                #               "descriptions": {
                #                   "en": "item6"
                #               }
                #           },
                #           "comment": "Creating Item 6"
                #       }]
                
                #return self.post(self.request, url, payload)


                return render(self.request,
                              'MaRDMO/Export_soon.html', 
                              status=200)
                


    def post_success(self, request, response):
        zenodo_url = ''#response.json().get('links', {}).get('self_html')
        if zenodo_url:
            return redirect(zenodo_url)
        else:
            return render(request, 'core/error.html', {
                'title': _('ZENODO error'),
                'errors': [_('The URL of the new dataset could not be retrieved.')]
            }, status=200)

    def get_post_url(self):
        return self.deposit_url

    def get_post_data(self):

        options = get_data('data/options.json')

        # MaRDMO: Mathematical Model Documentation
        if str(self.project.catalog).split('/')[-1] == 'mardmo-model-catalog':

            # Load Data for Mathematical Model Documentation
            questions = get_data('model/data/questions.json')
            mathmoddb = get_data('model/data/mapping.json')

            answers ={}
            for _, info in questions.items():
                answers = get_answer_model(self.project, answers, **info)
            
            # Refine Mathematical Model Information
            answers = model_relations(self.project, answers,mathmoddb)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.Model(self.project, answers, options)

            return answers, options, mathmoddb
        
        # MaRDMO: Algorithm Documentation
        if str(self.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':

            # Load Data for Mathematical Model Documentation
            questions = get_data('algorithm/data/questions.json')
            mathalgodb = get_data('algorithm/data/mapping.json')

            answers ={}
            for _, info in questions.items():
                answers = get_answer_algorithm(self.project, answers, **info)
            
            # Refine Mathematical Model Information
            answers = algorithm_relations(self.project, answers, mathalgodb)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.Algorithm(self.project, answers, options)

            return answers, options, mathalgodb

        # MaRDMO: Search Interdisciplinary Workflow, Mathematical Model or Algorithm
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-search-catalog':

            # Load Data for Interdisciplinary Workflow, Mathematical Model or Algorithm Search
            questions = get_data('search/data/questions.json')
            
            answers ={}
            for _, info in questions.items():
                answers = get_answer(self.project, answers, **info)

            # Get Results from MaRDI Resources
            answers = search(answers, options)

            return answers, options

        # MaRDMO: Interdisciplinary Workflow Documentation
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':

            # Load Data for Interdisciplinary Workflow Documentation
            questions = get_data('workflow/data/questions.json')
            
            answers ={}
            for _, info in questions.items():
                answers = get_answer_workflow(self.project, answers, **info)
            
            # Refine associated Disciplines
            answers = get_discipline(answers)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.Workflow(self.project, answers, options)
            
            return answers, options        
