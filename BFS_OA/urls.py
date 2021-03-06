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
from main_site import views as main_site_views
from user_info import views as user_views

urlpatterns = [
    path('login', user_views.auth),
    path('logout', user_views.deauth),
    path('register', user_views.register),
    # path('admin/', admin.site.urls),
    path('', main_site_views.index),
    path('', include("main_site.urls")),
    path('info/', include('user_info.urls')),
    path('weekly_summary/', include('weekly_summary.urls')),
    path('topic_manager/', include('topic_manager.urls')),
    path('academic_report/', include('academic_report.urls')),
    path('topic_manager_v2/', include('topic_manager_v2.urls')),
    path('newcomer/', include('newcomer.urls')),
    path('system/', include('main_site.urls')),
    path('ftp/',include('ftp_search.urls')),

]
