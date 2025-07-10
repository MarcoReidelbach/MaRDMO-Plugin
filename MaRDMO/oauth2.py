import logging
import copy
import requests
import re
import json

from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .utils import replace_in_dict

logger = logging.getLogger(__name__)


class OauthProviderMixin:

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
            _, *args = self.pop_from_session(request, 'request')
            return self.perform_post(request, access_token, *args)
        except ValueError:
            pass

        return self.render_error(request, _('OAuth authorization successful'), _('But no redirect could be found.'))

    def perform_post(self, request, access_token, url, jsons=None, files=None, multipart=None):
        
        init = copy.deepcopy(jsons)
        keys = list(jsons.keys())
        while keys:
            for key in list(jsons.keys()):
                if key in keys and not re.search(r"Item\d{10}", json.dumps(jsons[key].get('payload'))):
                    if not jsons[key]['id']:
                        if key.startswith('RELATION'):
                            if jsons[key]['exists'] == 'false':
                                response = requests.post(jsons[key]['url'], json=jsons[key]['payload'], headers=self.get_authorization_headers(access_token))
                                try:
                                    response.raise_for_status()
                                    jsons[key]['id'] = response.json()['id']
                                    jsons = replace_in_dict(jsons, key, response.json()['id'])
                                except requests.HTTPError:
                                    logger.warning('post error: %s (%s)', response.content, response.status_code)
                                    return self.render_error(request, _('Something went wrong'), _('Could not complete the POST request.'))
                        else:
                            response = requests.post(jsons[key]['url'], json=jsons[key]['payload'], headers=self.get_authorization_headers(access_token))
                            try:
                                response.raise_for_status()
                                jsons[key]['id'] = response.json()['id']
                                jsons = replace_in_dict(jsons, key, response.json()['id'])
                            except requests.HTTPError:
                                if response.status_code == 422:
                                    error_json = response.json()
                                    if error_json.get("code") == "data-policy-violation" and error_json.get("context", {}).get('violation') == 'item-label-description-duplicate':
                                        conflict_id = error_json.get("context", {}).get("violation_context", {}).get("conflicting_item_id")
                                        if conflict_id:
                                            jsons[key]['id'] = conflict_id
                                            jsons = replace_in_dict(jsons, key, conflict_id)
                                else:
                                    logger.warning('post error: %s (%s)', response.content, response.status_code)    
                                    return self.render_error(request, _('Something went wrong'), _('Could not complete the POST request.'))
                    else:
                        jsons = replace_in_dict(jsons, key, jsons[key]['id'])
                    keys.remove(key)
        
        final = jsons
        return self.post_success(request, init, final)

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

    def post_success(self, request, init, final):
        raise NotImplementedError
