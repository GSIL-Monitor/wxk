# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
# from flask_admin.model.fields import InlineFormField, InlineFieldList
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryForm, interval_types
from modules.forms.meta import scheduled_source, scheduled_area


class ScheduledMxCheckForm(form.Form):
    id = fields.StringField('编号')
    source = fields.SelectField('来源', choices=scheduled_source('da40d'))
    ataCode = fields.IntegerField('ATA章节')
    rii = fields.BooleanField('必检项RII')
    forceExec = fields.BooleanField('强制执行项')
    area = fields.SelectField('所属区域', choices=scheduled_area('da40d'))
    description = fields.StringField('内容描述')
    interval = InlineFormField(interval_types('da40d'),
                               label='间隔信息')
    relateDoc = InlineFormField(RelateDocForm, '相关文档')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryForm, '附件')
    etag = fields.HiddenField('etag')
