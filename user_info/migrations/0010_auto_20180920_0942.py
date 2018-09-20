# Generated by Django 2.1.1 on 2018-09-20 01:42

from django.db import migrations, models
import django.utils.translation


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0009_auto_20180920_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='real_name',
            field=models.CharField(blank=True, max_length=30, verbose_name=django.utils.translation.gettext),
        ),
        migrations.AlterField(
            model_name='worksummary',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]