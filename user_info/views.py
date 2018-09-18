from django.shortcuts import render, HttpResponse
from user_info.models import User, MeetingRecord
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
    user = User.objects.create_user(username="1234", password="1234")
    user.save()
    return render(request, 'register.html')


def record(request):
    MeetingRecord.objects.create(user_id=1, date="2018-09-18", time="20:17:00", cost_time=60, place="10#102",
                                 theme="马克思主义好", theme_content="学习十九大精神", remark="明天继续学习")
    records = MeetingRecord.objects.all()
    return render(request, 'user_info/meeting_record.html', {'records': records})
