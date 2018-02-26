# encoding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields

from util.fields import DateFieldInt


class MaintenanceLogForm(form.Form):

    id = fields.StringField('编号')
    aircraftId = fields.StringField('飞行器注册号')
    type = fields.StringField('类型')
    description = fields.StringField('维修描述信息')
    completeDate = DateFieldInt('完成日期')
    generateTime = DateFieldInt('生成时间')
    remark = fields.StringField('备注')
    serialNumber = fields.StringField('时控/寿件的序号')
    etag = fields.HiddenField('etag')
