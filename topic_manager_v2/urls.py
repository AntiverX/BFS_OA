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
    path('upload_history', views.upload_history),
    path('upload_history_api', views.upload_history_api),
    path('status', views.upload_status),
    path('status_api', views.upload_status_api),
    path('sen_email_to_luosenlin', views.sen_email_to_luosenlin, name="sen_email_to_luosenlin"),
]
