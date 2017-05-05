# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryForm
from modules.forms.meta import normal_check_category


class NormalCheckForm(form.Form):
    id = fields.StringField('编号')
    category = fields.SelectField('类别', choices=normal_check_category('r44'))
    description = fields.StringField('描述信息')
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    accessory = InlineFormField(AccessoryForm, '附件内容')
    remark = fields.StringField('备注信息')
    etag = fields.HiddenField('etag')
