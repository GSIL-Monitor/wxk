# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired
import json

from modules.models.project_tech.training_material import TrainigMaterial
from modules.views import CustomView
from modules.flows import BasicFlow
from modules.views.column_formatter import cancel_formatter
from util.fields.accessory_filed import TrainigMaterialMultiFileuploadField
from ..column_formatter import accessory_formatter
from util.str_to_dict import updateFileStr
from util.broker import file_move
from util.exception import BackendServiceError
from modules.views.operations import normal_operation_formatter


class _TrainigMaterialView(CustomView):

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
        '/static/js/training_material_validation.js',
    ]

    # 培训资料列表视图应显示的内容
    column_list = [
        'trainNumber', 'trainFileResourceName', 'trainFileResourceType',
        'operation'
    ]

    column_details_list = [
        'trainNumber', 'trainFileResourceType',
        'trainFileResourceName',
        'trainFileResourceContent',
        'trainFileResourceUrl'
    ]

    form_excluded_columns = ['addTime', 'updateUser', 'updTime',
                             'createTime', 'updateTime']
    # 对应内容的中文翻译
    column_labels = {
        'trainFileResourceName': '资料名称',
        'trainFileResourceType': '资料类型',
        'trainFileResourceContent': '资料内容',
        'trainNumber': '编号',
        'trainFileResourceUrl': '相关资料',
        'addTime': '制单时间',
        'updTime': '修改时间',
        'updateUser': '修改人',
        'operation': '操作',
        'cancel': '返回',
    }

    form_overrides = {
        'trainFileResourceType': partial(SelectField, choices=[
            ('飞机厂家资料', '飞机厂家资料'),
            ('发动机厂家资料', '发动机厂家资料'),
            ('工卡', '工卡'),
            ('公司文件', '公司文件'),
            ('技术规范', '技术规范'),
            ('其他', '其他'),
        ]),
        'trainFileResourceContent': partial(TextAreaField, render_kw={'rows': 3, 'style': 'resize:none;'}),
        'trainFileResourceUrl': partial(TrainigMaterialMultiFileuploadField),
    }

    one_line_columns = ['trainFileResourceContent', 'trainFileResourceUrl']

    support_flow = None
    use_inheritance_operation = False

    column_formatters = {
        'trainFileResourceUrl': accessory_formatter('trainFileResourceUrl'),
        'operation': normal_operation_formatter,
    }

    @property
    def form_widget_args(self):
        return {
            'trainNumber': {
                'readonly': True
            }
        }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.trainFileResourceContent.validators = [DataRequired()]
        return super(_TrainigMaterialView, self).validate_form(form)

    def on_model_change(self, form, model, is_created):
        super(_TrainigMaterialView, self).on_model_change(form, model, is_created)

        if not is_created:
            res = []
            new_type = form.trainFileResourceType.data
            old_type = form.trainFileResourceType.object_data
            file_str = model.trainFileResourceUrl
            if new_type != old_type and file_str:
                files_list = json.loads(file_str)
                for file_obj in files_list:
                    try:
                        tmp = updateFileStr(file_obj, new_type, unrelateDoc=True)
                        res.append(tmp.get('update'))
                        file_move(source=tmp.get('source'), target=tmp.get('target'))
                    except:
                        raise BackendServiceError('RabbitMq has something wrong')
                model.trainFileResourceUrl = json.dumps(res)
            self.session.commit()


TrainigMaterialView = partial(
    _TrainigMaterialView, TrainigMaterial, name='培训资料'
)
