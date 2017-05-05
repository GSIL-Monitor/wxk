# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField, InlineFieldList, FieldList

from ..commom import RelateDocForm, AccessoryForm, interval_types
from modules.forms.meta import scheduled_source, environment_category


class ScheduledMxCheckForm(form.Form):
    id = fields.StringField('编号')
    source = fields.SelectField('来源', choices=scheduled_source('as350'))
    environmentCategory = fields.SelectField(
        '环境类别', choices=environment_category('as350'))
    ataCode = fields.IntegerField('ATA章节')
    rii = fields.BooleanField('必检项RII')
    forceExec = fields.BooleanField('强制执行项')
    description = fields.StringField('内容描述')
    interval = InlineFieldList(InlineFormField(interval_types('as350')),
                               label='间隔信息', min_entries=1)
    relateDoc = InlineFormField(RelateDocForm, '相关文档信息')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryForm, '附件信息')
    aircraftsSers = FieldList(fields.StringField('飞机注册号列表'))
    reference = fields.StringField('参考章节')
    etag = fields.HiddenField('etag')
