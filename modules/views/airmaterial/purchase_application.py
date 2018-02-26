# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json
from flask import request, abort
from flask_admin import expose
from flask_admin.helpers import get_form_data
from modules.flows import PurchaseRequestFlow
from wtforms.validators import DataRequired
from flask_admin.helpers import is_form_submitted
from collections import OrderedDict

from util.fields import DateField
from util.widgets import DateWidget
from modules.models.airmaterial.purchase_application import PurchaseApplication
from modules.models.airmaterial.purchase_application import PurchaseMaterial
from modules.models.airmaterial.airmaterial_category import AirmaterialCategory
from modules.models.airmaterial.storage_list import AirMaterialStorageList
from ..column_formatter import accessory_formatter
from util.fields.accessory_filed import AirmaterialFileuploadField
from .with_inline_table import WithInlineTableView
from util.fields.select import RefreshSupplierSelectField
from airmaterial_fileds import *
from modules.views.approve_flow_with_uploadfile import ApproveFlowUploadFileView


class _PurchaseApplicationView(ApproveFlowUploadFileView):
    # 采购入库首页列CustomView显示的内容

    create_template = 'purchase_application/create.html'
    approve_edit_template = 'purchase_application/approve_edit.html'

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
        '/static/js/purchase_application.js',
    ]

    column_list = [
        'number', 'date', 'supplier', 'statusName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'date': '日期',
        'applicationDate': '申请日期',
        'partNumber': '件号',
        'name': '名称',
        'quantity': '数量',
        'unitPrice': '单价',
        'manufacturer': '生产厂商',
        'supplier': '供应商',
        'contactPerson': '联系人',
        'telephone': '电话',
        'fax': '传真',
        'mailbox': '邮箱',
        'receiver': '收货人',
        'accessory': '附件',
        'applicationInstruction': '申请说明',
        'budget': '预算',
        'remark': '备注',
        'statusName': '状态',
        'contractFile': '合同文件',
        'meetingFile': '会议纪要',
        'purchase': '航材'
    }
    # 查看页面显示的详情
    column_details_list = [
        'number', 'date', 'applicationDate', 'supplier', 'contactPerson',
        'telephone', 'fax', 'mailbox', 'receiver', 'remark', 'contractFile',
        'meetingFile', 'applicationInstruction', 'accessory'
    ]

    form_excluded_columns = ['statusName', 'contractFile', 'meetingFile',
                             'purchase', 'storage']
    support_flow = partial(PurchaseRequestFlow, 'purchase request flow')

    column_searchable_list = ('number', 'date', 'supplier', 'statusName')

    one_line_columns = ['applicationInstruction', 'accessory']

    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'applicationDate': partial(DateField, widget=DateWidget()),
        'accessory': partial(AirmaterialFileuploadField),
        'contractFile': partial(AirmaterialFileuploadField),
        'meetingFile': partial(AirmaterialFileuploadField),
        'supplier': partial(RefreshSupplierSelectField),
    }
    column_formatters = {
        'accessory': accessory_formatter('accessory'),
        'contractFile': accessory_formatter('contractFile'),
        'meetingFile': accessory_formatter('meetingFile'),
    }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.date.validators = [DataRequired()]
            form.applicationDate.validators = [DataRequired()]
        return super(_PurchaseApplicationView, self).validate_form(form)

    form_widget_args = {
        'number': {
            'readonly': True
        },
        'contactPerson': {
            'readonly': True
        },
        'telephone': {
            'readonly': True
        },
        'fax': {
            'readonly': True
        },
        'mailbox': {
            'readonly': True
        },

    }

    def __init__(self, *args, **kwargs):
        self.table_columns = OrderedDict([('category', AM_CATEGORY),
                                          ('partNumber', AM_PARTNUMBER),
                                          ('name', AM_NAME),
                                          ('manufacturer', AM_MANUFACTURER),
                                          ('unitPrice', AM_UNITPRICE),
                                          ('quantity', AM_QUANTITY),
                                          ('budget', AM_BUDGET)])
        self.relationField = 'purchase'
        self.f_key = 'application_id'
        self.relationModel = PurchaseMaterial
        super(_PurchaseApplicationView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)

        table_columns[0]['editor'] = 'select'
        table_columns[0]['selectOptions'] = ['一般航材', '工装设备', '消耗品',
                                             '化工品', '时控件', '时寿件']
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = []
        table_columns[1]['need'] = True
        table_columns[2]['readOnly'] = True
        table_columns[2]['need'] = True
        table_columns[3]['editor'] = 'select'
        table_columns[3]['selectOptions'] = self.get_manafacturers()
        table_columns[4]['type'] = 'numeric'
        table_columns[4]['format'] = '0.00'
        table_columns[4]['validator'] = 'nonnegative'
        table_columns[5]['type'] = 'numeric'
        table_columns[5]['format'] = '0'
        table_columns[5]['need'] = True
        table_columns[6]['type'] = 'numeric'
        table_columns[6]['format'] = '0.00'
        table_columns[6]['readOnly'] = True

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/purchase_application_table.js'
        })

        return json.dumps(table_columns)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        rowid = request.args.getlist('rowid')
        aoid = request.args.getlist('aoid')
        if not rowid and not aoid:
            table_datas = json.dumps([])
        else:
            if rowid:
                request_class = AirmaterialCategory
                ids = rowid
            if aoid:
                request_class = AirMaterialStorageList
                ids = aoid
            cats = request_class.query.filter(
                request_class.id.in_(ids)).all()
            table_datas = [[
                    cat.category, cat.partNumber,
                    cat.name, None, None, 1, None
                ] for cat in cats]

            table_datas = json.dumps(table_datas)

        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })
        return super(_PurchaseApplicationView, self).create_view()


PurchaseApplicationView = partial(
    _PurchaseApplicationView, PurchaseApplication, name='采购申请'
)
