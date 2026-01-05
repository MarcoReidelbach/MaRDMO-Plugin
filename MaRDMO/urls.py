'''Module containing URLSs for MaRDMO'''

from django.urls import path
from .views import get_progress, show_progress, show_success

urlpatterns = [
    path("progress/<str:job_id>/", show_progress, name="show_progress"),
    path("progress/<str:job_id>/status/", get_progress, name="get_progress"),
    path("success/<str:job_id>/", show_success, name="show_success"),
]
