from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"home/", views.home, name="home"),
    url(r"add/", views.showAddPage, name="showAddPage"),
    url(r"adddata/", views.add, name="add"),
    url(r"showTasks/", views.showTask, name="showTasks"),
    url(r"change(.+)/", views.finishedDay, name="DayFinished"),
    url(r"delete(.+)/", views.delete, name="delete"),
    url(r"analysis/", views.analysis, name="analysis"),
]