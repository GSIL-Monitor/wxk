# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from flask import request, jsonify
from wtforms.validators import DataRequired
from flask_admin import expose
from wtforms import DateField
from modules.flows import AssembleApplicationFlow
from util.widgets import DateWidget
from collections import OrderedDict
from modules.models.airmaterial.assemble_application import (
    AssembleApplication, AssembleApplicationList)
from modules.models.airmaterial import AirMaterialStorageList
from .out_storage_application_update_freezed_quantity import\
    UpdateStorageListFreezedQuantity
from airmaterial_fileds import *


class _AssembleApplicationView(UpdateStorageListFreezedQuantity):

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
        '/static/js/assemble_app_validation.js',
    ]
    """装机申请单"""
    column_list = [
        'number', 'date', 'applyPerson', 'applyDate', 'statusName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'date': '单据日期',
        'applyDate': '申请日期',
        'applyPerson': '申请人',
        'remark': '备注',
        'statusName': '状态',
        'putOutStore': '出库',
        'assemble': '装机'

    }

    column_searchable_list = ('applyPerson', 'number', 'statusName')
    # 查看页面显示的详情
    column_details_list = [
        'number', 'date', 'applyPerson', 'applyDate'
    ]

    form_excluded_columns = [
        'statusName', 'assembleApplicationList', 'putOutStore', 'assemble'
    ]
    support_flow = partial(AssembleApplicationFlow, 'purchase request flow')

    form_overrides = {
        'date': partial(DateField, widget=DateWidget()),
        'applyDate': partial(DateField, widget=DateWidget())
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
            form.applyDate.validators = [DataRequired()]
        return super(_AssembleApplicationView, self).validate_form(form)

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([
            ('category', AM_CATEGORY),
            ('partNumber', AM_PARTNUMBER),
            ('serialNum', AM_SERIALNUM),
            ('name', AM_NAME),
            ('quantity', AM_QUANTITY),
            ('manufacturer', AM_MANUFACTURER),
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
        self.f_key = 'assembleapplication_id'
        self.relationModel = AssembleApplicationList

        super(_AssembleApplicationView, self).__init__(*args, **kwargs)

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
        table_columns[2]['editor'] = 'select'
        table_columns[3]['selectOptions'] = []
        table_columns[3]['readOnly'] = True
        table_columns[3]['need'] = True
        table_columns[4]['type'] = 'numeric'
        table_columns[4]['format'] = '0'
        table_columns[4]['need'] = True
        table_columns[5]['editor'] = 'select'
        table_columns[5]['selectOptions'] = self.get_manafacturers()
        table_columns[7]['editor'] = 'select'
        table_columns[7]['selectOptions'] = self.get_aircraft()
        table_columns[7]['need'] = True
        table_columns[8]['editor'] = 'select'
        table_columns[8]['selectOptions'] = []
        table_columns[8]['checkNeed'] = True
        table_columns[9]['type'] = 'date'
        table_columns[9]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[10]['editor'] = 'select'
        table_columns[10]['selectOptions'] = []
        table_columns[10]['checkNeed'] = True
        table_columns[11]['validator'] = 'hhmm'
        table_columns[12]['validator'] = 'hhmm'
        table_columns[13]['type'] = 'numeric'
        table_columns[13]['format'] = '0'

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/assemble_application.js'
        })

        return json.dumps(table_columns)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        rowid = request.args.getlist('rowid')
        if rowid:
            materials = AirMaterialStorageList.query.filter(
                AirMaterialStorageList.id.in_(rowid)).all()
            table_datas = []
            table_datas = [[
                material.category, material.partNumber,
                material.serialNum, material.name,
                material.quantity - material.freezingQuantity,
                material.manufacturer,
                material.unit, None, material.effectiveDate,
                material.lastCheckDate,
                material.nextCheckDate, material.flyTime,
                material.engineTime, material.flightTimes,
            ] for material in materials]
            table_datas = json.dumps(table_datas)
        else:
            table_datas = json.dumps([])

        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })
        return super(_AssembleApplicationView, self).create_view()

    @expose('/get_pn_from_asap_ca/', methods=['GET'])
    def get_pn_from_asap_ca(self):
        try:
            ca = request.args.get('ca')
            num = request.args.get('num')
            if ca and num:
                inst = AssembleApplication.query.filter_by(number=num).first()
                materials = inst.assembleApplicationList
                data = [m.partNumber for m in materials if m.category == ca]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/get_number_from_asap_pn/', methods=['GET'])
    def get_number_from_asap_pn(self):
        try:
            pn = request.args.get('pn')
            num = request.args.get('num')
            if pn and num:
                inst = AssembleApplication.query.filter_by(number=num).first()
                materials = inst.assembleApplicationList
                data = [m.quantity for m in materials if m.partNumber == pn]
                data = json.dumps(data[0])
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')


AssembleApplicationView = partial(
    _AssembleApplicationView, AssembleApplication, name='装机申请'
)
