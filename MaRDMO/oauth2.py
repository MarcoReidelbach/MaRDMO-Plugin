import logging
import copy

from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from .utils import replace_in_dict

logger = logging.getLogger(__name__)


class OauthProviderMixin:

    def get(self, request, url):
        # Always require login for GET requests
        self.store_in_session(request, 'request', ('get', url))
        return self.authorize(request)

    def post(self, request, url, jsons=None, files=None, multipart=None):
        # Always require login for POST requests
        self.store_in_session(request, 'request', ('post', url, jsons, files, multipart))
        return self.authorize(request)

    def authorize(self, request):
        # Generate a random state and redirect the user to the OAuth login page
        state = get_random_string(length=32)
        self.store_in_session(request, 'state', state)
        url = self.authorize_url + '?' + urlencode(self.get_authorize_params(request, state))
        return HttpResponseRedirect(url)

    def callback(self, request):
        # Verify the state parameter
        if request.GET.get('state') != self.pop_from_session(request, 'state'):
            return self.render_error(request, _('OAuth authorization not successful'), _('State parameter did not match.'))

        # Exchange the authorization code for an access token
        url = self.token_url + '?' + urlencode(self.get_callback_params(request))
        response = requests.post(
            url,
            self.get_callback_data(request),
            auth=self.get_callback_auth(request),
            headers=self.get_callback_headers(request),
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error('callback error: %s (%s)', response.content, response.status_code)
            raise e

        response_data = response.json()
        access_token = response_data.get('access_token')

        # Replay the original request with the new access token
        try:
            method, *args = self.pop_from_session(request, 'request')
            if method == 'get':
                return self.perform_get(request, access_token, *args)
            elif method == 'post':
                return self.perform_post(request, access_token, *args)
        except ValueError:
            pass

        return self.render_error(request, _('OAuth authorization successful'), _('But no redirect could be found.'))

    def perform_get(self, request, access_token, url):
        response = requests.get(url, headers=self.get_authorization_headers(access_token))
        if response.status_code == 401:
            logger.warning('get forbidden: %s (%s)', response.content, response.status_code)
        else:
            try:
                response.raise_for_status()
                return self.get_success(request, response)
            except requests.HTTPError:
                logger.warning('get error: %s (%s)', response.content, response.status_code)
                return self.render_error(request, _('Something went wrong'), _('Could not complete the GET request.'))

    def perform_post(self, request, access_token, url, jsons=None, files=None, multipart=None):
        
        response = ''
        init = copy.deepcopy(jsons)
        for key in list(jsons.keys()):
            if not jsons[key]['id']:
                if key.startswith('RELATION'):
                    checks = requests.get(f"{jsons[key]['url']}?property={jsons[key]['payload']['statement']['property']['id']}").json()
                    for check in checks.get(jsons[key]['payload']['statement']['property']['id'], []):
                        if check['value']['content'] == jsons[key]['payload']['statement']['value']['content']:
                            break
                    else:
                        response = requests.post(jsons[key]['url'], json=jsons[key]['payload'], headers=self.get_authorization_headers(access_token))
                        try:
                            response.raise_for_status()
                            jsons[key]['id'] = response.json()['id']
                            jsons = replace_in_dict(jsons, key, response.json()['id'])
                        except requests.HTTPError:
                            logger.warning('post error: %s (%s)', response.content, response.status_code)
                            return self.render_error(request, _('Something went wrong'), _('Could not complete the POST request.'))
                        #jsons = replace_in_dict(jsons, key, response.json()['id'])
                else:
                    response = requests.post(jsons[key]['url'], json=jsons[key]['payload'], headers=self.get_authorization_headers(access_token))
                    try:
                        response.raise_for_status()
                        jsons[key]['id'] = response.json()['id']
                        jsons = replace_in_dict(jsons, key, response.json()['id'])
                    except requests.HTTPError:
                        logger.warning('post error: %s (%s)', response.content, response.status_code)
                        return self.render_error(request, _('Something went wrong'), _('Could not complete the POST request.'))
                    #jsons = replace_in_dict(jsons, key, response.json()['id'])
            else:
                jsons = replace_in_dict(jsons, key, jsons[key]['id'])
        final = jsons
        #if not response:
        return self.post_success(request, init, final) #response)
        #elif response.status_code == 401:
        #    logger.warning('post forbidden: %s (%s)', response.content, response.status_code)
        #else:
        #    try:
        #        response.raise_for_status()
        #        return self.post_success(request, response)
        #    except requests.HTTPError:
        #        logger.warning('post error: %s (%s)', response.content, response.status_code)
        #        return self.render_error(request, _('Something went wrong'), _('Could not complete the POST request.'))

    def render_error(self, request, title, message):
        return render(request, 'core/error.html', {'title': title, 'errors': [message]}, status=200)

    def get_session_key(self, key):
        return f'{self.class_name}.{key}'

    def store_in_session(self, request, key, data):
        session_key = self.get_session_key(key)
        request.session[session_key] = data

    def get_from_session(self, request, key):
        session_key = self.get_session_key(key)
        return request.session.get(session_key)

    def pop_from_session(self, request, key):
        session_key = self.get_session_key(key)
        return request.session.pop(session_key, None)

    def get_authorization_headers(self, access_token):
        return {'Authorization': f'Bearer {access_token}'}

    def get_authorize_params(self, request, state):
        raise NotImplementedError

    def get_callback_auth(self, request):
        return None

    def get_callback_headers(self, request):
        return {'Accept': 'application/json'}

    def get_callback_params(self, request):
        return {}

    def get_callback_data(self, request):
        return {}

    def get_success(self, request, response):
        raise NotImplementedError

    def post_success(self, request, init, final):
        raise NotImplementedError
