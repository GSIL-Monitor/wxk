# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.training_archive import TrainingArchive
from modules.views import CustomView
from modules.views.column_formatter import cancel_formatter
from wtforms.validators import DataRequired
from modules.flows import BasicFlow
from wtforms.validators import DataRequired, NumberRange
from util.widgets import DateTimeWidget
from wtforms import DateTimeField, TextAreaField
from modules.views.operations import normal_operation_formatter


class _TrainingArchiveView(CustomView):
    # 培训档案列表视图应显示的内容
    create_template = 'unvalidate/create.html'
    approve_edit_template = 'unvalidate/approve_edit.html'

    column_list = [
        'trainNumber', 'userName', 'trainRecordTime', 'trainRecordName'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'userName': '姓名',
        'trainRecordTime': '培训时间',
        'trainRecordName': '培训名称',
        'trainRecordContent': '培训内容',
        'trainRecordScore': '培训成绩',
        'trainNumber': '编号',
        'quarters': '岗位',
        'createUser': '制单人',
        'addTime': '制单时间',
        'updateUser': '修改人',
        'updTime': '修改时间',
        'submitUser': '提交人',
        'submitTime': '提交时间',
    }

    form_excluded_columns = ['statusName']

    support_flow = partial(BasicFlow, 'basic flow')

    column_details_list = [
        'trainNumber', 'userName', 'trainRecordTime', 'quarters',
        'trainRecordName', 'trainRecordScore', 'trainRecordContent',
    ]

    form_overrides = {
        'trainRecordTime': partial(DateTimeField, widget=DateTimeWidget()),
        'trainRecordContent': partial(TextAreaField,
                                      render_kw={'rows': 3,
                                                 'style': 'resize:none;'})
    }
    one_line_columns = ['trainRecordContent']

    @property
    def form_widget_args(self):
        return {
            'trainNumber': {
                'readonly': True
            }
        }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.userName.validators = [DataRequired()]
            form.trainRecordContent.validators = [DataRequired()]
        return super(_TrainingArchiveView, self).validate_form(form)


TrainingArchiveView = partial(
    _TrainingArchiveView, TrainingArchive, name='培训档案'
)
