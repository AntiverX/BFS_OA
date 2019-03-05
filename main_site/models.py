from django.db import models
from user_info.models import User


# Create your models here.
class Semester(models.Model):
    # 学期名称，如：2018-2019-1
    semester_name = models.TextField()
    # 学期开始日期
    start_date = models.DateField()
    # 学期结束日期
    end_date = models.DateField()

class BFS_OA_Config(models.Model):
    semester_start_time = models.DateField()


class Competition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 赛事名称
    name = models.TextField()
    # 报名开始时间
    registration_start_time = models.DateTimeField()
    # 报名结束时间
    registration_end_time = models.DateTimeField()
    # 比赛开始时间
    start_time = models.DateTimeField()
    # 比赛结束时间
    end_time = models.DateTimeField()
    # 比赛地址
    address = models.TextField()
    # 参与人员
    participant = models.TextField()
    # 注意事项
    attention = models.TextField()
    # 比赛情况
    condition = models.TextField()


class FileRecord(models.Model):
    time = models.DateTimeField(auto_now=True, null=True)
    title = models.TextField()
    name = models.TextField()


# 资产
class Lab_Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.TextField()
    name = models.TextField()
    model = models.TextField()
    manufacturer = models.TextField()
    number = models.TextField()
    parameter = models.TextField()
    buying_date = models.DateField()
    storing_place = models.TextField()
