# coding: utf-8

import datetime
import os
import time,re

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import simplejson as json                                                                                                          

from taggit.managers import TaggableManager
import jsonfield

from home.mixins import CommonMixin
from utils import *

USER_RE = re.compile(r'\@(?P<pet_name>.*?)(?=\s|$|\:)')


class Profile(CommonMixin, models.Model):
    user = models.ForeignKey(User, db_index=True, related_name="profile",unique=True)
    name = models.CharField(max_length=40, verbose_name=u'名字', unique=True)
    logo = models.CharField(max_length=300,default="",blank=True)
    sina_code = models.CharField(max_length=120, default='', blank=True, null=True, verbose_name='sina_code')#use for sina login
    sina_expire = models.CharField(max_length=120, default='', blank=True, null=True, verbose_name='sina_expire')#use for sina login
    date_created = models.DateTimeField(db_index=True,auto_now_add=True)

    class Meta:
        verbose_name = u'个人信息'
        verbose_name_plural = verbose_name
        ordering = ['-date_created']


    def __unicode__(self):
        return self.name

class Status(CommonMixin,models.Model):
    user = models.ForeignKey(User, db_index=True, related_name="status")
    content = models.TextField(u'亲，说点什么', max_length=30)
    comment_id = models.IntegerField(blank=True, null=True, db_index=True)##评论id
    forward_id = models.IntegerField(blank=True, null=True, db_index=True)##转发id
    quote_id = models.IntegerField(blank=True, null=True, db_index=True)##引用id
    date_created = models.DateTimeField()
    like_number = models.IntegerField(default=0)##引用id

    class Meta:
        verbose_name = '状态'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def get_time_this(self):
        return get_time_this(self.date_created)

    def comment_num(self):
        num = Status.objects.filter(comment_id = self.id).count()
        return num 

    def rt_num(self):
        num = Status.objects.filter(forward_id = self.id).count()
        return num

    def get_quote(self):
        if self.quote_id:
            rt_status = Status.objects.filter(pk=self.quote_id)
            if rt_status:
                return rt_status[0]
    def get_status(self):
        key='status'+str(self.id)
        from helper import *
        status = get_value(key)
        if status:
            return status['status']
        else:
            return self.content

def post_save_status(sender, instance, created, *args, **kwargs):
    if created:
        status = instance.content
        at_user = []
        for one in USER_RE.findall(status):
            profile = Profile.objects.filter(name=one)
            if profile:
                status = status.replace("@"+one, "<a  href='/weibo/"+ one +"'>@"+one +"</a>" )
                #at_user.append(profile.id)
                from helper import *
                create_status_cache(instance.id,{'status':status})
            else:
                continue

    #TODO,目前只处理了@转换的部分，还需要处理@提示，回复提示
post_save.connect(post_save_status, sender=Status)                                                                                                  


class Blog(CommonMixin,models.Model):
    user = models.ForeignKey(User, db_index=True, related_name="blog",unique=True)
    content = models.TextField(u'亲，说点什么', max_length=30)



class MyCache(CommonMixin, models.Model):
    key = models.CharField(max_length=60, verbose_name=u'key', unique=True,db_index=True)
    value = jsonfield.JSONField()

        



