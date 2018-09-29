# Created by liuye at 2018/9/14
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from bugstatistics.models import BUG


def bugstatistics(request):
    bug_list = BUG.objects.all().order_by('-id')
    return render(request, 'bugstatistics/index.html', {'bugs': bug_list})


@csrf_exempt
def add_bug(request):
    post_response = {'ret': 1, 'msg': 'post success!!'}
    get_response = {'error': '使用post请求!!'}
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        iteration = request.POST.get('iteration')
        print(iteration)
        version = request.POST.get('version')
        print(version)
        status = request.POST.get('status')
        print(status)
        BUG.objects.create(title=title, iteration=iteration, version=version, status=status)
        return JsonResponse(post_response)
    if request.method == 'GET':
        return JsonResponse(get_response)
