# encoding: utf-8
from __future__ import unicode_literals

from wtforms import form, fields
from flask_admin.model.fields import InlineFormField, InlineFieldList

from ..commom import RelateDocForm, AccessoryForm, interval_types


class UnscheduledMxCheckForm(form.Form):
    id = fields.StringField('编号')
    description = fields.StringField('描述')
    interval = InlineFieldList(InlineFormField(interval_types('r44')),
                               label='间隔信息', min_entries=1)
    relateDoc = InlineFormField(RelateDocForm, '相关文件')
    remark = fields.StringField('备注')
    accessory = InlineFormField(AccessoryForm, '附件内容')
    etag = fields.HiddenField('etag')
