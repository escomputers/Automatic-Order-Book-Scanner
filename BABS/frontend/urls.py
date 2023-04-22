from django.urls import path
from . import views

urlpatterns = [
    path("", views.tasks, name="tasks"),
    path("delete-tasks/", views.deletetasks, name="deletetasks"),
    path("charts/", views.charts, name="charts"),
    path("symbols/", views.symbols, name="symbols"),
]
