# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask_admin import expose
from flask import request
from flask_security import current_user
from wtforms.validators import DataRequired
from wtforms import TextAreaField
from wtforms import SelectField

from modules.models.production.troubleshooting import TroubleShooting
from modules.models.production.examine_repair_record import ExamineRepairRecord
from modules.models.production.fault_reports import FaultReports
from modules.views import CustomView
from modules.flows import TroubleShootingFlow
from util.fields import AirworthinessFileuploadField
from ..column_formatter import accessory_formatter
from util.fields import DateInt
from util.widgets import DateIntWidget
from util.fields import DateField, ComponentsDropdownsField
from modules.helper import get_allowed_aircrafts
from modules.views.mxp.base import get_allowed_models


class _TroubleShootingView(CustomView):
    """排故方案"""
    list_template = 'trouble_shooting/list.html'
    create_template = 'trouble_shooting/create.html'
    approve_edit_template = 'trouble_shooting/approve_edit.html'

    # 排故方案列表视图应显示的内容
    column_list = [
        'shootingNum', 'planeType', 'jihao', 'formulateDate',
        'formulatePerson', 'enforceStaff', 'statusName'
    ]

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/select_planeType.js',
        '/static/js/trouble_shooting.js',
        '/static/js/upload_file.js',
        '/static/js/jquery.validate.min.js',
    ]

    # 对应内容的中文翻译
    column_labels = {
        'shootingNum': '编号',
        'planeType': '机型',
        'jihao': '飞机注册号',
        'formulateDate': '制定日期',
        'formulatePerson': '制定人',
        'shootingFileUrl': '上传附件',
        'description': '故障及方案描述',
        'maintainStep': '维修措施',
        'enforceDate': '执行日期',
        'enforceStaff': '执行人员',
        'remark': '备注',
        'faultReports': '关联故障报告单号',
        'statusName': '状态',
        'erRecord': '关联的排故检修记录'
    }

    column_details_list = [
        'shootingNum', 'planeType', 'jihao', 'formulateDate',
        'formulatePerson', 'enforceDate', 'enforceStaff', 'remark',
        'faultReports', 'description', 'maintainStep', 'shootingFileUrl'
    ]
    form_widget_args = {
        'shootingNum': {
            'readonly': True
        },
    }

    support_flow = partial(TroubleShootingFlow, 'Finish flow', next_model=ExamineRepairRecord)

    form_excluded_columns = ['erRecord']
    column_searchable_list = ('shootingNum', 'jihao', 'formulatePerson',
                              'enforceStaff',)
    one_line_columns = ['description', 'maintainStep', 'shootingFileUrl']
    form_overrides = {
        'shootingFileUrl': partial(AirworthinessFileuploadField),
        'formulateDate': partial(DateInt, widget=DateIntWidget()),
        'enforceDate': partial(DateInt, widget=DateIntWidget()),
        'description': partial(TextAreaField,
                               render_kw={'rows': 3, 'style': 'resize:none;'}),
        'maintainStep': partial(TextAreaField,
                                render_kw={'rows': 3, 'style': 'resize:none;'}),
        'planeType': partial(SelectField, choices=[
            (model.value, model.label) for model in get_allowed_models()]),
        'jihao': partial(ComponentsDropdownsField),
    }

    column_formatters = {
        'shootingFileUrl': accessory_formatter('shootingFileUrl'),
    }

    def __init__(self, *args, **kwargs):

        self.extra_js = getattr(self, 'extra_js', [])
        self.extra_css = getattr(self, 'extra_css', [])

        self.column_formatters.update({
            'formulateDate': self.date_formatter_date,
            'enforceDate': self.date_formatter_date,
        })

        super(_TroubleShootingView, self).__init__(*args, **kwargs)

    def create_form(self, obj=None):
        if not request.form:
            self._create_form_class.formulatePerson.kwargs[
                'default'] = current_user.realName

        fr_id = request.args.get('id', '')
        if fr_id:
            inst = FaultReports.query.filter(FaultReports.id == fr_id).first()
            return self.create_form_with_default(inst, 'faultReports')

        return super(_TroubleShootingView, self).create_form(obj)

    @expose('/approve-edit-view/', methods=['GET', 'POST'])
    def approve_edit_view(self):

        return super(_TroubleShootingView, self).approve_edit_view()

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.faultReports.validators = [DataRequired()]
        return super(_TroubleShootingView, self).validate_form(form)

    def get_query(self):
        datas = super(_TroubleShootingView, self).get_query()
        return self.get_recieved_query(datas, 'troubleshooting')


TroubleShootingView = partial(
    _TroubleShootingView, TroubleShooting, name='排故方案'
)
