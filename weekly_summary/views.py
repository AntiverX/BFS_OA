from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect
from user_info.models import weekly_summary
import time

context = {
    'menus': {
        'summary_list': "周报列表",
        'report_mode': "汇报模式"
    }
}


@login_required
def index(request):
    context['username'] = request.user.username
    return render(request, 'index.html', context=context)


@login_required
def summary_list(request):
    week = time.strftime("%W")
    context['username'] = request.user.username
    submitted_weekly_summary = weekly_summary.objects.filter(week=week)
    if len(submitted_weekly_summary) == 0:
        return HttpResponse("no")
    submitted_weekly_summarys = {}
    for data in submitted_weekly_summary:
        submitted_weekly_summarys[str(data.real_name)] = [data.real_name, data.this_week_task.replace("\n", "<br>"),
                                                          data.next_week_task.replace("\n", "<br>")]
    context['submitted_weekly_summarys'] = submitted_weekly_summarys
    return render(request, 'weekly_summary/summary_list.html', context=context)


@login_required
def report_mode(request):
    week = time.strftime("%W")
    if request.method == "POST":
        status = request.POST['btn']
        real_name = request.POST['real_name']
        current_weekly_summary = weekly_summary.objects.get(week=week, real_name=real_name)
        if status == "is_present":
            current_weekly_summary.is_present = True
        elif status == "is_absent":
            current_weekly_summary.is_absent = True
        elif status == "is_left":
            current_weekly_summary.is_left = True
        current_weekly_summary.save()
        return HttpResponseRedirect("/weekly_summary/report_mode")
    context['username'] = request.user.username
    submitted_weekly_summary = weekly_summary.objects.filter(week=week, is_present=False, is_absent=False,
                                                             is_left=False)
    if len(submitted_weekly_summary) != 0:
        current_weekly_summary = {}
        current_weekly_summary['real_name'] = submitted_weekly_summary[0].real_name
        current_weekly_summary['this_week_task'] = submitted_weekly_summary[0].this_week_task.replace("\n", "<br>")
        current_weekly_summary['next_week_task'] = submitted_weekly_summary[0].next_week_task.replace("\n", "<br>")
        context['current_weekly_summary'] = current_weekly_summary
    return render(request, 'weekly_summary/report_mode.html', context=context)
