'''Module for Storing Data'''

import logging

from django.core.cache import cache

logger = logging.getLogger(__name__)

PROGRESS_CACHE_PREFIX = "mardmo_progress_"
SESSION_JOBS_KEY = "mardmo_jobs"


def _progress_cache_key(job_id):
    '''Progress Cache Key'''
    return f"{PROGRESS_CACHE_PREFIX}{job_id}"


def get_progress_data(job_id, default=None):
    '''Get Progress Data'''
    return cache.get(_progress_cache_key(job_id), default)


def set_progress_data(job_id, value, timeout=60 * 60):
    '''Set Progress Data'''
    cache.set(_progress_cache_key(job_id), value, timeout=timeout)


def clear_progress(job_id):
    '''Clear Progress Data'''
    cache.delete(_progress_cache_key(job_id))


class ProgressStore:
    """Dict-like wrapper around Django's cache for job progress data.

    This allows us to keep existing `_progress_store[...]` usages while
    backing the store with Django's cache backend.
    """

    def __getitem__(self, job_id):
        value = get_progress_data(job_id)
        if value is None:
            raise KeyError(job_id)
        return value

    def __setitem__(self, job_id, value):
        set_progress_data(job_id, value)

    def get(self, job_id, default=None):
        '''Get Progress Data'''
        return get_progress_data(job_id, default)


# Global progress store backed by Django's cache
_progress_store = ProgressStore()


def _register_job_for_session(request, job_id):
    """Remember job_id in the user's session.

    This is used to ensure that only the user who started the job can
    query its progress or see its result.
    """
    jobs = request.session.get(SESSION_JOBS_KEY, [])
    if job_id not in jobs:
        jobs.append(job_id)
        request.session[SESSION_JOBS_KEY] = jobs


def _unregister_job_for_session(request, job_id):
    jobs = request.session.get(SESSION_JOBS_KEY, [])
    if job_id in jobs:
        jobs.remove(job_id)
        request.session[SESSION_JOBS_KEY] = jobs


def _job_belongs_to_session(request, job_id):
    return job_id in request.session.get(SESSION_JOBS_KEY, [])
