# encoding: utf-8

from __future__ import unicode_literals
import re

from wtforms import fields
from wtforms.widgets import TextInput
from wtforms.validators import ValidationError
from wtforms.compat import text_type


class HourMinuteField(fields.Field):
    widget = TextInput()
    def e_init__(self, label=None, validators=None, **kwargs):
        super(HourMinuteField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        if len(valuelist) and valuelist[0]:
            message = "格式00:00"
            rep = '^(\d+):[0-5]\d$'
            if not re.match(rep, valuelist[0]):
                raise ValidationError(message)

            minute = float('%.2f' % float(int(valuelist[0].split(":")[1]) / 60.0))
            hour = int(valuelist[0].split(":")[0])
            
            self.data = hour + minute

    def _value(self):

        if self.data is not None:
            value = str(self.data)
            hour = str(int(value.split(".")[0]))
            minute = value.split(".")[1]
            # 四舍五入
            minite = int((float('.'.join(['0', minute])) * 60) + 0.5)
            minite = str(minite)
            if len(minite) < 2:
                minite = '0' + minite
            value = ':'.join([hour, minite])
            return text_type(value)
        else:
            return ''
