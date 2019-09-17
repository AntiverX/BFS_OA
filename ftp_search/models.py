from django.db import models

# Create your models here.
class FileRecord(models.Model):
    filename = models.TextField()
    filepath = models.TextField(primary_key=True)

class DirectoryRecord(models.Model):
    filename = models.TextField()
    filepath = models.TextField(primary_key=True)
