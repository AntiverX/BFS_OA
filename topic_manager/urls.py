from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.topic_manager),
    path('meeting_record', views.record),
    path('target', views.target),
    path('plan', views.plan),
    path('work_summary', views.work_summary),
    path('weekly_summary', views.weekly_summary),
    path('valid', views.valid),
]
