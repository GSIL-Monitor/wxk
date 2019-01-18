# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from wtforms.fields import SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask import request
from flask_admin import expose
from flask_security import current_user
from sqlalchemy_continuum import version_class
from sqlalchemy import or_
import json

from modules.models.project_tech.tech_material import TechMaterial
from modules.views import CustomView
from modules.views.column_formatter import cancel_formatter

from util.fields.accessory_filed import TechMaterialMultiFileuploadField
from util.fields import RefreshFileTypeSelectField
from modules.views.operations import normal_operation_formatter
from ..column_formatter import accessory_formatter, content_formatter
from modules.flows.approve_can_edit_flow import ApproveCanEdit
from modules.flows.states import InitialState, Reviewed
from util.str_to_dict import updateFileStr
from util.exception import BackendServiceError
from util.broker import file_move, file_remove
from modules.models.role import Role, BasicAction


class _TechMaterialView(CustomView):
    # 技术资料列表视图应显示的内容

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
        '/static/js/tech_material_validation.js',
    ]

    form_overrides = {
        'fileResourceType': partial(RefreshFileTypeSelectField),
        'relatePlanType': partial(SelectField, choices=[
            ('运5B（D）', '运5B（D）')]),
        'content': partial(TextAreaField, render_kw={
            'rows': 3, 'style': 'resize:none;'}),
        'fileResourceUrl': partial(TechMaterialMultiFileuploadField),
    }

    column_list = [
        'fileResourceNum', 'fileResourceName', 'fileResourceType',
        'relatePlanType', 'status', 'operation'
    ]

    support_flow = partial(ApproveCanEdit, 'approved can edit')
    # use_inheritance_operation = False

    column_details_list = [
        'fileResourceNum', 'version', 'fileResourceName', 'addTime',
        'fileResourceType', 'relatePlanType', 'content', 'fileResourceUrl',
    ]

    form_excluded_columns = ['addTime']

    one_line_columns = ['content', 'fileResourceUrl']
    # 对应内容的中文翻译
    column_labels = {
        'fileResourceNum': '文件编号',
        'fileResourceName': '文件名称',
        'fileResourceType': '文件类型',
        'relatePlanType': '相关机型',
        'version': '版本',
        'fileResourceUrl': '附件',
        'content': '资料内容',
        'addTime': '制单时间',
    }

    column_searchable_list = ('fileResourceNum', 'fileResourceName',
        'fileResourceType')

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'addTime': lambda v, c, m, p: m.addTime.strftime("%Y-%m-%d %H:%S:%M"),
        'operation': normal_operation_formatter,
        'fileResourceUrl': accessory_formatter('fileResourceUrl'),
        'content': content_formatter,
    }

    @property
    def form_widget_args(self):
        widget = {
            'fileResourceNum': {
                'readonly': True
            }
        }
        if not request:
            return {}
        if 'edit' in request.base_url:
                widget.update({
                    'fileResourceType': {'disabled': True}
                })
        return widget

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.fileResourceName.validators = [DataRequired()]
        return super(_TechMaterialView, self).validate_form(form)

    def get_query(self):

        datas = super(_TechMaterialView, self).get_query()

        ids = [item.id for item in datas] if datas.count() else []
        role = Role.query.join(
            BasicAction, Role.id == BasicAction.role_id
        ).filter(BasicAction.view == True,
                 BasicAction.model == 'techmaterial')

        if role.count() != 1 or role[0] not in current_user.roles:
            return datas

        query = self.model.query.filter(
            or_(self.model.id.in_(ids),
                self.model.auditStatus == Reviewed))

        return query

    def get_recieved_query(self, datas, model_name):

        ids = [item.id for item in datas] if datas.count() else []

        role = Role.query.join(
            BasicAction, Role.id == BasicAction.role_id
        ).filter(BasicAction.view == True,
                 BasicAction.model == 'techmaterial')

        if role.count() != 1 or role[0] not in current_user.roles:
            return datas

        query = self.model.query.filter(
            or_(self.model.id.in_(ids),
                self.model.auditStatus == Reviewed))

        return query

    def get_audit_form_class(self, model, verb):
        if verb == 'review':
            return self._action_view_cfg['review_only'].form
        return None

    def on_model_delete(self, model):
        file_str = model.fileResourceUrl
        files_list = json.loads(file_str)
        for file_obj in files_list:
            try:
                file_remove(key=file_obj.get('key'), name=file_obj.get('name'))
            except:
                raise BackendServiceError('RabbitMq has something wrong')


TechMaterialView = partial(
    _TechMaterialView, TechMaterial, name='技术资料'
)
