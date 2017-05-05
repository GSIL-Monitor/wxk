# coding: utf-8

from __future__ import unicode_literals
import logging

from flask import url_for, redirect, request, abort, flash, render_template
from flask_security import current_user
from flask_principal import Permission, RoleNeed
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView as SQLModelView

from modules.flows.status import Created
from modules.perms import ActionNeedPermission
from modules.flows.operations import Create, Edit, Delete, View
from modules.flows import BasicApprovalFlow
from modules.models.notification.notice import Notice

log = logging.getLogger("flask-admin.pymongo")


class CustomView(SQLModelView):

    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'
    details_template = 'details.html'

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
    ]

    column_display_actions = False

    support_popup = True

    # 下面的权限使得采用配置的方式决定哪些视图可以被用户看见

    # 必须全部满足的角色列表
    required_roles = []
    # 可接受的全部列表
    accepted_roles = []

    def __init__(self, *args, **kwargs):
        if not self.column_list:
            self.column_list = []

        self.column_list = list(self.column_list)

        # if self.show_operation and 'operation' not in self.column_list:
        #     self.column_list.append('operation')

        if not self.column_formatters:
            self.column_formatters = dict()

        # if self.show_operation:
        #     self.column_formatters['operation'] = _operation

        if not self.form_excluded_columns:
            self.form_excluded_columns = []

        self.form_excluded_columns = list(self.form_excluded_columns)

        # 默认的窗体不应该包含下面内容
        self.form_excluded_columns.extend(
            ['createTime', 'updateTime', 'statusName', 'audits'])

        super(CustomView, self).__init__(*args, **kwargs)

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        # 要求的权限优先级要高于可接受的权限
        if self.required_roles and isinstance(self.required_roles, list):
            perms = [
                Permission(RoleNeed(role)) for role in self.required_roles]
            for perm in perms:
                if not perm.can():
                    return False
            return True

        if self.accepted_roles and isinstance(self.accepted_roles, list):
            perm = Permission(
                *[RoleNeed(role) for role in self.accepted_roles])
            if not perm.can():
                return False
            return True

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                return abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

    def get_details_columns(self):
        only_columns = (self.column_details_list or
                        self.scaffold_list_columns())

        return self.get_column_names(
            only_columns=only_columns,
            excluded_columns=self.column_details_exclude_list,
        )

    def on_model_change(self, form, model, is_created):
        # 新增模型实例时，默认应该处于新建状态
        if is_created:
            model.status = Created
        super(CustomView, self).on_model_change(form, model, is_created)

    @property
    def can_create(self):
        # 使用属性的方式来重写框架原自带的can_create实现
        perm = ActionNeedPermission(
            self.model().__class__.__name__.lower(), Create)
        return perm.can()

    @property
    def can_edit(self):
        perm = ActionNeedPermission(
            self.model().__class__.__name__.lower(), Edit)
        return perm.can()

    @property
    def can_delete(self):
        perm = ActionNeedPermission(
            self.model().__class__.__name__.lower(), Delete)
        return perm.can()

    @property
    def can_view_details(self):
        try:
            perm = ActionNeedPermission(
                self.model().__class__.__name__.lower(), View)
            return perm.can()
        except:
            pass
        return False

    @expose('/custom-actions', methods=['POST'])
    def custom_action(self):
        try:
            query = self.model.query.filter(
                self.model.id.in_(request.args['id']))
            for item in query.all():
                flow = BasicApprovalFlow('Basic control flow', item)
                apply(getattr(flow, request.args['action']))
                '''TODO:因为产生通知的逻辑，及通知实例具体包含哪些内容，对应内容如何产生还不是很清楚，待需求明确后，再改
                状态变更后添加通知'''
                notifies = Notice(title=request.args['action'], status='新建')
                self.session.add(notifies)
                self.session.commit()

        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            self.session.rollback()
            flash('Unable to execute specified operation.')
        return redirect(self.get_url('.index_view'))
