# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask_admin import expose
from wtforms import SelectField, TextAreaField
from flask import request
from flask_security import current_user
from flask_admin.helpers import get_form_data

from modules.models.production.troubleshooting import TroubleShooting
from modules.models.production.examine_repair_record import ExamineRepairRecord
from modules.models.production.fault_reports import FaultReports
from modules.models.quality.reserved_fault import ReservedFault
from modules.views import CustomView
from modules.flows import BasicFlow
from util.fields import AirworthinessFileuploadField
from ..column_formatter import accessory_formatter
from util.fields import DateField, ComponentsDropdownsField
from util.widgets import DateWidget
from modules.helper import get_allowed_aircrafts
from modules.views.mxp.base import get_allowed_models
from modules.flows.states import Received


def trouble_shooting_choices():

    query = TroubleShooting.query.filter(
        TroubleShooting.auditStatus == Received,
        TroubleShooting.erRecord == None)

    return query


class _ExamineRepairRecordView(CustomView):

    # 排故检修记录列表视图应显示的内容
    column_list = [
        'recordNum', 'faultType', 'planeType', 'jihao', 'maintainDate',
        'faultAdress', 'maintainStaff', 'statusName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'recordNum': '编号',
        'faultType': '故障类型',
        'planeType': '机型',
        'jihao': '飞机注册号',
        'faultDate': '故障发生日期',
        'faultAdress': '故障地点',
        'reportsMaker': '故障报告人',
        'aircraftNumber': '飞行编号',
        'description': '故障描述',
        'maintainStep': '维修措施',
        'maintainDate': '维修日期',
        'maintainStaff': '维修人员',
        'repairFileUrl': '上传附件',
        'checkDate': '检查日期',
        'checkStaff': '检查人员',
        'Soluted': '是否解决故障',
        'remark': '备注',
        'troubleShooting': '关联排故方案编号',
        'statusName': '状态'
    }

    column_searchable_list = ('recordNum', 'faultType', 'jihao', 'faultAdress',
                              'maintainStaff',)

    column_details_list = [
        'recordNum', 'faultType', 'planeType', 'jihao', 'faultDate',
        'faultAdress', 'reportsMaker', 'aircraftNumber', 'maintainDate',
        'maintainStaff', 'checkDate', 'checkStaff', 'Soluted', 'remark',
        'troubleShooting', 'description', 'maintainStep', 'repairFileUrl'
    ]

    form_widget_args = {
        'recordNum': {
            'readonly': True
        },
    }

    form_excluded_columns = ['reservedFault']

    one_line_columns = ['description', 'maintainStep', 'repairFileUrl']

    support_flow = partial(BasicFlow, 'Finish flow', support_create=True)

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/upload_file.js',
        # '/static/js/select_planeType.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/examine_repair_record_validation.js',
    ]

    form_overrides = {
        'repairFileUrl': partial(AirworthinessFileuploadField),
        'faultDate': partial(DateField, widget=DateWidget()),
        'maintainDate': partial(DateField, widget=DateWidget()),
        'checkDate': partial(DateField, widget=DateWidget()),
        'description': partial(TextAreaField,
                               render_kw={'rows': 3, 'style': 'resize:none;'}),
        'maintainStep': partial(TextAreaField,
                                render_kw={'rows': 3, 'style': 'resize:none;'}),
        'planeType': partial(SelectField, choices=[
            (model.value, model.label) for model in get_allowed_models()]),
        'jihao': partial(ComponentsDropdownsField),
    }

    column_formatters = {
        'repairFileUrl': accessory_formatter('repairFileUrl'),
    }

    def on_model_change(self, form, model, is_created):
        super(_ExamineRepairRecordView, self).on_model_change(form, model, is_created)
        rf_id = request.args.get('id', '')
        view_url = request.args.get('view', '')
        if view_url and 'reservedfault' in view_url and is_created and rf_id:
            model.reservedFault_id = rf_id

    def __init__(self, *args, **kwargs):

        self.extra_js = getattr(self, 'extra_js', [])
        self.extra_css = getattr(self, 'extra_css', [])

        self.column_formatters.update({
            'faultDate': self.date_formatter_date,
            'maintainDate': self.date_formatter_date,
            'checkDate': self.date_formatter_date,
        })

        super(_ExamineRepairRecordView, self).__init__(*args, **kwargs)

    def create_form(self, obj=None):

        self._create_form_class.troubleShooting.kwargs['query_factory'] = trouble_shooting_choices

        ts_id = request.args.get('id', '')
        view_url = request.args.get('view', '')
        if ts_id:
            if view_url and 'troubleshooting' in view_url:
                ts = TroubleShooting.query.filter(TroubleShooting.id == ts_id).first()
                inst = FaultReports.query.join(
                    TroubleShooting,
                    TroubleShooting.faultReports_id == FaultReports.id
                ).filter(TroubleShooting.id == ts_id)
                tmp_form_class = self.get_create_form()
                datas = []
                for key, value in inst[0].__dict__.iteritems():
                    if key not in self.review_details_columns or\
                            key == 'recordNum':
                        continue
                    datas.append(key)
                    tmp = getattr(tmp_form_class, key)
                    tmp.kwargs['default'] = value

                tmp_form_class.troubleShooting.kwargs['default'] = ts
                tmp_form_class.faultType.kwargs['default'] = '严重故障'
                return tmp_form_class(get_form_data(), obj)

            if view_url and 'reservedfault' in view_url:
                rf = ReservedFault.query.filter(ReservedFault.id == ts_id).first()
                return self.create_form_with_default(rf)

        return super(_ExamineRepairRecordView, self).create_form(obj)


ExamineRepairRecordView = partial(
    _ExamineRepairRecordView, ExamineRepairRecord, name='排故检修记录'
)
