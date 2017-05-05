# coding: utf-8

from __future__ import unicode_literals
import logging

from flask import url_for, redirect, request, abort, flash
from flask_security import current_user
from flask_principal import Permission, RoleNeed
from flask_admin.contrib.pymongo import ModelView as MongoModelView
from flask_admin.babel import gettext
from flask_admin import expose

from util.api_request import APIRequest
from modules.flows.operations import Create, Edit, Delete, View
from modules.perms import ActionNeedPermission

log = logging.getLogger("flask-admin.pymongo")


class MongoCustomView(MongoModelView):

    list_template = 'list.html'
    create_template = 'modal/create.html'
    edit_template = 'modal/edit.html'
    details_template = 'details.html'

    # column_display_actions = False

    # 下面的权限使得采用配置的方式决定哪些视图可以被用户看见

    # 必须全部满足的角色列表
    required_roles = []
    # 可接受的全部列表
    accepted_roles = []

    def __init__(self, db, coll_name, action_name, *args, **kwargs):

        self._action_name = action_name.lower()

        self._mongo = db

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
        self.form_excluded_columns.extend(['createTime', 'updateTime'])

        coll = None
        if coll_name:
            coll = db[coll_name]

        super(MongoCustomView, self).__init__(coll, *args, **kwargs)

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

    # def get_details_columns(self):
    #     only_columns = (self.column_details_list or
    #                     self.scaffold_list_columns())

    #     return self.get_column_names(
    #         only_columns=only_columns,
    #         excluded_columns=self.column_details_exclude_list,
    #     )

    @property
    def can_create(self):
        # 使用属性的方式来重写框架原自带的can_create实现
        perm = ActionNeedPermission(self._action_name, Create)
        return perm.can()

    @property
    def can_edit(self):
        perm = ActionNeedPermission(self._action_name, Edit)
        return perm.can()

    @property
    def can_delete(self):
        perm = ActionNeedPermission(self._action_name, Delete)
        return perm.can()

    @property
    def can_view_details(self):
        try:
            perm = ActionNeedPermission(self._action_name, View)
            return perm.can()
        except:
            pass
        return False

    def create_model(self, form):
        try:
            model = form.data
            model = self.verify_and_modify_data(model)
            rt = APIRequest(self._api_url)
            rt.post_request(model)
        except Exception as ex:
            flash(gettext('Failed to create record. %(error)s',
                          error=ex.message), 'error')
            log.exception('Failed to create record.')
            return False

        return model

    def update_model(self, form, model):
        try:
            model.update(form.data)
            etag = model['etag']
            if 'id' not in model or 'etag' not in model:
                raise ValueError(
                    'Id or etag must be contained before you updating.')
            model = self.verify_and_modify_data(model)
            rt = APIRequest(self._api_url)
            rt = rt.put_request(model, etag)
        except Exception as ex:
            flash(gettext('Failed to update record. %(error)s',
                          error=ex.message), 'error')
            log.exception('Failed to update record.')
            return False

        return True

    def delete_model(self, model):
        try:
            rt = APIRequest(self._api_url)
            rt = rt.delete_request(model['etag'])
        except Exception as ex:
            flash(gettext('Failed to delete record. %(error)s', error=str(ex)),
                  'error')
            log.exception('Failed to delete record.')
            return False

        return True

    def verify_and_modify_data(self, obj):

        if 'relateDoc' in obj:
            obj.pop('relateDoc')
        if 'accessory' in obj:
            obj.pop('accessory')
        # TDDO
        if 'aircraftsSers' in obj:
            obj.pop('aircraftsSers')
        if 'startTracking' in obj:
            obj.pop('startTracking')

        # Must be removed
        if '_id' in obj:
            obj.pop('_id')

        return 

    @expose('/')
    def index_view(self):
        sub = request.args.get('sub')
        self._template_args.update({
            'view_list': self.view_list,
            'sub': sub,
            'name': self.name
        })
        self._list_columns = self.get_list_columns()
        return super(MongoCustomView, self).index_view()

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        self._create_form_class = self._delegate_to_sub('form')
        return super(MongoCustomView, self).create_view()

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        self._edit_form_class = self._delegate_to_sub('form')
        return super(MongoCustomView, self).edit_view()

    @property
    def default_subordinate_view(self):
        "默认的子视图索引"

        raise NotImplementedError()

    @property
    def coll(self):
        # 需要根据当前所加载的界面来决定到底使用那个模型序列
        coll_name = self._delegate_to_sub('coll_name')
        return self._mongo[coll_name]

    @coll.setter
    def coll(self, val):
        pass

    def scaffold_list_columns(self):
        return self._delegate_to_sub('column_list')

    def scaffold_form(self):
        return self._delegate_to_sub('form')

    @property
    def column_labels(self):
        return self._delegate_to_sub('column_labels')

    def _delegate_to_sub(self, key_name):
        sub = self.default_subordinate_view
        if request:
            sub = request.args.get('sub', self.default_subordinate_view)
        return self.view_list[sub][key_name]

    @property
    def api_url(self):
        return self._delegate_to_sub('_api_url')

    # 具体的子视图应该实现下面的内容
    @property
    def view_list(self):
        # 注意，应该返回一个dict
        return {}

    # @property
    # def form(self):
    #     return self._delegate_to_sub('form')
