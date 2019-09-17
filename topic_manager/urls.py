from django.contrib import admin
from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path('^$', views.topic_manager),
    re_path('^meeting_record$', views.record),
    re_path('^target$', views.target),
    re_path('^plan$', views.plan),
    re_path('^weekly_summary$', views.weekly_summary),
    re_path('^work_summary$', views.work_summary),
    re_path('^work_achievement$', views.work_achievement),
    re_path('^achievement_quantization$', views.achievement_quantization),
    re_path('^achievement_quantization_confirmation$', views.achievement_quantization_confirmation),
    re_path('^scholar_report$', views.scholar_report),
    re_path('^paper$', views.paper),
    re_path('^award$', views.award),
    re_path('^patent$', views.patent),
    re_path('^software$', views.software),
    re_path('^valid$', views.valid),
]
