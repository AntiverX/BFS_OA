from django.db import models

# Create your models here.
class UploadRecord(models.Model):
    user_name = models.TextField()
    file_name = models.TextField()
    upload_time = models.DateTimeField()