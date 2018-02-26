# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from copy import deepcopy
import json
from datetime import datetime

from flask_admin import expose
from flask import redirect, request, flash, jsonify, current_app
from flask_admin.form import FormOpts
from collections import OrderedDict
from flask_admin.babel import gettext
from wtforms import SelectField
from util.widgets import DateWidget
from util.fields import DateField
from flask_admin.helpers import get_form_data
from flask_admin.contrib.sqla import form
from flask_admin.helpers import get_redirect_target
from sqlalchemy import and_, or_

from modules.models.airmaterial import AirMaterialStorageList
from modules.views.operations import operation_formatter_without_flow, normal_operation_formatter
from modules.views import CustomView
from modules.perms import ActionNeedPermission
from modules.flows.operations import Create, CheckComplete
from modules.views.column_formatter import checkbox_formater
from modules.flows.operations import View
from sqlalchemy_continuum import version_class
from modules.models.id_generator import date_generator


class _CheckWarningView(CustomView):
    column_list = [
        'name', 'category', 'partNumber', 'serialNum', 'shelf', 'storehouse',
        'nextCheckDate', 'operations'
    ]
    # create_template = 'create.html'
    list_template = 'storage/yujing_list.html'
    can_create = False
    can_edit = True
    edit_template = 'storage/yujing_edit.html'

    # 对应内容的中文翻译
    column_labels = {
        'name': '名称',
        'category': '类型',
        'partNumber': '件号',
        'serialNum': '序号',
        'shelf': '架位',
        'nextCheckDate': '下次检查日期',
        'operations': '操作',
        'checkRecord': '检查说明',
        'storehouse': '仓库',
        'lastCheckDate': '记录检查时间'

    }

    support_flow = None

    column_searchable_list = ('name', 'category', 'partNumber')

    index_lists = []

    form_excluded_columns = [
        'name', 'category', 'partNumber', 'serialNum', 'shelf',
        'quantity', 'unit', 'flyTime', 'engineTime', 'flightTimes',
        'applicableModel', 'effectiveDate', 'certificateNum',
        'airworthinessTagNum', 'minStock', 'supplier',
        'manufacturer', 'statusName', 'freezingQuantity']

    form_overrides = {
        'nextCheckDate': partial(DateField, widget=DateWidget()),
        'lastCheckDate': partial(DateField, widget=DateWidget())
    }

    column_formatters = {
        'operations': partial(operation_formatter_without_flow,
                              operations=[CheckComplete]),
    }

    def is_accessible(self):
        return ActionNeedPermission('checkwarning', View).can()

    def get_level(self, data, yujing):

        if not data or not yujing:
            return ''
        tmp = datetime.strptime(data, "%Y-%m-%d")
        count = (tmp.date() - datetime.now().date()).days
        level = ''

        if yujing['lv2'] < count <= yujing['lv1']:
            level = 'yellow'
        elif yujing['lv3'] < count <= yujing['lv2']:
            level = 'orange'
        elif count <= yujing['lv3']:
            level = 'red'

        return level

    def get_query(self):
        datas = self.model.query.filter(
            self.model.nextCheckDate != None, self.model.nextCheckDate != '')

        return datas

    def get_yujing_level(self):

        cache = current_app.redis_cache._user_cache
        yujing = cache.get('checkwarning')
        if not yujing:
            return ''
        return json.loads(yujing)

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        self._list_columns = deepcopy(self._tmp_list_columns)
        self.list_template = 'storage/yujing_list.html'
        sort_column = 'nextCheckDate'

        count, datas = super(_CheckWarningView, self).get_list(
            page, sort_column, sort_desc, search, filters,
            execute=True, page_size=None)
        count = self.get_query().count()

        self.index_lists = datas
        yujing = self.get_yujing_level()

        levels = [self.get_level(x.nextCheckDate, yujing) for x in self.index_lists]
        self._template_args.update({
            'levels': levels,
        })
        category = request.args.get('category', '')
        if category == 'history':
            count, datas = self.history_set()
        return count, datas

    def history_set(self):
        self.list_template = 'storage/check_record.html'
        self._list_columns.remove(('operations', '操作'))
        self._list_columns.append(('lastCheckDate', '上次检查日期'))
        self._list_columns.append(('checkRecord', '检查说明'))
        count, datas = self.get_history()
        levels = []
        self._template_args.update({
            'levels': levels,
        })
        return count, datas

    @expose('/edit/', methods=['GET', 'POST'])
    def edit_view(self):
        return super(_CheckWarningView, self).edit_view()

    def edit_form(self, obj=None):
        obj.lastCheckDate = date_generator()

        return super(_CheckWarningView, self).edit_form(obj)

    def get_history(self):
        version = version_class(self.model)
        query = version.query.filter(
            version.nextCheckDate != None, version.nextCheckDate != '').order_by(
                version.nextCheckDate).all()
        datas = []
        for item in query:
            if 'nextCheckDate' in item.changeset.keys() or 'checkRecord' in item.changeset.keys():
                datas.append(item)
        page = request.args.get('page', 0, type=int)
        return len(datas), datas[page * 20:page * 20 + 20]

    def __init__(self, *args, **kwargs):

        self.extra_js = getattr(self, 'extra_js', [])
        self.extra_js.extend([
            # select2
            '/static/js/bootstrap-select.min.js',
            '/static/js/jquery.multi-select.js',
            '/static/js/components-dropdowns.js',
        ])

        self.extra_css = getattr(self, 'extra_css', [])
        self.extra_css.extend([
            '/static/css/mxp.css',
        ])

        super(_CheckWarningView, self).__init__(*args, **kwargs)
        self._tmp_list_columns = deepcopy(self._list_columns)


CheckWarningView = partial(_CheckWarningView,
                           AirMaterialStorageList,
                           endpoint='checkwarning',
                           name='检查预警')
