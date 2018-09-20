from django.shortcuts import render, HttpResponse
from user_info.models import User, Target, Plan, weekly_summary, WorkSummary, MeetingRecord
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import time

context = {
    'menus': {'my_info': "我的信息",
              'time_table': "课程表",
              'attendance': "考勤",
              'meeting_record': "会议记录",
              'target': "目标",
              'plan': "计划",
              'my_summary': "周报",
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
    user = User.objects.create_user(username="1234", password="1234")
    user.save()
    return render(request, 'register.html')


@login_required
def attendance(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "under_construction.html", context=context)


def record(request):
    MeetingRecord.objects.create(user_id=1, date="2018-09-18", time="20:17:00", cost_time=60, place="10#102",
                                 theme="马克思主义好", theme_content="学习十九大精神", remark="明天继续学习")
    records = MeetingRecord.objects.all()
    return render(request, 'user_info/meeting_record.html', {'records': records})


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
        type = request.POST['type']
        plan_name = request.POST['plan_name']
        plan_result = request.POST['plan_result']
        is_reviewed = request.POST['is_reviewed']
        head_person = request.POST['head_person']
        affiliated_person = request.POST['affiliated_person']
        planed_time = request.POST['planed_time']
        planed_start_time = request.POST['planed_start_time']
        planed_end_time = request.POST['planed_end_time']
        actual_time = request.POST['actual_time']
        actual_start_time = request.POST['actual_start_time']
        actual_end_time = request.POST['actual_end_time']
        advanced_postponed_time = request.POST['advanced_postponed_time']
        remark = request.POST['remark']
        target = Plan(
            user_id=request.user.id,
            type=type,
            plan_name=plan_name,
            plan_result=plan_result,
            is_reviewed=is_reviewed,
            head_person=head_person,
            affiliated_person=affiliated_person,
            planed_time=planed_time,
            planed_start_time=planed_start_time,
            planed_end_time=planed_end_time,
            actual_time=actual_time,
            actual_start_time=actual_start_time,
            actual_end_time=actual_end_time,
            advanced_postponed_time=advanced_postponed_time,
            remark=remark,
        )
        target.save()
        return render(request, "success.html", context=context)
    else:
        results = Plan.objects.all()
        context['results'] = results
        return render(request, "info/plan.html", context=context)


def work_summary(request):
    context['username'] = request.user.username
    if request.method == "POST":
        type = request.POST['type']
        summary = request.POST['summary']
        average_time = request.POST['average_time']
        man_day = request.POST['man_day']
        natural_day = request.POST['natural_day']
        remark = request.POST['remark']
        target = WorkSummary(
            user_id=request.user.id,
            type=type,
            summary=summary,
            average_time=average_time,
            man_day=man_day,
            natural_day=natural_day,
            remark=remark,
        )
        target.save()
        return render(request, "success.html", context=context)
    else:
        results = WorkSummary.objects.all()
        context['results'] = results
        return render(request, "info/work_summary.html", context=context)


def time_table(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "info/time_table.html", context=context)


def my_info(request):
    # TODO template及逻辑
    context['user'] = request.user
    return render(request, "info/my_info.html", context=context)


@login_required
def my_summary(request):
    week = time.strftime("%W")
    context['username'] = request.user.username
    real_name = request.user.real_name
    if request.method == 'GET':
        submitted_weekly_summary = weekly_summary.objects.filter(week=week, real_name=real_name)
        # return HttpResponse(type(submitted_weekly_summary))
        if len(submitted_weekly_summary) != 0:
            context['submitted_weekly_summary'] = submitted_weekly_summary[0]
        return render(request, 'weekly_summary/my_weekly_summary.html', context=context)
    else:
        this_week_task = request.POST['this_week_task']
        next_week_task = request.POST['next_week_task']
        submitted_weekly_summary = weekly_summary.objects.filter(week=week, real_name=real_name)
        if len(submitted_weekly_summary) != 0:
            submitted_weekly_summary[0].this_week_task = this_week_task
            submitted_weekly_summary[0].next_week_task = next_week_task
            submitted_weekly_summary[0].save()
        else:
            submitted_weekly_summary = weekly_summary(week=week, this_week_task=this_week_task,
                                                      next_week_task=next_week_task, real_name=request.user.real_name)
            submitted_weekly_summary.save()
        return render(request, 'success.html')
