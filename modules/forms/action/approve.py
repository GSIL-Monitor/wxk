# coding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields
from .user_select import get_related_user
from modules.flows.operations import Approved, SecondApproved
from util.fields.accessory_filed import AirmaterialFileuploadField
from wtforms.fields.core import Label


class ApproveForm(form.Form):

    # user = fields.HiddenField('审批用户')
    # timestamp = fields.HiddenField('审批时间')
    suggestion = fields.TextAreaField('审批意见')

    def __init__(self, model_name='', *args, **kwargs):
        super(ApproveForm, self).__init__(*args, **kwargs)


class SecondApproveForm(form.Form):

    # timestamp = fields.HiddenField('审批时间')
    suggestion = fields.TextAreaField('审批意见')

    related_user = fields.SelectField('二级审批人员')

    def __init__(self, model_name='', *args, **kwargs):
        super(SecondApproveForm, self).__init__(*args, **kwargs)
        self.related_user.choices = get_related_user(model_name, op=Approved)


class FileForm(form.Form):
    file = AirmaterialFileuploadField()

    def __init__(self, model_name='', label='', *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        if label:
            self.file.label = Label('file', label)