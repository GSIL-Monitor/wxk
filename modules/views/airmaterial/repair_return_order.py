# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from flask_admin import expose
from wtforms import DateField
from modules.flows import LoanInReturnFlow
from flask import request
from wtforms.validators import DataRequired
from util.widgets import DateWidget
from collections import OrderedDict
from modules.models.airmaterial import (
    RepairReturnOrder, RepairReturnMaterial, RepairApplication,
)
from util.fields.select import RefreshRepairSupplierSelectField
from with_inline_table import WithInlineTableView
from airmaterial_fileds import *


class _RepairReturnOrderView(WithInlineTableView):
    """送修归还视图"""
    list_template = 'storage/list.html'
    column_list = [
        'number', 'returnDate', 'repairCompany',
        'statusName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'returnDate': '归还日期',
        'repairCompany': '维修厂商',
        'contactPerson': '联系人',
        'remark': '备注',
        'statusName': '状态',
        'repairApplication': '送修申请单据编号',
    }
    column_searchable_list = ('repairCompany', 'number', 'statusName')
    # 查看页面显示的详情
    column_details_list = [
        'number', 'repairApplication', 'returnDate', 'repairCompany',
        'contactPerson', 'remark',
    ]

    form_excluded_columns = ['statusName', 'repairApplicationNum',
                             'repairReturnMaterials', 'storage']
    support_flow = partial(LoanInReturnFlow, 'repair return application flow')
    form_overrides = {
        'returnDate': partial(DateField, widget=DateWidget()),
        'repairCompany': partial(RefreshRepairSupplierSelectField),
    }
    form_widget_args = {
        'number': {
            'readonly': True
        },
    }
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
        '/static/js/customview_formvalidation.js',
        '/static/js/repair_return_validation.js',
    ]

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.repairApplication.validators = [DataRequired()]
            form.returnDate.validators = [DataRequired()]
        return super(_RepairReturnOrderView, self).validate_form(form)

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([
            ('category', AM_CATEGORY),
            ('partNumber', AM_PARTNUMBER),
            ('serialNum', AM_SERIALNUM),
            ('name', AM_NAME),
            ('quantity', AM_QUANTITY),
            ('manufacturer', AM_MANUFACTURER),
            ('lastCheckDate', AM_LASTCHECKDATE),
            ('flyTime', AM_FLYTIME),
            ('engineTime', AM_ENGINETIME),
            ('flightTimes', AM_FLIGHTTIMES),
        ])
        self.relationField = 'repairReturnMaterials'
        self.f_key = 'application_id'
        self.relationModel = RepairReturnMaterial

        super(_RepairReturnOrderView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)
            table_columns[i]['need'] = False

        table_columns[0]['editor'] = 'select'
        table_columns[0]['selectOptions'] = ['一般航材', '工装设备', '消耗品', '化工品', '时控件', '时寿件']
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = []
        table_columns[1]['need'] = True
        table_columns[3]['need'] = True
        table_columns[3]['readOnly'] = True
        table_columns[4]['type'] = 'numeric'
        table_columns[4]['format'] = '0'
        table_columns[4]['readOnly'] = True
        table_columns[6]['type'] = 'date'
        table_columns[6]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[7]['validator'] = 'hhmm'
        table_columns[8]['validator'] = 'hhmm'
        table_columns[9]['type'] = 'numeric'
        table_columns[9]['format'] = '0'

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/repair_return_order.js'
        })

        return json.dumps(table_columns)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        ao_id = request.args.get('id', '')
        table_datas = json.dumps([])
        if ao_id:
            inst_model = RepairApplication.query.filter(
                RepairApplication.id == ao_id).first()
            table_datas = [[inst.category, inst.partNumber, inst.serialNum, inst.name,
                            inst.quantity, inst.manufacturer, None, inst.flyTime,
                            inst.engineTime, inst.flightTimes,
                            ] for inst in inst_model.repairAppl]
            table_datas = json.dumps(table_datas)
        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })
        return super(_RepairReturnOrderView, self).create_view()

    def create_form(self, obj=None):
        ao_id = request.args.get('id', '')
        if ao_id:
            inst = RepairApplication.query.filter(
                RepairApplication.id == ao_id).first()
            return self.create_form_with_default(inst, 'repairApplication')
        return super(_RepairReturnOrderView, self).create_form(obj)

    def get_audit_form_class(self, model, verb):
        if verb == 'review':
            return self._action_view_cfg['review_only'].form
        return None


RepairReturnOrderView = partial(
    _RepairReturnOrderView, RepairReturnOrder, name='送修归还'
)
