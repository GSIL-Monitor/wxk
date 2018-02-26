# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask import url_for
from jinja2 import Markup
from flask_admin import expose
from flask import request
from wtforms.validators import DataRequired
from sqlalchemy import not_

from modules.views import CustomView
from modules.models import Role, BasicAction
from modules.roles import SuperAdmin, AllAction
from modules.flows import all_actions
from util import get_username

from .column_labels import all_labels
from .inline_action import ActionsInlineForm
from ..perms import model_allowed_perms, get_model_display_name


def related_user_formatter(ctx, view, model, name):
    # 把用户遍历一遍
    users = model.users.all()

    f_ = []
    for user in users:
        active_label = 'info' if user.active else 'default'
        btn = '<a class="btn btn-xs btn-%(label)s" href="%(url)s"><i class="fa fa-user"></i> %(name)s</a>' % {
            'label': active_label,
            'url': url_for('user.details_view', id=str(user.id)),
            'name': get_username(user),
        }
        f_.append(btn)

    return Markup(''.join(f_))


def actions_formatter(model):
    # WUJG: 这里的实现返回的并不是通常格式化所需的html内容
    # 因为模板的定制化缘故，这里的返回内容，需要特殊对待，具体查看
    # 对应模板的使用方式

    actions = model.actions
    items = dict()
    for action in actions:
        # 查找所有对应模型里包含为True的操作
        display_name = get_model_display_name(action.model)
        for verb in all_actions:
            if getattr(action, verb, False):
                if display_name not in items:
                    # 主键是模型的名称
                    items[display_name] = []
                items[display_name].append(all_labels[verb])
        if display_name in items:
            # 格式化成字符串
            items[display_name] = Markup(', '.join(items[display_name]))

    return items, len(items)


class _RoleAdminView(CustomView):

    support_flow = False

    create_template = 'role/create.html'
    edit_template = 'role/edit.html'
    details_template = 'role/details.html'

    column_display_actions = True

    required_roles = [SuperAdmin]

    column_labels = {
        'name': '角色名称',
        'description': '角色职责说明',
        'users': '关联用户',
        'actions': '允许的操作',
    }

    inline_models = (ActionsInlineForm(BasicAction, True),)

    column_details_list = ['name', 'description', 'users', 'actions']

    column_formatters = {
        'users': related_user_formatter,
    }

    def get_query(self):
        # 不准操作超级管理员的权限
        return self.session.query(self.model).filter(not_(Role.name.in_([SuperAdmin, AllAction])))

    @expose('/create/', methods=['GET', 'POST'])
    def create_view(self):
        self._template_args.update({
            'all_actions': [item.encode('utf-8') for item in all_actions],
            'model_allowed_perms': model_allowed_perms
        })
        return super(_RoleAdminView, self).create_view()

    @expose('/edit/', methods=['GET', 'POST'])
    def edit_view(self):

        self._template_args.update({
            'all_actions': [item.encode('utf-8') for item in all_actions],
            'model_allowed_perms': model_allowed_perms
        })

        return super(_RoleAdminView, self).edit_view()

    @expose('/details/')
    def details_view(self):
        self._template_args.update({
            'allowed_actions': actions_formatter,
        })
        return super(_RoleAdminView, self).details_view()

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.name.validators = [DataRequired()]
        return super(_RoleAdminView, self).validate_form(form)

    def on_model_change(self, form, model, is_created):

        actions = model.actions
        if not actions:
            return
        # 如果具有复核权限, 则应同时具有复核通过和复核拒绝权限;
        # 如果具有审批权限, 则应同时具有审批通过和审批拒绝权限;
        # 如果具有提交权限, 则应同时具有提交和再次提交权限;
        for item in actions:
            for val in item.__dir__():
                if getattr(item, val):
                    item.view = True
                    break
            item.review_approve = item.review_refuse = item.review
            item.approved = item.approve_refuse = item.approve
            item.submit_review = item.review_again = item.submit
            item.second_approved = item.second_approve_refuse = item.second_approved


RoleAdminView = partial(
    _RoleAdminView, Role, name='角色管理'
)
