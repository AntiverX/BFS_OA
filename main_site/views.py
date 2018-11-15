from django.shortcuts import render, HttpResponseRedirect
from BFS_OA.settings import BASE_DIR
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
import time
from .models import FileRecord, BFS_OA_Config
import os
import random

current_week = time.strftime("%W")
start_week = BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1]
current_semester_week = int(current_week) - int(start_week)

context = {
    'menus': {'bulletin': "通知公告",
              'news': "新闻",
              'library': "图书室",
              'competition': "近期比赛"
              },
    'config': BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None,
    'current_semester_week': current_semester_week,
}


def index(request):
    if request.user.is_authenticated:
        context['user'] = request.user
        return render(request, 'index/index.html', context=context)
    else:
        return render(request, 'index/index.html')


# 通知公告
@login_required
def bulletin(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "index/bulletin.html", context=context)


# 新闻
@login_required
def news(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "index/news.html", context=context)


# 图书馆
@login_required
def library(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "index/library.html", context=context)


# 竞赛
@login_required
def competition(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "index/competition.html", context=context)


@login_required
def settings(request):
    context = {}
    if request.user.id == 1 or request.user.is_admin:
        context = {
            'menus': {'/system/settings': "系统设置"}
        }
        if request.method == "POST":
            semester_start_time = request.POST['semester_start_time']
            config = BFS_OA_Config.objects.filter()
            if len(config) == 0:
                new_config = BFS_OA_Config(
                    semester_start_time=semester_start_time
                )
                new_config.save()
            else:
                config[0].semester_start_time = semester_start_time
                config[0].save()
            return HttpResponseRedirect("/system/settings")
        else:
            config = BFS_OA_Config.objects.filter()
            if len(config) != 0:
                context['config'] = config[0]
            return render(request, "index/settings.html", context=context)
    else:
        context["error"] = "你无权访问此页面！"
        return render(request, "error.html", context=context)


def about(request):
    context = {}
    return render(request, "index/about.html", context=context)


def uploader(request):
    users = [
        "王帅鹏", "秦枭喃", "门元昊", "张毅飞", "于雪青", "王逸洲", "徐冰妤",
        "李筱雅", "程浩卿", "董思佳", "郝靖伟", "李蕊", "李东超", "王海洲",
        "刘宇", "喻露", "王睿怡", "候留洋", "胡雅娴", "佟彤", "李业晨",
    ]
    context = {}
    if request.method == "POST":
        file = request.FILES.get('file')
        title = request.POST['title']
        name = request.POST['name']
        file_name = BASE_DIR + "/static/file/" + title + " - " + name + ".docx"
        with open(file_name.encode(), "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        new_record = FileRecord(
            title=title,
            name=name
        )
        new_record.save()
        context['success'] = "上传成功！"
        return render(request, "success.html", context=context)
    else:
        fileRecord = FileRecord.objects.all()
        for fileRecord_ in fileRecord:
            if fileRecord_.name in users:
                users.remove(fileRecord_.name)
        context['users'] = users
        context['user_count'] = len(users)
        context["results"] = fileRecord
        return render(request, "index/upload.html", context=context)


def random_service(request):
    users = [
        "王帅鹏", "秦枭喃", "门元昊", "张毅飞", "于雪青", "王逸洲", "徐冰妤",
        "李筱雅", "程浩卿", "董思佳", "郝靖伟", "李  蕊", "李东超", "王海洲",
        "刘  宇", "喻  露", "王睿怡", "候留洋", "胡雅娴", "佟  彤", "李业晨",
    ]
    random_value = random.randint(0, len(users) - 1)
    return HttpResponse(users[random_value])
