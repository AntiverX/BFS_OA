from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from BFS_OA.settings import BASE_DIR
from .models import UploadRecord
from user_info.models import User
import datetime
import pytz
from django.urls import reverse
import os

# Create your views here.
def index(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        short_file_name = "/static/file/topic_manager/" + request.user.group_name + "-课题管理-" + request.user.real_name + "-" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M') + ".xlsx"
        file_name = BASE_DIR + "/static/file/topic_manager/" + request.user.group_name + "-课题管理-" + request.user.real_name + "-" + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M') + ".xlsx"
        with open(file_name.encode(), "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        new_record = UploadRecord(
            user_name=request.user.real_name,
            file_name=short_file_name,
            upload_time=datetime.datetime.now(),
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
    all_record = UploadRecord.objects.filter(user_name=request.user.real_name)
    context = {
        'all_record': all_record,
    }
    return render(request, 'topic_manager_v2/upload_history.html', context=context)


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


def sen_email_to_luosenlin(request):
    if request.method == "POST":
        # 开始时间
        start_time = request.POST['start_time']
        # 结束时间
        end_time = request.POST['end_time']
        # 未到
        absent = request.POST['absent']
        # 迟到
        late = request.POST['late']
        # 请假
        ask_for_leave = request.POST['ask_for_leave']
        # 课题管理表未更新成员名单
        upload_fail_real_name = request.POST['upload_fail_real_name']
        # 获得组内所有人名单
        group_users = User.objects.filter(group_name=request.user.group_name)
        # 自动打包并发送
        send_email(start_time, end_time, absent, late, ask_for_leave, upload_fail_real_name, group_users)
        # 获得所有人的管理表路径
        group_path = [UploadRecord.objects.filter(user_name=user.real_name).order_by("-upload_time")[0].file_name for user in group_users if len(UploadRecord.objects.filter(user_name=user.real_name)) > 0]

        return HttpResponseRedirect(reverse("sen_email_to_luosenlin"))
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


def send_email(start_time: datetime.datetime, end_time: datetime.datetime, absent: str, late: str, ask_for_leave: str, upload_fail_real_name, group_users):
    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    import smtplib
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import zipfile
    port = 25
    smtp_server = "mail.isclab.org"
    sender_email = "wangshuaipeng@bfs.bit.edu.cn"
    receiver_email = "wangshuaipeng@bfs.bit.edu.cn"
    password = "123456"
    body = '''
    网络安全3组-组会参会情况-{}
    时间：2019年08月27日 {}-{}
    未到：{}
    迟到：{}
    请假：{}
    课题管理表更新情况：全部更新
    '''.format(start_time.strftime("%Y.%m.%d"),start_time.strftime("%H:%M"),end_time.strftime("%H:%M"),absent,late,ask_for_leave)
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "网络安全3组-组会参会情况-" + start_time.strftime("%Y.%m.%d")
    message["cc"] = receiver_email  # Recommended for mass emails

    # Add body to email

    message.attach(MIMEText(body, "plain"))

    excel_paths = [BASE_DIR + UploadRecord.objects.filter(user_name=user.real_name).order_by("-upload_time")[0].file_name for user in group_users if len(UploadRecord.objects.filter(user_name=user.real_name)) > 0]
    attach_file_name = "网络安全3组-课题管理表.zip"
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
        filename=('utf8', '', attach_file_name),
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    with smtplib.SMTP("mail.isclab.org", 25) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
