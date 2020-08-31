from django.db import models
from django.utils.timezone import now

# Create your models here.
class UploadRecord(models.Model):
    user_name = models.TextField(default="")
    username = models.TextField(default="")
    file_name = models.TextField(default="")
    upload_time = models.DateTimeField()
    group_name = models.TextField(default="")

class DailyReport(models.Model):
    username = models.TextField()
    real_name = models.TextField()
    fill_time = models.DateTimeField(default=now)
    date = models.DateField()
    name = models.TextField(default="")
    sub_name = models.TextField(default="")
    day = models.FloatField(default=0.0)
    quantitative = models.TextField(default="")
    qualitative = models.TextField(default="")
    type = models.TextField(default="")

class Semester(models.Model):
    edit_time = models.DateTimeField(default=now)
    semester_name = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()