# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryFileForm,\
    TrackingDescForm, IntervalRadioDescForm
from ..meta import bell_scheduled_source


class ScheduledMxCheckForm(form.Form):
    id = fields.StringField('编号')
    source = fields.SelectField('来源', choices=bell_scheduled_source)
    ataCode = fields.IntegerField('ATA章节')
    rii = fields.BooleanField('必检项RII')
    forceExec = fields.BooleanField('强制执行')
    startTracking = InlineFormField(TrackingDescForm, '开始跟踪时间点')
    userFlag = fields.BooleanField('用户输入时间点')
    description = fields.StringField('维修描述')
    interval = InlineFormField(IntervalRadioDescForm, '间隔类型')
    relateDoc = InlineFormField(RelateDocForm, '相关文档')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryFileForm, '附件')
    etag = fields.HiddenField('etag')
