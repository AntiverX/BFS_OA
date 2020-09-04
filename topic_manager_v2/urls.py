"""BFS_OA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('index', views.index),
    path('my_daily_report', views.daily_report),
    path('daily_report_summary', views.daily_report_summary),
    path('daily_report_summary_api', views.daily_report_summary_api),
    path('delete_daily_report_summary_api', views.delete_daily_report_summary_api),
    path('group_daily_report_summary', views.group_daily_report_summary),
    path('group_daily_report_summary_api', views.group_daily_report_summary_api),
    path('upload_history', views.upload_history),
    # 周报相关
    path('my_base_weekly_report', views.base_weekly_report),
    path('my_weekly_report', views.weekly_report),
    path('weekly_report_summary', views.weekly_report_summary),
    path('weekly_report_summary_api', views.weekly_report_summary_api),

    path('upload_history_api', views.upload_history_api),
    path('status', views.upload_status),
    path('status_api', views.upload_status_api),
    path('sen_email_to_luosenlin', views.sen_email_to_luosenlin, name="sen_email_to_luosenlin"),
    path('semester_manage', views.semester_manage),
    path('semester_manage_history', views.semester_manage_history),
    path('semester_manage_api', views.semester_manage_api),
    path('edit_semester_api/<str:semester_name>/', views.edit_semester_api),
]
