from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('summary_list', views.summary_list, name="summary_list"),
    path('report_mode', views.report_mode, name="report_mode"),
    path('name_list', views.name_list, name="name_list"),
]
