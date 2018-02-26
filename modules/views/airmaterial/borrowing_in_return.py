# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from collections import OrderedDict
from wtforms import DateField
from wtforms.validators import DataRequired
import json
from flask import request, jsonify
from flask_admin import expose

from util.widgets import DateWidget
from modules.flows.states import Borrowed
from modules.models.airmaterial.borrowing_in_return import \
    BorrowingInReturnModel, BorrowingInReturnMaterial
from modules.flows import BorrowInReturnFlow
from modules.models.airmaterial import LendApplication, AirMaterialStorageList
from .out_storage_application_update_freezed_quantity import\
    UpdateStorageListFreezedQuantity
from airmaterial_fileds import *


def lenappllication_choices():
    query = LendApplication.query.filter(
        LendApplication.auditStatus == Borrowed)
    return query


class _BorrowingInReturnView(UpdateStorageListFreezedQuantity):
    """借入归还视图"""
    list_template = 'storage/list.html'

    column_list = [
        'number', 'lendCategory', 'companyName', 'borrow', 'statusName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'returnDate': '归还日期',
        'lendCategory': '借入类型',
        'companyName': '单位名称',
        'contactPerson': '联系人',
        'remark': '备注',
        'statusName': '状态',
        'companyAddr': '单位地址',
        'telephone': '联系电话',
        'fax': '传真',
        'mailbox': '邮箱',
        'borrow': '借入申请单号',
        'putOutStore': '出库',
        'name': '名称',
        'category': '类别',
        'quantity': '数量',
        'partNumber': '件号',

    }
    # 查看页面显示的详情
    column_details_list = [
        'number', 'borrow', 'returnDate', 'lendCategory', 'telephone', 'fax',
        'companyAddr', 'mailbox', 'companyName', 'contactPerson', 'remark'
    ]

    form_excluded_columns = [
        'statusName', 'borrowingInReturnMaterials', 'putOutStore'
    ]
    column_searchable_list = ('lendCategory', 'companyName', 'number', 'statusName')

    inline_column = 'borrowInReturn_id'
    inline_model = BorrowingInReturnMaterial

    column_export_list = [
        'category', 'partNumber', 'name', 'quantity', 'companyName',
        'contactPerson', 'telephone']

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
        '/static/js/borrow_validation.js',
    ]

    support_flow = partial(BorrowInReturnFlow, 'borrow request storage flow')

    form_overrides = {
        'returnDate': partial(DateField, widget=DateWidget()),
    }

    @property
    def form_widget_args(self):
        return {
            'number': {
                'readonly': True,
            },
            'lendCategory': {
                'readonly': True,
            },

        }

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([
            ('category', AM_CATEGORY),
            ('partNumber', AM_PARTNUMBER),
            ('serialNum', AM_SERIALNUM),
            ('name', AM_NAME),
            ('quantity', AM_QUANTITY),
            ('effectiveDate', AM_EFFECTIVEDATE),
            ('lastCheckDate', AM_LASTCHECKDATE),
            ('nextCheckDate', AM_NEXTCHECKDATE),
            ('flyTime', AM_FLYTIME),
            ('engineTime', AM_ENGINETIME),
            ('flightTimes', AM_FLIGHTTIMES),
        ])

        self.relationField = 'borrowingInReturnMaterials'
        self.f_key = 'borrowInReturn_id'
        self.relationModel = BorrowingInReturnMaterial

        super(_BorrowingInReturnView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)
            table_columns[i]['need'] = False

        table_columns[0]['readOnly'] = True
        table_columns[0]['need'] = True
        table_columns[1]['readOnly'] = True
        table_columns[1]['need'] = True
        table_columns[2]['readOnly'] = True
        table_columns[3]['readOnly'] = True
        table_columns[3]['need'] = True
        table_columns[4]['need'] = True
        table_columns[4]['type'] = 'numeric'
        table_columns[4]['format'] = '0'
        table_columns[5]['editor'] = 'select'
        table_columns[5]['selectOptions'] = []
        table_columns[5]['checkNeed'] = True
        table_columns[6]['type'] = 'date'
        table_columns[6]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[7]['editor'] = 'select'
        table_columns[7]['selectOptions'] = []
        table_columns[7]['checkNeed'] = True
        table_columns[8]['validator'] = 'hhmm'
        table_columns[9]['validator'] = 'hhmm'
        table_columns[10]['type'] = 'numeric'
        table_columns[10]['format'] = '0'

        self._template_args.update({
            'inline_table': True,
            'can_add_line': False,
            'can_del_line': True,
            'extra_table_js': 'js/borrowing_in_return_table.js'
        })

        return json.dumps(table_columns)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        rowid = request.args.getlist('rowid')
        if rowid:
            cats = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.id.in_(rowid)).all()
            table_datas = [[
                cat.category, cat.partNumber, cat.serialNum, cat.name,
                cat.quantity - cat.freezingQuantity, cat.effectiveDate,
                cat.lastCheckDate, cat.nextCheckDate,
                cat.flyTime, cat.engineTime, cat.flightTimes,
            ] for cat in cats]

            table_datas = json.dumps(table_datas)
        else:
            table_datas = json.dumps([])

        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })
        return super(_BorrowingInReturnView, self).create_view()

    def create_form(self, obj=None):
        ao_id = request.args.get('id', '')

        if ao_id:
            inst = LendApplication.query.filter(
                LendApplication.id == ao_id).first()
            return self.create_form_with_default(inst, 'borrow')
        self._create_form_class.borrow.kwargs['query_factory'] = lenappllication_choices
        return super(_BorrowingInReturnView, self).create_form(obj)

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.borrow.validators = [DataRequired()]
            form.returnDate.validators = [DataRequired()]
            form.lendCategory.validators = [DataRequired()]
        return super(_BorrowingInReturnView, self).validate_form(form)

     # 从数据库里以单号查询借入申请信息以json返回
    @expose('/get_borrow_info/', methods=['GET'])
    def get_borrow_info(self):
        try:
            borrow = request.args.get('borrow')
            if borrow:
                item = LendApplication.query.filter(
                    LendApplication.number == borrow).first()
                data = [item.lendCategory, item.companyName,
                        item.contactPerson, item.companyAddr,
                        item.telephone, item.fax,
                        item.mailbox]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    def get_audit_form_class(self, model, verb):
        if verb == 'review':
            return self._action_view_cfg['review_only'].form
        return None


BorrowingInReturnView = partial(
    _BorrowingInReturnView, BorrowingInReturnModel, name='借入归还'
)
