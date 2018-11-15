from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect
from topic_manager.models import WeeklySummary
import time
from main_site.models import BFS_OA_Config

current_week = time.strftime("%W")
start_week = BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1]
current_semester_week = int(current_week) - int(start_week)

context = {
    'menus': {
        'summary_list': "周报列表",
        'report_mode': "汇报模式"
    },
    'config': BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None,
    'current_semester_week': current_semester_week,
}


@login_required
def index(request):
    context['username'] = request.user.username
    return render(request, 'index/index.html', context=context)


@login_required
def summary_list(request):
    week = current_semester_week
    context['username'] = request.user.username
    submitted_weekly_summary = WeeklySummary.objects.filter(week=week)
    context['results'] = submitted_weekly_summary
    return render(request, 'weekly_summary/summary_list.html', context=context)


# 汇报模式
@login_required
def report_mode(request):
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
        context['username'] = request.user.username
        submitted_weekly_summary = WeeklySummary.objects.all()
        # if len(submitted_weekly_summary) != 0:
        #     current_weekly_summary = {}
        #     current_weekly_summary['real_name'] = submitted_weekly_summary[0].real_name
        #     current_weekly_summary['this_week_task'] = submitted_weekly_summary[0].this_week_task.replace("\n", "<br>")
        #     current_weekly_summary['next_week_task'] = submitted_weekly_summary[0].next_week_task.replace("\n", "<br>")
        #     context['current_weekly_summary'] = current_weekly_summary
        context['results'] = submitted_weekly_summary
        return render(request, 'weekly_summary/report_mode.html', context=context)
