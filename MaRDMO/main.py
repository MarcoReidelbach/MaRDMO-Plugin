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
from .utils import get_mathmoddb, get_data, get_new_ids, get_questionsAL, get_questionsMO, get_questionsPU, get_questionsSE, get_questionsWO, merge_dicts_with_unique_keys, query_sparql
from .config import endpoint

from .model.worker import prepareModel
from .model.utils import get_answer_model

from .algorithm.sparql import queryAlgorithmDocumentation
from .algorithm.worker import algorithm_relations
from .algorithm.utils import get_answer_algorithm, dict_to_triples_mathalgodb, generate_sparql_insert_with_new_ids_mathalgodb

from .workflow.sparql import queryPreview
from .workflow.utils import compare_items, get_answer_workflow, get_discipline
from .workflow.models import ModelProperties, Variables, Parameters
from .workflow.worker import prepareWorkflowExport

from .search.worker import search
from .search.utils import get_answer_search

from .publication.worker import PublicationRetriever

logger = logging.getLogger(__name__)

class BaseMaRDMOExportProvider(OauthProviderMixin, Export):

    @property
    def oauth2_client_id(self):
        return settings.MARDMO_PROVIDER['oauth2_client_id']

    @property
    def oauth2_client_secret(self):
        return settings.MARDMO_PROVIDER['oauth2_client_secret']
    
    @property
    def mathalgodb_id(self):
        return settings.MARDMO_PROVIDER['mathalgodb_id']

    @property
    def mathalgodb_secret(self):
        return settings.MARDMO_PROVIDER['mathalgodb_secret']

    @property
    def wikibase_url(self):
        return 'https://test.wikidata.org' #'https://staging.mardi4nfdi.org'

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
        return reverse('oauth_callback', args=['wikibase'])

    def get_authorize_params(self, request, state):
        return {
            'response_type': 'code',
            'client_id': self.oauth2_client_id,
            'state': state
        }

    def get_callback_data(self, request):
        return {
            'client_id': self.oauth2_client_id,
            'client_secret': self.oauth2_client_secret,
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
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':
            
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
                                              'mathmoddbURI': endpoint['mathmoddb']['uri'],
                                              'mathalgodbURI': endpoint['mathalgodb']['uri'],
                                              'mardiURI': endpoint['mardi']['uri'],
                                              'wikidataURI': endpoint['wikidata']['uri']}, 
                           status=200)
        
        # Non-MaRDMO Catalog
        else:

            return render(self.request, 'core/error.html', {
                'title': _('Catalog Error'),
                'errors': [_('The catalog is not supported by the MaRDMO Plugin.')]
            }, status=200)


    def submit(self):
        if 'cancel' in self.request.POST:
            return redirect('project', self.project.id)
        else:
            # MaRDMO: Mathematical Model Documentation
            if str(self.project.catalog).split('/')[-1] == 'mardmo-model-catalog':

                if not (self.oauth2_client_id and self.oauth2_client_secret):
                    # Check for MaRDI Portal Credentials
                    return render(self.request, 
                                  'core/error.html', 
                                  {'title': _('Missing Credentials'),
                                   'errors': [_('Credentials for MaRDI Portal are missing!')]}, 
                                  status=200)
                
                data = self.get_post_data()
                
                try:
                    payload = prepareModel.export(data[0], self.wikibase_url)
                except Exception as err:
                    return render(self.request, 
                                  'core/error.html', 
                                  {'title': _('Value Error'),
                                   'errors': [err]}, 
                                  status=200)
                
                url = self.get_post_url()
                           
                return self.post(self.request, url, payload)

            # MaRDMO: Algorithm Documentation
            if str(self.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':

                if not (self.mathalgodb_id and self.mathalgodb_secret):
                    # Check for MathAlgoDB Credentials
                    return render(self.request, 
                                  'core/error.html', 
                                  {'title': _('Missing Credentials'),
                                   'errors': [_('Credentials for MathAlgoDB are missing!')]}, 
                                  status=200)

                data = self.get_post_data()
                
                # Merge answers related to mathematical model
                merged_dict = merge_dicts_with_unique_keys(data[0], ['algorithm', 'problem', 'software', 'benchmark', 'publication'])
                # Generate list of triples
                triple_list, ids = dict_to_triples_mathalgodb(merged_dict)
                # Generate query for MathModDB KG
                query = generate_sparql_insert_with_new_ids_mathalgodb(triple_list)
                
                response = requests.post(endpoint['mathalgodb']['update'], data=query, headers={
                                        "Content-Type": "application/sparql-update",
                                        "Accept": "text/turtle"},
                                        auth=(self.mathalgodb_id, self.mathalgodb_secret),
                                        verify = False
                                    )
                
                if response.status_code == 204:
                    ids = get_new_ids(self.project, ids, queryAlgorithmDocumentation['IDCheck'], endpoint['mathalgodb']['sparql'], 'mathalgodb')
                    # Links to newly created Entities
                    return render(self.request,
                                  'MaRDMO/algorithmExport.html', 
                                  {'ids': ids,
                                   'mathalgodb_uri': endpoint['mathalgodb']['uri']}, 
                                  status=200)
                else:
                    return render(self.request,
                                  'MaRDMO/workflowError.html', 
                                  {'error': 'The algorithm could not be integrated into the MathAlgoDB!'}, 
                                  status=200)

            # MaRDMO: Search Interdisciplinary Workflow, Mathematical Models or Algorithms    
            elif str(self.project.catalog).split('/')[-1] == 'mardmo-search-catalog':

                data = self.get_post_data()

                options = get_data('data/options.json')
                
                if data[0]['search']['options'] == options['InterdisciplinaryWorkflow']:
                    datatype = "Workflow(s)"
                    source = "MaRDI Portal"
                elif data[0]['search']['options'] == options['MathematicalModel']:
                    datatype = "Mathematical Model(s)"
                    source = "MathModDB KG"
                elif data[0]['search']['options'] == options['Algorithm']:
                    datatype = "Algorithm(s)"
                    source = "MathAlgoDB KG"

                return render(self.request,
                              'MaRDMO/searchResults.html', 
                              {'datatype': datatype,
                               'source': source,   
                               'noResults': data[0]['no_results'],
                               'links': data[0]['links']}, 
                              status=200)
            
            # MaRDMO: Interdisciplinary Workflow Documentation
            elif str(self.project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':

                if not (self.oauth2_client_id and self.oauth2_client_secret):
                    # Check for MaRDI Portal Credentials
                    return render(self.request, 
                                  'core/error.html', 
                                  {'title': _('Missing Credentials'),
                                   'errors': [_('Credentials for MaRDI Portal are missing!')]}, 
                                  status=200)

                data = self.get_post_data()
                try:
                    payload = prepareWorkflowExport(data[0], self.project.title, self.wikibase_url)
                except Exception as err:
                    return render(self.request, 
                                  'core/error.html', 
                                  {'title': _('Value Error'),
                                   'errors': [err]}, 
                                  status=200)


                url = self.get_post_url()
                
                return self.post(self.request, url, payload)

    def post_success(self, request, init, final):

        ids = compare_items(init, final)

        # Links to newly created Entities
        return render(request,
                      'MaRDMO/portalExport.html', 
                      {'ids': ids,
                       'mardi_uri': endpoint['mardi']['uri']}, 
                      status=200)

    def get_post_url(self):
        return self.deposit_url

    def get_post_data(self):

        options = get_data('data/options.json')

        # MaRDMO: Mathematical Model Documentation
        if str(self.project.catalog).split('/')[-1] == 'mardmo-model-catalog':

            # Load Data for Model & Publication Documentation
            questions = get_questionsMO() | get_questionsPU()
            mathmoddb = get_mathmoddb()

            answers ={}
            for _, info in questions.items():
                answers = get_answer_model(self.project, answers, **info)
            
            # Prepare Mathematical Model Preview
            answers = prepareModel.preview(answers)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.WorkflowOrModel(self.project, answers, options)
            
            return answers, options, mathmoddb
        
        # MaRDMO: Algorithm Documentation
        if str(self.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':

            # Load Data for Mathematical Model Documentation
            questions = get_questionsAL() | get_questionsPU()
            mathalgodb = get_data('algorithm/data/mapping.json')

            answers ={}
            for _, info in questions.items():
                answers = get_answer_algorithm(self.project, answers, **info)
            
            # Refine Mathematical Model Information
            answers = algorithm_relations(self.project, answers, mathalgodb)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.Algorithm(self.project, answers)

            return answers, options, mathalgodb

        # MaRDMO: Search Interdisciplinary Workflow, Mathematical Model or Algorithm
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-search-catalog':

            # Load Data for Interdisciplinary Workflow, Mathematical Model or Algorithm Search
            questions = get_questionsSE()
            
            answers ={}
            for _, info in questions.items():
                answers = get_answer_search(self.project, answers, **info)

            # Get Results from MaRDI Resources
            answers = search(answers, options)

            return answers, options

        # MaRDMO: Interdisciplinary Workflow Documentation
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':

            # Load Data for Interdisciplinary Workflow Documentation
            questions = questions = get_questionsWO() | get_questionsPU()
            
            answers ={}
            for _, info in questions.items():
                answers = get_answer_workflow(self.project, answers, **info)
            
            # Refine associated Disciplines
            answers = get_discipline(answers)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.WorkflowOrModel(self.project, answers, options)
            
            return answers, options        
