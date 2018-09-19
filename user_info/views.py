from django.shortcuts import render, HttpResponse
from user_info.models import User, Target, Plan
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

context = {
    'menus': {'my_info': "我的信息",
              'time_table': "课程表",
              'attendance': "考勤",
              'meeting_record': "会议记录",
              'target': "目标",
              'plan': "计划",
              'weekly_summary': "周报",
              'work_summary': "工作总结"
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
    user = User.objects.create_user(username="Antiver", password="wang@85#2")
    user.save()
    return render(request, 'register.html')


@login_required
def attendance(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "under_construction.html", context=context)


def meeting_record(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "under_construction.html", context=context)


def target(request):
    context['username'] = request.user.username
    if request.method == "POST":
        expected_result = request.POST['expected_result']
        content = request.POST['content']
        time_consumed = request.POST['time_consumed']
        target = Target(user_id=request.user.id, expected_result=expected_result, content=content,
                        time_consumed=time_consumed)
        target.save()
        return render(request, "success.html", context=context)
    else:
        results = Target.objects.all()
        context['results'] = results
        return render(request, "info/target.html", context=context)


def plan(request):
    context['username'] = request.user.username
    if request.method == "POST":
        expected_result = request.POST['expected_result']
        content = request.POST['content']
        time_consumed = request.POST['time_consumed']
        target = Target(user_id=request.user.id, expected_result=expected_result, content=content,
                        time_consumed=time_consumed)
        target.save()
        return render(request, "success.html", context=context)
    else:
        results = Plan.objects.all()
        context['results'] = results
        return render(request, "info/plan.html", context=context)


def work_summary(request):
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
