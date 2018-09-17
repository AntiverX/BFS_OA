from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.my_summary),
    path('my_summary', views.my_summary),
    path('summary_list', views.summary_list),
    path('report_mode', views.report_mode)
]
