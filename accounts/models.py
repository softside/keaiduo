# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    favourite_snack = models.CharField(_('favourite snack'),
                                       max_length=5)
    name = models.CharField(max_length=40, verbose_name=u'名字', unique=True)
    logo = models.CharField(max_length=300,default="",blank=True)
    sina_code = models.CharField(max_length=120, default='', blank=True,
                                 null=True, verbose_name='sina_code')#use for sina login
    sina_expire = models.CharField(max_length=120, default='',
                                   blank=True, null=True,
                                   verbose_name='sina_expire')#use for sina login
    date_created = models.DateTimeField(db_index=True,auto_now_add=True)

    class Meta:
        verbose_name = u'个人信息'
        verbose_name_plural = verbose_name
        ordering = ['-date_created']


    def __unicode__(self):
        return self.name
