# Created by liuye at 2018/9/14
from django.shortcuts import render
from bugstatistics.models import BUG


def bugstatistics(request):
    bug_list = BUG.objects.all()
    return render(request, 'bugstatistics/index.html', {'bugs':bug_list})


def add_bug(request):
    return render(request, 'bugstatistics/add_bug.html')