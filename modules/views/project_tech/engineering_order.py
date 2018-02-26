# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask import url_for, redirect, request, flash
from wtforms.validators import DataRequired, NumberRange
from wtforms import HiddenField
from flask_admin.babel import gettext
from flask_admin.form import BaseForm, FormOpts, rules
from flask_admin.helpers import (get_form_data, validate_form_on_submit,
                                 get_redirect_target, flash_errors)
from flask_security import current_user
from sqlalchemy import or_
from sqlalchemy_continuum import version_class
from wtforms import SelectField

from flask_admin import expose
from modules.models.project_tech.airworthiness import Airworthiness
from modules.models.project_tech.engineering_order import EngineeringOrder
from modules.views import CustomView
from modules.flows import EOFlow
from ..column_formatter import accessory_formatter
from modules.views.select_plantype import PlaneTypeSelectableMixin
from util.fields import (EngineeringOrderFileuploadField,
                         InputSelectMixinField,
                         DateField, ComponentsDropdownsField)
from util.widgets import DateWidget
from modules.models.role import Role, BasicAction
from modules.views.mxp.base import get_allowed_models


class _EngineeringOrderView(CustomView):
    extra_js = [
        '/static/js/upload_file.js',
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/switch_form.js',
        '/static/js/select_planeType.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/engineeringorder_validation.js',
    ]

    # 工程指令列表视图应显示的内容
    column_list = [
        'insNum', 'insTitle', 'insCategory', 'statusName',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'insNum': '指令号',
        'insTitle': '标题',
        'insCategory': '指令类别',
        'relateFileUrl': '相关文档',
        'planeType': '机型',
        'jihao': '飞机注册号',
        'effectPart': '受影响部件',
        'effectEngine': '受影响的发动机',
        'grantTime': '发放期限',
        'finishTime': '完成期限',
        'executeTime': '执行日期',
        'isClaim': '能否索赔',
        'stopHours': '工时停场时',
        'repeatePeriod': '重复周期',
        'ataCode': 'ATA章节号',
        'usability': '适用性',
        'manualChange': '手册更改',
        'isFeedback': '是否反馈',
        'reason': '概述/理由',
        'remark': '备注/说明',
        'statusName': '状态',
        'maintenanceRecord': '关联的维护保养记录',
        'airworthiness': '关联的适航文件编号'
    }

    # 待复核的内容要少
    column_details_list = [
        'insNum', 'insTitle', 'insCategory', 'planeType',
        'jihao', 'effectPart', 'effectEngine', 'grantTime', 'finishTime',
        'executeTime', 'isClaim', 'stopHours', 'repeatePeriod', 'ataCode',
        'usability', 'manualChange', 'isFeedback', 'remark',
        'maintenanceRecord', 'airworthiness', 'reason', 'relateFileUrl'
    ]

    support_flow = partial(EOFlow, 'Default basic approval flow')

    form_excluded_columns = ['troubleshooting',
                             'maintenanceRecord']

    column_formatters = {
        'relateFileUrl': accessory_formatter('relateFileUrl'),
    }

    one_line_columns = ['reason', 'relateFileUrl']

    column_searchable_list = ('insNum', 'insTitle', 'insCategory',)

    form_overrides = {
        'relateFileUrl': partial(EngineeringOrderFileuploadField),
        'repeatePeriod': partial(InputSelectMixinField),
        'grantTime': partial(DateField, widget=DateWidget()),
        'finishTime': partial(DateField, widget=DateWidget()),
        'executeTime': partial(DateField, widget=DateWidget()),
        'planeType': partial(SelectField, choices=[
            (model.value, model.label) for model in get_allowed_models()]),
        'jihao': partial(ComponentsDropdownsField),
    }

    def create_form(self, obj=None):

        ao_id = request.args.get('id', '')

        if ao_id:
            inst = Airworthiness.query.filter(Airworthiness.id == ao_id).first()
            return self.create_form_with_default(inst, 'airworthiness')

        return super(_EngineeringOrderView, self).create_form(obj)

    def on_model_change(self, form, model, is_created):
        super(_EngineeringOrderView, self).on_model_change(form, model, is_created)
        ao_id = request.args.get('id', '')
        if is_created and ao_id:
            model.airworthiness_id = ao_id

    @property
    def form_widget_args(self):
        return {
            'insNum': {
                'readonly': True
            },
        }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.repeatePeriod.validators = [DataRequired('请输入正数')]
            form.insNum.validators = [DataRequired()]

        return super(_EngineeringOrderView, self).validate_form(form)

    def get_query(self):
        datas = super(_EngineeringOrderView, self).get_query()
        return self.get_recieved_query(datas, 'engineeringorder')


EngineeringOrderView = partial(
    _EngineeringOrderView, EngineeringOrder, name='工程指令'
)
