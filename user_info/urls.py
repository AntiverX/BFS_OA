from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.info),
    path('register', views.register),
    path('time_table', views.time_table),
    path('attendance', views.attendance),
    path('meeting_record', views.meeting_record),
    path('target', views.target),
    path('plan', views.plan),
    path('weekly_summary', views.work_summary),
    path('work_summary', views.work_summary)
]
