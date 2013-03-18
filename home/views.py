# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.html import escape as safescape


from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django import forms
from utils import *
from models import Blog,Status

def logout_page(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('index')

def index(request,template_name="home/index.html"):
    status = Status.objects.filter(comment_id__isnull = True)
    ctx = {'status':status,}
    return render(request, template_name, ctx)

class BlogEditForm(forms.ModelForm):
    class Meta(object):
        model = Blog
        fields =(
            'content',
            )

@csrf_exempt
def new_blog(request,blog_id=None,template_name="blog/new.html"):
    if request.method == "POST":
        form = BlogEditForm(request.POST)
        if form.is_valid():

            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('index')
    else:
        form = BlogEditForm()
        ctx = {'form':form}
    return  render(request, template_name, ctx)

def edit_blog(request,blog_id=None,template_name="blog/new.html"):
    blog = get_object_or_404(Blog,pk=blog_id)
    if request.method == "POST":
        form = BlogEditForm(request.POST,instance=blog)
        if form.is_valid():
            blog = form.save()
            return redirect('/')
    else:
        form = BlogEditForm(instance=blog)
        ctx = {'form':form}
    return  render(request, template_name, ctx)


@login_required
@csrf_exempt
def new_status(request):
    user = request.user
    if request.method == "POST":
        text = request.POST.get('text', '')
        if text:
            status = Status.objects.create(user=user,
                                        content=text,)
#            save_timeline_by_pet(pet.id, status.id)
#            for one in pet.get_followers():
#                save_timeline_by_pet(one.id, status.id)
#
#    sina = request.POST.get('sina','')#同步到sina
#    if sina:
#        client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
#        profile = request.user.get_profile()
#        client.set_access_token(profile.sina_code, profile.sina_expire)
#        try:
#            if pic_id:
#                pet_pic = PetPicture.objects.get(id=pic_id)
#                status = client.post.statuses__upload(status=text,pic=open(pet_pic.image.url))
#            else:
#                status = client.post.statuses__update(status=text)
#        except APIError:
#            log.info(APIError)
    return HttpResponseRedirect('/')
@login_required
def get_comment(request):
    status_id = int(request.GET.get('status_id', 0))
    comments = Status.objects.filter(comment_id=status_id)
    comment_num = comments.count()
    if comment_num > 6:
        remain_num = comment_num - 6
    return render(request,'widget/status_comment.html', locals())


@csrf_exempt
@login_required
def post_comment(request):
    if request.method == 'POST':
        text = safescape(request.POST.get('comment_text', '')).strip()
        rt = request.POST.get("rt", '')
        comment_id = request.POST.get('status_id')
        c_status = get_object_or_404(Status, pk=comment_id)

        status = Status.objects.create(user=request.user, content=text, comment_id=comment_id)

        if rt:
            status = PetStatus.objects.create(pet=pet, forward_id=comment_id,
                                       status=text,)
    return redirect_back(request)

@csrf_exempt
@login_required
def post_rt(request, status_id):
    status = get_object_or_404(Status, pk=status_id)

    forward_id = status.id
    quote_id = status.quote_id or status.id
    content = safescape(request.POST.get('content', ''))
    if content:
        status = Status.objects.create(user=request.user, forward_id=forward_id, quote_id=quote_id,
                                       content=content,)
    return HttpResponse("Y")
