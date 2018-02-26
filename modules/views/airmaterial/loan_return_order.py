# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from collections import OrderedDict
from flask import request
from flask_admin import expose
import json

from wtforms import DateField, SelectField
from modules.flows import LoanInReturnFlow
from wtforms.validators import DataRequired
from util.widgets import DateWidget
from modules.models.airmaterial import (
    LoanReturnOrder, LoanReturnMaterial, LoanApplicationOrder
)
from .with_inline_table import WithInlineTableView
from airmaterial_fileds import *


class _LoanReturnOrderView(WithInlineTableView):
    """借出归还视图"""
    list_template = 'storage/list.html'

    column_list = [
        'number', 'loanCategory', 'borrowCompany', 'statusName',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'date': '单据日期',
        'loanCategory': '借出类型',
        'borrowCompany': '归还单位',
        'companyAddr': '单位地址',
        'contactPerson': '联系人',
        'telephone': '联系电话',
        'fax': '传真',
        'mailbox': '邮箱',
        'remark': '备注',
        'returnDate': '归还日期',
        'statusName': '状态',
        'loanApplication': '借出申请单编号',
        'name': '名称',
        'category': '类别',
        'quantity': '数量',
        'partNumber': '件号',
    }

    column_searchable_list = ('loanCategory', 'number',
                              'statusName', 'borrowCompany')
    # 查看页面显示的详情
    column_details_list = [
        'number', 'loanCategory', 'borrowCompany', 'companyAddr', 'contactPerson',
        'loanApplication', 'telephone', 'fax', 'mailbox', 'remark', 'returnDate',
    ]

    form_excluded_columns = [
        'statusName', 'storage', 'loanReturnMaterials', 'date']

    support_flow = partial(LoanInReturnFlow, 'loan return flow')

    inline_model = LoanReturnMaterial
    inline_column = 'loanReturnOrder_id'
    column_export_list = [
        'category', 'partNumber', 'name', 'quantity', 'borrowCompany',
        'contactPerson', 'telephone']


    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'returnDate': partial(DateField, widget=DateWidget()),
    }
    form_widget_args = {
        'number': {
            'readonly': True
        },
        'loanCategory': {
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
        '/static/js/load_return_validation.js',
    ]

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([('category', AM_CATEGORY),
                                          ('partNumber', AM_PARTNUMBER),
                                          ('serialNum', AM_SERIALNUM),
                                          ('name', AM_NAME),
                                          ('manufacturer', AM_MANUFACTURER),
                                          ('quantity', AM_QUANTITY),
                                          ('lastCheckDate', AM_LASTCHECKDATE),
                                          ('flyTime', AM_FLYTIME),
                                          ('engineTime', AM_ENGINETIME),
                                          ('flightTimes', AM_FLIGHTTIMES)])

        self.relationField = 'loanReturnMaterials'
        self.f_key = 'loanReturnOrder_id'
        self.relationModel = LoanReturnMaterial

        super(_LoanReturnOrderView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)

        table_columns[0]['editor'] = 'select'
        table_columns[0]['selectOptions'] = [
            '一般航材', '工装设备', '消耗品', '化工品', '时控件', '时寿件']
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = []
        table_columns[1]['need'] = True
        table_columns[3]['readOnly'] = True
        table_columns[4]['readOnly'] = True
        table_columns[6]['type'] = 'date'
        table_columns[6]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[7]['validator'] = 'hhmm'
        table_columns[8]['validator'] = 'hhmm'

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/loan_return_order_table.js'
        })

        return json.dumps(table_columns)

    form_widget_args = {
        'number': {
            'readonly': True
        },
    }

    def create_form(self, obj=None):
        ao_id = request.args.get('id', '')

        if ao_id:
            inst = LoanApplicationOrder.query.filter(
                LoanApplicationOrder.id == ao_id).first()
            return self.create_form_with_default(inst, 'loanApplication')

        return super(_LoanReturnOrderView, self).create_form(obj)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):

        ao_id = request.args.get('id', '')
        table_datas = json.dumps([])
        if ao_id:
            inst_model = LoanApplicationOrder.query.filter(
                LoanApplicationOrder.id == ao_id).first()
            table_datas = [[
                inst.category, inst.partNumber, inst.serialNum,
                inst.name, inst.manufacturer, inst.quantity,
                inst.lastCheckDate, inst.flyTime,
                inst.engineTime, inst.flightTimes,
            ] for inst in inst_model.loanMaterials]
            table_datas = json.dumps(table_datas)
        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })
        return super(_LoanReturnOrderView, self).create_view()

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.returnDate.validators = [DataRequired()]
            form.loanCategory.validators = [DataRequired()]
        return super(_LoanReturnOrderView, self).validate_form(form)

    def get_audit_form_class(self, model, verb):
        if verb == 'review':
            return self._action_view_cfg['review_only'].form
        return None


LoanReturnOrderView = partial(
    _LoanReturnOrderView, LoanReturnOrder, name='借出归还'
)
