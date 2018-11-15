from django.db import models
from user_info.models import User


# 目标
class Target(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.TextField()
    time = models.DateField()
    expected_result = models.TextField()
    time_consumed = models.TextField()
    content = models.TextField()
    end_of_term_summary = models.TextField()
    semester = models.TextField(null=True)


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=32)
    plan_name = models.CharField(max_length=32)
    plan_result = models.TextField()
    is_reviewed = models.BooleanField()
    head_person = models.CharField(max_length=32)
    affiliated_person = models.TextField()
    planed_time = models.IntegerField()
    planed_start_time = models.DateField()
    planed_end_time = models.DateField()
    actual_time = models.IntegerField(null=True)
    actual_start_time = models.DateField(null=True)
    actual_end_time = models.DateField(null=True)
    advanced_postponed_time = models.IntegerField()
    remark = models.TextField()


# 会议记录
class MeetingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    cost_time = models.IntegerField()
    place = models.CharField(max_length=50)
    theme = models.TextField()
    theme_content = models.TextField()
    remark = models.TextField(null=True)


# 工作总结
class WorkSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    type = models.CharField(max_length=32)
    summary = models.TextField()
    average_time = models.CharField(max_length=32)
    all_days = models.IntegerField()
    man_day = models.TextField(null=True)
    natural_day = models.TextField(null=True)
    remark = models.TextField(null=True)


# 周报
class WeeklySummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField(default=0)
    submit_time = models.DateTimeField(auto_now=True)
    average_work_hour = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    absent_hour = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    real_name = models.CharField(max_length=150)
    this_week_task = models.TextField()
    next_week_task = models.TextField()
    is_present = models.BooleanField(default=False)  # 到场
    is_absent = models.BooleanField(default=False)  # 未到
    is_left = models.BooleanField(default=False)  # 请假
