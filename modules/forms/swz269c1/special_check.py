# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField

from ..commom import RelateDocForm, AccessoryFileForm
from ..meta import special_check_category


class SpecialCheckForm(form.Form):
    id = fields.StringField('编号')
    category = fields.SelectField(
        '类别', choices=special_check_category)
    description = fields.StringField('维修描述')
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryFileForm, '附件')
    etag = fields.HiddenField('etag')
