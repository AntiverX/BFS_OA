from django.db import models


# Create your models here.
class weekly_summary(models.Model):
    # TODO 把周报model移到user_info里
    real_name = models.CharField(max_length=150)
    this_week_task = models.TextField()
    next_week_task = models.TextField()
    submit_time = models.DateTimeField(auto_now=True)
    week = models.IntegerField(default=0)
    is_present = models.BooleanField(default=False)
    is_absent = models.BooleanField(default=False)
    is_left = models.BooleanField(default=False)
