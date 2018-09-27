# coding=utf-8
# Created by liuye at 2018/9/26

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from customApi.models import customApi


@csrf_exempt
def custom_api(request):
    post_response = {'ret': 'post success!!'}
    get_response = {'ret': 'get success!!'}
    if request.method == 'POST':
        className = request.POST.get('className')
        print(className)
        pkgName = request.POST.get('pkgName')
        print(pkgName)
        version = request.POST.get('version')
        print(version)
        leakDetail = request.POST.get('leakDetail')
        print(leakDetail)
        customApi.objects.create(className=className, pkgName=pkgName, version=version, leakDetail=leakDetail)
        return JsonResponse(post_response)
    if request.method == 'GET':
        return JsonResponse(get_response)
