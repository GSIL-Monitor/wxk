# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryForm
from modules.forms.meta import parking_category


class ShortLongTermParkingForm(form.Form):
    id = fields.StringField('编号')
    category = fields.SelectField('类别', choices=parking_category('as350'))
    description = fields.StringField('描述信息')
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    remark = fields.StringField('备注信息')
    accessory = InlineFormField(AccessoryForm, '附件内容')
    reference = fields.StringField('参考章节')
    etag = fields.HiddenField('etag')
