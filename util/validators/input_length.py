# coding: utf-8

from __future__ import unicode_literals

from wtforms.validators import ValidationError


class InputLength(object):

    # 默认长度为6，可自由定制长度
    def __init__(self, message='密码的长度最少6位', c_length=6):
        self.message = message
        self.c_length = c_length

    # 表单字段长度验证
    def __call__(self, form, field):
        message = self.message
        if field.data:
            if len(field.data) < self.c_length:
                raise ValidationError(message)
