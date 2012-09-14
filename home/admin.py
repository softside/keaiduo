# -*- coding: UTF-8 -*-
from django.contrib import admin
from home.models import *

for cls in [Profile,Blog,Status]:
    admin.site.register(cls)