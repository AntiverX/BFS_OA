from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from BFS_OA.settings import BASE_DIR
import datetime
from .models import Train, PollRecord
from django.urls import reverse
from user_info.models import User
import operator


# Create your views here.
def index(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        training_type = request.POST['training_type']
        if training_type == "reference_training":
            file_name = "{}/static/file/reference_training/{}-文献检索培训-{}.zip".format(BASE_DIR, request.user.real_name, datetime.datetime.now().strftime('%Y.%m.%d %H:%M'))
            short_file_name = "/static/file/reference_training/{}-文献检索培训-{}.zip".format(request.user.real_name, datetime.datetime.now().strftime('%Y.%m.%d %H:%M'))
        elif training_type == "cpp_training":
            file_name = "{}/static/file/cpp_training/{}-C++索培训-{}.zip".format(BASE_DIR, request.user.real_name, datetime.datetime.now().strftime('%Y.%m.%d %H:%M'))
            short_file_name = "/static/file/cpp_training/{}-C++索培训-{}.zip".format(request.user.real_name, datetime.datetime.now().strftime('%Y.%m.%d %H:%M'))
        else:
            file_name = ""
            short_file_name = ""
        with open(file_name.encode(), "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        new_record = Train(
            user_name=request.user.real_name,
            file_name=short_file_name,
            upload_time=datetime.datetime.now(),
            training_type=training_type,
        )
        new_record.save()
        return HttpResponseRedirect(reverse('newcomer_index'))
    else:
        try:
            context = {
                'have_uploaded': 1,
                'all_record': Train.objects.filter(user_name=request.user.real_name),
            }
        except:
            context = {
                'have_uploaded': 0,
            }
        return render(request, 'newcomer/index.html', context=context)


def score(request, type):
    if request.method == "GET" and type == "reference_training":
        all_newcomer = User.objects.filter(student_type="新生")
        not_scored_newcomer = []
        for nwecomer in all_newcomer:
            existing_record = PollRecord.objects.filter(newcomer_name=nwecomer.real_name, training_type="reference_training")
            if len(existing_record) == 0:
                not_scored_newcomer.append(nwecomer)
        context = {
            'active': "reference",
            'all_newcomer': not_scored_newcomer,
            'title': '文献检索培训答辩评分表',
            'score_1': "汇报过程（20）",
            'score_2': "五个问题（40）",
            'score_3': "培训收获（20）",
            'score_4': "问题回答（20）",
            'hint': '''<p>评分标准:</p>
                    <p>汇报过程：PPT制作，演讲效果，时间控制</p>
                    <p>五个问题：文档最后五个问题简要展示情况</p>
                    <p>培训收获：有充分收获，反思深刻</p>
                    <p>问题回答：问题理解准确，回答正确</p>''',
            'type': "reference_training",
        }
        return render(request, 'newcomer/score.html', context=context)
    elif request.method == "GET" and type == "cpp_training":
        all_newcomer = User.objects.filter(student_type="新生")
        not_scored_newcomer = []
        for nwecomer in all_newcomer:
            existing_record = PollRecord.objects.filter(newcomer_name=nwecomer.real_name, training_type="cpp_training")
            if len(existing_record) == 0:
                not_scored_newcomer.append(nwecomer)
        context = {
            'active': "cpp",
            'all_newcomer': not_scored_newcomer,
            'title': 'C++培训答辩评分表',
            'score_1': "汇报过程（20）",
            'score_2': "编程能力（40）",
            'score_3': "培训收获（20）",
            'score_4': "问题回答（20）",
            'hint': '''<p>评分标准:</p>
                    <p>汇报过程：PPT制作，演讲效果，时间控制</p>
                    <p>编程能力：考核得分，PPT答辩情况</p>
                    <p>培训收获：有充分收获，反思深刻</p>
                    <p>问题回答：问题理解准确，回答正确</p>''',
            'type': "cpp_training",
        }
        return render(request, 'newcomer/score.html', context=context)
    elif request.method == "POST":
        new_record = PollRecord(
            newcomer_name=request.POST['newcomer_name'],
            score_1=request.POST['score_1'],
            score_2=request.POST['score_2'],
            score_3=request.POST['score_3'],
            score_4=request.POST['score_4'],
            user_name=request.user.real_name,
            training_type=request.POST['training_type'],
            remark=request.POST['remark'],
        )
        new_record.save()
        return HttpResponseRedirect(reverse('score', kwargs={'type': request.POST['training_type']}))


def status(request):
    cpp_scores = {}
    reference_scores = {}
    all_newcomer = User.objects.filter(student_type="新生")
    for newcomer in all_newcomer:
        # 计算C++平均分
        results = PollRecord.objects.filter(newcomer_name=newcomer.real_name, training_type="cpp_training")
        cpp_score = 0
        for result in results:
            cpp_score = cpp_score + result.score_1 + result.score_2 + result.score_3 + result.score_4
        try:
            cpp_scores[newcomer.real_name] = cpp_score / len(results)
        except:
            cpp_scores[newcomer.real_name] = 0
        # 计算文献检索平均分
        results = PollRecord.objects.filter(newcomer_name=newcomer.real_name, training_type="reference_training")
        reference_score = 0
        for result in results:
            reference_score = reference_score + result.score_1 + result.score_2 + result.score_3 + result.score_4
        try:
            reference_scores[newcomer.real_name] = reference_score / len(results)
        except:
            reference_scores[newcomer.real_name] = 0
    reference_scores = sorted(reference_scores.items(), key=operator.itemgetter(1), reverse=True)
    cpp_scores = sorted(cpp_scores.items(), key=operator.itemgetter(1), reverse=True)
    context = {
        'cpp_scores': cpp_scores,
        'reference_scores': reference_scores,
    }
    return render(request, 'newcomer/status.html', context=context)


def status_detail(request, type, newcomer_name):
    if type == "cpp_training":
        comment_type = "C++培训"
        comments = PollRecord.objects.filter(newcomer_name=newcomer_name, training_type="cpp_training")
    else:
        comment_type = "文献检索培训"
        comments = PollRecord.objects.filter(newcomer_name=newcomer_name, training_type="reference_training")
    context = {
        'type': comment_type,
        'comments': comments,
    }
    return render(request, 'newcomer/status_detail.html', context=context)
