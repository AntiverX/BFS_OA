from django.shortcuts import render, HttpResponse
from user_info.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import time
from django.core.exceptions import *
from main_site.models import BFS_OA_Config
import datetime


def auth(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            context['error'] = "用户名或密码错误"
            return render(request, "error.html", context=context)
    else:
        return render(request, 'auth/login.html')


@login_required
def deauth(request):
    logout(request)
    return HttpResponseRedirect("/")


# 注册
def register(request):
    if request.method == "POST":
        context = {}
        username = request.POST['username']
        current_user = username
        password = request.POST['password']
        real_name = request.POST['real_name']
        student_id = request.POST['student_id']
        group_name = request.POST['group_name']
        student_type = "新生" if int(request.POST['password'][4:6]) == datetime.datetime.now().year % 100 else "硕士研究生"
        user = User.objects.create_user(username=username,
                                        password=password,
                                        real_name=real_name,
                                        current_user=current_user,
                                        student_id=student_id,
                                        is_display_all=False,
                                        group_name=group_name,
                                        student_type=student_type,)
        user.save()
        context['success'] = "注册成功！"
        context['return_link'] = "/"
        return render(request, 'success.html', context=context)
    else:
        return render(request, 'auth/register.html')


# 新生培训
@login_required
def train(request):
    # TODO template及逻辑

    return render(request, "info/train.html")


# 课程表
@login_required
def time_table(request):
    context = {
        'config': BFS_OA_Config.objects.filter()[0] if len(BFS_OA_Config.objects.filter()) != 0 else None,
        'current_semester_week': int(time.strftime("%W")) - int(
            BFS_OA_Config.objects.filter()[0].semester_start_time.isocalendar()[1]),
        'user': request.user,
    }
    class_1, class_2, class_3, class_4, class_5 = [], [], [], [], []
    for i in range(7):
        class_1.append(TimeTable.objects.filter(class_number=1, day=i + 1, user_id=request.user.id) if len(
            TimeTable.objects.filter(class_number=1, day=i + 1, user_id=request.user.id)) != 0 else None)
        class_2.append(TimeTable.objects.filter(class_number=2, day=i + 1, user_id=request.user.id) if len(
            TimeTable.objects.filter(class_number=2, day=i + 1, user_id=request.user.id)) != 0 else None)
        class_3.append(TimeTable.objects.filter(class_number=3, day=i + 1, user_id=request.user.id) if len(
            TimeTable.objects.filter(class_number=3, day=i + 1, user_id=request.user.id)) != 0 else None)
        class_4.append(TimeTable.objects.filter(class_number=4, day=i + 1, user_id=request.user.id) if len(
            TimeTable.objects.filter(class_number=4, day=i + 1, user_id=request.user.id)) != 0 else None)
        class_5.append(TimeTable.objects.filter(class_number=5, day=i + 1, user_id=request.user.id) if len(
            TimeTable.objects.filter(class_number=5, day=i + 1, user_id=request.user.id)) != 0 else None)
    context['classes_1'] = class_1
    context['classes_2'] = class_2
    context['classes_3'] = class_3
    context['classes_4'] = class_4
    context['classes_5'] = class_5
    return render(request, "info/time_table.html", context=context)


# 课程列表
@login_required
def time_table_list(request):
    if request.method == 'POST':
        class_name = request.POST['class_name']
        teacher_name = request.POST['teacher_name']
        week_start = request.POST['week_start']
        week_end = request.POST['week_end']
        day = request.POST['day']
        class_number = request.POST['class_number']
        class_location = request.POST['class_location']
        if request.POST['target_id'] != "":
            if request.POST['btn'] == "delete":
                existing_class = TimeTable.objects.get(id=request.POST['target_id'])
                existing_class.delete()
            else:
                existing_class = TimeTable.objects.get(id=request.POST['target_id'])
                existing_class.class_name = class_name
                existing_class.teacher_name = teacher_name
                existing_class.week_start = week_start
                existing_class.week_end = week_end
                existing_class.day = day
                existing_class.class_number = class_number
                existing_class.class_location = class_location
                try:
                    existing_class.save()
                except (ValueError, ValidationError) as err:
                    context = {
                        'error': err,
                    }
                    return render(request, 'error.html', context=context)
        else:
            new_class = TimeTable.objects.create(
                user=request.user,
                class_name=class_name,
                teacher_name=teacher_name,
                week_start=week_start,
                week_end=week_end,
                day=day,
                class_number=class_number,
                class_location=class_location,
            )
            try:
                new_class.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponseRedirect('time_table_list')
    else:
        context = {

        }
        context['username'] = request.user.username
        context['results'] = TimeTable.objects.filter(user=request.user)
        return render(request, "info/time_table_list.html", context=context)


# 个人信息
@login_required
def my_info(request):
    if request.method == "POST":
        info = User.objects.get(id=request.user.id)
        info.gender = request.POST['gender']
        info.nationality = request.POST['nationality']
        info.born_in = request.POST['born_in']
        info.id_number = request.POST['id_number']
        info.student_id = request.POST['student_id']
        info.entrance_time = request.POST['entrance_time']
        info.graduate_time = request.POST['graduate_time']
        info.major = request.POST['major']
        info.group_name = request.POST['group_name']
        info.tutor = request.POST['tutor']
        info.bank_name = request.POST['bank_name']
        info.bank_id = request.POST['bank_id']
        info.phone_number = request.POST['phone_number']
        info.email = request.POST['email']
        info.past_school = request.POST['past_school']
        info.past_unit = request.POST['past_unit']
        info.thesis_defense_score = request.POST['thesis_defense_score']
        info.degree_paper = request.POST['degree_paper']
        info.student_type = request.POST['student_type']
        info.real_name = request.POST['real_name']
        try:
            info.save()
        except (ValueError, ValidationError) as err:
            context = {
                'error': err,
            }
            return render(request, 'error.html', context=context)

        return HttpResponseRedirect('/info/my_info')
    else:
        info = User.objects.get(id=request.user.id)
        context = {
            'info': info,
        }
        return render(request, "info/my_info.html", context=context)


# 资产管理
@login_required
def asset(request):
    if request.method == "POST":
        if request.POST['target_to_delete'] != "":
            target_to_delete = request.POST['target_to_delete']
            existing_asset = Asset.objects.get(id=target_to_delete)
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
            existing_asset = Asset.objects.get(id=target_id)
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
                context = {
                    'error': err,
                }
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
            new_asset = Asset(
                user=request.user, type=type, name=name, model=model, manufacturer=manufacturer, number=number,
                parameter=parameter, buying_date=buying_date, storing_place=storing_place
            )
            try:
                new_asset.save()
            except (ValueError, ValidationError) as err:
                context = {
                    'error': err,
                }
                return render(request, 'error.html', context=context)
        return HttpResponseRedirect('/info/asset')
    else:
        results = Asset.objects.all()
        context = {
        }
        context['assets'] = results
        return render(request, "info/asset.html", context=context)


# 表单验证
def valid(request):
    if request.method == "POST":
        if request.POST['class_name'] == "username":
            if len(request.POST['value']) < 5:
                return HttpResponse("太短辣，至少5个字符哦")
            if len(request.POST['value']) > 20:
                return HttpResponse("太长辣，最多20个字符哦")
            else:
                return HttpResponse("OK")
        elif request.POST['class_name'] == "password":
            if len(request.POST['value']) < 8:
                return HttpResponse("太短辣，至少8个字符哦")
            if len(request.POST['value']) > 20:
                return HttpResponse("太长辣，最多20个字符哦")
            else:
                return HttpResponse("OK")
        elif request.POST['class_name'] == "real_name":
            if len(request.POST['value']) < 2:
                return HttpResponse("你的名字只有姓？")
            if len(request.POST['value']) > 20:
                return HttpResponse("你的名字太长了，怕是有问题哦")
            else:
                return HttpResponse("OK")
        elif request.POST['class_name'] == "student_id":
            if not request.POST['value'].isdigit() or len(request.POST['value']) != 10:
                return HttpResponse("学号必须是十位数字哦")
            else:
                return HttpResponse("OK")
        elif request.POST['class_name'] == "week_start":
            if request.POST['value'].isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("不能为空")
        elif request.POST['class_name'] == "week_end":
            if request.POST['value'].isdigit():
                return HttpResponse("OK")
            else:
                return HttpResponse("不能为空")
        else:
            if len(request.POST['value']) != 0:
                return HttpResponse("OK")
            else:
                return HttpResponse("不能为空")
