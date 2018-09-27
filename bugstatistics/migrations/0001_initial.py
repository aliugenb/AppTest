# Generated by Django 2.1.1 on 2018-09-14 08:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BUG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='bug标题')),
                ('iteration', models.CharField(max_length=30, verbose_name='需求')),
                ('version', models.CharField(max_length=30, verbose_name='版本')),
                ('status', models.CharField(choices=[('p', 'pass'), ('a', 'activated')], max_length=30, verbose_name='状态')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('end_time', models.DateTimeField(auto_now=True, verbose_name='关闭时间')),
            ],
        ),
    ]