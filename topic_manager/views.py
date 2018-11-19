"""
课题管理页面的所有view
Author：Antiver
"""

from django.shortcuts import render, HttpResponse
from topic_manager.models import MeetingRecord, Target, Plan, WorkSummary, WeeklySummary
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
import re
from main_site.models import BFS_OA_Config
import time

context = {
    'menus': {
        'target': "目标",
        'plan': "计划",
        'weekly_summary': "周报",
        'meeting_record': "会议记录",
        'work_summary': "工作总结",
    },
}


@login_required
def topic_manager(request):
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    context['current_semester_week'] = int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1])
    return render(request, 'index/index.html', context=context)


# 目标
@login_required
def target(request):
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    context['current_semester_week'] = int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1])
    if request.method == "POST":
        expected_result = request.POST['expected_result']
        content = request.POST['content']
        time_consumed = request.POST['time_consumed']
        end_of_term_summary = request.POST['end_of_term_summary']
        semester = request.POST['semester']
        fill_time = request.POST['date']
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            if request.POST['btn'] == "delete":
                submitted_target = Target.objects.get(id=target_id)
                submitted_target.delete()
            else:
                submitted_target = Target.objects.get(id=target_id)
                submitted_target.expected_result = expected_result
                submitted_target.content = content
                submitted_target.time_consumed = time_consumed
                submitted_target.end_of_term_summary = end_of_term_summary
                submitted_target.time = fill_time
                submitted_target.semester = semester
                try:
                    submitted_target.save()
                except (ValueError, ValidationError) as err:
                    context['error'] = err
                    return render(request, 'error.html', context=context)
            return HttpResponseRedirect('/topic_manager/target')
        else:
            submitted_target = Target(
                user=request.user,
                expected_result=expected_result,
                content=content,
                time_consumed=time_consumed,
                end_of_term_summary=end_of_term_summary,
                time=fill_time,
                semester=semester
            )
            try:
                submitted_target.save()
            except (ValueError, ValidationError) as err:
                context['error'] = err
                return render(request, 'error.html', context=context)
            return HttpResponseRedirect('/topic_manager/target')
    else:
        results = Target.objects.filter(user=request.user)
        context['results'] = results
        return render(request, "topic_manager/target.html", context=context)


# 计划
@login_required
def plan(request):
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    context['current_semester_week'] = int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1])
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
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            existing_target = Plan.objects.get(id=target_id)
            if request.POST['btn'] == "delete":
                existing_target.delete()
            else:
                existing_target.type = type
                existing_target.plan_name = plan_name
                existing_target.plan_result = plan_result
                existing_target.is_reviewed = is_reviewed
                existing_target.head_person = head_person
                existing_target.affiliated_person = affiliated_person
                existing_target.planed_start_time = planed_start_time
                existing_target.planed_end_time = planed_end_time
                existing_target.actual_time = actual_time if actual_time != "" else None
                existing_target.actual_start_time = actual_start_time if actual_start_time != "" else None
                existing_target.actual_end_time = actual_end_time if actual_end_time != "" else None
                existing_target.advanced_postponed_time = advanced_postponed_time
                existing_target.remark = remark
                try:
                    existing_target.save()
                except (ValueError, ValidationError) as err:
                    context['error'] = err
                    return render(request, 'error.html', context=context)
        else:
            new_plan = Plan(
                user=request.user,
                type=type,
                plan_name=plan_name,
                plan_result=plan_result,
                is_reviewed=is_reviewed,
                head_person=head_person,
                affiliated_person=affiliated_person,
                planed_time=planed_time,
                planed_start_time=planed_start_time,
                planed_end_time=planed_start_time,
                actual_time=actual_time if actual_time != "" else None,
                actual_start_time=actual_start_time if actual_start_time != "" else None,
                actual_end_time=actual_end_time if actual_end_time != "" else None,
                advanced_postponed_time=advanced_postponed_time,
                remark=remark,
            )
            new_plan.save()
            try:
                new_plan.save()
            except (ValueError, ValidationError) as err:
                context['error'] = err
                return render(request, 'error.html', context=context)
        return HttpResponseRedirect('/topic_manager/plan')
    else:
        results = Plan.objects.filter(user=request.user)
        context['results'] = results
        return render(request, "topic_manager/plan.html", context=context)


# 周报
@login_required
def weekly_summary(request):
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    context['current_semester_week'] = int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1])
    if request.method == 'POST':
        average_work_hour = request.POST['average_work_hour']
        absent_hour = request.POST['absent_hour']
        this_week_task = request.POST['this_week_task']
        next_week_task = request.POST['next_week_task']
        week = request.POST['week']
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            submitted_weekly_summary = WeeklySummary.objects.get(id=target_id)
            if request.POST['btn'] == "delete":
                submitted_weekly_summary.delete()
            else:
                submitted_weekly_summary.average_work_hour = average_work_hour
                submitted_weekly_summary.absent_hour = absent_hour
                submitted_weekly_summary.this_week_task = this_week_task
                submitted_weekly_summary.next_week_task = next_week_task
                submitted_weekly_summary.week = week
                try:
                    submitted_weekly_summary.save()
                except (ValueError, ValidationError) as err:
                    context['error'] = err
                    return render(request, 'error.html', context=context)
        else:
            week = request.POST['week']
            submitted_weekly_summary = WeeklySummary(user=request.user, week=week, this_week_task=this_week_task,
                                                     next_week_task=next_week_task, real_name=request.user.real_name,
                                                     average_work_hour=average_work_hour, absent_hour=absent_hour)
            try:
                submitted_weekly_summary.save()
            except (ValueError, ValidationError) as err:
                context['error'] = err
                return render(request, 'error.html', context=context)
        return HttpResponseRedirect('/topic_manager/weekly_summary')
    else:
        weekly_summary = WeeklySummary.objects.filter(user=request.user)
        weekly_summarys = weekly_summary.order_by('week')
        context['weekly_summarys'] = weekly_summarys
        return render(request, 'topic_manager/weekly_summary.html', context=context)


# 会议记录
@login_required
def record(request):
    context['current_semester_week'] = int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1])
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None

    if request.method == "POST":
        date = request.POST['date']
        start_time = request.POST['time']
        cost_time = request.POST['cost_time']
        place = request.POST['place']
        theme = request.POST['theme']
        theme_content = request.POST['theme_content']
        remark = request.POST['remark']
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            existing_record = MeetingRecord.objects.get(id=target_id)
            if request.POST['btn'] == "delete":
                existing_record.delete()
            else:
                existing_record.date = date
                existing_record.time = start_time
                existing_record.cost_time = cost_time
                existing_record.place = place
                existing_record.theme = theme
                existing_record.theme_content = theme_content
                existing_record.remark = remark
                try:
                    existing_record.save()
                except (ValueError, ValidationError) as err:
                    context['error'] = err
                    return render(request, 'error.html', context=context)
        else:
            new_record = MeetingRecord(
                user=request.user, date=date, time=time, cost_time=cost_time, place=place,
                theme=theme, theme_content=theme_content, remark=remark
            )
            try:
                new_record.save()
            except (ValueError, ValidationError) as err:
                context['error'] = err
                return render(request, 'error.html', context=context)
        return HttpResponseRedirect('/topic_manager/meeting_record')
    else:
        results = MeetingRecord.objects.filter(user=request.user)
        context['results'] = results
        return render(request, "topic_manager/meeting_record.html", context=context)


# 工作总结
@login_required
def work_summary(request):
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    context['current_semester_week'] = int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1])
    if request.method == "POST":
        type = request.POST['type']
        summary = request.POST['summary']
        average_time = request.POST['average_time']
        man_day = request.POST['man_day']
        natural_day = request.POST['natural_day']
        remark = request.POST['remark']
        date = request.POST['date']
        all_days = request.POST['all_days']
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            existing_record = WorkSummary.objects.get(id=target_id)
            if request.POST['btn'] == "delete":
                existing_record.delete()
            else:
                existing_record.type = type
                existing_record.summary = summary
                existing_record.average_time = average_time
                existing_record.man_day = man_day
                existing_record.natural_day = natural_day
                existing_record.remark = remark
                existing_record.all_days = all_days
                existing_record.save()
        else:
            new_work_summary = WorkSummary(
                user=request.user,
                type=type,
                summary=summary,
                average_time=average_time,
                man_day=man_day,
                natural_day=natural_day,
                remark=remark,
                date=date,
                all_days=all_days
            )
            try:
                new_work_summary.save()
            except (ValueError, ValidationError) as err:
                context['error'] = err
                return render(request, 'error.html', context=context)
        return HttpResponseRedirect('/topic_manager/work_summary')
    else:
        results = WorkSummary.objects.filter(user=request.user)
        context['results'] = results
        return render(request, "topic_manager/work_summary.html", context=context)


@login_required
def valid(request):
    if request.method == "POST":
        class_name = request.POST['class_name']
        value = request.POST['value']

        if class_name == "semester":
            if re.match(r'[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]-[1,2]', value) is not None:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的学期")
        elif class_name == "time_consumed":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的用时")
        elif class_name == "expected_result":
            if len(value):
                return HttpResponse("OK")
            else:
                return HttpResponse("不能没有预期成果")
        elif class_name == "content":
            if len(value):
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确内容")
        elif class_name == "week":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确工作周")
        elif class_name == "average_work_hour":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确工作周")
        elif class_name == "this_week_task":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确工作周")
        elif class_name == "next_week_task":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确工作周")
        elif class_name == "cost_time":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确工作周")
        elif class_name == "theme":
            if len(value) != 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确工作周")
        elif class_name == "remark":
            if len(value) != 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确工作周")
        elif class_name == "theme_content":
            if len(value) != 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确工作周")
        elif class_name == "average_time":
            if re.match(r"[0-9]{1,2}.[0-9]/[0-9]{1,2}.[0-9]", value) is not None:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确平均工作小时")
        elif class_name == "summary":
            if len(value) != 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确平均工作小时")
        elif class_name == "man_day":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的人日")
        elif class_name == "natural_day":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的自然日")
