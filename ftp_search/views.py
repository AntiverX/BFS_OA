from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
import ftplib
from .models import FileRecord, DirectoryRecord
import os
from multiprocessing import cpu_count
import time
from django.db import transaction

# FTP服务器地址
server_address = ""


class FTP():
    def __init__(self, host, username, password):
        self.ftp = ftplib.FTP(host, username, password)
        self.ftp.encoding = 'utf-8'
        self.all_directory = []
        self.all_files = 0

    # 判断一个路径是否为一个目录
    def is_directory(self, pathname):
        try:
            content = self.ftp.nlst(pathname)
            if len(content) == 1:
                return 0
            else:
                return 1
        except Exception as e:
            print(e)

    # 以数组形式列出目录中的文件
    def list_directory(self, pathname):
        try:
            content = self.ftp.nlst(pathname)
            return content
        except Exception as e:
            print(e)

    # 遍历文件夹
    def traverse_directory_and_get_directory(self, pathname):
        for filename in self.list_directory(pathname):
            if self.is_directory(filename):
                self.all_directory.append(filename)
                new_record = DirectoryRecord(filename=filename.split('/')[-1], filepath=filename)
                new_record.save()
                self.traverse_directory_and_get_directory(filename)
            else:
                pass

    def traverse_file(self, pathname):
        for filename in self.list_directory(pathname):
            if not self.is_directory(filename):
                new_record = FileRecord(filename=filename.split('/')[-1], filepath=filename)
                new_record.save()
                self.all_files += 1
            else:
                pass


# Create your views here.
def index(request):
    if request.method == "POST":
        key = request.POST['key']
        return HttpResponseRedirect("http://192.168.2.7/?search={}&c=1000".format(key))
    else:
        return render(request, 'ftp_search/index.html', context=None)


@transaction.atomic
def ftp_settings(request):
    if request.method == "GET":
        return render(request, 'ftp_search/ftp_settings.html', context=None)
    else:
        if request.POST['action'] == "search_directory":
            DirectoryRecord.objects.all().delete()
            FileRecord.objects.all().delete()
            ftp = FTP('192.168.5.2', 'BFS-AQ', 'WLAQ')
            start = time.time()
            ftp.traverse_directory_and_get_directory("/")
            all_directory = DirectoryRecord.objects.all()
            for directory in all_directory:
                ftp.all_directory.index(directory.filepath)
            # for pathname in ftp.all_directory:
            #             #     ftp.traverse_file(pathname)
            end = time.time()
            return HttpResponse("Time:{},Directory:{},RecordLength:{}".format(end - start, len(ftp.all_directory),len(all_directory)))
