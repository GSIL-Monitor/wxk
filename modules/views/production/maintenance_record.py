# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from wtforms import SelectField, DateTimeField
from flask_admin import expose
from flask import request, redirect
from flask_admin.helpers import get_redirect_target
from wtforms.validators import DataRequired, NumberRange

from modules.models.production.maintenance_record import MaintenanceRecord
from modules.models.project_tech.engineering_order import EngineeringOrder
from modules.models.user import User
from modules.views import CustomView
from modules.flows import BasicFlow
from ..select_plantype import PlaneTypeSelectableMixin
from util.widgets import DateWidget
from util.fields.select import choiceRealNameSelectField
from util.fields import DateField, ComponentsDropdownsField
from modules.flows.states import Received
from modules.helper import get_allowed_aircrafts
from modules.views.mxp.base import get_allowed_models


def engineer_choices():

    query = EngineeringOrder.query.filter(
        EngineeringOrder.auditStatus == Received,
        EngineeringOrder.maintenanceRecord == None)

    return query


class _MaintenanceRecordView(CustomView):
    """维护保养记录"""
    create_template = 'unvalidate/create.html'
    approve_edit_template = 'unvalidate/approve_edit.html'

    column_list = ['recordNum', 'planeType', 'jihao', 'checkType',
                   'checkPlace', 'involvePerson', 'checkDate', 'checkContent',
                   'statusName']

    column_labels = {
        'recordNum': '编号',
        'planeType': '机型',
        'jihao': '飞机注册号',
        'checkType': '检查类型',
        'checkPlace': '检查地点',
        'effectPart': '受影响部件',
        'effectEngine': '受影响的发动机',
        'stopTime': '工时停场时',
        'involvePerson': '涉及人员',
        'checkDate': '检查日期',
        'checkContent': '检查内容',
        'statusName': '状态',
        'faultReports': '关联的工程指令'
    }

    column_details_list = ['recordNum', 'faultReports', 'planeType', 'jihao',
                           'checkType', 'checkPlace', 'effectPart',
                           'effectEngine', 'stopTime', 'involvePerson',
                           'checkDate', 'checkContent']

    support_flow = partial(BasicFlow, 'Finish flow', support_create=True)
    column_searchable_list = ('recordNum', 'checkType', 'involvePerson',
        'checkPlace', 'jihao',)

    one_line_columns = ['checkContent']

    form_overrides = {
        'checkDate': partial(DateField, widget=DateWidget()),
        'involvePerson': partial(choiceRealNameSelectField),
        'planeType': partial(SelectField, choices=[
            (model.value, model.label) for model in get_allowed_models()]),
        'jihao': partial(ComponentsDropdownsField),
    }

    @property
    def form_widget_args(self):
        return {
            'recordNum': {
                'readonly': True
            },
        }

    def __init__(self, *args, **kwargs):

        self.extra_js = getattr(self, 'extra_js', [])
        self.extra_js.extend([
            '/static/js/bootstrap-datetimepicker.min.js',
            '/static/js/datetimepicker.zh-cn.js',
            '/static/js/select_planeType.js'
        ])

        self.extra_css = getattr(self, 'extra_css', [])
        self.extra_css.extend([
            '/static/css/datepicker.css',
            '/static/css/bootstrap-datetimepicker.min.css',
        ])
        super(_MaintenanceRecordView, self).__init__(*args, **kwargs)

    def create_form(self, obj=None):

        self._create_form_class.faultReports.kwargs['query_factory'] = engineer_choices
        eo_id = request.args.get('id', '')
        if eo_id:
            inst = EngineeringOrder.query.filter(EngineeringOrder.id == eo_id).first()
            return self.create_form_with_default(inst, 'faultReports')

        return super(_MaintenanceRecordView, self).create_form(obj)

    def on_model_change(self, form, model, is_created):
        super(_MaintenanceRecordView, self).on_model_change(form, model, is_created)
        eo_id = request.args.get('id', '')
        if is_created and eo_id:
            model.faultReports_id = eo_id

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.recordNum.validators = [DataRequired()]
            form.checkDate.validators = [DataRequired()]
            form.checkContent.validators = [DataRequired()]

        return super(_MaintenanceRecordView, self).validate_form(form)


MaintenanceRecordView = partial(_MaintenanceRecordView, MaintenanceRecord,
                                name='维护保养记录')
