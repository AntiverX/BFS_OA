from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Train(models.Model):
    user_name = models.TextField()
    file_name = models.TextField()
    training_type = models.TextField()
    upload_time = models.DateTimeField()

class PollRecord(models.Model):
    newcomer_name = models.CharField(max_length=30)
    score_1 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    score_2 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(40)]
    )
    score_3 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    score_4 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    remark = models.TextField()
    user_name = models.CharField(max_length=30, default="")
    training_type = models.CharField(max_length=30, default="")