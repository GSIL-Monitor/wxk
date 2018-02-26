# encoding: utf-8

from __future__ import unicode_literals

from wtforms import fields
from wtforms.validators import ValidationError
from ..widgets.input_select_widget import InputSelectWidget


class InputSelectMixinField(fields.StringField):

    widget = InputSelectWidget()

    def __init__(self, label=None, validators=None, **kwargs):
        super(InputSelectMixinField, self).__init__(label, validators, **kwargs)

    def process(self, formdata, data=None):
        self.process_errors = []

        if formdata:
            tmp = []
            select = '%s-type' % self.name
            value = '%s-value' % self.name

            if value in formdata and formdata[value]:
                tmp.append(formdata[value])
                if select in formdata:
                    tmp.append(formdata[select])
            data = "%s%s" % (tmp[0], tmp[1]) if len(tmp) == 2 else ''
            try:
                if float(tmp[0]) <= 0:
                    data = None
            except:
                data = None

        return super(InputSelectMixinField, self).process(formdata, data)

    def process_formdata(self, valuelist):
        if valuelist:

            self.data = valuelist

    def populate_obj(self, obj, name):
        # 存储数据库的时候，会掉用该方法

        if self.data:
            return setattr(obj, name, self.data)
