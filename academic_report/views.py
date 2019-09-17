from django.shortcuts import render, HttpResponse
from .models import AcademicReport, Comment


# Create your views here.
def index(request):
    latest_academic_report = AcademicReport.objects.all().order_by('-created_date')
    contxt = {
        'latest_academic_report': latest_academic_report,
    }
    return render(request, 'academic_report/index.html', context=contxt)


# 我的学术报告，可以新建学术报告。可以上传学术报告，包括文件，内容简介
def my_report(request):
    # TODO
    return render(request, 'academic_report/my_report.html', context=None)


# 所有的学术报告奥
def all_report(request):
    all_record = AcademicReport.objects.all()
    context = {
        'all_record': all_record,
    }
    return render(request, 'academic_report/all_report.html', context=context)
