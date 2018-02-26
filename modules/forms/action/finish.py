# coding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields
# from modules.flows.operations import Finish

# from util.fields.datetime_field import DateField


class RoutineWorkFinishForm(form.Form):

    # 例行工作的完成使用的是实体的检查日期
    # timestamp = DateField('完成时间')
    remark = fields.HiddenField()

