# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from collections import OrderedDict
from flask import request, jsonify
from flask_admin import expose
import json

from wtforms import DateField, SelectField
from modules.flows import BorrowRequestFlow
from wtforms.validators import DataRequired
from util.widgets import DateWidget
from modules.models.airmaterial.lend_application import LendApplication, LendApplicationMaterial
from ..column_formatter import accessory_formatter
from modules.models.airmaterial.storage_list import AirMaterialStorageList
from modules.models.airmaterial.airmaterial_category import AirmaterialCategory
from util.fields.accessory_filed import AirmaterialFileuploadField
from .with_inline_table import WithInlineTableView
from modules.forms.action import ApproveForm
from modules.flows.operations import Review
from airmaterial_fileds import *
from modules.views.approve_flow_with_uploadfile import ApproveFlowUploadFileView


class _LendApplicationView(ApproveFlowUploadFileView):
    """借入申请"""

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
        '/static/js/lend_application_validation.js',
    ]

    column_list = [
        'number', 'date', 'lendCategory',
        'companyName', 'applicationDate', 'statusName',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'date': '日期',
        'companyName': '单位名称',
        'companyAddr': '单位地址',
        'contactPerson': '联系人',
        'telephone': '电话',
        'fax': '传真',
        'mailbox': '邮箱',
        'accessory': '附件',
        'partNumber': '件号',
        'serialNum': '序号',
        'name': '名称',
        'lendCategory': '借入类型',
        'category': '类别',
        'flightTime': '飞行小时',
        'engineTime': '发动机小时',
        'quantity': '数量',
        'applicationReason': '申请原因',
        'applicationDate': '申请日期',
        'remark': '备注',
        'statusName': '状态',
        'contractFile': '合同文件',
    }
    # 查看页面显示的详情
    column_details_list = [
        'number', 'lendCategory', 'date', 'applicationDate',
        'companyName', 'companyAddr', 'contactPerson', 'telephone', 'fax',
        'mailbox', 'remark', 'contractFile', 'accessory', 'applicationReason'
    ]

    form_excluded_columns = [
        'statusName', 'storage', 'contractFile',
        'borrowingInReturn', 'lendApplicationMaterials'
    ]

    inline_column = 'lendApplication_id'
    inline_model = LendApplicationMaterial

    column_export_list = [
        'category', 'partNumber', 'name', 'quantity', 'companyName',
        'contactPerson', 'telephone']

    support_flow = partial(BorrowRequestFlow, 'borrow request storage flow')

    one_line_columns = ['applicationReason', "accessory"]

    column_searchable_list = ('number', 'date', 'lendCategory', 'companyName', 'applicationDate', 'statusName')
    airmaterial_category = [
        ('一般航材', '一般航材'),
        ('工装设备', '工装设备'),
        ('消耗品', '消耗品'),
        ('化工品', '化工品'),
    ]

    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'applicationDate': partial(DateField, widget=DateWidget()),
        'category': partial(SelectField, choices=airmaterial_category),
        'accessory': partial(AirmaterialFileuploadField),
    }

    column_formatters = {
        'accessory': accessory_formatter('accessory'),
        'contractFile': accessory_formatter('contractFile'),
    }

    form_widget_args = {
        'number': {
            'readonly': True
        },
    }

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([('category', AM_CATEGORY),
                                          ('partNumber', AM_PARTNUMBER),
                                          ('name', AM_NAME),
                                          ('quantity', AM_QUANTITY)])

        self.relationField = 'lendApplicationMaterials'
        self.f_key = 'lendApplication_id'
        self.relationModel = LendApplicationMaterial
        super(_LendApplicationView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)

        table_columns[0]['editor'] = 'select'
        table_columns[0]['selectOptions'] = ['一般航材', '工装设备', '消耗品', '化工品', '时控件', '时寿件']
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = []
        table_columns[1]['need'] = True
        table_columns[2]['readOnly'] = True
        table_columns[2]['need'] = True
        table_columns[3]['type'] = 'numeric'
        table_columns[3]['format'] = '0'
        table_columns[3]['need'] = True

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/lend_application_table.js'
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
            table_datas = [[cat.category, cat.partNumber, cat.name, 1
                            ] for cat in cats]
            table_datas = json.dumps(table_datas)

        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })
        return super(_LendApplicationView, self).create_view()

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.date.validators = [DataRequired()]
            form.applicationDate.validators = [DataRequired()]
        return super(_LendApplicationView, self).validate_form(form)

    @expose('/get_pn_form_lend_app/', methods=['GET'])
    def get_pn_form_lend_app(self):
        try:
            num = request.args.get('num')
            if num:
                items = LendApplication.query.filter(LendApplication.number == num).first()
                data = [item.partNumber for item in items.lendApplicationMaterials]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    def get_audit_form_class(self, model, verb):
        if model.lendCategory == '一般航材'and verb == Review:
            return ApproveForm
        return None


LendApplicationView = partial(
    _LendApplicationView, LendApplication, name='借入申请'
)
