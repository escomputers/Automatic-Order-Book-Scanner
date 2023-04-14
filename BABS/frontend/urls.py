from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="dashboard"),
    path("jobs/", views.jobs, name="jobs")
]
