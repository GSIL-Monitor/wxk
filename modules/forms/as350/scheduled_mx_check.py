# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryFileForm, IntervalDescForm
from ..meta import as_scheduled_source, environment_category


class ScheduledMxCheckForm(form.Form):
    id = fields.StringField('编号')
    source = fields.SelectField('来源', choices=as_scheduled_source)
    environmentCategory = fields.SelectField(
        '环境类别', choices=environment_category)
    ataCode = fields.IntegerField('ATA章节')
    rii = fields.BooleanField('必检项RII')
    forceExec = fields.BooleanField('强制执行')
    description = fields.StringField('维修描述')
    interval = InlineFormField(IntervalDescForm, '间隔类型')
    relateDoc = InlineFormField(RelateDocForm, '相关文档')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryFileForm, '附件')
    aircraftsSers = fields.StringField('飞机注册号')
    reference = fields.StringField('参考章节')
    etag = fields.HiddenField('etag')
