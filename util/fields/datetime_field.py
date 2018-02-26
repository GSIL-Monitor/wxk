# encoding: utf-8

from __future__ import unicode_literals
import easy_date
import time
from datetime import date

from wtforms import fields
try:
    from wtforms.fields.core import _unset_value as unset_value
except ImportError:
    from wtforms.utils import unset_value

from ..widgets import DateWidget, DateTimeWidget, DateIntWidget


class DateField(fields.DateField):
    """用于处理日期与Unix时间戳的正确显示。"""
    widget = DateWidget()

    def __init__(self, label=None, validators=None, **kwargs):
        super(DateField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        if len(valuelist) and valuelist[0]:
            if isinstance(valuelist[0], date):
                valuelist[0] = valuelist[0].strftime('%Y-%m-%d')
            self.data = valuelist[0]


class DateFieldInt(DateField):

    def process_formdata(self, valuelist):
        super(DateFieldInt, self).process_formdata(valuelist)
        if self.data:
            self.data = int(self.data)


class DateTimeFieldInt(fields.DateField):

    widget = DateTimeWidget()

    def __init__(self, label=None, validators=None, **kwargs):
        super(DateTimeFieldInt, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        if len(valuelist) and valuelist[0]:
            self.data = int(easy_date.convert_from_string(
                valuelist[0], '%Y-%m-%d %H:%M:%S', None, float))


class DateInt(fields.DateField):

    widget = DateIntWidget()

    def __init__(self, label=None, validators=None, **kwargs):
        super(DateInt, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        if len(valuelist) and valuelist[0]:
            self.data = int(easy_date.convert_from_string(
                valuelist[0], '%Y-%m-%d', None, float))
