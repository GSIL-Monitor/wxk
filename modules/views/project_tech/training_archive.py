# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.training_archive import TrainingArchive
from .base import ProjectTechViewBase


class _TrainingArchiveView(ProjectTechViewBase):
    # 培训档案列表视图应显示的内容
    column_list = [
        'userName', 'trainRecordTime', 'trainRecordName',
        'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'userName': '姓名',
        'trainRecordTime': '培训时间',
        'trainRecordName': '培训名称',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


TrainingArchiveView = partial(
    _TrainingArchiveView, TrainingArchive, name='培训档案'
)
