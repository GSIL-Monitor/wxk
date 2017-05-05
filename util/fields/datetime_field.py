# encoding: utf-8

from __future__ import unicode_literals
import easy_date

from wtforms import fields, ValidationError
try:
    from wtforms.fields.core import _unset_value as unset_value
except ImportError:
    from wtforms.utils import unset_value

from ..widgets import DateWidget


class DateField(fields.DateField):
    """用于处理日期与Unix时间戳的正确显示。"""
    widget = DateWidget()

    def __init__(self, label=None, validators=None, **kwargs):
        super(DateField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        if len(valuelist) and valuelist[0]:
            self.data = easy_date.convert_from_string(
                valuelist[0], '%Y-%m-%d', None, float)
