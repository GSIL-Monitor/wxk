# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from flask_admin import expose
from flask import request, jsonify
from collections import OrderedDict
from wtforms import DateField

from modules.flows import LoanApplicationFlow
from wtforms.validators import DataRequired
from util.widgets import DateWidget
from modules.models.airmaterial.loan_application_order import (
    LoanApplicationOrder, LoanMaterial)
from modules.models.airmaterial.manufacturer import Manufacturer
from modules.models.airmaterial.storage_list import AirMaterialStorageList
from .out_storage_application_update_freezed_quantity import\
    UpdateStorageListFreezedQuantity
from modules.forms.action import ApproveForm
from modules.flows.operations import Review
from ..column_formatter import accessory_formatter
from airmaterial_fileds import *
from modules.views.approve_flow_with_uploadfile import ApproveFlowUploadFileView
from util.fields.accessory_filed import AirmaterialFileuploadField


class _LoanApplicationOrderView(ApproveFlowUploadFileView,
                                UpdateStorageListFreezedQuantity):
    """借出申请视图"""

    column_list = [
        'number', 'loanCategory', 'borrowCompany', 'statusName', 'applicationDate'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'applicationDate': '申请日期',
        'loanCategory': '借出类型',
        'date': '单据日期',
        'companyAddr': '单位地址',
        'applicationReason': '申请原因',
        'borrowCompany': '借用单位',
        'contactPerson': '联系人',
        'remark': '备注',
        'statusName': '状态',
        'contractFile': '合同文件',
        'telephone': '联系电话',
        'fax': '传真',
        'mailbox': '邮箱',
        'name': '名称',
        'category': '类别',
        'quantity': '数量',
        'partNumber': '件号',

    }
    column_searchable_list = (
        'loanCategory', 'number',
        'statusName', 'borrowCompany'
    )

    form_excluded_columns = ['contractFile', 'statusName']


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
        '/static/js/load_application_validation.js',
    ]

    # 查看页面显示的详情
    column_details_list = [
        'number', 'applicationDate', 'applicationReason', 'loanCategory',
        'date', 'companyAddr', 'borrowCompany', 'contactPerson', 'telephone',
        'fax', 'mailbox', 'remark', 'contractFile'
    ]

    form_excluded_columns = [
        'statusName', 'loanReturnOrders', 'loanMaterials', 'putOutStore', 'contractFile'
    ]

    support_flow = partial(LoanApplicationFlow, 'loan application flow')

    inline_model = LoanMaterial
    inline_column = 'loanApplication_id'
    column_export_list = [
        'category', 'partNumber', 'name', 'quantity', 'borrowCompany',
        'contactPerson', 'telephone']


    column_formatters = {
        'contractFile': accessory_formatter('contractFile'),
    }
    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'applicationDate': partial(DateField, widget=DateWidget()),
        'contractFile': partial(AirmaterialFileuploadField),
    }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.date.validators = [DataRequired()]
            form.applicationDate.validators = [DataRequired()]
            form.loanCategory.validators = [DataRequired()]
        return super(_LoanApplicationOrderView, self).validate_form(form)

    @property
    def form_widget_args(self):
        return {
            'number': {
                'readonly': True
            },
        }

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([
            ('category', AM_CATEGORY),
            ('partNumber', AM_PARTNUMBER),
            ('serialNum', AM_SERIALNUM),
            ('name', AM_NAME),
            ('manufacturer', AM_MANUFACTURER),
            ('quantity', AM_QUANTITY),
            ('effectiveDate', AM_EFFECTIVEDATE),
            ('lastCheckDate', AM_LASTCHECKDATE),
            ('nextCheckDate', AM_NEXTCHECKDATE),
            ('flyTime', AM_FLYTIME),
            ('engineTime', AM_ENGINETIME),
            ('flightTimes', AM_FLIGHTTIMES),
        ])
        self.relationField = 'loanMaterials'
        self.f_key = 'loanApplication_id'
        self.relationModel = LoanMaterial

        super(_LoanApplicationOrderView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)
            table_columns[i]['need'] = False

        table_columns[0]['editor'] = 'select'
        table_columns[0]['selectOptions'] = [
            '一般航材', '工装设备', '消耗品', '化工品', '时控件', '时寿件'
        ]
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = []
        table_columns[1]['need'] = True
        table_columns[2]['editor'] = 'select'
        table_columns[2]['selectOptions'] = []
        table_columns[3]['readOnly'] = True
        table_columns[3]['need'] = True
        table_columns[4]['editor'] = 'select'
        table_columns[4]['selectOptions'] = self.get_manufacturer()
        table_columns[5]['type'] = 'numeric'
        table_columns[5]['need'] = True
        table_columns[5]['format'] = '0'
        table_columns[6]['editor'] = 'select'
        table_columns[6]['selectOptions'] = []
        table_columns[6]['checkNeed'] = True
        table_columns[7]['type'] = 'date'
        table_columns[7]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[8]['editor'] = 'select'
        table_columns[8]['selectOptions'] = []
        table_columns[8]['checkNeed'] = True
        table_columns[9]['validator'] = 'hhmm'
        table_columns[10]['validator'] = 'hhmm'
        table_columns[11]['type'] = 'numeric'
        table_columns[11]['format'] = '0'

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/loan_application_table.js',
        })

        return json.dumps(table_columns)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        rowid = request.args.getlist('rowid')
        if rowid:
            stos = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.id.in_(rowid)).all()
            table_datas = [
                [sto.category, sto.partNumber, sto.serialNum, sto.name,
                 sto.manufacturer, sto.quantity - sto.freezingQuantity,
                 sto.effectiveDate,
                 sto.lastCheckDate, sto.nextCheckDate,
                 sto.flyTime, sto.engineTime,
                 sto.flightTimes, sto.effectiveDate] for sto in stos]
            table_datas = json.dumps(table_datas)
        else:
            table_datas = json.dumps([])

        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })
        return super(_LoanApplicationOrderView, self).create_view()

    @expose('/get_pn_from_loan_ca/', methods=['GET'])
    def get_pn_from_loan_ca(self):
        try:
            ca = request.args.get('ca')
            num = request.args.get('num')
            if ca and num:
                inst = LoanApplicationOrder.query.filter_by(number=num).first()
                materials = inst.loanMaterials
                data = [m.partNumber for m in materials if m.category == ca]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=404, message='Not Found')

    @expose('/get_sn_from_loan_pn/', methods=['GET'])
    def get_sn_from_loan_pn(self):
        try:
            pn = request.args.get('pn')
            num = request.args.get('num')
            if pn and num:
                inst = LoanApplicationOrder.query.filter_by(number=num).first()
                materials = inst.loanMaterials
                data = [m.serialNum for m in materials if m.partNumber == pn]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=404, message='Not Found')

    @expose('/get_from_loan_pn/', methods=['GET'])
    def get_from_loan_pn(self):
        try:
            pn = request.args.get('pn')
            num = request.args.get('num')
            if pn and num:
                inst = LoanApplicationOrder.query.filter_by(number=num).first()
                materials = inst.loanMaterials
                materials = [m for m in materials if m.partNumber == pn]
                data = [[m.category, m.partNumber, m.serialNum, m.name,
                        m.manufacturer, m.quantity, m.flyTime,
                        m.engineTime, m.flightTimes, m.lastCheckDate,
                        m.nextCheckDate] for m in materials]
                data = json.dumps(data[0])
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=404, message='Not Found')

    def get_audit_form_class(self, model, verb):
        if model.loanCategory == '一般' and verb == Review:
            return ApproveForm
        return None


LoanApplicationOrderView = partial(
    _LoanApplicationOrderView, LoanApplicationOrder, name='借出申请'
)
