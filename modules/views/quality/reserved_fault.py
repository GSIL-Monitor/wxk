# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask_admin import expose
from wtforms.fields import SelectField, DateTimeField
from wtforms.validators import DataRequired, NumberRange
import time
from wtforms import SelectField

from modules.models.quality.reserved_fault import ReservedFault
from modules.views import CustomView
from modules.flows.retain_flow import RetainFlow
from util.widgets import DateTimeWidget
from util.fields import DateInt, ComponentsDropdownsField
from util.widgets import DateIntWidget
from modules.flows.operations import createER
from modules.helper import get_allowed_aircrafts
from modules.views.mxp.base import get_allowed_models


class _ReservedFaultView(CustomView):
    # 保留故障列表视图应显示的内容
    create_template = 'unvalidate/create.html'
    approve_edit_template = 'unvalidate/approve_edit.html'

    column_list = ['reservedNum', 'planeType', 'jihao',
                   'engineNum', 'statusName']

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/select_planeType.js',
        '/static/js/reserved_fault.js'
    ]

    # 对应内容的中文翻译
    column_labels = {
        'reservedNum': '编号',
        'planeType': '机型',
        'flyhours': '飞行小时数',
        'jihao': '注册号',
        'engineNum': '发动机序号',
        'description': '保留故障描述',
        'expectAlter': '预期更改方法',
        'measure': '采取措施',
        'reason': '申请保留原因',
        'limit': '申请保留期限',
        'proposer': '申请人',
        'date': '申请日期',
        'licenceNO': '执照号',
        'remarks': '备注',
        'createTime': '制单时间',
        'updateTime': '修改时间',
        'statusName': '状态',
    }

    column_details_list = [
        'reservedNum', 'planeType', 'flyhours', 'jihao', 'engineNum',
        'measure', 'limit', 'proposer', 'date', 'licenceNO', 'remarks',
        'description', 'expectAlter', 'reason',
    ]

    use_inheritance_operation = True

    support_flow = partial(RetainFlow, 'one approval flow', create_action=createER)

    form_excluded_columns = ['action', 'erRecord']
    column_searchable_list = ('reservedNum',)

    one_line_columns = ['description', 'expectAlter', 'reason']

    form_overrides = {
        'measure': partial(SelectField, choices=[
            ('按备注栏的要求', '按备注栏的要求'),
            ('挂禁止操作指示牌', '挂禁止操作指示牌'),
            ('其他', '其他'),
        ]),
        'date': partial(DateInt, widget=DateIntWidget()),
        'limit': partial(DateInt, widget=DateIntWidget()),
        'planeType': partial(SelectField, choices=[
            (model.value, model.label) for model in get_allowed_models()]),
        'jihao': partial(ComponentsDropdownsField),
    }

    @property
    def form_widget_args(self):
        return {
            'reservedNum': {
                'readonly': True
            },
            'relateNum': {
                'readonly': True
            },
        }

    def __init__(self, *args, **kwargs):

        self.extra_js = getattr(self, 'extra_js', [])
        self.extra_css = getattr(self, 'extra_css', [])
        self.column_formatters.update({
            'date': self.date_formatter_date,
            'limit': self.date_formatter_date,
        })
        super(_ReservedFaultView, self).__init__(*args, **kwargs)

    @expose('/new/', methods=['GET', 'POST'])
    def create_view(self):
        for field in ['limit', 'date']:
            set_field = getattr(self._create_form_class, field)
            set_field.kwargs.update({'default': time.time()})
        return super(_ReservedFaultView, self).create_view()

    @expose('/approve-edit-view/', methods=['GET', 'POST'])
    def approve_edit_view(self):

        return super(_ReservedFaultView, self).approve_edit_view()

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.description.validators = [DataRequired()]
            form.reason.validators = [DataRequired()]
            form.date.validators = [DataRequired()]
            if form.flyhours.data:
                form.flyhours.validators = [NumberRange(
                    min=0, message='请输入合理的数值')]
            form.limit.validators = [DataRequired(),
                                     NumberRange(min=form.date.data,
                                     message="申请保留期限应晚于申请日期")]
        return super(_ReservedFaultView, self).validate_form(form)


ReservedFaultView = partial(
    _ReservedFaultView, ReservedFault, name='保留故障'
)
