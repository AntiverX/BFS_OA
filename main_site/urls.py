from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('^settings$', views.settings, name="setting"),
    path('users_management', views.users_management),
]
