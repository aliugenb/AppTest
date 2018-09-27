# Created by liuye at 2018/9/9
import os

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def imgupload(request):
    if request.method == "POST":
        f = request.FILES.get('imgFile')
        baseDir = os.path.dirname(os.path.abspath(__name__));
        jpgdir = os.path.join(baseDir, 'imgupload','img');
        if not os.path.exists(jpgdir):
            os.makedirs(jpgdir)
        filename = os.path.join(jpgdir, f.name);
        fobj = open(filename, 'wb');
        for chrunk in f.chunks():
            fobj.write(chrunk);
        fobj.close();
    return render(request, 'imgupload/index.html')