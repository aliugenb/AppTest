# Created by liuye at 2018/9/9
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def add(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


def learn(request):
    string = u'hello'
    tutorial_list = ["HTML", "CSS", "jQuery", "Python", "Django"]
    info_dict = {'site': u'自强学堂', 'content': u'各种IT技术教程'}
    int_list = map(str, range(100))
    return render(request, 'imgupload/index.html', {'tutorial_list': tutorial_list, 'string': string,
                                                    'info_dict': info_dict, 'int_list': int_list})