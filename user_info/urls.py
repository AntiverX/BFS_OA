from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.info),
    path('register', views.register),
    path('time_table', views.time_table),
    path('attendance', views.attendance),
    path('my_info', views.my_info),

]