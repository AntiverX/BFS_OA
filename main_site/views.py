from django.shortcuts import render, HttpResponseRedirect
from BFS_OA.settings import BASE_DIR
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
import os, time, re, random
from .models import FileRecord, BFS_OA_Config, Lab_Asset, Semester
from user_info.models import User
from django.core.exceptions import *
import datetime

context = {
    'menus': {
        'bulletin': "通知公告",
        'news': "新闻",
        'library': "图书室",
        'competition': "近期比赛"
    },
}


def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            new_current_user = request.POST['current_user']
            request.user.current_user = new_current_user
            request.user.save()
            return HttpResponseRedirect("/")
        else:
            context['user'] = request.user
            context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
            return render(request, 'index/index.html', context=context)
    else:
        return render(request, 'index/index.html')


# 通知公告
@login_required
def bulletin(request):
    # TODO template及逻辑
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    return render(request, "index/bulletin.html", context=context)


# 新闻
@login_required
def news(request):
    # TODO template及逻辑
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    return render(request, "index/news.html", context=context)


# 图书馆
@login_required
def library(request):
    # TODO template及逻辑
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    return render(request, "index/library.html", context=context)


# 竞赛
@login_required
def competition(request):
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    if request.method == "POST":
        pass
    else:
        return render(request, "index/competition.html", context=context)


@login_required
def settings(request):
    context = {}
    if request.user.id == 1 or request.user.is_admin:
        context = {
            # 'current_semester_week': int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1]),
            'user': request.user,
            'config': BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
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
        context = {
            'menus': {
                '/system/settings': "界面设置",
            }
        }
        return render(request, "index/settings.html", context=context)

# 设置学期相关的内容
@login_required
def semester(request):
    if request.user.id == 1 or request.user.is_admin:
        if request.method == "POST":
            if request.POST['target_id'] != "":
                target_id = request.POST['target_id']
                existing_record = Semester.objects.get(id=target_id)
                if request.POST['btn'] == "delete":
                    existing_record.delete()
                else:
                    existing_record.semester_name = request.POST['semester_name']
                    existing_record.start_date = request.POST['start_date']
                    existing_record.end_date = request.POST['end_date']
            else:
                new_record = Semester(
                    semester_name=request.POST['semester_name'],
                    start_date=request.POST['start_date'],
                    end_date=request.POST['end_date'],
                )
                try:
                    new_record.save()
                except (ValueError, ValidationError) as err:
                    context = {
                        'error': err,
                    }
                    return render(request, 'error.html', context=context)
            return HttpResponse("success")
        else:
            context = {
                "results": Semester.objects.all(),
            }
            return render(request, "index/semester_settings.html", context=context)


def user_settings(request):
    return HttpResponse("/")


@login_required
def users_management(request):
    if request.user.id == 1 or request.user.is_admin:
        context = {
            'menus': {
                '/system/settings': "系统设置",
                '/system/users_management': "用户管理",
            },
            'current_semester_week': int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1]),
            'user': request.user,
            'config': BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
        }
        if request.method == "GET":
            users = User.objects.all()
            context['results'] = users
            return render(request, "index/users_management.html", context=context)
        else:
            target_id = request.POST['target_id']
            user = User.objects.get(id=target_id)
            if request.POST['btn'] == "delete":
                user.delete()
            else:
                user.username = request.POST['username']
                user.real_name = request.POST['real_name']
                user.is_admin = request.POST['is_admin']
                user.is_student = request.POST['is_student']
                user.is_teacher = request.POST['is_teacher']
                user.save()
            return HttpResponseRedirect("/system/users_management")


@login_required
def asset(request):
    context['user'] = request.user
    context['config'] = BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None
    if request.method == "POST":
        if request.POST['target_to_delete'] != "":
            target_to_delete = request.POST['target_to_delete']
            existing_asset = Lab_Asset.objects.get(id=target_to_delete)
            existing_asset.delete()
            return HttpResponseRedirect('/info/asset')
        if request.POST['target_id'] != "":
            target_id = request.POST['target_id']
            type = request.POST['type']
            name = request.POST['name']
            model = request.POST['model']
            manufacturer = request.POST['manufacturer']
            number = request.POST['number']
            parameter = request.POST['parameter']
            buying_date = request.POST['buying_date']
            storing_place = request.POST['storing_place']
            existing_asset = Lab_Asset.objects.get(id=target_id)
            existing_asset.type = type
            existing_asset.name = name
            existing_asset.model = model
            existing_asset.manufacturer = manufacturer
            existing_asset.number = number
            existing_asset.parameter = parameter
            existing_asset.buying_date = buying_date
            existing_asset.storing_place = storing_place
            try:
                existing_asset.save()
            except (ValueError, ValidationError) as err:
                context['error'] = err
                return render(request, 'error.html', context=context)
        else:
            type = request.POST['type']
            name = request.POST['name']
            model = request.POST['model']
            manufacturer = request.POST['manufacturer']
            number = request.POST['number']
            parameter = request.POST['parameter']
            buying_date = request.POST['buying_date']
            storing_place = request.POST['storing_place']
            new_asset = Lab_Asset(
                user=request.user, type=type, name=name, model=model, manufacturer=manufacturer, number=number,
                parameter=parameter, buying_date=buying_date, storing_place=storing_place
            )
            try:
                new_asset.save()
            except (ValueError, ValidationError) as err:
                context['error'] = err
                return render(request, 'error.html', context=context)
        return HttpResponseRedirect('/info/asset')
    else:
        results = Lab_Asset.objects.all()
        context['assets'] = results
        return render(request, "info/asset.html", context=context)


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


@login_required
def get_current_week(request):
    days = (datetime.date.today() - BFS_OA_Config.objects.filter()[0].semester_start_time).days
    return HttpResponse(int(days / 7))
    # return HttpResponse(int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1]))


@login_required
def get_current_week_range(request):
    return HttpResponse(int(time.strftime("%W")) - int(BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1]))


def valid(request):
    if request.method == "POST":
        if 'time' in request.POST['class_name']:
            if re.match(r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}", request.POST['value']) is not None:
                return HttpResponse("OK")
            else:
                return HttpResponse("请输入正确的时间")
        else:
            if len(request.POST['value']) != 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("不能为空")
