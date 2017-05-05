# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.unroutine_work import UnroutineWork
from .base import ProjectTechViewBase


class _UnroutineWorkView(ProjectTechViewBase):
    # 非例行工作列表视图应显示的内容
    column_list = [
        'flxgzNum', 'jihao', 'statusName',
        'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'flxgzNum': '编号',
        'jihao': '注册号',
        'statusName': '状态',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


UnroutineWorkView = partial(
    _UnroutineWorkView, UnroutineWork, name='非例行工作'
)
