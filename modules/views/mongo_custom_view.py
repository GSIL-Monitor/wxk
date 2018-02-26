# coding: utf-8

from __future__ import unicode_literals
import logging
import datetime

from werkzeug.exceptions import BadRequest
from flask import url_for, redirect, request, abort, flash, jsonify
from flask_security import current_user
from flask_admin.contrib.pymongo import ModelView as MongoModelView
from flask_admin import expose
from flask_admin.helpers import (get_redirect_target, flash_errors)

from modules.views.column_formatter import cancel_formatter
from translations import gettext
from ..flows.operations import Create, Edit, Delete, View
from ..perms import ActionNeedPermission
from .mixin import Mixin
from ..proxy import proxy


log = logging.getLogger("flask-admin.pymongo")


class MongoCustomView(Mixin, MongoModelView):

    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'
    details_template = 'details.html'

    column_display_actions = False
    # 所有基于mongo的模型，使用_id字段来默认倒序排序
    column_default_sort = ('_id', True)

    # 顶部搜索控件是否显示
    top_search_form = True

    # 下面的权限使得采用配置的方式决定哪些视图可以被用户看见

    # 必须全部满足的角色列表
    required_roles = []
    # 可接受的全部列表
    accepted_roles = []

    extra_js = [
        '/static/js/custom_action.js',
    ]

    support_popup = True

    export_types = ['csv', 'xlsx']

    def __init__(self, db, coll_name, action_name, *args, **kwargs):

        self._action_name = action_name.lower()

        self._api_proxy = proxy

        self._mongo = db

        if not self.column_list:
            self.column_list = []

        self.column_list = list(self.column_list)

        if not self.column_formatters:
            self.column_formatters = dict()

        self.column_details_list = self.column_details_list or []
        # WUJG: 这里无需检查查看权限，即使不存在权限，这里的显示内容也无关紧要
        # 确保返回按钮在最后
        if 'return' in self.column_details_list:
            self.column_details_list.remove('return')
        self.column_details_list.append('return')
        self.column_formatters.update({
            'return': cancel_formatter,
        })

        if not self.form_excluded_columns:
            self.form_excluded_columns = []

        self.form_excluded_columns = list(self.form_excluded_columns)

        # 默认的窗体不应该包含下面内容
        self.form_excluded_columns.extend(['createTime', 'updateTime'])

        coll = None
        if coll_name:
            coll = self._mongo[coll_name]

        super(MongoCustomView, self).__init__(coll, *args, **kwargs)

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
            self._api_proxy.create(
                model, self.get_real_url(self._api_url, model))
        except Exception as ex:
            flash(gettext('Failed to create record. %(error)s',
                          error=unicode(ex)), 'error')
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
            self._api_proxy.update(
                model, etag,
                self.get_real_url(self._api_url, model))
        except Exception as ex:
            flash(gettext('Failed to update record. %(error)s',
                          error=ex.message), 'error')
            log.exception('Failed to update record.')
            return False

        return True

    def delete_model(self, model):

        try:
            etag = model['etag']
            self._api_proxy.delete(etag, self.get_real_url(self._api_url, model))
        except Exception as ex:
            flash(gettext('Failed to delete record. %(error)s', error=str(ex)),
                  'error')
            log.exception('Failed to delete record.')
            return False

        return True

    def verify_and_modify_data(self, obj):

        # TDDO
        if 'aircraftsSers' in obj:
            obj.pop('aircraftsSers')

        if 'etag' in obj:
            obj.pop('etag')

        # Must be removed
        if '_id' in obj:
            obj.pop('_id')

        return obj

    @expose('/unique/')
    def unique_test(self):
        try:
            id = request.args.get('id', None)
            if id is not None:
                # 直接做唯一性性检测
                if self.coll.find_one({'id': id}) is None:
                    return jsonify(code=200, message='Ok')

            return jsonify(code=409, message='Already Exist')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/')
    def index_view(self):
        sub = request.args.get('sub', self.default_subordinate_view)
        self._template_args.update({
            'view_list': self.view_list,
            'sub': sub,
            'name': self.name,
            'img': 'img/%s' % self.default_image,
        })
        self._list_columns = self.get_list_columns()
        return super(MongoCustomView, self).index_view()

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        sub = request.args.get('sub', self.default_subordinate_view)
        self._template_args.update({
            'sub': sub,
            'time_formatter': datetime.time,
        })
        self._create_form_class = self._delegate_to_sub('form')
        self.override_fields(self._create_form_class)
        return super(MongoCustomView, self).create_view()

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        sub = request.args.get('sub', self.default_subordinate_view)
        self._template_args.update({
            'sub': sub,
            'time_formatter': datetime.time,
        })
        self._edit_form_class = self._delegate_to_sub('form')
        self.override_fields(self._edit_form_class)
        return super(MongoCustomView, self).edit_view()

    @expose('/details/')
    def details_view(self):
        sub = request.args.get('sub', self.default_subordinate_view)
        self._template_args.update({
            'sub': sub,
            'time_formatter': datetime.time,
        })
        self._edit_form_class = self._delegate_to_sub('form')
        return super(MongoCustomView, self).details_view()

    @expose('/delete/', methods=('POST',))
    def delete_view(self):

        """
            Delete model view. Only POST method is allowed.
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_delete:
            return redirect(return_url)

        form = self.delete_form()

        if self.validate_form(form):
            # id is InputRequired()
            id = form.id.data

            model = self.get_one(id)

            if model is None:
                flash(gettext('Record does not exist.'), 'error')
                return redirect(return_url)

            # message is flashed from within delete_model if it fails
            if self.delete_model(model):
                flash(gettext('Record was successfully deleted.'), 'success')
                return redirect(self.get_save_return_url(model, is_created=False))
        else:
            flash_errors(form, message='Failed to delete record. %(error)s')

        return super(MongoCustomView, self).delete_view()

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
        ret = self._delegate_to_sub('column_labels') or {}
        ret.update({
            'operation': '操作',
            'return': '返回',
        })
        return ret

    def _delegate_to_sub(self, key_name):
        sub = self.default_subordinate_view
        if request:
            sub = request.args.get('sub', self.default_subordinate_view)

        try:
            if key_name in self.view_list[sub]:
                return self.view_list[sub][key_name]
        except KeyError:
            raise BadRequest()

        return None

    @property
    def _api_url(self):
        return self._delegate_to_sub('_api_url')

    # 具体的子视图应该实现下面的内容
    @property
    def view_list(self):
        # 注意，应该返回一个dict
        return {}

    def get_real_url(self, url, model):
        return url

    @property
    def default_image(self):
        return 'profile_user.jpg'

    def _get_model_name(self):
        return self._action_name

    @property
    def action_name(self):
        return self._action_name

    def override_fields(self, class_name):
        pass
