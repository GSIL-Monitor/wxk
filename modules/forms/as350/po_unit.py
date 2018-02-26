# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryFileForm, IntervalDescForm


class POUnitForm(form.Form):
    id = fields.StringField('编号')
    description = fields.StringField('维修描述')
    interval = InlineFormField(IntervalDescForm, '间隔类型')
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryFileForm, '附件')
    ataCode = fields.IntegerField('ATA章节')
    aircraftsSers = fields.StringField('飞机注册号')
    reference = fields.StringField('参考章节')
    etag = fields.HiddenField('etag')
