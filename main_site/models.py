from django.db import models
from user_info.models import User

# Create your models here.

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
    partitipant = models.TextField()
    # 注意事项
    attentation = models.TextField()
    # 比赛情况
    condiditon = models.TextField()


class FileRecord(models.Model):
    time = models.DateTimeField(auto_now=True,null=True)
    title = models.TextField()
    name = models.TextField()
