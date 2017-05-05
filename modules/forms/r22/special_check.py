# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryForm
from modules.forms.meta import special_check_category


class SpecialCheckForm(form.Form):
    id = fields.StringField('编号')
    category = fields.SelectField('类别', choices=special_check_category('r22'))
    description = fields.StringField('描述信息')
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    remark = fields.StringField('备注信息')
    accessory = InlineFormField(AccessoryForm, '附件内容')
    etag = fields.HiddenField('etag')
