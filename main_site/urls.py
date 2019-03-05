from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('^settings$', views.settings, name="setting"),
    re_path('^users_management$', views.users_management),
    re_path('^semester$', views.semester),
]
