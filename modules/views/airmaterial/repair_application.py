# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import json

from flask_admin import expose
from wtforms import DateField
from ..column_formatter import accessory_formatter
from modules.flows import RepairApplicationFlow
from flask import request, jsonify
from wtforms.validators import DataRequired
from util.widgets import DateWidget
from collections import OrderedDict
from modules.models.airmaterial import RepairApplication, RepairMaterial
from modules.models.airmaterial.storage_list import AirMaterialStorageList
from util.fields.accessory_filed import AirmaterialFileuploadField
from util.fields.select import RefreshRepairSupplierSelectField
from .out_storage_application_update_freezed_quantity import\
    UpdateStorageListFreezedQuantity
from airmaterial_fileds import *
from modules.views.approve_flow_with_uploadfile import ApproveFlowUploadFileView


class _RepairApplicationView(ApproveFlowUploadFileView,
                             UpdateStorageListFreezedQuantity):
    """送修申请视图"""
    column_list = [
        'number', 'applicationDate', 'repairCompany',
        'statusName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'applicationDate': '申请日期',
        'repairCompany': '维修厂商',
        'contactPerson': '联系人',
        'telephone': '联系电话',
        'fax': '传真',
        'mailbox': '邮箱',
        'budget': '预算',
        'accessory': '附件',
        'remark': '备注',
        'statusName': '状态',
        'contractFile': '合同文件',
    }

    column_searchable_list = ('repairCompany', 'number', 'statusName')
    # 查看页面显示的详情
    column_details_list = [
        'number', 'applicationDate', 'repairCompany',
        'contactPerson', 'telephone', 'fax', 'mailbox',
        'budget', 'remark', 'contractFile', 'accessory',
    ]

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
        '/static/js/repair_validation.js',
        '/static/js/upload_file.js',
    ]

    form_excluded_columns = [
        'statusName', 'repairAppl', 'contractFile', 'repairReturnOrder',
        'putOutStore'
    ]
    support_flow = partial(RepairApplicationFlow, 'repair application flow')

    one_line_columns = ['accessory']

    column_formatters = {
        'contractFile': accessory_formatter('contractFile'),
        'accessory': accessory_formatter('accessory'),
    }
    form_overrides = {
        'accessory': partial(AirmaterialFileuploadField),
        'contractFile': partial(AirmaterialFileuploadField),
        'applicationDate': partial(DateField, widget=DateWidget()),
        'repairCompany': partial(RefreshRepairSupplierSelectField),
    }

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

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.applicationDate.validators = [DataRequired()]
        return super(_RepairApplicationView, self).validate_form(form)

    def __init__(self, *args, **kwargs):

        self.table_columns = OrderedDict([
            ('category', AM_CATEGORY),
            ('partNumber', AM_PARTNUMBER),
            ('serialNum', AM_SERIALNUM),
            ('name', AM_NAME),
            ('quantity', AM_QUANTITY),
            ('manufacturer', AM_MANUFACTURER),
            ('effectiveDate', AM_EFFECTIVEDATE),
            ('lastCheckDate', AM_LASTCHECKDATE),
            ('nextCheckDate', AM_NEXTCHECKDATE),
            ('planeNum', AM_DISPLANENUM),
            ('planeType', AM_PLANETYPE),
            ('assembleDate', AM_ASSEMBLEDATE),
            ('disassembleDate', AM_DISASSEMBLEDATE),
            ('repairedReuseDate', AM_REPAIREDREUSEDATE),
            ('totalUseTime', AM_TOTALUSETIME),
            ('flyTime', AM_FLYTIME),
            ('engineTime', AM_ENGINETIME),
            ('flightTimes', AM_FLIGHTTIMES)
        ])
        self.relationField = 'repairAppl'
        self.f_key = 'application_id'
        self.relationModel = RepairMaterial

        super(_RepairApplicationView, self).__init__(*args, **kwargs)

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
        table_columns[2]['editor'] = 'select'
        table_columns[2]['selectOptions'] = []
        table_columns[3]['readOnly'] = True
        table_columns[3]['need'] = True
        table_columns[4]['need'] = True
        table_columns[4]['type'] = 'numeric'
        table_columns[5]['editor'] = 'select'
        table_columns[5]['selectOptions'] = self.get_manafacturers()
        table_columns[6]['editor'] = 'select'
        table_columns[6]['selectOptions'] = []
        table_columns[6]['checkNeed'] = True
        table_columns[7]['type'] = 'date'
        table_columns[7]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[8]['editor'] = 'select'
        table_columns[8]['selectOptions'] = []
        table_columns[8]['checkNeed'] = True
        table_columns[9]['editor'] = 'select'
        table_columns[9]['selectOptions'] = self.get_aircraft()
        table_columns[10]['editor'] = 'select'
        table_columns[10]['selectOptions'] = [self.plane_type]
        table_columns[11]['type'] = 'date'
        table_columns[11]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[12]['type'] = 'date'
        table_columns[12]['dateFormat'] = 'YYYY-MM-DD'
        table_columns[15]['validator'] = 'hhmm'
        table_columns[16]['validator'] = 'hhmm'
        table_columns[17]['type'] = 'numeric'
        table_columns[17]['format'] = '0'

        self._template_args.update({
            'inline_table': True,
            'can_add_line': True,
            'can_del_line': True,
            'extra_table_js': 'js/repair_application.js'
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
                cat.quantity - cat.freezingQuantity, cat.manufacturer,
                cat.effectiveDate, cat.lastCheckDate, cat.nextCheckDate,
                None, self.plane_type, None, None,
                None, None, cat.flyTime, cat.engineTime, cat.flightTimes
            ] for cat in cats]

            table_datas = json.dumps(table_datas)
        else:
            table_datas = json.dumps([])

        self._template_args.update({
            'table_columns': self.init_table_columns(),
            'table_datas': table_datas,
        })
        return super(_RepairApplicationView, self).create_view()

    @expose('/approve-edit-view/', methods=['POST', 'GET'])
    def approve_edit_view(self):
        self._template_args.update({
            'table_columns': self.init_table_columns(),
        })
        return super(_RepairApplicationView, self).approve_edit_view()

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

        return super(_RepairApplicationView, self).details_view()

    @expose('/getTime/', methods=['GET'])
    def getTime(self):
        try:
            ca = request.args.get('ca')
            if ca:
                items = RepairMaterial.query.filter(RepairMaterial.partNumber == ca).all()
                data = [item.serialNum for item in items]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')

        return jsonify(code=404, message='Not Found')

    @expose('/get_pn_from_repair_ca/', methods=['GET'])
    def get_pn_from_repair_ca(self):
        try:
            ca = request.args.get('ca')
            num = request.args.get('num')
            if ca and num:
                inst = RepairApplication.query.filter_by(number=num).first()
                materials = inst.repairAppl
                data = [m.partNumber for m in materials if m.category == ca]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=404, message='Not Found')

    @expose('/get_sn_from_repair_pn/', methods=['GET'])
    def get_sn_from_repair_pn(self):
        try:
            pn = request.args.get('pn')
            num = request.args.get('num')
            if pn and num:
                inst = RepairApplication.query.filter_by(number=num).first()
                materials = inst.repairAppl
                data = [m.serialNum for m in materials if m.partNumber == pn]
                data = json.dumps(data)
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=404, message='Not Found')

    @expose('/get_from_repair_pn/', methods=['GET'])
    def get_from_repair_pn(self):
        try:
            pn = request.args.get('pn')
            num = request.args.get('num')
            if pn and num:
                inst = RepairApplication.query.filter_by(number=num).first()
                materials = inst.repairAppl
                materials = [m for m in materials if m.partNumber == pn]
                data = [[m.category, m.partNumber, m.serialNum, m.name,
                        m.manufacturer, m.quantity, m.flyTime,
                        m.engineTime, m.flightTimes] for m in materials]
                data = json.dumps(data[0])
                return jsonify(code=200, data=data, message='Ok')
        except Exception:
            return jsonify(code=400, message='Bad Argument')
        return jsonify(code=404, message='Not Found')


RepairApplicationView = partial(
    _RepairApplicationView, RepairApplication, name='送修申请'
)
