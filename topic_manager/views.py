"""
课题管理页面的所有view
Author：Antiver
"""

from django.shortcuts import render, HttpResponse
from topic_manager.models import MeetingRecord, Target, Plan, WorkSummary, WeeklySummary, WorkAchievement, AchievementQuantization, AchievementQuantizationConfirmation,ScholarReport
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
import re
import json


@login_required
def topic_manager(request):
    return render(request, 'topic_manager/index.html')


# 目标
@login_required
def target(request):
    if request.method == "POST":
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            submitted_target = Target.objects.get(id=target_id)
            if request.POST['btn'] == "delete":
                submitted_target.delete()
            else:
                submitted_target.expected_result = request.POST['expected_result']
                submitted_target.content = request.POST['content']
                submitted_target.time_consumed = request.POST['time_consumed']
                submitted_target.end_of_term_summary = request.POST['end_of_term_summary']
                submitted_target.time = request.POST['date']
                submitted_target.semester = request.POST['semester']
                try:
                    submitted_target.save()
                except (ValueError, ValidationError) as err:
                    context = {
                        'error': err,
                    }
                    return render(request, 'error.html', context=context)
        else:
            submitted_target = Target(
                user=request.user,
                expected_result=request.POST['expected_result'],
                content=request.POST['content'],
                time_consumed=request.POST['time_consumed'],
                end_of_term_summary=request.POST['end_of_term_summary'],
                time=request.POST['date'],
                semester=request.POST['semester'],
            )
            try:
                submitted_target.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponse('success')
    else:
        results = Target.objects.filter(user=request.user)
        context = {
            'results': results,
        }
        return render(request, "topic_manager/target.html", context=context)


# 计划
@login_required
def plan(request):
    if request.method == "POST":
        if request.POST['target_id'] != "" and request.POST['btn'] == "delete":
            target_id = request.POST['target_id']
            existing_target = Plan.objects.get(id=target_id)
            existing_target.delete()
            return HttpResponseRedirect('/topic_manager/plan')

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
                    context = {
                        'error': err,
                    }
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
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponse('success')
    else:
        results = Plan.objects.filter(user=request.user)
        context = {
            'results': results,
        }
        return render(request, "topic_manager/plan.html", context=context)


# 周报
@login_required
def weekly_summary(request):
    if request.method == 'POST':
        if request.POST['target_id'] != "" and request.POST['btn'] == "delete":
            target_id = request.POST['target_id']
            existing_target = WeeklySummary.objects.get(id=target_id)
            existing_target.delete()
            return HttpResponseRedirect('/topic_manager/weekly_summary')

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
                    context = {
                        'error': err,
                    }
                    return render(request, 'error.html', context=context)
        else:
            submitted_weekly_summary = WeeklySummary(user=request.user, week=week, this_week_task=this_week_task,
                                                     next_week_task=next_week_task, real_name=request.user.real_name,
                                                     average_work_hour=average_work_hour, absent_hour=absent_hour)
            try:
                submitted_weekly_summary.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponse('success')
    else:
        weekly_summary = WeeklySummary.objects.filter(user=request.user)
        weekly_summarys = weekly_summary.order_by('week')
        context = {
            'weekly_summarys': weekly_summarys
        }
        return render(request, 'topic_manager/weekly_summary.html', context=context)


# 会议记录
@login_required
def record(request):
    if request.method == "POST":
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            existing_record = MeetingRecord.objects.get(id=target_id)
            if request.POST['btn'] == "delete":
                existing_record.delete()
            else:
                existing_record.date = request.POST['date']
                existing_record.time = request.POST['time']
                existing_record.cost_time = request.POST['cost_time']
                existing_record.place = request.POST['place']
                existing_record.theme = request.POST['theme']
                existing_record.theme_content = request.POST['theme_content']
                existing_record.remark = request.POST['remark']
                try:
                    existing_record.save()
                except (ValueError, ValidationError) as err:
                    context = {
                        'error': err,
                    }
                    return render(request, 'error.html', context=context)
        else:
            new_record = MeetingRecord(
                user=request.user,
                date=request.POST['date'],
                time=request.POST['time'],
                cost_time=request.POST['cost_time'],
                place=request.POST['place'],
                theme=request.POST['theme'],
                theme_content=request.POST['theme_content'],
                remark=request.POST['remark'],
                real_name=request.user.real_name,
            )
            try:
                new_record.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponse('success')
    else:
        results = MeetingRecord.objects.filter(real_name=request.user.current_user)
        context = {
            'results': results,
        }
        return render(request, "topic_manager/meeting_record.html", context=context)


# 工作总结
@login_required
def work_summary(request):
    if request.method == "POST":
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            existing_record = WorkSummary.objects.get(id=target_id)
            if request.POST['btn'] == "delete":
                existing_record.delete()
            else:
                existing_record.date = request.POST['date']
                existing_record.type = request.POST['type']
                existing_record.summary = request.POST['summary']
                existing_record.average_time = request.POST['average_time']
                existing_record.man_day = request.POST['man_day']
                existing_record.natural_day = request.POST['natural_day']
                existing_record.remark = request.POST['remark']
                days = json.loads(request.POST['man_day'])
                all_days = 0
                for day in days:
                    all_days += int(day)
                existing_record.all_days = all_days
                existing_record.total_man_day = request.POST['total_man_day']
                existing_record.save()
        else:
            days = json.loads(request.POST['man_day'])
            all_days = 0
            for day in days:
                all_days += int(day)
            new_work_summary = WorkSummary(
                user=request.user,
                type=request.POST['type'],
                summary=request.POST['summary'],
                average_time=request.POST['average_time'],
                man_day=request.POST['man_day'],
                natural_day=request.POST['natural_day'],
                remark=request.POST['remark'],
                date=request.POST['date'],
                all_days=all_days,
                total_man_day=request.POST['total_man_day'],
            )
            try:
                new_work_summary.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponse('success')
    else:
        results = WorkSummary.objects.filter(user=request.user)
        context = {
            'results': results,
        }
        return render(request, "topic_manager/work_summary.html", context=context)


# 工作成果
@login_required
def work_achievement(request):
    if request.method == "POST":
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            existing_record = WorkAchievement.objects.get(id=target_id)
            if request.POST['btn'] == "delete":
                existing_record.delete()
            else:
                existing_record.date = request.POST['date']
                existing_record.semester = request.POST['semester']
                existing_record.achievement_name = request.POST['achievement_name']
                existing_record.man_day = request.POST['man_day']
                existing_record.major_contributor = request.POST['major_contributor']
                existing_record.is_finished = request.POST['is_finished']
                existing_record.paper_published = request.POST['paper_published']
                existing_record.paper_contributed = request.POST['paper_contributed']
                existing_record.patent_published = request.POST['patent_published']
                existing_record.patent_contributed = request.POST['patent_contributed']
                existing_record.software_published = request.POST['software_published']
                existing_record.software_contributed = request.POST['software_contributed']
                existing_record.application_composed = request.POST['application_composed']
                existing_record.document_composed = request.POST['document_composed']
                existing_record.software_finished = request.POST['software_finished']
                existing_record.document_summary = request.POST['document_summary']
                existing_record.help_freshmen = request.POST['help_freshmen']
                existing_record.departure = request.POST['departure']
                existing_record.comment = request.POST['comment']
                existing_record.save()
        else:
            new_record = WorkAchievement(
                user=request.user,
                real_name=request.user.real_name,
                date=request.POST['date'],
                semester=request.POST['semester'],
                achievement_name=request.POST['achievement_name'],
                man_day=request.POST['man_day'],
                major_contributor=request.POST['major_contributor'],
                is_finished=request.POST['is_finished'],
                paper_published=request.POST['paper_published'],
                paper_contributed=request.POST['paper_contributed'],
                patent_published=request.POST['patent_published'],
                patent_contributed=request.POST['patent_contributed'],
                software_published=request.POST['software_published'],
                software_contributed=request.POST['software_contributed'],
                application_composed=request.POST['application_composed'],
                document_composed=request.POST['document_composed'],
                software_finished=request.POST['software_finished'],
                document_summary=request.POST['document_summary'],
                help_freshmen=request.POST['help_freshmen'],
                departure=request.POST['departure'],
                comment=request.POST['comment'],
            )
            try:
                new_record.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponse('success')
    else:
        results = WorkAchievement.objects.filter(user=request.user)
        context = {
            'results': results,
        }
        return render(request, "topic_manager/work_achievement.html", context=context)


# 业绩量化
@login_required
def achievement_quantization(request):
    if request.method == "POST":
        # 提供了记录的ID，要么删除该记录，要么修改该记录
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            existing_record = AchievementQuantization.objects.get(id=target_id)
            # 删除该记录
            if request.POST['btn'] == "delete":
                existing_record.delete()
            # 修改该记录
            else:
                existing_record.date = request.POST['date']
                existing_record.semester = request.POST['semester']
                existing_record.paper_published = request.POST['paper_published']
                existing_record.paper_contributed = request.POST['paper_contributed']
                existing_record.patent_published = request.POST['patent_published']
                existing_record.patent_contributed = request.POST['patent_contributed']
                existing_record.software_published = request.POST['software_published']
                existing_record.software_contributed = request.POST['software_contributed']
                existing_record.application_composed = request.POST['application_composed']
                existing_record.document_composed = request.POST['document_composed']
                existing_record.software_finished = request.POST['software_finished']
                existing_record.document_summary = request.POST['reward']
                existing_record.help_freshmen = request.POST['scholar_report_times']
                existing_record.departure = request.POST['average_work_hour']
                existing_record.comment = request.POST['proposition']
                existing_record.comment = request.POST['competition_organized']
                existing_record.comment = request.POST['absent_times_for_scholar_report']
                existing_record.comment = request.POST['absent_times_for_ranking']
                existing_record.save()
        else:
            new_record = AchievementQuantization(
                user=request.user,
                real_name=request.user.real_name,
                date=request.POST['date'],
                semester=request.POST['semester'],
                paper_published=request.POST['paper_published'],
                paper_contributed=request.POST['paper_contributed'],
                patent_published=request.POST['patent_published'],
                patent_contributed=request.POST['patent_contributed'],
                software_published=request.POST['software_published'],
                software_contributed=request.POST['software_contributed'],
                application_composed=request.POST['application_composed'],
                document_composed=request.POST['document_composed'],
                software_finished=request.POST['software_finished'],
                reward=request.POST['reward'],
                scholar_report_times=request.POST['scholar_report_times'],
                average_work_hour=request.POST['average_work_hour'],
                proposition=request.POST['proposition'],
                competition_organized=request.POST['competition_organized'],
                absent_times_for_scholar_report=request.POST['absent_times_for_scholar_report'],
                absent_times_for_ranking=request.POST['absent_times_for_ranking'],
            )
            try:
                new_record.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponse('success')
    else:
        results = AchievementQuantization.objects.filter(user=request.user)
        context = {
            'results': results,
        }
        return render(request, "topic_manager/achievement_quantization.html", context=context)


# 工作量认定
@login_required
def achievement_quantization_confirmation(request):
    if request.method == "POST":
        # 提供了记录的ID，要么删除该记录，要么修改该记录
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            existing_record = AchievementQuantizationConfirmation.objects.get(id=target_id)
            # 删除该记录
            if request.POST['btn'] == "delete":
                existing_record.delete()
            # 修改该记录
            else:
                existing_record.date = request.POST['date']
                existing_record.primary_classification = request.POST['primary_classification']
                existing_record.secondary_classification = request.POST['secondary_classification']
                existing_record.number = ""
                existing_record.completion_type = request.POST['completion_type']
                existing_record.man_days = request.POST['man_days']
                existing_record.level = request.POST['level']
                existing_record.tangible_work = request.POST['tangible_work']
                existing_record.remark = request.POST['remark']
                existing_record.group_confirmation = request.POST['group_confirmation']
                existing_record.tutor_confirmation = request.POST['tutor_confirmation']
                existing_record.save()
        else:
            new_record = AchievementQuantizationConfirmation(
                user=request.user,
                real_name=request.user.real_name,
                date=request.POST['date'],
                primary_classification=request.POST['primary_classification'],
                secondary_classification=request.POST['secondary_classification'],
                number="",
                completion_type=request.POST['completion_type'],
                man_days=request.POST['man_days'],
                level=request.POST['level'],
                tangible_work=request.POST['tangible_work'],
                remark=request.POST['remark'],
                group_confirmation=request.POST['group_confirmation'],
                tutor_confirmation=request.POST['tutor_confirmation'],
            )
            try:
                new_record.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponse('success')
    else:
        results = AchievementQuantizationConfirmation.objects.filter(user=request.user)
        context = {
            'results': results,
        }
        return render(request, "topic_manager/achievement_quantization_confirmation.html", context=context)


# 学术报告
@login_required
def scholar_report(request):
    if request.method == "POST":
        # 提供了记录的ID，要么删除该记录，要么修改该记录
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            existing_record = ScholarReport.objects.get(id=target_id)
            # 删除该记录
            if request.POST['btn'] == "delete":
                existing_record.delete()
            # 修改该记录
            else:
                existing_record.start_time = request.POST['start_time']
                existing_record.duration = request.POST['duration']
                existing_record.grade = request.POST['grade']
                existing_record.is_archived = request.POST['is_archived']
                existing_record.report_title = request.POST['report_title']
                existing_record.questioner = request.POST['questioner']
                existing_record.question = request.POST['question']
                existing_record.reply_status = request.POST['reply_status']
                existing_record.remark = request.POST['remark']
                existing_record.save()
        else:
            new_record = ScholarReport(
                user=request.user,
                real_name=request.user.real_name,
                start_time=request.POST['start_time'],
                duration=request.POST['duration'],
                grade=request.POST['grade'],
                is_archived=request.POST['is_archived'],
                report_title=request.POST['report_title'],
                questioner=request.POST['questioner'],
                question=request.POST['question'],
                reply_status=request.POST['reply_status'],
                remark=request.POST['remark'],
            )
            try:
                new_record.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponse('success')
    else:
        results = ScholarReport.objects.filter(user=request.user)
        context = {
            'results': results,
        }
        return render(request, "topic_manager/scholar_report.html", context=context)


@login_required
def valid(request):
    if request.method == "POST":
        class_name = request.POST['class_name']
        value = request.POST['value']
        # 验证日期
        if class_name == "date":
            if re.match(r'[0-9][0-9][0-9][0-9]-[0,1,2][0-9]-[0,1,2,3][0-9]', value) is not None:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的日期")
        elif class_name == "day":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的天数")
        # 验证学期
        elif class_name == "semester":
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
        # 周报相关的验证
        elif class_name == "week":
            if value.isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确工作周")
        elif class_name == "average_work_hour":
            if re.match(r'^[0-9]{1,2}(.[0-9]){0,1}$', value) is not None:
                return HttpResponse("OK")
            return HttpResponse("请输入正确周平均日工作时间")
        elif class_name == "this_week_task":
            if len(value) > 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的本周工作")
        elif class_name == "next_week_task":
            if len(value) > 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的下周工作")
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
            if re.match(r"^[0-9]{1,2}(.[0-9]){0,1}/[0-9]{1,2}(.[0-9]){0,1}$", value) is not None:
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
        elif class_name == "end_of_term_summary":
            if len(value) > 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的期末总结")
        # 计划相关的验证
        else:
            if len(value) > 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("输入内容不能为空")
