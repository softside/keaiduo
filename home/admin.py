# -*- coding: utf-8 -*-
from django.contrib import admin
from home.models import *

for cls in [Blog,Status,MyCache]:
    admin.site.register(cls)
