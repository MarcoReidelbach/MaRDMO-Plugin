'''Main Export Functions of MaRDMO'''

import logging
import requests

from django import forms
from django.conf import settings
from django.shortcuts import redirect, render, reverse
from django.utils.translation import gettext_lazy as _

from rdmo.projects.exports import Export
from rdmo.services.providers import OauthProviderMixin

from .config import endpoint
from .getters import get_answers, get_general_item_url, get_mathmoddb, get_mathalgodb, get_options, get_questions_algorithm, get_questions_model, get_questions_publication, get_questions_search, get_questions_workflow
from .helpers import  inline_mathml, merge_dicts_with_unique_keys, process_question_dict
from .oauth2 import OauthProviderMixin

from .model.worker import prepareModel
from .model.checks import checks

from .algorithm.sparql import queryAlgorithmDocumentation
from .algorithm.worker import algorithm_relations
from .algorithm.utils import dict_to_triples_mathalgodb, generate_sparql_insert_with_new_ids_mathalgodb, update_ids

from .workflow.utils import compare_items, get_discipline
from .workflow.worker import prepareWorkflow

from .search.worker import search

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
        return endpoint['mardi']['uri']

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

            # Get answers, options, and mathmoddb             
            answers, options, mathmoddb = self.get_post_data()
            
            # Adjust MathML for Preview
            inline_mathml(answers)

            return render(self.request, 
                          'MaRDMO/mardmoPreview.html', 
                          {'form': self.ExportForm(), 'include_file': 
                                'MaRDMO/modelTemplate.html',
                                'include_params': {'title': self.project.title},
                                                   'answers': answers,
                                                   'option': options|mathmoddb}, 
                           status=200)
        
        # MaRDMO: Algorithm Documentation
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':
            
            # Get answers, options, mathalgodb
            answers, options, mathalgodb = self.get_post_data()
            
            return render(self.request, 
                          'MaRDMO/mardmoPreview.html', 
                          {'form': self.ExportForm(), 'include_file': 
                                'MaRDMO/algorithmTemplate.html',
                                'include_params': {'title': self.project.title},
                                                   'answers': answers,
                                                   'option': options|mathalgodb}, 
                           status=200)


        # MaRDMO: Search Interdisciplinary Workflows, Mathematical Models or Algorithms
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-search-catalog':

            answers, options = self.get_post_data()

            return render(self.request, 
                          'MaRDMO/mardmoPreview.html', 
                          {'form': self.ExportForm(), 'include_file': 
                           'MaRDMO/searchTemplate.html',
                           'include_params': {'title': self.project.title},
                                              'answers': answers,
                                              'option': options}, 
                           status=200)
        
        # MaRDMO: Interdisciplinary Workflow Documentation
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':

            answers, options = self.get_post_data()

            # Get Model Data
            prepare = prepareWorkflow()
            answers = prepare.preview(answers)

            # Adjust MathML for Preview
            inline_mathml(answers)
            
            return render(self.request, 
                          'MaRDMO/mardmoPreview.html', 
                          {'form': self.ExportForm(), 'include_file': 
                           'MaRDMO/workflowTemplate.html',
                           'include_params': {'title': self.project.title},
                                              'answers': answers,
                                              'option': options,
                                              'mathmoddbURI': endpoint['mardi']['uri'],
                                              'mathalgodbURI': endpoint['mathalgodb']['uri'],
                                              'mardiURI': get_general_item_url(),
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
                
                answers, *__ = self.get_post_data()
                
                checker = checks()
                err = checker.run(self.project, answers)
                if err:
                    # Stop export if documentation incomplete / inconsitent
                    return render(self.request, 
                                  'core/error.html', 
                                  {'title': _("Incomplete or Inconsistent Documentation"),
                                   'errors': err}, 
                                  status=200)
                try:
                    prepare = prepareModel()
                    payload = prepare.export(answers, self.wikibase_url)
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

                answers, *__ = self.get_post_data()
                
                # Merge answers related to mathematical model
                merged_dict = merge_dicts_with_unique_keys(answers, ['algorithm', 'problem', 'software', 'benchmark', 'publication'])
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
                    ids = update_ids(self.project, ids, queryAlgorithmDocumentation['IDCheck'], endpoint['mathalgodb']['sparql'], 'mathalgodb')
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

                answers, options = self.get_post_data()
                
                if answers['search']['options'] == options['InterdisciplinaryWorkflow']:
                    datatype = "Workflow(s)"
                    source = "MaRDI Portal"
                elif answers['search']['options'] == options['MathematicalModel']:
                    datatype = "Mathematical Model(s)"
                    source = "MathModDB KG"
                elif answers['search']['options'] == options['Algorithm']:
                    datatype = "Algorithm(s)"
                    source = "MathAlgoDB KG"

                return render(self.request,
                              'MaRDMO/searchResults.html', 
                              {'datatype': datatype,
                               'source': source,   
                               'noResults': answers['no_results'],
                               'links': answers['links']}, 
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

                answers, *__ = self.get_post_data()
                try:
                    prepare = prepareWorkflow()
                    payload = prepare.export(answers, self.project.title, self.wikibase_url)
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
                       'mardi_uri': get_general_item_url}, 
                      status=200)

    def get_post_url(self):
        return self.deposit_url

    def get_post_data(self):

        options = get_options()

        # MaRDMO: Mathematical Model Documentation
        if str(self.project.catalog).split('/')[-1] == 'mardmo-model-catalog':

            # Load Data for Model & Publication Documentation
            questions = get_questions_model() | get_questions_publication()
            mathmoddb = get_mathmoddb()

            answers = process_question_dict(project = self.project, 
                                            questions = questions, 
                                            get_answer = get_answers)
            
            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.WorkflowOrModel(self.project, answers, options)
            
            # Prepare Mathematical Model (Preview)
            prepare = prepareModel()
            answers = prepare.preview(answers)

            return answers, options, mathmoddb
        
        # MaRDMO: Algorithm Documentation
        if str(self.project.catalog).split('/')[-1] == 'mardmo-algorithm-catalog':

            # Load Data for Mathematical Model Documentation
            questions = get_questions_algorithm() | get_questions_publication()
            mathalgodb = get_mathalgodb()

            answers = process_question_dict(project = self.project, 
                                            questions = questions, 
                                            get_answer = get_answers)
            
            # Refine Mathematical Model Information
            answers = algorithm_relations(self.project, answers, mathalgodb)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.Algorithm(self.project, answers)
            
            return answers, options, mathalgodb

        # MaRDMO: Search Interdisciplinary Workflow, Mathematical Model or Algorithm
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-search-catalog':

            # Load Data for Interdisciplinary Workflow, Mathematical Model or Algorithm Search
            questions = get_questions_search()
            
            answers = process_question_dict(project = self.project, 
                                            questions = questions, 
                                            get_answer = get_answers)

            # Get Results from MaRDI Resources
            answers = search(answers, options)

            return answers, options

        # MaRDMO: Interdisciplinary Workflow Documentation
        elif str(self.project.catalog).split('/')[-1] == 'mardmo-interdisciplinary-workflow-catalog':

            # Load Data for Interdisciplinary Workflow Documentation
            questions = get_questions_workflow() | get_questions_publication()
            
            answers = process_question_dict(project = self.project, 
                                            questions = questions, 
                                            get_answer = get_answers)
            
            # Refine associated Disciplines
            answers = get_discipline(answers)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.WorkflowOrModel(self.project, answers, options)
            
            return answers, options        
