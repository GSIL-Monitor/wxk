# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryFileForm, As350IntervalDescForm


class LifeControlUnitForm(form.Form):
    id = fields.StringField('编号')
    name = fields.StringField('部件名')
    pn = fields.StringField('Pn件号')
    description = fields.StringField('维修描述')
    interval = InlineFormField(As350IntervalDescForm, '间隔类型')
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryFileForm, '附件')
    aircraftsSers = fields.StringField('飞机注册号')
    reference = fields.StringField('参考章节')
    etag = fields.HiddenField('etag')
