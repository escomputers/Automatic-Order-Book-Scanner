from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="dashboard"),
    path("add-tasks/", views.addtasks, name="addtasks"),
    path("delete-tasks/", views.deletetasks, name="deletetasks")
]
