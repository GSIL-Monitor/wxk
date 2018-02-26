# coding: utf-8

from __future__ import unicode_literals

import re
from wtforms.validators import ValidationError


class LetterNumberRequired(object):
    def __init__(self, message="只能输入字母和数字"):
        self.message = message

    def __call__(self, form, field):
        message = self.message
        rep = '^[A-Za-z0-9]+$'
        if field.data:
            if not re.match(rep, field.data):
                raise ValidationError(message)
