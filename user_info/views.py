from django.shortcuts import render, HttpResponse
from user_info.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import time

context = {
    'menus': {'my_info': "我的信息",
              'time_table': "课程表",
              'attendance': "考勤",
              'asset': "资产"
              }
}


@login_required
def info(request):
    context['username'] = request.user.username
    return render(request, 'info/info.html', context=context)


def auth(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("auth failed!")
    else:
        return render(request, 'login.html')


@login_required
def deauth(request):
    logout(request)
    return HttpResponseRedirect("/")


def register(request):
    user = User.objects.create_user(username="1234", password="1234")
    user.save()
    return render(request, 'register.html')


@login_required
def attendance(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "under_construction.html", context=context)


def time_table(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "info/time_table.html", context=context)


def my_info(request):
    # TODO template及逻辑
    context['user'] = request.user
    return render(request, "info/my_info.html", context=context)



