from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="dashboard"),
    path("add-jobs/", views.addjobs, name="addjobs")
]
