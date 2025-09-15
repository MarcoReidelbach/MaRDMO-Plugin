'''Main Export Functions of MaRDMO'''

import logging
from abc import ABC

import requests

from django import forms
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect, render, reverse
from django.utils.translation import gettext_lazy as _

from rdmo.projects.exports import Export
from rdmo.services.providers import OauthProviderMixin

from .config import endpoint
from .getters import (
    get_answers,
    get_general_item_url,
    get_mathmoddb,
    get_mathalgodb,
    get_options,
    get_questions
)
from .helpers import  inline_mathml, merge_dicts_with_unique_keys, process_question_dict
from .oauth2 import OauthProviderMixin

from .model.worker import PrepareModel
from .model.checks import checks

from .algorithm.sparql import queryAlgorithmDocumentation
from .algorithm.worker import algorithm_relations
from .algorithm.utils import (
    dict_to_triples_mathalgodb,
    generate_sparql_insert_with_new_ids_mathalgodb,
    update_ids
)

from .workflow.utils import compare_items, get_discipline
from .workflow.worker import prepareWorkflow
from .search.worker import search
from .publication.worker import PublicationRetriever

logger = logging.getLogger(__name__)

class BaseMaRDMOExportProvider(OauthProviderMixin, Export, ABC):
    '''Base Class providing URLs and Credentials.'''
    @property
    def oauth2_client_id(self):
        '''Provide OAuth2 Client ID'''
        return settings.MARDMO_PROVIDER['oauth2_client_id']

    @property
    def oauth2_client_secret(self):
        '''Provide OAuth2 Client Secret'''
        return settings.MARDMO_PROVIDER['oauth2_client_secret']

    @property
    def mathalgodb_id(self):
        '''Provide MathAlgoDB ID'''
        return settings.MARDMO_PROVIDER['mathalgodb_id']

    @property
    def mathalgodb_secret(self):
        '''Provide MathAlgoDB Secret'''
        return settings.MARDMO_PROVIDER['mathalgodb_secret']

    @property
    def wikibase_url(self):
        '''Provide MaRDI Portal URL'''
        return endpoint['mardi']['uri']

    @property
    def authorize_url(self):
        '''Provide OAuth2 Authorize URL'''
        return f'{self.wikibase_url}/w/rest.php/oauth2/authorize'

    @property
    def token_url(self):
        '''Provide OAuth2 Token URL'''
        return f'{self.wikibase_url}/w/rest.php/oauth2/access_token'

    @property
    def redirect_path(self):
        '''Provide OAuth2 Callback Path'''
        return reverse('oauth_callback', args=['wikibase'])

    def get_authorize_params(self, request, state):
        '''Get Authoritaion Parameter for OAuth2 Protocol'''
        return {
            'response_type': 'code',
            'client_id': self.oauth2_client_id,
            'state': state
        }

    def get_callback_data(self, request):
        '''Get Callback Data for OAuth2 Protocol'''
        return {
            'client_id': self.oauth2_client_id,
            'client_secret': self.oauth2_client_secret,
            'grant_type': 'authorization_code',
            'code': request.GET.get('code')
        }

class MaRDMOExportProvider(BaseMaRDMOExportProvider):
    """Handles MaRDMO export logic.

    Attributes:
        request: The Django HttpRequest associated with the provider.
    """

    request: HttpRequest

    class ExportForm(forms.Form):
        '''Placeholder Export Form Class'''

    def render(self):
        '''Render Preview of User Answers'''
        # MaRDMO: Mathematical Model Documentation
        if str(self.project.catalog).endswith('mardmo-model-catalog'):

            # Get answers, options, and mathmoddb
            answers, options, mathmoddb = self.get_post_data()

            # Adjust MathML for Preview
            inline_mathml(answers)
            
            return render(
                self.request,
                'MaRDMO/mardmoPreview.html', 
                {
                    'form': self.ExportForm(),
                    'include_file': 'MaRDMO/modelTemplate.html',
                    'include_params': {
                        'title': self.project.title
                    },
                    'answers': answers,
                    'option': options|mathmoddb
                },
                status=200
            )

        # MaRDMO: Algorithm Documentation
        if str(self.project.catalog).endswith('mardmo-algorithm-catalog'):

            # Get answers, options, mathalgodb
            answers, options, mathalgodb = self.get_post_data()

            return render(
                self.request,
                'MaRDMO/mardmoPreview.html',
                {
                    'form': self.ExportForm(),
                    'include_file': 'MaRDMO/algorithmTemplate.html',
                    'include_params': {
                        'title': self.project.title
                    },
                    'answers': answers,
                    'option': options|mathalgodb
                },
                status=200
            )

        # MaRDMO: Search Interdisciplinary Workflows, Mathematical Models or Algorithms
        if str(self.project.catalog).endswith('mardmo-search-catalog'):

            answers, options = self.get_post_data()

            return render(
                self.request,
                'MaRDMO/mardmoPreview.html',
                {
                    'form': self.ExportForm(),
                    'include_file': 'MaRDMO/searchTemplate.html',
                    'include_params': {
                        'title': self.project.title
                    },
                    'answers': answers,
                    'option': options
                },
                status=200
            )

        # MaRDMO: Interdisciplinary Workflow Documentation
        if str(self.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):

            answers, options = self.get_post_data()

            # Get Model Data
            prepare = prepareWorkflow()
            answers = prepare.preview(answers)

            # Adjust MathML for Preview
            inline_mathml(answers)

            return render(
                self.request,
                'MaRDMO/mardmoPreview.html',
                {
                    'form': self.ExportForm(),
                    'include_file': 'MaRDMO/workflowTemplate.html',
                    'include_params': {
                        'title': self.project.title
                    },
                    'answers': answers,
                    'option': options,
                    'mathmoddbURI': endpoint['mardi']['uri'],
                    'mathalgodbURI': endpoint['mathalgodb']['uri'],
                    'mardiURI': get_general_item_url(),
                    'wikidataURI': endpoint['wikidata']['uri']
                },
                status=200
            )

        # Non-MaRDMO Catalog
        return render(
            self.request,
            'core/error.html',
            {
                'title': _('Catalog Error'),
                'errors': [_('The catalog is not supported by the MaRDMO Plugin.')]
            },
            status=200
        )

    def submit(self):
        """Dispatch submission based on catalog type."""

        # Handle cancel for all submissions
        if 'cancel' in self.request.POST:
            return redirect('project', self.project.id)

        catalog = str(self.project.catalog)

        if catalog.endswith('mardmo-model-catalog'):
            return self.submit_mardmo_model()
        if catalog.endswith('mardmo-algorithm-catalog'):
            return self.submit_mardmo_algorithm()
        if catalog.endswith('mardmo-search-catalog'):
            return self.submit_mardmo_search()
        if catalog.endswith('mardmo-interdisciplinary-workflow-catalog'):
            return self.submit_mardmo_workflow()

        # Default fallback if catalog type is unknown
        return render(
            self.request,
            'core/error.html',
            {
                'title': _('Unknown catalog'),
                'errors': [_('Cannot handle this catalog type.')]
            },
            status=400
        )

    def submit_mardmo_model(self):
        """Submit MaRDMO Mathematical Model Documentation."""

        # Check MaRDI Portal Credentials
        if not (self.oauth2_client_id and self.oauth2_client_secret):
            return render(
                self.request,
                'core/error.html',
                {
                    'title': _('Missing Credentials'),
                    'errors': [_('Credentials for MaRDI Portal are missing!')]
                },
                status=200
            )

        answers, *__ = self.get_post_data()
        
        # Validate documentation completeness / consistency
        checker = checks()
        err = checker.run(self.project, answers)
        if err:
            return render(
                self.request,
                'core/error.html',
                {
                    'title': _("Incomplete or Inconsistent Documentation"),
                    'errors': err
                },
                status=200
            )

        # Prepare payload
        try:
            prepare = PrepareModel()
            payload = prepare.export(answers, self.wikibase_url)
        except (ValueError, KeyError) as err:
            return render(
                self.request,
                'core/error.html',
                {
                    'title': _('Value Error'),
                    'errors': [err]
                },
                status=200
            )

        return self.post(self.request, payload)


    def submit_mardmo_algorithm(self):
        """Submit MaRDMO Algorithm Documentation."""

        # Check MathAlgoDB Credentials
        if not (self.mathalgodb_id and self.mathalgodb_secret):
            return render(
                self.request,
                'core/error.html',
                {
                    'title': _('Missing Credentials'),
                    'errors': [_('Credentials for MathAlgoDB are missing!')]
                },
                status=200
            )

        answers, *__ = self.get_post_data()

        # Merge answers related to mathematical model
        merged_dict = merge_dicts_with_unique_keys(
            answers,
            [
                'algorithm',
                'problem',
                'software',
                'benchmark',
                'publication'
            ]
        )

        # Generate list of triples
        triple_list, ids = dict_to_triples_mathalgodb(merged_dict)

        # Generate SPARQL query
        query = generate_sparql_insert_with_new_ids_mathalgodb(triple_list)

        try:
            response = requests.post(
                endpoint['mathalgodb']['update'],
                data=query,
                headers={
                    "Content-Type": "application/sparql-update",
                    "Accept": "text/turtle"
                },
                auth=(self.mathalgodb_id, self.mathalgodb_secret),
                verify=False,
                timeout=60
            )
        except requests.RequestException as err:
            return render(
                self.request,
                'core/error.html',
                {'title': _('Request Error'), 'errors': [err]},
                status=500
            )

        if response.status_code == 204:
            ids = update_ids(
                self.project,
                ids,
                queryAlgorithmDocumentation['IDCheck'],
                endpoint['mathalgodb']['sparql'],
                'mathalgodb'
            )
            return render(
                self.request,
                'MaRDMO/algorithmExport.html',
                {'ids': ids, 'mathalgodb_uri': endpoint['mathalgodb']['uri']},
                status=200
            )

        return render(
            self.request,
            'MaRDMO/workflowError.html',
            {'error': 'The algorithm could not be integrated into the MathAlgoDB!'},
            status=200
        )

    def submit_mardmo_search(self):
        """Submit MaRDMO Search Interdisciplinary Workflow, Models, or Algorithms."""

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
        else:
            datatype = "Unknown"
            source = "Unknown"

        return render(
            self.request,
            'MaRDMO/searchResults.html',
            {
                'datatype': datatype,
                'source': source,
                'noResults': answers['no_results'],
                'links': answers['links']
            },
            status=200
        )

    def submit_mardmo_workflow(self):
        """Submit MaRDMO Interdisciplinary Workflow Documentation."""

        # Check MaRDI Portal Credentials
        if not (self.oauth2_client_id and self.oauth2_client_secret):
            return render(
                self.request,
                'core/error.html',
                {
                    'title': _('Missing Credentials'),
                    'errors': [_('Credentials for MaRDI Portal are missing!')]
                },
                status=200
            )

        answers, *__ = self.get_post_data()

        try:
            prepare = prepareWorkflow()
            payload = prepare.export(answers, self.project.title, self.wikibase_url)
        except (ValueError, KeyError) as err:
            return render(
                self.request,
                'core/error.html',
                {
                    'title': _('Value Error'),
                    'errors': [err]
                },
                status=200
            )

        return self.post(self.request, payload)

    def post_success(self, request, init, final):
        '''Display created Items, if Post successful'''
        ids = compare_items(init, final)

        # Links to newly created Entities
        return render(
            request,
            'MaRDMO/portalExport.html',
            {
                'ids': ids,
                'mardi_uri': get_general_item_url
            },
            status=200
        )

    def get_post_data(self):
        '''Function which gathers User Answers for individual catalogs.'''
        options = get_options()

        # MaRDMO: Mathematical Model Documentation
        if str(self.project.catalog).endswith('mardmo-model-catalog'):

            # Load Data for Model & Publication Documentation
            questions = get_questions('model') | get_questions('publication')
            mathmoddb = get_mathmoddb()

            answers = process_question_dict(
                project = self.project,
                questions = questions,
                get_answer = get_answers
            )

            # Retrieve Publications related to Model
            answers = PublicationRetriever.WorkflowOrModel(
                self.project,
                answers,
                options
            )

            # Prepare Mathematical Model (Preview)
            prepare = PrepareModel()
            answers = prepare.preview(answers)

            return answers, options, mathmoddb

        # MaRDMO: Algorithm Documentation
        if str(self.project.catalog).endswith('mardmo-algorithm-catalog'):

            # Load Data for Mathematical Model Documentation
            questions = get_questions('algorithm') | get_questions('publication')
            mathalgodb = get_mathalgodb()

            answers = process_question_dict(
                project = self.project,
                questions = questions,
                get_answer = get_answers
            )

            # Refine Mathematical Model Information
            answers = algorithm_relations(answers)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.Algorithm(
                self.project,
                answers
            )

            return answers, options, mathalgodb

        # MaRDMO: Search Interdisciplinary Workflow, Mathematical Model or Algorithm
        if str(self.project.catalog).endswith('mardmo-search-catalog'):

            # Load Data for Interdisciplinary Workflow, Mathematical Model or Algorithm Search
            questions = get_questions('search')

            answers = process_question_dict(
                project = self.project,
                questions = questions,
                get_answer = get_answers
            )

            # Get Results from MaRDI Resources
            answers = search(
                answers,
                options
            )

            return answers, options

        # MaRDMO: Interdisciplinary Workflow Documentation
        if str(self.project.catalog).endswith('mardmo-interdisciplinary-workflow-catalog'):

            # Load Data for Interdisciplinary Workflow Documentation
            questions = get_questions('workflow') | get_questions('publication')

            answers = process_question_dict(
                project = self.project,
                questions = questions,
                get_answer = get_answers
            )

            # Refine associated Disciplines
            answers = get_discipline(answers)

            # Retrieve Publications related to Workflow
            answers = PublicationRetriever.WorkflowOrModel(
                self.project,
                answers,
                options
            )

            return answers, options

        # Default fallback if catalog type is unknown
        return render(
            self.request,
            'core/error.html',
            {
                'title': _('Unknown catalog'),
                'errors': [_('Cannot handle this catalog type.')]
            },
            status=400
        )
