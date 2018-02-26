# coding: utf-8

from __future__ import unicode_literals

from wtforms.validators import ValidationError


class DataUniqueRequired(object):
    def __init__(self, model, fielddata, message='已经存在'):
        self.message = message
        self.model = model
        self.fielddata = fielddata

    def __call__(self, form, field):
        message = self.message
        if field.data:
            if field.object_data != field.data:
                uniqueDate = getattr(self.model, self.fielddata)
                tmp = self.model.query.filter(
                    uniqueDate == field.data).first()
                if tmp:
                    raise ValidationError(message)
