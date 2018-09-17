from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = {
        'menus': {'info': "我的信息",
                  'schedule': "课程表", },
        'username' : request.user.username
    }
    return render(request, 'index.html', context=context)

