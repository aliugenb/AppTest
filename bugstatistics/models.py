from django.db import models
from django.utils import timezone as timezone


class BUG(models.Model):
    STATUS_OPTIONS = (
        ('p', 'pass'),
        ('a', 'activated')
    )
    title = models.CharField('bug标题', max_length=1024)
    iteration = models.CharField('需求', max_length=30)
    version = models.CharField('版本', max_length=30)
    status = models.CharField('状态', max_length=30, choices=STATUS_OPTIONS)
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    end_time = models.DateTimeField('关闭时间', auto_now=True)