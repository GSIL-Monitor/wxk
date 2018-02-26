# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from flask_admin import expose
from flask import url_for, redirect, request, abort
from wtforms import DateField
from modules.flows import AssembleFlow
from wtforms.validators import DataRequired
from util.widgets import DateWidget
from collections import OrderedDict

from modules.models.airmaterial.assemble import Assemble
from modules.models.airmaterial.assemble_application import (
    AssembleApplicationList, AssembleApplication)
from modules.views import CustomView
from .with_inline_table import WithInlineTableView
from airmaterial_fileds import *


class _AssembleView(WithInlineTableView):
    """装机单"""
    list_template = 'storage/list.html'

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/bootstrap-select.min.js',
        '/static/js/jquery.multi-select.js',
        '/static/js/components-dropdowns.js',
        '/static/js/select_planeType.js',
        '/static/js/inline_table.js',
        '/static/js/numbro.js',
        '/static/js/languages.js',
        '/static/js/zh-CN.min.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/moment.min.js',
        '/static/js/pikaday.js',
        '/static/js/pikaday-zh.js',
        '/static/js/upload_file.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/assemble_validate.js',
    ]

    column_list = [
        'number', 'date', 'assemblePerson', 'assembleDate', 'statusName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'date': '单据日期',
        'assembleDate': '装机日期',
        'assemblePerson': '装机人',
        'remark': '备注',
        'statusName': '状态',
        'assembleApplication': '装机申请'

    }

    column_searchable_list = ('assemblePerson', 'number', 'statusName')
    # 查看页面显示的详情
    column_details_list = [
        'number', 'date', 'assemblePerson', 'assembleDate', 'assembleApplication']

    form_excluded_columns = ['statusName', 'assembleApplicationList']
    support_flow = partial(AssembleFlow, 'purchase request flow')

    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'assembleDate': partial(DateField, widget=DateWidget())
    }
    column_formatters = {
    }

    form_widget_args = {
        'number': {
            'readonly': True
        },
    }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.date.validators = [DataRequired()]
            form.assembleDate.validators = [DataRequired()]
        return super(_AssembleView, self).validate_form(form)

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([
            ('category', AM_CATEGORY),
            ('partNumber', AM_PARTNUMBER),
            ('serialNum', AM_SERIALNUM),
            ('name', AM_NAME),
            ('manufacturer', AM_MANUFACTURER),
            ('quantity', AM_QUANTITY),
            ('unit', AM_UNIT),
            ('planeNum', AM_PLANENUM),
            ('effectiveDate', AM_EFFECTIVEDATE),
            ('lastCheckDate', AM_LASTCHECKDATE),
            ('nextCheckDate', AM_NEXTCHECKDATE),
            ('flyTime', AM_FLYTIME),
            ('engineTime', AM_ENGINETIME),
            ('flightTimes', AM_FLIGHTTIMES),
        ])
        self.relationField = 'assembleApplicationList'
        self.f_key = 'assemble_id'
        self.relationModel = AssembleApplicationList

        super(_AssembleView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)

        table_columns[0]['readOnly'] = True
        table_columns[0]['need'] = True
        table_columns[1]['readOnly'] = True
        table_columns[1]['need'] = True
        table_columns[2]['readOnly'] = True
        table_columns[3]['readOnly'] = True
        table_columns[3]['need'] = True
        table_columns[4]['readOnly'] = True
        table_columns[5]['type'] = 'numeric'
        table_columns[5]['format'] = '0'
        table_columns[5]['need'] = True
        table_columns[6]['readOnly'] = True
        table_columns[7]['need'] = True
        table_columns[7]['editor'] = 'select'
        table_columns[7]['selectOptions'] = self.get_aircraft()
        table_columns[8]['readOnly'] = True
        table_columns[8]['checkNeed'] = True
        table_columns[9]['type'] = 'date'
        table_columns[9]['need'] = True
        table_columns[9]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[10]['readOnly'] = True
        table_columns[10]['checkNeed'] = True
        table_columns[11]['validator'] = 'hhmm'
        table_columns[12]['validator'] = 'hhmm'
        table_columns[13]['type'] = 'numeric'
        table_columns[13]['format'] = '0'

        self._template_args.update({
            'inline_table': True,
            'can_add_line': False,
            'can_del_line': True,
            'extra_table_js': 'js/assemble.js'
        })

        return json.dumps(table_columns)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        ao_id = request.args.get('id', '')
        table_datas = json.dumps([])
        if ao_id:
            inst_model = AssembleApplication.query.filter(
                AssembleApplication.id == ao_id).first()
            table_datas = [[
                inst.category, inst.partNumber, inst.serialNum, inst.name,
                inst.manufacturer, inst.quantity, inst.unit, inst.planeNum,
                inst.effectiveDate, inst.lastCheckDate, inst.nextCheckDate,
                inst.flyTime, inst.engineTime, inst.flightTimes,
            ] for inst in inst_model.assembleApplicationList]
            table_datas = json.dumps(table_datas)
        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })
        return super(_AssembleView, self).create_view()

    def create_form(self, obj=None):
        ao_id = request.args.get('id', '')
        if ao_id:
            inst = AssembleApplication.query.filter(
                AssembleApplication.id == ao_id).first()
            return self.create_form_with_default(inst, 'assembleApplication')
        return super(_AssembleView, self).create_form(obj)


AssembleView = partial(
    _AssembleView, Assemble, name='装机'
)
