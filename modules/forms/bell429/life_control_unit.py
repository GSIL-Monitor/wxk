# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField, InlineFieldList

from ..commom import RelateDocForm, AccessoryForm, interval_types


class LifeControlUnitForm(form.Form):
    id = fields.StringField('编号')
    ataCode = fields.IntegerField('ATA章节号')
    name = fields.StringField('部件名')
    pn = fields.StringField('Pn件号')
    description = fields.StringField('描述信息')
    interval = InlineFieldList(InlineFormField(interval_types('bell429')),
                               lable='间隔信息', min_entries=1)
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    remark = fields.StringField('备注信息')
    accessory = InlineFormField(AccessoryForm, '附件信息')
    etag = fields.HiddenField('etag')
