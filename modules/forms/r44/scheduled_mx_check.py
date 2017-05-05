# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField, InlineFieldList

from ..commom import RelateDocForm, AccessoryForm, interval_types
from modules.forms.meta import scheduled_source


class ScheduledMxCheckForm(form.Form):
    id = fields.StringField('编号')
    source = fields.SelectField('来源', choices=scheduled_source('r44'))
    rii = fields.BooleanField('必检项RII')
    forceExec = fields.BooleanField('强制执行项')
    description = fields.StringField('内容描述')
    interval = InlineFieldList(InlineFormField(interval_types('r44')),
                               label='间隔信息', min_entries=1)
    relateDoc = InlineFormField(RelateDocForm, '相关文档')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryForm, '附件')
    etag = fields.HiddenField('etag')
