from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("", views.tasks, name="tasks"),
    path("delete-tasks/", views.deletetasks, name="deletetasks"),
    path("charts/", views.charts, name="charts"),
=======
    path("", views.home, name="dashboard"),
    path("add-tasks/", views.addtasks, name="addtasks"),
    path("delete-tasks/", views.deletetasks, name="deletetasks"),
    path("charts/", views.charts, name="charts")
>>>>>>> main
]
