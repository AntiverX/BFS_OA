from django.shortcuts import render, HttpResponse
from user_info.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required
def info(request):
    context = {
        'menus': {'my_info': "我的信息",
                  'schedule': "课程表",
                  'attendance': "考勤",
                  'meeting_record': "会议记录",
                  'target': "目标",
                  'plan': "计划",
                  'weekly_summary': "周报",
                  'work_summary': "工作总结"
                  },
        'username': request.user.username,
    }
    return render(request, 'index.html', context=context)


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
    user = User.objects.create_user(username="Antiver", password="wang@85#2")
    user.save()
    return render(request, 'register.html')
