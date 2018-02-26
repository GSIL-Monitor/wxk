# coding: utf-8

from __future__ import unicode_literals

from wtforms.validators import ValidationError, DataRequired, StopValidation
from wtforms.compat import string_types


class PlusNumberRequired(DataRequired):

    def __call__(self, form, field):
        # 首先验证是不是空值
        if not str(field.data) or isinstance(field.data, string_types) and not field.data.strip():
            if self.message is None:
                message = field.gettext('该字段是必输项')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)
        # 再次验证里面的值是不是非负数
        if field.data:
            try:
                number = int(field.data)
                if number < 0:
                    if self.message is None:
                        message = field.gettext('该字段输入的必须为非负数')
                    else:
                        message = self.message
                    raise ValidationError(message)
            except:
                raise ValidationError(message)
