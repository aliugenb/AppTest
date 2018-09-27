# Created by liuye at 2018/9/9
from django.shortcuts import render


def sharetext(request):
    return render(request, 'sharetext/sharetext.html')