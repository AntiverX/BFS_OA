from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from BFS_OA.settings import BASE_DIR
from .models import UploadRecord,DailyReport,WeeklyReport, Semester
from user_info.models import User
import datetime
import pytz
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def index(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        short_file_name = "/static/file/topic_manager/" + request.user.group_name + "-课题管理-" + request.user.real_name + "-v3.6-" + datetime.datetime.now().strftime('%Y.%m.%d') + ".xlsx"
        file_name = BASE_DIR + "/static/file/topic_manager/" + request.user.group_name + "-课题管理-" + request.user.real_name + "-v3.6-" + datetime.datetime.now().strftime('%Y.%m.%d') + ".xlsx"
        with open(file_name.encode(), "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        new_record = UploadRecord(
            user_name=request.user.real_name,
            username=request.user.username,
            file_name=short_file_name,
            upload_time=datetime.datetime.now(),
            group_name=request.user.group_name,
        )
        new_record.save()
        context = None
        return HttpResponseRedirect('/topic_manager_v2/index')
    else:
        try:
            context = {
                'have_uploaded': 1,
                'last_update_time': UploadRecord.objects.filter(user_name=request.user.real_name).order_by('-upload_time')[0].upload_time
            }
        except:
            context = {
                'have_uploaded': 0,
                'last_update_time': '你还没有上传过课题管理表'
            }
    return render(request, 'topic_manager_v2/index.html', context=context)


def upload_history(request):
    return render(request, 'topic_manager_v2/upload_history.html', context=None)

def upload_history_api(request):
    all_history = UploadRecord.objects.filter(group_name=request.user.group_name).order_by('-upload_time')
    all_record = []
    for history in all_history:
        new_record = {
            'real_name': history.user_name,
            'username': history.username,
            'path': history.file_name,
            'time': history.upload_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
        }
        all_record.append(new_record)
    return JsonResponse(all_record, safe=False)

def upload_status(request):
    class Status:
        def __init__(self, real_name, last_upload_time, should_upload_time):
            self.real_name = real_name
            self.last_upload_time = last_upload_time
            self.should_upload_time = should_upload_time

    record = []
    all_student = User.objects.filter(is_student=True,group_name=request.user.group_name)
    for student in all_student:
        try:
            last_upload_time = UploadRecord.objects.filter(user_name=student.real_name).order_by('-upload_time')[0].upload_time
        except:
            last_upload_time = datetime.datetime(2000, 1, 1, 0, 0, 0, 0, pytz.timezone('Asia/Shanghai'))
        should_upload_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        new_status = Status(student.real_name, last_upload_time, should_upload_time)
        record.append(new_status)
    context = {
        'all_record': record,
    }
    return render(request, 'topic_manager_v2/status.html', context=context)

@csrf_exempt
def upload_status_api(request):
    class Status:
        def __init__(self, real_name, last_upload_time, should_upload_time):
            self.real_name = real_name
            self.last_upload_time = last_upload_time
            self.should_upload_time = should_upload_time

    record = []
    all_student = User.objects.filter(is_student=True,group_name=request.user.group_name)
    for student in all_student:
        try:
            last_upload_time = UploadRecord.objects.filter(user_name=student.real_name).order_by('-upload_time')[0].upload_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
        except:
            last_upload_time = datetime.datetime(2000, 1, 1, 0, 0, 0, 0, pytz.timezone('Asia/Shanghai'))
        should_upload_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        new_status = {
            'real_name':student.real_name,
            'last_upload_time':last_upload_time.strftime('%Y-%m-%d %H:%M:%S'),
            'should_upload_time':should_upload_time.strftime('%Y-%m-%d %H:%M:%S'),

        }
        record.append(new_status)
    return JsonResponse(record,safe=False)

# @csrf_exempt
def sen_email_to_luosenlin(request):
    if request.method == "POST":
        # 开始时间
        start_time = request.POST['date_time'].split(',')[0]
        # 结束时间
        end_time = request.POST['date_time'].split(',')[1]
        # 未到
        absent = request.POST['absent']
        # 迟到
        late = request.POST['late']
        # 请假
        ask_for_leave = request.POST['ask_for_leave']
        # 课题管理表未更新成员名单
        upload_fail_real_name = request.POST['upload_fail_real_name']
        # 发送给
        send_to = request.POST['send_to'].split(",")
        # 额外抄送
        cc = request.POST['cc'].split(",")
        # 获得组内所有人名单
        group_users = User.objects.filter(group_name=request.user.group_name)
        # 自动打包并发送
        send_email(request,start_time, end_time, absent, late, ask_for_leave, upload_fail_real_name, group_users,cc,send_to)
        # 获得所有人的管理表路径
        group_path = [UploadRecord.objects.filter(user_name=user.real_name).order_by("-upload_time")[0].file_name for user in group_users if len(UploadRecord.objects.filter(user_name=user.real_name)) > 0]

        # return HttpResponseRedirect(reverse("sen_email_to_luosenlin"))
        context = {
            'success':"发送成功",
            'return_link':reverse("sen_email_to_luosenlin")
        }
        return render(request,'success.html',context=context)
    else:
        # 当前时间
        current_time = datetime.datetime.now().replace(tzinfo=pytz.timezone('Asia/Shanghai'))
        # 获得组内所有人
        group_users = User.objects.filter(group_name=request.user.group_name)
        # 获得未按时上传的人的真名
        upload_fail_real_name = [user.real_name for user in group_users if len(UploadRecord.objects.filter(user_name=user.real_name)) == 0 or (current_time - UploadRecord.objects.filter(user_name=user.real_name).order_by("-upload_time")[0].upload_time).days > 7]
        context = {
            'current_time': current_time,
            'upload_fail_real_name': " ".join(upload_fail_real_name),
        }
        return render(request, 'topic_manager_v2/sen_email_to_luosenlin.html', context=context)


def send_email(request, start_time: datetime.datetime, end_time: datetime.datetime, absent: str, late: str, ask_for_leave: str, upload_fail_real_name, group_users,cc,send_to):
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    import smtplib
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import zipfile
    sender_email = "robot@bfs.bit.edu.cn"
    receiver_email = send_to
    password = "123456"
    body = '''
    {}组-组会参会情况-{}
    时间：2019年08月27日 {}-{}
    未到：{}
    迟到：{}
    请假：{}
    课题管理表未更新：{}
    
    <html>
    <head></head>
    <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
    </body>
    </html>
    '''.format(request.user.group_name,start_time.strftime("%Y.%m.%d"),start_time.strftime("%H:%M"),end_time.strftime("%H:%M"),absent,late,ask_for_leave,upload_fail_real_name)

    html_body ='''
    <html>
      <head>
    
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
      </head>
      <body text="#000000" bgcolor="#FFFFFF">
        <div class="moz-text-html" lang="x-unicode">
          <p><span style="color: rgb(0, 0, 128); font-family: 'Microsoft
              YaHei UI'; text-indent: 28px;">{}组-组会参会情况-{}<br>
            </span></p>
          <div style="color: rgb(0, 0, 128); font-family: 'Microsoft YaHei
            UI'; text-indent: 2em;">时间：{} {}-{}</div>
          <div style="color: rgb(0, 0, 128); font-family: 'Microsoft YaHei
            UI'; text-indent: 2em;">未到：{}</div>
          <div style="color: rgb(0, 0, 128); font-family: 'Microsoft YaHei
            UI'; text-indent: 2em;">迟到：{}</div>
          <div style="color: rgb(0, 0, 128); font-family: 'Microsoft YaHei
            UI'; text-indent: 2em;">请假：{}</div>
          <div style="color: rgb(0, 0, 128); font-family: 'Microsoft YaHei
            UI'; text-indent: 2em;">课题管理表未更新：{}</div>
            <br />
            <div style="color: rgb(0, 0, 128); font-family: 'Microsoft YaHei
                UI'; text-indent: 2em;">此邮件为自动生成，请勿回复</div>
        </div>
      </body>
    </html>
    '''.format(request.user.group_name,start_time.strftime("%Y.%m.%d"),start_time.strftime("%Y年%m月%d日"),start_time.strftime("%H:%M"),end_time.strftime("%H:%M"),absent,late,ask_for_leave,upload_fail_real_name)
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ",".join(receiver_email)
    message["Subject"] = "{}组-组会参会情况-{}".format(request.user.group_name,start_time.strftime("%Y.%m.%d"))
    if cc[0] != "":
        message["cc"] = ",".join(cc)

    # Add body to email

    # message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    excel_paths = [BASE_DIR + UploadRecord.objects.filter(user_name=user.real_name).order_by("-upload_time")[0].file_name for user in group_users if len(UploadRecord.objects.filter(user_name=user.real_name)) > 0]
    attach_file_name = "{}组-课题管理表.zip".format(request.user.group_name)
    real_file_path = BASE_DIR + "/static/NSC.zip"
    zf = zipfile.ZipFile(real_file_path, mode='w')
    for excel_path in excel_paths:
        zf.write(excel_path,excel_path.split("/")[-1])
    zf.close()
    # Open PDF file in binary mode
    with open(real_file_path, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        "attachment",
        filename=('gb2312', '', attach_file_name),
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    with smtplib.SMTP("mail.isclab.org", 25) as server:
        server.login(sender_email, password)
        if cc[0] != "":
            server.sendmail(sender_email, (receiver_email,cc), text)
        else:
            server.sendmail(sender_email, receiver_email, text)


def daily_report(request):
    if request.method == "POST":
        date = request.POST['date']
        name = request.POST.get('name', '')
        sub_name = request.POST['sub_name']
        day = request.POST.get('day', '')
        quantitative = request.POST['quantitative']
        qualitative = request.POST['qualitative']
        type = request.POST['type']
        if name == "" or sub_name == "" or day == "" or qualitative == "" or qualitative == "":
            return JsonResponse("有未完成的内容", safe=False)
        if type == "本日工作":
            existing_record1 = DailyReport.objects.filter(date=date,username=request.user.username, type="本日工作")
            # if len(existing_record) > 0:
            existing_day = float(day)
            for record in existing_record1:
                existing_day += float(record.day)
            if existing_day > 1.0:
                return JsonResponse("本日工作超过了1人日", safe=False)
        else:
            existing_record1 = DailyReport.objects.filter(date=date,username=request.user.username, type="明日计划")
            # if len(existing_record) > 0:
            existing_day = float(day)
            for record in existing_record1:
                existing_day += float(record.day)
            if existing_day > 1.0:
                return JsonResponse("明日计划超过了1人日", safe=False)

        new_record = DailyReport(
            username=request.user.username,
            real_name=request.user.real_name,
            group_name=request.user.group_name,
            date=date,
            name=name,
            sub_name=sub_name,
            day = day,
            quantitative = quantitative,
            qualitative = qualitative,
            type = type,
        )
        new_record.save()
        return JsonResponse("success",safe=False)
    else:
        today = datetime.datetime.now()
        records = DailyReport.objects.filter(username=request.user.username, date=today.strftime("%Y-%m-%d"), type="本日工作")
        today_percentage = 0.0
        for record in records:
            today_percentage += record.day * 100
        records = DailyReport.objects.filter(username=request.user.username, date=today.strftime("%Y-%m-%d"), type="明日计划")
        tomorrow_percentage = 0.0
        for record in records:
            tomorrow_percentage += record.day * 100
        context = {
            'today_percentage' : today_percentage,
            'tomorrow_percentage' : tomorrow_percentage,
        }
        return render(request,'topic_manager_v2/daily_report.html',context=context)

def daily_report_summary(request):
    return render(request, 'topic_manager_v2/daily_report_summary.html', context=None)

def daily_report_summary_api(request):
    records = []
    all_records = DailyReport.objects.filter(username=request.user.username).order_by('date', '-type')
    date_occur = []
    for record in all_records:
        new_status = {
            'id': record.id,
            'real_name':record.real_name,
            'date':record.date if record.date not in date_occur else "",
            'name':record.name,
            'sub_name':record.sub_name,
            'day': record.day,
            'quantitative': record.quantitative,
            'qualitative': record.qualitative,
            'type': record.type if record.date.strftime("%d %b %Y")+record.type not in date_occur else "",
        }

        # if record.date not in date_occur:
        #     date_occur.append(record.date)
        # if record.date.strftime("%d %b %Y")+record.type not in date_occur:
        #     date_occur.append(record.date.strftime("%d %b %Y")+record.type)
        records.append(new_status)
    return JsonResponse(records,safe=False)

@csrf_exempt
def delete_daily_report_summary_api(request):
    record = DailyReport.objects.filter(username=request.user.username, id=request.POST['id'])
    if len(record) > 0:
        record.delete()
    return JsonResponse("success",safe=False)

@csrf_exempt
def edit_daily_report_summary_api(request):
    if request.method == "POST":
        date = request.POST['date']
        name = request.POST.get('name', '')
        sub_name = request.POST['sub_name']
        day = request.POST.get('day', '')
        quantitative = request.POST['quantitative']
        qualitative = request.POST['qualitative']
        type = request.POST['type']
        id =  request.POST['id']
        if name == "" or sub_name == "" or day == "" or qualitative == "" or qualitative == "":
            return JsonResponse("有未完成的内容", safe=False)
        if type == "本日工作":
            existing_record1 = DailyReport.objects.filter(username=request.user.username)
            # if len(existing_record) > 0:
            existing_day = float(day)
            for record in existing_record1:
                existing_day += float(record.day)
            if existing_day > 1.0:
                return JsonResponse("本日工作超过了1人日", safe=False)
        else:
            existing_record1 = DailyReport.objects.filter(date=date,username=request.user.username, type="明日计划")
            # if len(existing_record) > 0:
            existing_day = float(day)
            for record in existing_record1:
                existing_day += float(record.day)
            if existing_day > 1.0:
                return JsonResponse("明日计划超过了1人日", safe=False)
        existing_record = DailyReport.objects.filter(id=id, username=request.user.username)
        existing_record.date = date
        existing_record.name = name
        existing_record.sub_name = sub_name
        existing_record.day = day
        existing_record.day = day
        existing_record.quantitative = quantitative
        existing_record.qualitative = qualitative
        existing_record.save()
        return JsonResponse("success", safe=False)

def group_daily_report_summary(request):
    return render(request, 'topic_manager_v2/group_daily_report_summary.html', context=None)

def group_daily_report_summary_api(request):
    records = []
    all_records = DailyReport.objects.filter(group_name=request.user.group_name).order_by('username', 'fill_time', 'type')
    date_occur = []
    for record in all_records:
        new_status = {
            'real_name':record.real_name,
            'date':record.date if record.real_name+record.date.strftime("%d %b %Y") not in date_occur else "",
            'name':record.name,
            'sub_name':record.sub_name,
            'day': record.day,
            'quantitative': record.quantitative,
            'qualitative': record.qualitative,
            'type': record.type if record.real_name+record.date.strftime("%d %b %Y")+record.type not in date_occur else "",
        }

        if record.real_name+record.date.strftime("%d %b %Y") not in date_occur:
            date_occur.append(record.real_name+record.date.strftime("%d %b %Y"))
        if record.real_name+record.date.strftime("%d %b %Y")+record.type not in date_occur:
            date_occur.append(record.real_name+record.date.strftime("%d %b %Y")+record.type)
        records.append(new_status)
    return JsonResponse(records,safe=False)

def base_weekly_report(request):
    if request.method == "POST":
        date = request.POST['date']
        average_work_time = request.POST['average_work_time']
        valid_work_time = request.POST['valid_work_time']
        absence = request.POST['absence']
        rate = request.POST['rate']
        self_rate = request.POST['self_rate']
        any_questions = request.POST['any_questions']

        if date == "" or average_work_time == "" or valid_work_time == "" or absence == "" or rate == "" or self_rate == "" or any_questions == "":
            return JsonResponse("有未完成的内容", safe=False)
        # 平均工作时间/有效时间
        new_record = WeeklyReport(
            username=request.user.username,
            real_name=request.user.real_name,
            date=date,
            type="用时情况",
            name="平均工作时间",
            day = 0,
            quantitative = average_work_time,
            hidden_order = 0,
        )
        new_record = WeeklyReport(
            username=request.user.username,
            real_name=request.user.real_name,
            date=date,
            type="用时情况",
            name="有效时间",
            day = 0,
            quantitative = valid_work_time,
            hidden_order=1,
        )
        new_record.save()
        # 请假情况
        new_record = WeeklyReport(
            username=request.user.username,
            real_name=request.user.real_name,
            date=date,
            type="用时情况",
            name="请假情况",
            day = 0,
            quantitative = absence,
            hidden_order=3,
        )
        new_record.save()
        # 周评分（组长意见）
        new_record = WeeklyReport(
            username=request.user.username,
            real_name=request.user.real_name,
            date=date,
            type="本周工作",
            name="周评分",
            day = 0,
            quantitative = rate,
            hidden_order=4,
        )
        new_record.save()
        # 自评级（优/良/中/差）
        new_record = WeeklyReport(
            username=request.user.username,
            real_name=request.user.real_name,
            date=date,
            type="本周工作",
            name="自评级",
            day = 0,
            quantitative = self_rate,
            hidden_order=5,
        )
        new_record.save()
        # 问题建议
        new_record = WeeklyReport(
            username=request.user.username,
            real_name=request.user.real_name,
            date=date,
            type="问题建议",
            name="",
            day = 0,
            quantitative = any_questions,
            hidden_order=999,
        )
        new_record.save()
        return JsonResponse("success",safe=False)
    else:
        return render(request,'topic_manager_v2/base_weekly_report.html',context=None)

def weekly_report(request):
    if request.method == "POST":
        date = request.POST['date']
        name = request.POST.get('tomorrow_name', '')
        sub_name = request.POST['sub_name']
        day = request.POST.get('tomorrow_day', '')
        quantitative = request.POST['tomorrow_quantitative']
        qualitative = request.POST['tomorrow_qualitative']
        type = request.POST['type']
        if name == "" or sub_name == "" or day == "" or qualitative == "" or qualitative == "":
            return JsonResponse("有未完成的内容", safe=False)
        if type == "本日工作":
            existing_record1 = WeeklyReport.objects.filter(date=date,username=request.user.username, type="本日工作")
            # if len(existing_record) > 0:
            existing_day = float(day)
            for record in existing_record1:
                existing_day += float(record.day)
            if existing_day > 1.0:
                return JsonResponse("本日工作超过了1人日", safe=False)
        else:
            existing_record1 = WeeklyReport.objects.filter(date=date,username=request.user.username, type="明日计划")
            # if len(existing_record) > 0:
            existing_day = float(day)
            for record in existing_record1:
                existing_day += float(record.day)
            if existing_day > 1.0:
                return JsonResponse("明日计划超过了1人日", safe=False)

        new_record = WeeklyReport(
            username=request.user.username,
            real_name=request.user.real_name,
            date=date,
            name=name,
            sub_name=sub_name,
            day = day,
            quantitative = quantitative,
            qualitative = qualitative,
            type = type,
            hidden_order= 6 if type == "本周工作" else 7,
        )
        new_record.save()
        return JsonResponse("success",safe=False)
    else:
        today = datetime.datetime.now()
        records = WeeklyReport.objects.filter(username=request.user.username, date=today.strftime("%Y-%m-%d"), type="本日工作")
        today_percentage = 0.0
        for record in records:
            today_percentage += record.day * 100
        records = WeeklyReport.objects.filter(username=request.user.username, date=today.strftime("%Y-%m-%d"), type="明日计划")
        tomorrow_percentage = 0.0
        for record in records:
            tomorrow_percentage += record.day * 100
        context = {
            'today_percentage' : today_percentage,
            'tomorrow_percentage' : tomorrow_percentage,
        }
        return render(request,'topic_manager_v2/weekly_report.html',context=context)

def weekly_report_summary(request):
    return render(request, 'topic_manager_v2/weekly_report_summary.html', context=None)

def weekly_report_summary_api(request):
    records = []
    all_records = WeeklyReport.objects.filter(username=request.user.username).order_by('date', 'hidden_order')
    date_occur = []
    for record in all_records:
        new_status = {
            'real_name':record.real_name,
            'date':record.date if record.date not in date_occur else "",
            'name': record.name,
            'sub_name':record.sub_name,
            'day': record.day if record.day != 0 else "",
            'quantitative': record.quantitative,
            'qualitative': record.qualitative,
            'type': record.type if record.date.strftime("%d %b %Y")+record.type not in date_occur else "",
        }
        if record.date not in date_occur:
            date_occur.append(record.date)
        if record.date.strftime("%d %b %Y")+record.type not in date_occur:
            date_occur.append(record.date.strftime("%d %b %Y")+record.type)
        records.append(new_status)
    return JsonResponse(records,safe=False)

def semester_manage(request):
    if request.method == "POST":
        semester_name = request.POST['semester_name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if semester_name == "" or start_date == "" or end_date == "":
            return JsonResponse("有未完成的内容", safe=False)
        new_record = Semester(
            semester_name=semester_name,
            start_date=start_date,
            end_date=end_date,
        )
        new_record.save()
        return JsonResponse("success",safe=False)
    else:
        return render(request, 'topic_manager_v2/semester_manage.html', context=None)

def semester_manage_history(request):
    return render(request, 'topic_manager_v2/semester_manage_history.html', context=None)

def semester_manage_api(request):
    records = []
    all_records = Semester.objects.all()
    for record in all_records:
        new_status = {
            'semester_name':record.semester_name,
            'start_date':record.start_date,
            'end_date':record.end_date,
        }
        records.append(new_status)
    return JsonResponse(records,safe=False)

def edit_semester_api(request, semester_name):
    try:
        record = Semester.objects.get(semester_name=semester_name)
        record.delete()
    except Exception as e:
        return JsonResponse(str(e), safe=False)
    dict = {
        'message': 'success',
    }
    return JsonResponse(dict, safe=False)