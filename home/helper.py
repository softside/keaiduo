# coding: utf-8

from django.utils import simplejson as json
from models import Status,MyCache

def get_value(key):
	value = MyCache.objects.filter(key = key)
	if value:
		return value[0].value

def create_status_cache(status_id,content):
	key = 'status'+str(status_id)
	MyCache.objects.create(key = key,value=content)

