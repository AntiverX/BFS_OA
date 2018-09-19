from django.shortcuts import render

context = {
    'menus': {'bulletin': "通知公告",
              'news': "新闻",
              'library': "图书室"
              }
}


def index(request):
    # TODO 主页制作，模仿其他系统样式

    if request.user.is_authenticated:
        context['username'] = request.user.username
        return render(request, 'index.html', context=context)
    else:
        return render(request, 'index.html')


def bulletin(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "bulletin.html", context=context)


def news(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "news.html", context=context)

def library(request):
    # TODO template及逻辑
    context['username'] = request.user.username
    return render(request, "library.html", context=context)