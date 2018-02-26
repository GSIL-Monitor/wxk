# coding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields
from .user_select import get_related_user
from modules.flows.operations import ReviewApprove


class ReviewForm(form.Form):

    # user = fields.HiddenField('复核用户')
    # timestamp = fields.HiddenField('复核时间')
    suggestion = fields.TextAreaField('复核意见')
    related_user = fields.SelectField('审批人员')

    def __init__(self, model_name='', *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.related_user.choices = get_related_user(model_name, op=ReviewApprove)


class ReviewOnlyForm(form.Form):

    suggestion = fields.TextAreaField('复核意见')

    def __init__(self, model_name='', *args, **kwargs):
        super(ReviewOnlyForm, self).__init__(*args, **kwargs)