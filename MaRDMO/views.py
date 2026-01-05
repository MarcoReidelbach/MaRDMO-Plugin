'''Module containing Views for MaRDMO'''

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET

from MaRDMO.getters import get_item_url
from MaRDMO.oauth2 import _progress_store
from MaRDMO.store import clear_progress, _unregister_job_for_session, _job_belongs_to_session


@login_required
def get_progress(request, job_id):
    """Return JSON progress updates"""
    if not _job_belongs_to_session(request, job_id):
        raise Http404()

    data = _progress_store.get(job_id, {"progress": 0, "done": False})
    return JsonResponse(data)


@login_required
@require_GET
def show_progress(request, job_id):
    """Render the progress bar page"""
    if not _job_belongs_to_session(request, job_id):
        raise Http404()

    return render(request, "MaRDMO/progress.html", {"job_id": job_id})


@login_required
@require_GET
def show_success(request, job_id):
    """Render the Success Page"""
    if not _job_belongs_to_session(request, job_id):
        raise Http404()

    job_data = _progress_store.get(job_id)
    if not job_data or "ids" not in job_data:
        return render(
            request,
            "core/error.html",
            {
                "title": "Not ready",
                "errors": ["Job not found."],
            },
        )

    # Once the success page is shown we can drop the progress entry
    clear_progress(job_id)
    _unregister_job_for_session(request, job_id)

    return render(
        request,
        "MaRDMO/portalExport.html",
        {
            "ids": job_data["ids"],
            "mardi_uri": get_item_url('mardi'),
        },
    )
