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
from django.urls import path, include
from . import views
from user_info import views as user_views

urlpatterns = [
    path('login', user_views.auth),
    path('logout', user_views.deauth),
    path('admin/', admin.site.urls),
    path('', views.index),
    path('info/', include('user_info.urls')),
    path('weekly_summary/', include('weekly_summary.urls')),
    path('monthly_summary/', include('monthly_summary.urls')),
    path('topic_manager/', include('topic_manager.urls')),
    path('bulletin', views.bulletin),
    path('news', views.news),
    path('library', views.library),
]
