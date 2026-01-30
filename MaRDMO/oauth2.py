'''Functions for OAuth2 Authorization with live progress tracking and redirect'''

import logging
import copy
import time
import random
import threading

from urllib.parse import urlencode

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .helpers import replace_in_dict, compare_items
from .store import _register_job_for_session

logger = logging.getLogger(__name__)

# Global in-memory progress store
_progress_store = {}


class OauthProviderMixin:
    '''Class containing functions for the authorization, post, and
       callback related to the OAuth2 protocol.'''

    # ------------------- OAUTH FLOW -------------------

    def post(self, request, jsons=None, dependency=None):
        '''Start the Posting Process'''
        self.store_in_session(request, 'request', ('post', jsons, dependency))
        return self.authorize(request)

    def authorize(self, request):
        '''Authorize for Posting'''
        state = get_random_string(length=32)
        self.store_in_session(request, 'state', state)
        url = self.authorize_url + '?' + urlencode(self.get_authorize_params(request, state))
        return HttpResponseRedirect(url)

    def callback(self, request):
        '''OAuth callback after user authorization'''
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
            timeout=10
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.error('callback error: %s (%s)', response.content, response.status_code)
            return self.render_error(
                request,
                _('OAuth process failed'),
                e
            )

        response_data = response.json()
        access_token = response_data.get('access_token')

        # Retrieve the original post request data

        # Retrieve the original post request data
        data = self.pop_from_session(request, 'request')
        if not data:
            return self.render_error(
                request,
                _('OAuth authorization successful'),
                _('But no redirect could be found.'),
            )

        _method, jsons, dependency = data

        # ------------------- ASYNC POSTING -------------------

        # Generate job ID and store initial progress in the cache
        job_id = get_random_string(16)
        _register_job_for_session(request, job_id)
        _progress_store[job_id] = {
            "progress": 0,
            "done": False,
            "phase": "starting",
            "error": None,
        }

        # Start posting thread
        thread = threading.Thread(
            target=self._background_post,
            args=(request, access_token, jsons, dependency, job_id),
            daemon=True,
        )
        thread.start()

        # Immediately render progress page
        return HttpResponseRedirect(
            reverse("show_progress", args=[job_id])
        )

    # ------------------- BACKGROUND PROCESS -------------------

    def _background_post(self, request, access_token, jsons, dependency, job_id):
        """
        Run the Wikibase posting in the background.
        Posts all 'Item*' payloads first, then all 'RELATION*' payloads.
        Updates _progress_store[job_id] continuously with phase and progress info.
        """

        logger.info("[%s] Background posting started", job_id)

        try:
            keys = list(jsons.keys())

            # --- Separate item and relation keys
            item_keys = list(dependency)
            relation_keys = [k for k in keys if k.startswith(("RELATION", "ALIAS"))]

            num_items = len(item_keys)
            num_relations = len(relation_keys)
            total = num_items + num_relations
            completed = 0

            init = copy.deepcopy(jsons)

            # --- Phase 1: Items
            _progress_store[job_id] = {"progress": 0, "done": False, "phase": "items"}
            logger.info("[%s] Starting item upload: %s items", job_id, num_items)

            for key in item_keys:
                try:
                    jsons = self._post_data(key, jsons, access_token)
                except RuntimeError as err:
                    logger.exception("[%s] Failed posting item %s: %s", job_id, key, err)
                    _progress_store[job_id] = {
                        "progress": int((completed / total) * 100),
                        "done": True,
                        "phase": "error",
                        "error": f"Error posting item {key}: {err}",
                    }
                    return

                completed += 1
                _progress_store[job_id] = {
                    "progress": int((completed / total) * 100),
                    "done": False,
                    "phase": "items",
                }
                time.sleep(0.1)

            # --- Phase 2: Relations
            _progress_store[job_id] = {
                "progress": int((completed / total) * 100),
                "done": False,
                "phase": "relations",
            }
            logger.info("[%s] Starting relation upload: %s relations", job_id, num_relations)

            for key in relation_keys:
                try:
                    jsons = self._post_data(key, jsons, access_token)
                except RuntimeError as err:
                    logger.exception("[%s] Failed posting relation %s: %s", job_id, key, err)
                    _progress_store[job_id] = {
                        "progress": int((completed / total) * 100),
                        "done": True,
                        "phase": "error",
                        "error": f"Error posting relation {key}: {err}",
                    }
                    return

                completed += 1
                _progress_store[job_id] = {
                    "progress": int((completed / total) * 100),
                    "done": False,
                    "phase": "relations",
                }
                time.sleep(0.1)

            # --- All done
            ids = compare_items(init, jsons)
            _progress_store[job_id] = {
                "progress": 100,
                "done": True,
                "phase": "done",
                "error": None,
                "ids": ids,
                "redirect": request.build_absolute_uri(
                    reverse("show_success", args=[job_id])
                ),
            }

            logger.info(
                "[%s] Posting complete. Redirect -> /services/success/%s/",
                job_id,
                job_id,
            )

        except Exception as e:
            logger.exception("[%s] Unexpected error: %s", job_id, e)
            _progress_store[job_id] = {
                "progress": int((completed / total) * 100) if total else 0,
                "done": True,
                "phase": "error",
                "error": str(e),
            }

    # ------------------- CORE POST LOGIC -------------------

    def _post_data(self, key, jsons, access_token):
        """Post data for a single key, handles both relations and items."""

        # No Post, if key not in Payload
        if not jsons.get(key):
            return jsons

        item = jsons[key]

        # No Post, if item already on Portal
        if key.startswith('Item') and item.get('id'):
            return replace_in_dict(jsons, key, item['id'])

        # No Post, if relation already on Portal
        if key.startswith('RELATION') and item.get('exists') == 'true':
            return jsons

        session = getattr(self, "_session", None)
        if session is None:
            session = requests.Session()
            self._session = session

        url = item['url']
        payload = item['payload']
        headers = self.get_authorization_headers(access_token)
        response = None

        for attempt in range(1, 6):
            try:
                response = session.post(url, json=payload, headers=headers, timeout=120)
                response.raise_for_status()
                wait = 0.1 + random.uniform(0, 0.5)
                time.sleep(wait)
                return self._handle_response(response, key, jsons)

            except requests.exceptions.Timeout:
                time.sleep(1.5 ** attempt + random.uniform(0, 0.5))
                continue

            except requests.exceptions.ConnectionError:
                time.sleep(1.5 ** attempt + random.uniform(0, 0.5))
                continue

            except requests.HTTPError as exc:
                resp = exc.response
                status = resp.status_code if resp is not None else "no_response"
                if status == 429:
                    retry_after = int(resp.headers.get("Retry-After", 5))
                    time.sleep(retry_after)
                    continue
                if status == 403:
                    time.sleep(1.5 ** attempt + random.uniform(0, 0.5))
                    continue
                if isinstance(status, int) and status >= 500:
                    time.sleep(1.5 ** attempt + random.uniform(0, 0.5))
                    continue
                if status == 422:
                    return self._handle_policy_violation(resp, key, jsons)
                raise RuntimeError(_("POST request failed")) from exc

        raise RuntimeError(_("POST request failed after multiple retries"))

    def _handle_response(self, response, key, jsons):
        """Handle POST response and update placeholders."""
        response.raise_for_status()
        if not key.startswith("ALIAS"):
            jsons[key]['id'] = response.json().get('id')
            jsons = replace_in_dict(jsons, key, jsons[key]['id'])
        return jsons

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
        return jsons

    # ------------------- HELPERS -------------------

    def render_error(self, request, title, message):
        '''Function to Render Errors'''
        return render(
            request,
            'core/error.html',
            {
                'title': title,
                'errors': [message]
            },
            status=200
        )

    def get_session_key(self, key):
        '''Function to get Session Key'''
        return f'{self.class_name}.{key}'

    def store_in_session(self, request, key, data):
        '''Function to store in Session'''
        request.session[self.get_session_key(key)] = data

    def pop_from_session(self, request, key):
        '''Function to pop from Session'''
        return request.session.pop(self.get_session_key(key), None)

    def get_from_session(self, request, key):
        '''Function to get from Session'''
        session_key = self.get_session_key(key)
        return request.session.get(session_key)

    def get_authorization_headers(self, access_token):
        '''Function to get Authorization Headers'''
        return {'Authorization': f'Bearer {access_token}'}

    def get_authorize_params(self, request, state):
        '''Function to get Authorize Parameters'''
        raise NotImplementedError

    def get_callback_auth(self, request):
        '''Function to get Callback Authoriaztion'''
        return None

    def get_callback_headers(self, request):
        '''Function to get Callback Headers'''
        return {'Accept': 'application/json',
                'User-Agent': 'MaRDMO (https://zib.de; reidelbach@zib.de)'}

    def get_callback_params(self, request):
        '''Function to get Callback Parameters'''
        return {}

    def get_callback_data(self, request):
        '''Function to get Callback Data'''
        return {}

    def post_success(self, request, init, final):
        '''Function for Post Success'''
        raise NotImplementedError
