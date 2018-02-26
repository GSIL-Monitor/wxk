# coding: utf-8
from __future__ import unicode_literals

import json
from functools import partial
from flask_admin import expose
from flask import request, jsonify
from wtforms import DateField
from wtforms.validators import DataRequired
from collections import OrderedDict
from modules.flows import DisassembleOrderFlow
from util.widgets import DateWidget
from modules.models.airmaterial import DisassembleOrder, DisassembleMaterial
from .inline_table import InlineTable
from modules.views import CustomView
from .with_inline_table import WithInlineTableView
from modules.helper import get_plane_infos_by_pn, get_pn_by_category
from airmaterial_fileds import *


class _DisassembleOrderView(WithInlineTableView):
    # 拆机单首页列表视图应显示的内容

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
        '/static/js/disassemble_validate.js',
    ]

    column_list = [
        'number', 'disassemblePerson', 'disassembleDate', 'statusName',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'date': '单据日期',
        'disassemblePerson': '拆机人',
        'disassembleDate': '拆机日期',
        'remark': '备注',
        'statusName': '状态',
    }
    # 查看页面显示的详情
    column_details_list = [
        'number', 'date', 'disassemblePerson',
        'disassembleDate', 'remark',
    ]

    form_excluded_columns = ['statusName', 'disassembleMaterials', 'storage']

    support_flow = partial(DisassembleOrderFlow, 'disassemble flow')

    column_searchable_list = (
        'number', 'date', 'disassemblePerson', 'disassembleDate', 'statusName')

    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'disassembleDate': partial(DateField, widget=DateWidget()),
    }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.date.validators = [DataRequired()]
            form.disassembleDate.validators = [DataRequired()]
        return super(_DisassembleOrderView, self).validate_form(form)

    def __init__(self, *args, **kwargs):
        self.table_columns = OrderedDict([
            ('planeNum', AM_PLANENUM),
            ('category', AM_CATEGORY),
            ('partNumber', AM_PARTNUMBER),
            ('serialNum', AM_SERIALNUM),
            ('name', AM_NAME),
            ('quantity', AM_QUANTITY),
            ('unit', AM_UNIT),
            ('manufacturer', AM_MANUFACTURER),
            ('effectiveDate', AM_EFFECTIVEDATE),
            ('lastCheckDate', AM_LASTCHECKDATE),
            ('nextCheckDate', AM_NEXTCHECKDATE),
            ('flyTime', AM_FLYTIME),
            ('engineTime', AM_ENGINETIME),
            ('flightTimes', AM_FLIGHTTIMES),
        ])
        self.relationField = 'disassembleMaterials'
        self.f_key = 'disassembleOrder_id'
        self.relationModel = DisassembleMaterial

        super(_DisassembleOrderView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)
            table_columns[i]['need'] = False
        # 设置表格格式
        table_columns[0]['editor'] = 'select'
        table_columns[0]['selectOptions'] = []
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = ['一般航材', '工装设备', '消耗品', '化工品', '时控件', '时寿件']
        table_columns[1]['need'] = True
        table_columns[2]['type'] = 'autocomplete'
        table_columns[2]['readOnly'] = True
        table_columns[2]['source'] = ['']
        table_columns[2]['strict'] = True
        table_columns[2]['trimDropdown'] = False
        table_columns[2]['allowInvalid'] = False
        table_columns[2]['need'] = True
        table_columns[4]['need'] = True
        table_columns[4]['readOnly'] = True
        table_columns[5]['type'] = 'numeric'
        table_columns[5]['format'] = '0'
        table_columns[5]['need'] = True
        table_columns[6]['readOnly'] = True
        table_columns[7]['editor'] = 'select'
        table_columns[7]['selectOptions'] = self.get_manafacturers()
        table_columns[8]['type'] = 'date'
        table_columns[8]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[8]['checkNeed'] = True
        table_columns[9]['type'] = 'date'
        table_columns[9]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[10]['type'] = 'date'
        table_columns[10]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[10]['checkNeed'] = True
        table_columns[11]['validator'] = 'hhmm'
        table_columns[12]['validator'] = 'hhmm'

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/disassemble_order.js',
        })

        return json.dumps(table_columns)

    @property
    def form_widget_args(self):
        return {
            'number': {
                'readonly': True
            },
        }

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):

        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': json.dumps([]),
        })
        return super(_DisassembleOrderView, self).create_view()

    @expose('/approve-edit-view/', methods=['POST', 'GET'])
    def approve_edit_view(self):
        self._template_args.update({
            'table_columns': self.init_table_columns(),
        })
        return super(_DisassembleOrderView, self).approve_edit_view()

    def before_edit_form(self, model):
        self._template_args.update({
            'table_datas': self.get_table_data_from_db(model),
        })

    @expose('/details/')
    def details_view(self):

        self._template_args.update({
            'table_columns': self.get_readonly_table(),
            'table_datas': self.get_table_data_from_db(),
            'extra_table_js': 'js/inline_table_details.js'
        })

        return super(_DisassembleOrderView, self).details_view()

    @expose('/action-view/', methods=['POST', 'GET'])
    def action_view(self):
        self._template_args.update({
            'table_columns': self.get_readonly_table(),
            'table_datas': self.get_table_data_from_db(),
        })
        return super(_DisassembleOrderView, self).action_view()

    @expose('/get_plane_infos_from_pn/', methods=['POST', 'GET'])
    def get_plane_infos_from_pn(self):
        try:
            ca = request.args.get('ca')
            pn = request.args.get('pn')
            plane_num = request.args.get('planeNum')
            if ca and pn and plane_num:
                data = get_plane_infos_by_pn(pn, plane_num, ca)
                data = json.dumps(data)
            return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=400, message='Not Found')

    @expose('/get_pn_from_bounded_category/', methods=['GET'])
    def get_pn_from_bounded_category(self):
        try:
            ca = request.args.get('ca')
            if ca:
                data = get_pn_by_category(ca)
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=400, message='Not Found')

    @expose('/get-bounded-aircraft/', methods=['POST', 'GET'])
    def get_bounded_aircraft(self):
        bounded = request.args.get('bounded')
        data = self.get_aircraft(bounded)
        data = json.dumps(data)
        return jsonify(code=200, data=data, message='Ok')


DisassembleOrderView = partial(
    _DisassembleOrderView, DisassembleOrder, name='拆机单'
)
