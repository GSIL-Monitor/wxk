# coding: utf-8

from __future__ import unicode_literals

import re
from wtforms.validators import ValidationError


class LowercaseRequired(object):
    def __init__(self, message="只能输入小写字母"):
        self.message = message

    def __call__(self, form, field):
        message = self.message
        rep = '^[a-z]+$'
        if field.data:
            if not re.match(rep, field.data):
                raise ValidationError(message)
