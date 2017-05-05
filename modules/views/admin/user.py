# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.roles import SuperAdmin
from modules.views import CustomView
from modules.models import User


class _UserAdminView(CustomView):

    column_display_actions = True

    required_roles = [SuperAdmin]

    list_columns = [
        'username', 'realname', 'email', 'roles', 'active'
    ]

    column_labels = {
        'realname': '真实姓名',
        'username': '用户名',
        'email': 'E-mail',
        'roles': '拥有权限',
        'active': '是否激活'
    }

    form_excluded_columns = [
        'confirmed_at', 'last_login_at', 'current_login_at',
        'last_login_ip', 'current_login_ip', 'login_count',
    ]


UserAdminView = partial(
    _UserAdminView, User, name='用户管理',
    menu_icon_type='fa', menu_icon_value='fa-users'
)
