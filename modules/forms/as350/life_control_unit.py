# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField, InlineFieldList, FieldList

from ..commom import RelateDocForm, AccessoryForm, interval_types


class LifeControlUnitForm(form.Form):
    id = fields.StringField('编号')
    name = fields.StringField('部件名')
    pn = fields.StringField('Pn件号')
    description = fields.StringField('描述信息')
    interval = InlineFieldList(InlineFormField(interval_types('as350')),
                               label='间隔信息', min_entries=1)
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    remark = fields.StringField('备注信息')
    accessory = InlineFormField(AccessoryForm, '附件')
    aircraftsSers = FieldList(fields.StringField('飞机注册号列表'))
    reference = fields.StringField('参考章节')
    etag = fields.HiddenField('etag')
