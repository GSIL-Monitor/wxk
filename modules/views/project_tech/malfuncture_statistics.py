# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech\
    .malfuncture_statistics import MalfunctureStatistics
from .base import ProjectTechViewBase


class _MalfunctureStatisticsView(ProjectTechViewBase):
    # 故障统计列表视图应显示的内容
    column_list = [
        'statisDate', 'feiliNum', 'checkType', 'statisFrom', 'ataNum',
        'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'statisDate': '故障日期',
        'feiliNum': '飞机号',
        'checkType': '检查类别',
        'statisFrom': '故障来源',
        'ataNum': 'ATA章节号',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


MalfunctureStatisticsView = partial(
    _MalfunctureStatisticsView, MalfunctureStatistics, name='故障统计'
)
