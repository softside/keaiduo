#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext as Context

from keaiduo.settings import APP_KEY,APP_SECRET,CALLBACK_URL
from accounts.models import MyProfile

from home.weibo import APIClient



def create_sina_user(uid):
    name = "sina_"+uid
    random_password = User.objects.make_random_password(length=10, allowed_chars='123456789')
    user  = User.objects.filter(username=name)
    if not user:
        user = User.objects.create_user(name,'',random_password)
        user.is_active = True
        user.save()
        return user
    return user[0]


def sina_auth_redirect(request):
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    return HttpResponseRedirect(url)


def callback(request):
    code = request.GET.get('code')
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    client.set_access_token(access_token, expires_in)
    sina_info = client.get.users__show(uid=r.uid)
    username="sina_"+r.uid
    sinauser = User.objects.filter(username=username)
    if request.user.is_authenticated() and len(sinauser) > 0 and sinauser[0] != request.user:
            return HttpResponse("错误！每个微博帐号只能绑定一个帐号！")
    if len(sinauser) > 0 :
        #处理已绑定的存在的用户
        login_user = sinauser[0]

        login_user.backend='django.contrib.auth.backends.ModelBackend'
        login(request, login_user)
        profile = login_user.get_profile()
        profile.sina_code = access_token
        profile.sina_expire = expires_in
        profile.save()
        return HttpResponseRedirect("/")
    if request.user.is_authenticated() :
        #这个是处理绑定微薄账号的
        user = request.user
        user.username = username
        user.save()
        profile = user.get_profile()
        profile.sina_code = access_token
        profile.sina_expire = expires_in
        profile.save()
        return HttpResponseRedirect(reverse('/'))

    user = create_sina_user(r.uid)
    user.backend='django.contrib.auth.backends.ModelBackend'
    login(request, user)
    name = sina_info['name']
    t_profile = Profile.objects.filter(name=name)#判断昵称可用
    profile , _= Profile.objects.get_or_create(user=user)
    form = ProfileEditForm(instance=profile)
    profile.name = name
    if t_profile:
        profile.name=username
    profile.sina_code=access_token
    profile.sina_expire = expires_in
    profile.save()
    return HttpResponseRedirect(reverse('/'))


@login_required
def sina_sign_off(request):
    user = request.user
    if not user.username.startswith("sina_"):
        return HttpResponseRedirect(reverse('profile_edit'))
    username = datetime.now().strftime("%Y%m%d%H%M%S%f")
    user.username = "sign_off"+username
    user.save()
    profile = user.get_profile()
    profile.sina_code =""
    profile.sina_expire=""
    profile.save()
    return HttpResponseRedirect(reverse('profile_edit'))
