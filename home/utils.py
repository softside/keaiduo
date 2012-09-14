#! /usr/bin/env python
#coding=utf-8
import os, sys, re
import urllib
import random
import string
from datetime import datetime
from HTMLParser import HTMLParser
from django.conf import settings
from django.http import HttpResponseRedirect
from urlparse import urlparse, urljoin, ParseResult


def get_time_this(orig_date, now_date=None):
    if now_date is None:
        now_date = datetime.now()
    diff = now_date - orig_date
    total_seconds = (diff.microseconds + (diff.seconds + diff.days * 24 * 3600) * 10**6) / 10**6
    #In version 2.7, there is total_seconds() attr of timedelta,which can be used here,
    #use this because my dev machine is mac osx 10.6
    if total_seconds < 0:
        return '1秒'
    elif total_seconds <= 60:
        return '%s秒前'% diff.seconds
    elif total_seconds <= 3600:
        return '%s分钟前' %(diff.seconds / 60)
    elif  orig_date.date() == now_date.date():
        return '今天'+datetime.strftime(orig_date,'%H:%S')
    else:
        return datetime.strftime(orig_date,'%m月%d日 %H:%S')

def redirect_back(request):
    referer = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer)
    
class TextExtractor(HTMLParser):
    def __init__(self, sz_limit=100):
        HTMLParser.__init__(self)
        self.data = ''
        self.sz_limit = sz_limit
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ('style', 'script'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag.lower() in ('style', 'script'):
            self.skip = False

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)
        
    def handle_data(self, data):
        if self.skip:
            return
        data = data.strip()
        data = data.replace(u'\u3000', ' ')
        data = re.sub(r'[\s\u3000][\s\u3000]+', ' ', data, re.U)
        self.data += data
        if len(self.data) > self.sz_limit:
            self.data = self.data[:self.sz_limit]
            raise DataOKException()
        
def extract_text(html_text, sz_limit=100, use_strip=True):
    parser = TextExtractor(sz_limit=sz_limit)
    try:
        parser.feed(html_text)
    except DataOKException:
        pass
    if use_strip:
        return parser.data.strip()
    else:
        return parser.data            