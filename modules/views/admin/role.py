# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.roles import SuperAdmin
from modules.views import CustomView
from modules.models import Role, BasicAction

from .inline_action import ActionsInlineForm


class _RoleAdminView(CustomView):

    column_display_actions = True

    required_roles = [SuperAdmin]

    column_labels = {
        'name': '权限名',
        'description': '权限职责说明',
        'uesrs': '关联用户',
        'actions': '允许的操作',
    }

    # TODO: 如何根据不同的模型是否支持扩展操作而定义？
    inline_models = (ActionsInlineForm(BasicAction, True),)


RoleAdminView = partial(
    _RoleAdminView, Role, name='权限管理',
    menu_icon_type='fa', menu_icon_value='fa-user'
)
