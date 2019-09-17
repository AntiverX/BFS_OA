from django.db import models


# Create your models here.
class AcademicReport(models.Model):
    user_id = models.IntegerField()
    created_date = models.DateTimeField()
    start_date = models.DateTimeField()
    title = models.TextField()
    content = models.TextField()


class Comment(models.Model):
    academic_report_id = models.IntegerField()
