import os
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
project_dir = os.path.abspath(os.path.dirname(__file__))
print project_dir
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'home.views.index', name='index'),
    url(r'^login/$', 'home.weibo_views.sina_auth_redirect', name='login'),
    url(r'^sinacallback/$', 'home.weibo_views.callback'),
    url(r'^logout/$', 'home.views.logout_page', name='logout'),
    url(r'^accounts/', include('userena.urls')),

    url(r'^blog/new/$', 'home.views.new_blog', name='new_blog'),
    url(r'^blog/(?P<pk>\d+)/$', 'home.views.new_blog', name='blog_item'),
    url(r'^blog/(?P<pk>\d+)/edit/$', 'home.views.new_blog', name='edit_blog'),

    url(r'^status/new/$', 'home.views.new_status', name='new_status'),
    url(r'^get_comment$', 'home.views.get_comment', name='get_comment'),
    url(r'^post_comment$', 'home.views.post_comment', name='post_comment'),
    url(r'^post_rt/(?P<status_id>\d+)/$', 'home.views.post_rt', name='post_rt'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(project_dir, 'static')}),




)
