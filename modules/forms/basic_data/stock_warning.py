# coding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields
from wtforms.validators import DataRequired, NumberRange

fields_kw = {'class': "form-control"}

data_require = '请输入数字。'
number_require = '请输入小于1000的正整数。'

validate = [DataRequired(data_require), NumberRange(1, 1000, number_require)]


class StockWarningForm(form.Form):
    chemicalwarningfiled_yellow = fields.IntegerField(
        validators=validate, render_kw=fields_kw)
    chemicalwarningfiled_orange = fields.IntegerField(
        validators=validate, render_kw=fields_kw)
    chemicalwarningfiled_red = fields.IntegerField(
        validators=validate, render_kw=fields_kw)
    consumewarningfiled_yellow = fields.IntegerField(
        validators=validate, render_kw=fields_kw)
    consumewarningfiled_orange = fields.IntegerField(
        validators=validate, render_kw=fields_kw)
    consumewarningfiled_red = fields.IntegerField(
        validators=validate, render_kw=fields_kw)

    def validate(self):
        if not super(StockWarningForm, self).validate():
            return False
        if self.chemicalwarningfiled_yellow.data <= self.chemicalwarningfiled_orange.data:
            raise ValueError('化工品，橙色预警应小于黄色预警值')
        if self.chemicalwarningfiled_orange.data <= self.chemicalwarningfiled_red.data:
            raise ValueError('化工品，红色预警应小于橙色预警值')
        if self.consumewarningfiled_yellow.data <= self.consumewarningfiled_orange.data:
            raise ValueError('消耗品，橙色预警应小于黄色预警值')
        if self.consumewarningfiled_orange.data <= self.consumewarningfiled_red.data:
            raise ValueError('消耗品，红色预警应小于橙色预警值')
        return True
