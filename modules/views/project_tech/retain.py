# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask_admin import expose
from flask import request, redirect
from flask_admin.helpers import get_redirect_target
import time

from modules.models.project_tech.retain import Retain
from wtforms.validators import NumberRange, DataRequired
from modules.views import CustomView
from modules.flows import RetainFlow
from ..select_plantype import PlaneTypeSelectableMixin
from modules.models.production.troubleshooting import TroubleShooting
from util.fields import DateInt
from util.widgets import DateIntWidget
from modules.flows.operations import CreateRW


class _RetainView(CustomView, PlaneTypeSelectableMixin):
    # 保留工作列表视图应显示的内容
    create_template = 'unvalidate/create.html'
    approve_edit_template = 'unvalidate/approve_edit.html'

    column_list = [
        'retainNum', 'planeType', 'flihtTime', 'statusName'
    ]

    extra_js = [
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/switch_form.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/select_planeType.js',
        '/static/js/retain.js'
    ]

    # 对应内容的中文翻译
    column_labels = {
        'retainNum': '编号',
        'planeType': '机型',
        'flihtTime': '飞行小时',
        'jihao': '飞机注册号',
        'engineNum': '发动机序号',
        'reseason': '申请保留原因',
        'limit': '申请保留期限',
        'proposer': '申请人',
        'date': '申请日期',
        'licenceNO': '执照号',
        'content': '保留工作内容',
        'other': '其他',
        'statusName': '状态',
        'routineWorks': '例行工作',
    }

    column_details_list = [
        'retainNum', 'planeType', 'flihtTime', 'jihao', 'engineNum',
        'limit', 'proposer', 'date', 'licenceNO',
        'other', 'reseason', 'content'
    ]

    form_widget_args = {
        'retainNum': {
            'readonly': True
        },
    }

    support_flow = partial(RetainFlow, 'retain flow', create_action=CreateRW)

    form_excluded_columns = ['routineWorks']

    column_searchable_list = ('retainNum',)

    one_line_columns = ['reseason', 'content']

    form_overrides = {
        'date': partial(DateInt, widget=DateIntWidget()),
        'limit': partial(DateInt, widget=DateIntWidget()),
    }

    def __init__(self, *args, **kwargs):

        self.extra_js = getattr(self, 'extra_js', [])
        self.extra_css = getattr(self, 'extra_css', [])

        self.column_formatters = self.column_formatters or {}
        self.column_formatters.update({
            'date': self.date_formatter_date,
            'limit': self.date_formatter_date,
        })

        super(_RetainView, self).__init__(*args, **kwargs)

    def create_form(self, obj=None):
        self.select_override('_create_form_class')
        for field in ['limit', 'date']:
            set_field = getattr(self._create_form_class, field)
            set_field.kwargs.update({'default': time.time()})

        return super(_RetainView, self).create_form(obj)

    @expose('/approve-edit-view/', methods=['GET', 'POST'])
    def approve_edit_view(self):
        self.select_override('_edit_form_class')
        return super(_RetainView, self).approve_edit_view()

    @expose('/create_st_action')
    def create_st_action(self):

        # 动作指示可能来源于请求的url
        id = request.args.get('id', '')
        action = request.args.get('action', '')

        self._custom_action(id, request.form, action)

        inst = self.model.query.filter(self.model.id == id).first()
        st_id = inst.troubleShootings[-1].id

        return_url = get_redirect_target() or self.get_url('.index_view')

        return redirect(self.get_url('troubleshootings.approve_edit_view',
                                     id=st_id,
                                     return_url=return_url))

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            if form.flihtTime.data:
                form.flihtTime.validators = [NumberRange(
                    min=0, message='请输入合理的数值')]
            form.limit.validators = [DataRequired(),
                                     NumberRange(min=form.date.data,
                                     message="申请保留期限应晚于申请日期")]
        return super(_RetainView, self).validate_form(form)


RetainView = partial(_RetainView, Retain, name='保留工作')
