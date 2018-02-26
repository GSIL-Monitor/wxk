# coding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields
from wtforms.validators import DataRequired
from wtforms.fields.core import Label

from modules.flows.operations import (SubmitReview, ReviewApprove, SecondApproved,
                                      Receive, Approved)
from modules.models.role import BasicAction, Role
from modules.models.user import roles_users, User
from modules.roles import AllAction


content = ["1", "2", "3"]
authorityChoice = [(item, item) for item in content]


def get_related_user(model_name, op):

    data = {
        'model': model_name,
        'review_approve': 1,
        'review_refuse': 1
    }
    if op == ReviewApprove:
        data = {
            'model': model_name,
            'approved': 1,
            'approve_refuse': 1
        }

    if op == Approved:
        data = {
            'model': model_name,
            'second_approved': 1,
            'second_approve_refuse': 1
        }

    if op == Receive:
        data = {
            'model': model_name,
            'receive': 1,
        }

    query = BasicAction.query.filter_by(**data).all()
    roles_ids = []
    for item in query:
        roles_ids.append(item.role_id)
    roles = Role.query.filter(Role.id.in_(roles_ids), Role.name != AllAction).all()
    users = []
    for role in roles:
        users.extend(User.query.filter(User.roles.contains(role)).all())
    names = []
    for val in users:
        names.append(val.username)
    return [(item.username, item.realName) for item in users]


class UserSelectForm(form.Form):

    related_user = fields.SelectField('复核人员', choices=authorityChoice)

    def __init__(self, label='', op=SubmitReview, model_name='', *args, **kwargs):
        super(UserSelectForm, self).__init__(*args, **kwargs)
        self.related_user.choices = get_related_user(model_name, op=op)
        if label:
            self.related_user.label = Label('related_user', label)
