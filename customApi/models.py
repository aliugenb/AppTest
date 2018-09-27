from django.utils import timezone as timezone

from django.db import models

# Create your models here.


class customApi(models.Model):
    className = models.TextField('className')
    pkgName = models.CharField('pkgName', max_length=1024)
    version = models.CharField('版本', max_length=1024)
    leakDetail = models.TextField("详细信息")
    create_time = models.DateTimeField('创建时间', default=timezone.now)
