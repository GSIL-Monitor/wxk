# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from flask_security import current_user
from flask import url_for, redirect, request
from flask_admin import expose
from flask_admin.helpers import get_redirect_target
from wtforms.validators import NumberRange, DataRequired
from sqlalchemy import or_

from wtforms import SelectField, TextAreaField

from modules.models.project_tech.airworthiness import Airworthiness
from modules.models.project_tech.engineering_order import EngineeringOrder
from modules.views import CustomView
from modules.flows import ADFlow
from util.fields import AirworthinessFileuploadField, DateField, ComponentsDropdownsField
from ..column_formatter import accessory_formatter
from modules.views.select_plantype import PlaneTypeSelectableMixin
from util.widgets import DateWidget
from modules.models.role import Role, BasicAction
from modules.helper import get_allowed_aircrafts
from modules.views.mxp.base import get_allowed_models


class _AirworthinessView(CustomView):

    # 适航文件列表视图应显示的内容

    extra_js = [
        '/static/js/upload_file.js',
        '/static/js/bootbox.min.js',
        '/static/js/custom_action.js',
        '/static/js/bootstrap-switch.min.js',
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/switch_form.js',
        '/static/js/jquery.validate.min.js',
        '/static/js/select_planeType.js',
        '/static/js/customview_formvalidation.js',
        '/static/js/airworthiness_validation.js',
    ]

    column_list = [
        'continusNum', 'cname', 'concategory', 'isExec', 'statusName',
    ]

    # 对应内容的中文翻译
    column_labels = {
        'continusNum': '编号',
        'cname': '名称',
        'isExec': '是否限期执行',
        'execTime': '执行期限',
        'statusName': '状态',
        'yujing': '预警',
        'concategory': '类别',
        'relateFileUrl': '相关文件',
        'planeType': '机型',
        'jihao': '飞机注册号',
        'effectPart': '受影响部件',
        'effectEngine': '受影响的发动机',
        'publishTime': '颁布日期',
        'execTime': '生效日期',
        'execCost': '执行费用',
        'isExec': '执行能力',
        'stopTime': '停场时间',
        'needTime': '所需工时',
        'fromWhere': '出处',
        'usability': '适用性',
        'isClaim': '能否索赔',
        'engineerSuggestion': '工程师意见',
        'conabstract': '原文摘要',
        'remark': '备注',
    }

    # 待复核的内容要少
    column_details_list = [
        'continusNum', 'cname', 'planeType', 'jihao', 'execTime',
        'publishTime', 'effectPart', 'effectEngine', 'concategory',
        'fromWhere', 'execCost', 'isClaim', 'isExec',
        'stopTime', 'needTime', 'engineerSuggestion', 'remark',
        'usability', 'conabstract', 'relateFileUrl'

    ]

    form_overrides = {
        'relateFileUrl': partial(AirworthinessFileuploadField),
        'publishTime': partial(DateField, widget=DateWidget()),
        'execTime': partial(DateField, widget=DateWidget()),
        'conabstract': partial(TextAreaField, render_kw={'rows': 3,
                                          'style': 'resize:none;'}),
        'planeType': partial(SelectField, choices=[
            (model.value, model.label) for model in get_allowed_models()]),
        'jihao': partial(ComponentsDropdownsField),
    }

    column_formatters = {
        'relateFileUrl': accessory_formatter('relateFileUrl'),
    }

    one_line_columns = ['conabstract', 'relateFileUrl']

    column_searchable_list = ('continusNum', 'cname', 'concategory')

    form_excluded_columns = ['engineeringOrders']

    support_flow = partial(ADFlow, 'Default basic approval flow', next_model=EngineeringOrder)

    # def get_query(self):
    #     # 不准操作管理员，且假定只有一个超级管理员
    #     query = self.model.query().
    #     return self.session.query(self.model).filter(self.model.action.allowed.username.in_(current_user.username)).all()


    @property
    def form_widget_args(self):
        return {
            'continusNum': {
                'readonly': True
            },
        }

    @expose('/create_eo_action')
    def create_eo_action(self):

        # 动作指示可能来源于请求的url
        id = request.args.get('id', '')
        action = request.args.get('action', '')

        self._custom_action(id, request.form, action)

        inst = self.model.query.filter(self.model.id == id).first()
        eo_id = inst.engineeringOrders[-1].id

        return_url = get_redirect_target() or self.get_url('.index_view')

        return redirect(self.get_url('engineeringorder.create_view',
                                     id=eo_id,
                                     return_url=return_url))

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.continusNum.validators = [DataRequired()]
            form.execTime.validators = [DataRequired()]
            if form.execCost.data:
                form.execCost.validators = [NumberRange(min=0, message='请输入合理的数值')]
            if form.stopTime.data:
                form.stopTime.validators = [NumberRange(min=0, message='请输入合理的数值')]
            if form.needTime.data:
                form.needTime.validators = [NumberRange(min=0, message='请输入合理的数值')]
            form.publishTime.validators = [
                DataRequired(),
                NumberRange(max=form.execTime.data,
                            message="颁布日期应早于生效日期")]
        return super(_AirworthinessView, self).validate_form(form)

    def get_query(self):
        datas = super(_AirworthinessView, self).get_query()
        return self.get_recieved_query(datas, 'airworthiness')


AirworthinessView = partial(
    _AirworthinessView, Airworthiness, name='适航文件'
)
