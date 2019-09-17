from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect
import time
import datetime
from main_site.models import BFS_OA_Config
from user_info.models import User

context = {
}


@login_required
def index(request):
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    return render(request, 'weekly_summary/index.html', context=context)


# 周报列表
@login_required
def summary_list(request):
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    week = int(((datetime.date.today() - BFS_OA_Config.objects.filter()[0].semester_start_time).days) / 7)
    context['username'] = request.user.username
    submitted_weekly_summary = WeeklySummary.objects.filter(week=week)
    context['results'] = submitted_weekly_summary
    return render(request, 'weekly_summary/summary_list.html', context=context)


# 汇报模式
@login_required
def report_mode(request):
    week = int(((datetime.date.today() - BFS_OA_Config.objects.filter()[0].semester_start_time).days) / 7)
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    if request.method == "POST":
        status = request.POST['btn']
        current_weekly_summary = WeeklySummary.objects.get(id=request.POST['target_id'])
        if status == "is_present":
            current_weekly_summary.is_present = True
            current_weekly_summary.is_absent = False
            current_weekly_summary.is_left = False
        elif status == "is_absent":
            current_weekly_summary.is_absent = True
            current_weekly_summary.is_present = False
            current_weekly_summary.is_left = False
        elif status == "is_left":
            current_weekly_summary.is_left = True
            current_weekly_summary.is_absent = False
            current_weekly_summary.is_present = False
        current_weekly_summary.save()
        return HttpResponseRedirect("/weekly_summary/report_mode")
    else:
        submitted_weekly_summary = WeeklySummary.objects.filter(week=week)
        context['results'] = submitted_weekly_summary
        return render(request, 'weekly_summary/report_mode.html', context=context)


# 周报异常名单
@login_required
def name_list(request):
    class AbnormalUser(object):
        real_name = ""
        reason = ""

        def __init__(self, real_name, reason):
            self.real_name = real_name
            self.reason = reason

    week = int(((datetime.date.today() - BFS_OA_Config.objects.filter()[0].semester_start_time).days) / 7)
    if request.method == "GET":
        users = User.objects.filter(is_teacher=False)
        AbnormalUserList = []
        user_name_list = []
        for user in users:
            user_name_list.append(user.real_name)
        users_submitted_weekly_report = WeeklySummary.objects.filter(week=week)
        for user_submitted_weekly_report in users_submitted_weekly_report:
            user_name_list.remove(user_submitted_weekly_report.real_name)
        for name in user_name_list:
            abnormalUser = AbnormalUser(name, "周报未填写")
            AbnormalUserList.append(abnormalUser)
        users_submitted_weekly_report_but_with_other_reason = WeeklySummary.objects.filter(week=week).filter(is_present=False)
        for user_submitted_weekly_report_but_with_other_reason in users_submitted_weekly_report_but_with_other_reason:
            # 请假
            if user_submitted_weekly_report_but_with_other_reason.is_left == True:
                abnormalUser = AbnormalUser(user_submitted_weekly_report_but_with_other_reason.real_name, "请假")
                AbnormalUserList.append(abnormalUser)
            # 未到
            elif user_submitted_weekly_report_but_with_other_reason.is_absent == True:
                abnormalUser = AbnormalUser(user_submitted_weekly_report_but_with_other_reason.real_name, "未到")
                AbnormalUserList.append(abnormalUser)
        context = {
            'results':AbnormalUserList
        }
        return render(request, "weekly_summary/name_list.html", context=context)
