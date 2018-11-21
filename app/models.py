#_*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class Datas(models.Model):
    all_data = models.CharField(max_length=1000)
    create_time = models.DateTimeField(default=datetime.now)
    result = models.CharField(null=True, max_length=200)

    class Meta:
        verbose_name = u"数据"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.all_data
