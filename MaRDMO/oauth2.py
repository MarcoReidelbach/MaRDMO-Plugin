'''Functions for OAuth2 Authorization'''

import logging
import copy
import re
import json
import time
import random

from urllib.parse import urlencode

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .helpers import replace_in_dict

logger = logging.getLogger(__name__)


class OauthProviderMixin:
    '''Class containing functions for the authorization, post, and
       callback related to the OAuth2 protocoll.'''
    def post(self, request, jsons=None):
        '''Start the Posting Process'''
        self.store_in_session(request, 'request', ('post', jsons))
        return self.authorize(request)

    def authorize(self, request):
        '''Authorize for Posting'''
        state = get_random_string(length=32)
        self.store_in_session(request, 'state', state)
        url = self.authorize_url + '?' + urlencode(self.get_authorize_params(request, state))
        return HttpResponseRedirect(url)

    def callback(self, request):
        '''Ensure the Callback'''
        if request.GET.get('state') != self.pop_from_session(request, 'state'):
            return self.render_error(
                request,
                _('OAuth authorization not successful'),
                _('State parameter did not match.')
            )

        # Exchange the authorization code for an access token
        url = self.token_url + '?' + urlencode(self.get_callback_params(request))
        response = requests.post(
            url,
            self.get_callback_data(request),
            auth=self.get_callback_auth(request),
            headers=self.get_callback_headers(request),
            timeout = 10
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error(
                'callback error: %s (%s)',
                response.content,
                response.status_code
            )
            raise e

        response_data = response.json()
        access_token = response_data.get('access_token')

        # Replay the original request with the new access token
        try:
            _method, jsons = self.pop_from_session(request, 'request')
            return self.perform_post(
                request,
                access_token,
                jsons
            )
        except ValueError:
            pass

        return self.render_error(
            request,
            _('OAuth authorization successful'),
            _('But no redirect could be found.')
        )

    def perform_post(self, request, access_token, jsons=None):
        """Perform the actual Post"""
        init = copy.deepcopy(jsons)
        keys = list(jsons.keys())

        while keys:
            for key in list(jsons.keys()):
                if key not in keys:
                    continue

                payload = jsons[key].get("payload")
                url = jsons[key].get("url")

                if re.search(r"Item\d{10}", json.dumps(payload)):
                    continue
                if re.search(r"Item\d{10}", json.dumps(url)):
                    continue

                try:
                    if not jsons[key]['id']:
                        jsons = self._post_data(key, jsons, access_token)
                    else:
                        jsons = replace_in_dict(jsons, key, jsons[key]['id'])
                except RuntimeError as err:
                    return self.render_error(
                        request,
                        _('Something went wrong'),
                        str(err)
                    )

                time.sleep(0.1)

                keys.remove(key)

        final = jsons
        return self.post_success(request, init, final)

    def _post_data(self, key, jsons, access_token):
        """Post data for a single key, handles both relations and items, with retries and backoff."""
        item = jsons[key]

        # Skip existing relations
        if key.startswith('RELATION') and item.get('exists') == 'true':
            return jsons

        # Reuse a requests.Session() to improve performance
        session = getattr(self, "_session", None)
        if session is None:
            session = requests.Session()
            self._session = session

        url = item['url']
        payload = item['payload']
        headers = self.get_authorization_headers(access_token)
        response = None

        for attempt in range(1, 5 + 1):
            try:
                response = session.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                wait = 0.1 + random.uniform(0, 0.5)
                time.sleep(wait)
                return self._handle_response(response, key, jsons)

            except requests.exceptions.Timeout:
                wait = 1.5 ** attempt + random.uniform(0, 0.5)
                logger.warning(f"Timeout while posting {key} (attempt {attempt}/{5}), retrying in {wait:.2f}s")
                time.sleep(wait)
                continue

            except requests.exceptions.ConnectionError as exc:
                wait = 1.5 ** attempt + random.uniform(0, 0.5)
                logger.warning(f"Connection error posting {key}: {exc} (attempt {attempt}/{5}), retrying in {wait:.2f}s")
                time.sleep(wait)
                continue

            except requests.HTTPError as exc:
                status = response.status_code if response else "no_response"
                content = response.text if response else "n/a"

                if status == 429:  # Too Many Requests
                    retry_after = int(response.headers.get("Retry-After", 5))
                    logger.warning(f"Rate limit hit for {key}, waiting {retry_after}s before retry")
                    time.sleep(retry_after)
                    continue

                if isinstance(status, int) and status >= 500:  # Server-side transient error
                    wait = 1.5 ** attempt + random.uniform(0, 0.5)
                    logger.warning(f"Server error {status} posting {key}, retrying in {wait:.2f}s")
                    time.sleep(wait)
                    continue

                if status == 422:
                    return self._handle_policy_violation(response, key, jsons)

                logger.error(f"HTTP error posting {key}: {status} - {content}")
                raise RuntimeError(_("POST request failed")) from exc

            except requests.exceptions.RequestException as exc:
                logger.error(f"Unexpected request error while posting {key}: {exc}")
                raise RuntimeError(_("Unexpected network error")) from exc

        # If we reach this point, all retries failed
        logger.error(f"POST {url} failed after {5} retries")
        raise RuntimeError(_("POST request failed after multiple retries"))

    def _handle_response(self, response, key, jsons):
        """Handle POST response and update placeholders.
           Returns updated jsons or raises on error.
        """
        try:
            response.raise_for_status()
            jsons[key]['id'] = response.json()['id']
            return replace_in_dict(jsons, key, response.json()['id'])

        except requests.HTTPError as exc:
            if response.status_code == 422:
                return self._handle_policy_violation(response, key, jsons)

            logger.warning('post error: %s (%s)', response.content, response.status_code)
            raise RuntimeError(_("POST request failed")) from exc


    def _handle_policy_violation(self, response, key, jsons):
        """Handle data-policy-violation errors and return updated jsons"""
        error_json = response.json()
        if error_json.get("code") == "data-policy-violation":
            violation = error_json.get("context", {}).get("violation")
            if violation == 'item-label-description-duplicate':
                conflict_id = (
                    error_json["context"]
                    .get("violation_context", {})
                    .get("conflicting_item_id")
                )
                if conflict_id:
                    jsons[key]['id'] = conflict_id
                    return replace_in_dict(jsons, key, conflict_id)

        # No fix possible → just return unchanged jsons
        return jsons

    def render_error(self, request, title, message):
        '''Render Error'''
        return render(request, 'core/error.html', {'title': title, 'errors': [message]}, status=200)

    def get_session_key(self, key):
        '''Get Session Key'''
        return f'{self.class_name}.{key}'

    def store_in_session(self, request, key, data):
        '''Store in Session'''
        session_key = self.get_session_key(key)
        request.session[session_key] = data

    def get_from_session(self, request, key):
        '''Get from Session'''
        session_key = self.get_session_key(key)
        return request.session.get(session_key)

    def pop_from_session(self, request, key):
        '''Pop from Session'''
        session_key = self.get_session_key(key)
        return request.session.pop(session_key, None)

    def get_authorization_headers(self, access_token):
        '''Get Authorization Header'''
        return {'Authorization': f'Bearer {access_token}'}

    def get_authorize_params(self, request, state):
        '''Get Authorization Parameter'''
        raise NotImplementedError

    def get_callback_auth(self, request):
        '''Get Callback Authorization'''
        return None

    def get_callback_headers(self, request):
        '''Get Callback Headers'''
        return {'Accept': 'application/json'}

    def get_callback_params(self, request):
        '''Get Callback Parameters'''
        return {}

    def get_callback_data(self, request):
        '''Get Callback Data'''
        return {}

    def post_success(self, request, init, final):
        '''Post Success'''
        raise NotImplementedError
