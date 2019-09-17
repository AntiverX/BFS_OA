from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('^settings$', views.settings, name="setting"),
    re_path('^users_management$', views.users_management),
    re_path('^semester$', views.semester),
    re_path('^server_manage$', views.server_manage),
    re_path('^bulletin_and_news_manage$', views.bulletin_and_news_manage),
    path('bulletin', views.bulletin),
    path('news', views.news),
    path('library', views.library),
    path('about', views.about),
    path('competition', views.competition),
    path('upload', views.uploader),
    path('random', views.random_service),
    path('get_current_week', views.get_current_week),
    path('get_current_week_range', views.get_current_week_range),
]
