# coding: utf-8

from __future__ import unicode_literals

from wtforms.validators import ValidationError

from modules.models.user import User


class EmailUniqueRequired(object):
    def __init__(self, message='该邮箱已经被注册'):
        self.message = message

    def __call__(self, form, field):
        message = self.message
        rep = '^[a-z]+$'
        if field.data:
            if field.object_data != field.data:
                user = User.query.filter_by(email=field.data).first()
                if user:
                    raise ValidationError(message)
