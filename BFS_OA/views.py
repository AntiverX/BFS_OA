from django.shortcuts import render


def index(request):
    context = {
        'menus': {'bulletin': "通知公告",
                  'news': "新闻",
                  'library': "图书室"
                  }
    }
    if request.user.is_authenticated:
        context['username'] = request.user.username
        return render(request, 'index.html', context=context)
    else:
        return render(request, 'index.html')
