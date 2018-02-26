# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask_admin import expose
from flask import request, redirect
from flask_admin.helpers import get_redirect_target
from wtforms import SelectField

from modules.models.production.fault_reports import FaultReports
from modules.views import CustomView
from modules.flows import FaultReportsFlow
from modules.models.production.troubleshooting import TroubleShooting
from util.fields import AirworthinessFileuploadField
from ..column_formatter import accessory_formatter
from util.fields import DateField
from util.widgets import DateWidget
from util.fields import DateField, ComponentsDropdownsField
from modules.helper import get_allowed_aircrafts
from modules.views.mxp.base import get_allowed_models


class _FaultReportsView(CustomView):

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/select_planeType.js',
        '/static/js/fault_report.js',
        '/static/js/upload_file.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/faultreports_validation.js',
    ]

    column_list = [
        'recordNum', 'planeType', 'jihao', 'faultDate',
        'faultAdress', 'reportsMaker', 'aircraftNumber',
        'statusName'
    ]

    column_labels = {
        'recordNum': '编号',
        'planeType': '机型',
        'jihao': '飞机注册号',
        'faultDate': '故障发生日期',
        'faultAdress': '故障地点',
        'reportsMaker': '故障报告人',
        'aircraftNumber': '飞行编号',
        'description': '故障描述',
        'relateFileUrl': '上传附件',
        'remark': '备注',
        'statusName': '状态',
    }

    column_details_list = ['recordNum', 'planeType', 'jihao', 'faultDate',
                           'faultAdress', 'reportsMaker', 'aircraftNumber', 'remark',
                           'description', 'relateFileUrl']

    support_flow = partial(
        FaultReportsFlow, 'fault report flow', next_model=TroubleShooting)

    form_overrides = {
        'faultDate': partial(DateField, widget=DateWidget()),
        'relateFileUrl': partial(AirworthinessFileuploadField),
        'planeType': partial(SelectField, choices=[
            (model.value, model.label) for model in get_allowed_models()]),
        'jihao': partial(ComponentsDropdownsField),
    }
    column_searchable_list = ('recordNum', 'faultAdress', 'reportsMaker',
                              'aircraftNumber', 'jihao',)
    form_excluded_columns = ['troubleShootings']

    one_line_columns = ['description', 'relateFileUrl']

    column_formatters = {
        'relateFileUrl': accessory_formatter('relateFileUrl'),
    }

    form_widget_args = {
        'recordNum': {
            'readonly': True
        },
    }

    @expose('/approve-edit-view/', methods=['GET', 'POST'])
    def approve_edit_view(self):

        return super(_FaultReportsView, self).approve_edit_view()


FaultReportsView = partial(
    _FaultReportsView, FaultReports, name='故障报告')
