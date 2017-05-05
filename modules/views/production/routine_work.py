# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.production\
    .routine_work import RoutineWork
from .base import PMViewBase


class _RoutineWorkView(PMViewBase):
    # 例行工作列表视图应显示的内容
    column_list = [
        'jihao', 'planeType', 'jcType',
        'contextDesc', 'jcTime', 'jcAdress', 'statusName', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'jihao': '飞机注册号',
        'planeType': '机型',
        'jcType': '检查类型',
        'contextDesc': '内容描述',
        'jcTime': '检查日期',
        'jcAdress': '检查地点',
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


RoutineWorkView = partial(
    _RoutineWorkView, RoutineWork, name='例行工作'
)
