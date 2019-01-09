from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect
from topic_manager.models import WeeklySummary
import time
import datetime
from main_site.models import BFS_OA_Config

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
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    week = time.strftime("%W")
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
        submitted_weekly_summary = WeeklySummary.objects.filter(week=int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1])).filter(is_present=False, is_absent=False, is_left=False)
        context['results'] = submitted_weekly_summary
        return render(request, 'weekly_summary/report_mode.html', context=context)

# 周报异常名单
@login_required
def name_list(request):
    if request.method == "GET":
        context = {}
        return render(request,"weekly_summary/name_list.html",context=context)