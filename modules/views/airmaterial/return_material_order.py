# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from flask_admin import expose
from util.fields import DateField
from wtforms import TextAreaField
from collections import OrderedDict
from modules.flows import DisassembleOrderFlow
from wtforms.validators import DataRequired
from util.widgets import DateWidget
from modules.models.airmaterial.return_material_order import (
    ReturnMaterialOrder, ReturnMaterial)
from modules.models.airmaterial.airmaterial_category import AirmaterialCategory
from .inline_table import InlineTable
from with_inline_table import WithInlineTableView
from airmaterial_fileds import *


class _ReturnMaterialOrderView(WithInlineTableView):
    # 退料单首页列表视图应显示的内容

    create_template = 'return_material_order/create.html'
    approve_edit_template = 'return_material_order/approve_edit.html'

    column_list = [
        'number', 'returnPerson', 'status', 'returnDate'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'date': '日期',
        'returnPerson': '退料人',
        'returnDate': '退料日期',
        'remark': '备注',
        'returnReason': '退料原因',
        'statusName': '状态',
    }
    column_details_list = [
        'number', 'date', 'returnPerson',
        'returnDate', 'remark', 'returnReason'
    ]

    form_excluded_columns = ['statusName', 'storage', 'returnMaterials']

    # 退料单流程与拆机流程相同
    support_flow = partial(DisassembleOrderFlow, 'return material flow')

    one_line_columns = ['returnReason']

    column_searchable_list = ('number', 'date', 'returnPerson', 'returnDate', 'statusName')

    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'returnDate': partial(DateField, widget=DateWidget()),
        'returnReason': partial(TextAreaField, render_kw={'rows': 3, 'style': 'resize:none;'}),

    }

    @property
    def form_widget_args(self):
        return {
            'number': {
                'readonly': True
            },
        }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.date.validators = [DataRequired()]
            form.returnDate.validators = [DataRequired()]
        return super(_ReturnMaterialOrderView, self).validate_form(form)

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([
            ('category', AM_CATEGORY),
            ('partNumber', AM_PARTNUMBER),
            ('serialNum', AM_SERIALNUM),
            ('name', AM_NAME),
            ('quantity', AM_QUANTITY),
            ('unit', AM_UNIT),
            ('flightNum', AM_PLANENUM),
        ])
        self.relationField = 'returnMaterials'
        self.f_key = 'application_id'
        self.relationModel = ReturnMaterial

        super(_ReturnMaterialOrderView, self).__init__(*args, **kwargs)

    def init_table_columns(self):
        table_columns = []
        for i in range(len(self.table_columns)):
            column = {}
            column.update({'title': self.table_columns.values()[i]})
            table_columns.append(column)
            table_columns[i]['need'] = False

        table_columns[0]['editor'] = 'select'
        table_columns[0]['selectOptions'] = ['一般航材', '工装设备', '消耗品',
                                             '化工品', '时控件', '时寿件']
        table_columns[0]['need'] = True
        table_columns[1]['editor'] = 'select'
        table_columns[1]['selectOptions'] = []
        table_columns[1]['need'] = True
        table_columns[3]['readOnly'] = True
        table_columns[4]['type'] = 'numeric'
        table_columns[4]['format'] = '0'
        table_columns[4]['need'] = True
        table_columns[5]['readOnly'] = True
        table_columns[6]['editor'] = 'select'
        table_columns[6]['selectOptions'] = self.get_aircraft()

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/return_material_order.js',
        })

        return json.dumps(table_columns)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):

        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': json.dumps([]),
        })
        return super(_ReturnMaterialOrderView, self).create_view()


ReturnMaterialOrderView = partial(
    _ReturnMaterialOrderView, ReturnMaterialOrder, name='退料单'
)
