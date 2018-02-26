# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from wtforms import DateTimeField
from wtforms.validators import NumberRange, DataRequired
from flask_security import current_user
from sqlalchemy import or_
from sqlalchemy_continuum import version_class

from modules.models.project_tech.training_plan import TrainingPlan
from modules.views import CustomView
from modules.flows import OneApprovalFlow
from util.widgets import DateTimeWidget
from util.fields.accessory_filed import TrainigPlanMultiFileuploadField
from flask_admin.tools import rec_getattr
from ..column_formatter import accessory_formatter
from modules.models.base import db
from modules.models.user import User
 

class _TrainingPlanView(CustomView):
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
        '/static/js/training_plan_validation.js',
    ]

    # 培训计划列表视图应显示的内容
    column_list = [
        'trainPlanNum', 'trainPlanContent', 'trainPlanStartTime', 'status'
    ]

    # 待复核的内容要少
    column_details_list = [
        'trainPlanNum', 'trainPlanStartTime', 'trainPlanEndTime',
        'trainPlanGzFrom', 'trainPlanPlace', 'trainPlanTeacher',
        'trainPlanJoin', 'trainPlanContent', 'trainPlanFileUrl'
    ]

    # 对应内容的中文翻译
    column_labels = {
        'trainPlanNum': '编号',
        'trainPlanContent': '培训内容',
        'trainPlanStartTime': '培训开始时间',
        'trainPlanEndTime': '培训结束时间',
        'trainPlanGzFrom': '培训单位',
        'trainPlanPlace': '培训地点',
        'trainPlanTeacher': '培训教员',
        'trainPlanFileUrl': '相关文件',
        'trainPlanJoin': '参与培训人员',
        'createUser': '制单人',
        'addTime': '制单时间',
        'updateUser': '修改人',
        'updTime': '修改时间',
    }

    column_searchable_list = ('trainPlanNum',)
    one_line_columns = ['trainPlanContent', 'trainPlanFileUrl']

    form_overrides = {
        'trainPlanStartTime': partial(DateTimeField, widget=DateTimeWidget()),
        'trainPlanEndTime': partial(DateTimeField, widget=DateTimeWidget()),
        'trainPlanFileUrl': partial(TrainigPlanMultiFileuploadField),
    }

    @property
    def form_widget_args(self):
        return {
            'trainPlanNum': {
                'readonly': True
            },
        }

    column_formatters = {
        'trainPlanFileUrl': accessory_formatter('trainPlanFileUrl'),
    }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.trainPlanStartTime.validators = [DataRequired()]
            form.trainPlanEndTime.validators = [
                DataRequired(),
                NumberRange(min=form.trainPlanStartTime.data,
                            message="结束时间应晚于开始时间")]
        return super(_TrainingPlanView, self).validate_form(form)


TrainingPlanView = partial(
    _TrainingPlanView, TrainingPlan, name="培训计划"
)
