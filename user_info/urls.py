from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.register),
    path('time_table', views.time_table),
    path('time_table_list', views.time_table_list),
    path('train', views.train),
    path('my_info', views.my_info, name="user_info_my_info"),
    path('asset', views.asset),
    path('valid', views.valid),
    path('user_info_api', views.user_info_api, name="user_info_my_info"),
    path('user_manage', views.user_manage, name="user_manage"),
    # path('edit_user/<str:username>/', views.edit_user, name="edit_user"),
]
