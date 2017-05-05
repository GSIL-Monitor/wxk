# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.retain import Retain
from .base import ProjectTechViewBase


class _RetainView(ProjectTechViewBase):
    # 保留工作列表视图应显示的内容
    column_list = [
        'blgzNum', 'zhuceNum', 'statusName',
        'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'blgzNum': '编号',
        'zhuceNum': '注册号',
        'statusName': '状态',
        'yujing': '预警',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


RetainView = partial(_RetainView, Retain, name='保留工作')
