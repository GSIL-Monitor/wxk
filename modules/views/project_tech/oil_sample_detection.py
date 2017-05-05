# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.oil_sample_detection import OilSampleDetection
from .base import ProjectTechViewBase


class _OilSampleDetectionView(ProjectTechViewBase):
    # 油样检测列表视图应显示的内容
    column_list = [
        'id', 'oilName', 'banbenTime', 'statusName',
        'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'id': '编号',
        'oilName': '油样名称',
        'banbenTime': '报告日期',
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


OilSampleDetectionView = partial(
    _OilSampleDetectionView, OilSampleDetection, name='油样检测'
)
