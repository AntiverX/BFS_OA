from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('register', views.register),
    path('time_table', views.time_table),
    path('time_table_list', views.time_table_list),
    path('train', views.train),
    path('my_info', views.my_info),
    path('asset', views.asset),
    path('valid', views.valid),

]
