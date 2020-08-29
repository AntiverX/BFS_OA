from django.db import models
from django.utils.timezone import now

# Create your models here.
class UploadRecord(models.Model):
    user_name = models.TextField()
    username = models.TextField()
    file_name = models.TextField()
    upload_time = models.DateTimeField()
    group_name = models.TextField(default="")

class DailyReport(models.Model):
    username = models.TextField()
    real_name = models.TextField()
    fill_time = models.DateTimeField(default=now)
    date = models.DateField()
    finished_work = models.TextField()
    tomorrow_work = models.TextField()
    remarks = models.TextField()
