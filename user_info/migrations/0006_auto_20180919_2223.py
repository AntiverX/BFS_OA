# Generated by Django 2.1.1 on 2018-09-19 14:23

from django.db import migrations, models
import django.utils.translation


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0005_auto_20180915_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='MettingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('type', models.CharField(max_length=32)),
                ('plan_name', models.CharField(max_length=32)),
                ('plan_result', models.TextField()),
                ('is_reviewed', models.BooleanField()),
                ('head_person', models.CharField(max_length=32)),
                ('affiliated_person', models.TextField()),
                ('planed_time', models.IntegerField()),
                ('planed_start_time', models.DateField()),
                ('planed_end_time', models.DateField()),
                ('actual_time', models.IntegerField()),
                ('actual_start_time', models.DateField()),
                ('actual_end_time', models.DateField()),
                ('is_advanced', models.BooleanField()),
                ('is_postponed', models.BooleanField()),
                ('remark', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('term', models.CharField(max_length=32)),
                ('time', models.DateTimeField(auto_now=True)),
                ('expected_result', models.CharField(max_length=32)),
                ('time_consumed', models.IntegerField()),
                ('content', models.TextField()),
                ('end_of_term_summary', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('date', models.DateField()),
                ('monday', models.TextField()),
                ('tuesday', models.TextField()),
                ('wednesday', models.TextField()),
                ('thursday', models.TextField()),
                ('friday', models.TextField()),
                ('saturday', models.TextField()),
                ('sunday', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('date', models.DateField()),
                ('type', models.CharField(max_length=32)),
                ('summary', models.TextField()),
                ('average_time', models.CharField(max_length=32)),
                ('man_day', models.IntegerField()),
                ('natural_day', models.IntegerField()),
                ('remark', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='real_name',
            field=models.CharField(blank=True, max_length=30, verbose_name=django.utils.translation.gettext),
        ),
    ]
