# coding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields
from flask import flash
from wtforms.validators import DataRequired, NumberRange

fields_kw = {'class': "form-control"}

data_require = '请输入数字。'
number_require = '请输入小于1000的正整数。'

validateNum = [DataRequired(data_require), NumberRange(1, 1000, number_require)]


class CheckWarningForm(form.Form):
    warningfiled_yellow = fields.IntegerField(
        validators=validateNum, render_kw=fields_kw)
    warningfiled_orange = fields.IntegerField(
        validators=validateNum, render_kw=fields_kw)
    warningfiled_red = fields.IntegerField(
        validators=validateNum, render_kw=fields_kw)

    def validate(self):
        if not super(CheckWarningForm, self).validate():
            return False
        if self.warningfiled_yellow.data <= self.warningfiled_orange.data:
            raise ValueError('橙色预警应小于黄色预警值')
        if self.warningfiled_orange.data <= self.warningfiled_red.data:
            raise ValueError('红色预警应小于橙色预警值')
        return True
