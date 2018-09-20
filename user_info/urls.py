from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.info),
    path('register', views.register),
<<<<<<< HEAD
    path('time_table', views.time_table),
    path('attendance', views.attendance),
    path('meeting_record', views.meeting_record),
    path('target', views.target),
    path('plan', views.plan),
    path('weekly_summary', views.work_summary),
    path('work_summary', views.work_summary),
    path('my_info', views.my_info),
    path('my_summary', views.my_summary),
    path('record', views.record),
]
=======
    path('record', views.record),
]
>>>>>>> 71a0bbb9ab9532bcdd2ea7b549afd6760c91841d
