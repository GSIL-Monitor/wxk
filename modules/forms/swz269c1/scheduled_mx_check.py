# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryFileForm, IntervalDescForm
from ..meta import scheduled_source


class ScheduledMxCheckForm(form.Form):
    id = fields.StringField('编号')
    source = fields.SelectField('来源', choices=scheduled_source)
    rii = fields.BooleanField('必检项RII')
    forceExec = fields.BooleanField('强制执行')
    description = fields.StringField('维修描述')
    interval = InlineFormField(IntervalDescForm, '间隔类型')
    relateDoc = InlineFormField(RelateDocForm, '相关文档')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryFileForm, '附件')
    etag = fields.HiddenField('etag')
