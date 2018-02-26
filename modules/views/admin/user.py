# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired
from sqlalchemy import not_

from modules.views import CustomView
from modules.models import User, Role
from modules.roles import SuperAdmin
from util.validators.lowercase_required import LowercaseRequired
from util.validators.user_unique_required import UserUniqueRequired
from util.validators.email_unique_required import EmailUniqueRequired
from util.validators.input_length import InputLength


class _UserAdminView(CustomView):
    create_template = 'unvalidate/create.html'

    support_flow = False

    column_display_actions = True

    required_roles = [SuperAdmin]

    column_list = [
        'username', 'realName', 'email', 'roles', 'active'
    ]

    column_labels = {
        'realName': '真实姓名',
        'username': '用户名',
        'email': 'E-mail',
        'roles': '拥有权限',
        'active': '是否激活',
        'nickName': '显示名称',
        'password': '口令',
        'phone': '联系电话',
        'last_login_ip': '上次登录IP',
        'current_login_ip': '当前登录IP',
        'last_login_at': '上次登录时间',
        'current_login_at': '当前登录时间',
        'confirmed_at': '激活时间',
        'login_count': '登录次数',
    }

    column_details_list = column_list + [
        'phone', 'last_login_ip', 'current_login_ip',
        'last_login_at', 'current_login_at', 'confirmed_at',
        'login_count',
    ]

    form_excluded_columns = [
        'confirmed_at', 'last_login_at', 'current_login_at',
        'last_login_ip', 'current_login_ip', 'login_count', 'uesrs',
        'actions'
    ]

    def get_query(self):
        # 不准操作管理员，且假定只有一个超级管理员
        return self.session.query(self.model).filter(not_(User.username.in_(['admin', 'hfga'])))

    def __init__(self, *args, **kwargs):
        self.form_overrides = self.form_overrides or {}

        self.form_overrides.update({
            'roles': partial(
                QuerySelectMultipleField,
                query_factory=lambda: self.session.query(Role).filter(
                    Role.name != SuperAdmin)),
        })

        super(_UserAdminView, self).__init__(*args, **kwargs)

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.username.validators = [LowercaseRequired(),
                                        DataRequired(), UserUniqueRequired()]
            form.email.validators = [EmailUniqueRequired()]
            form.realName.validators = [DataRequired()]
            # password字段指定长度验证
            form.password.validators = [InputLength()]
        return super(_UserAdminView, self).validate_form(form)


UserAdminView = partial(
    _UserAdminView, User, name='用户管理'
)
