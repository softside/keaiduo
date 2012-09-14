# coding: utf-8

from django.db import models
from datetime import datetime

class CommonMixin(object):
    def before_save(self):
        pass
    def after_save(self):
        pass

    def save(self, **kwargs):
        if not self.pk:
            self.date_created = datetime.now()
        intact = kwargs.pop('intact', False)
        if not intact:
            self.date_modified = datetime.now()
        super(CommonMixin, self).save(**kwargs)
        self.after_save()