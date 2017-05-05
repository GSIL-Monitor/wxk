# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.production\
    .production_order import ProductionOrder
from .base import PMViewBase


class _ProductionOrderView(PMViewBase):
    # 生产指令列表视图应显示的内容
    column_list = [
        'sczlNum', 'shejiPlane', 'gongzuoContext',
        'statusName', 'yujing', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'sczlNum': '编号',
        'shejiPlane': '涉及飞机',
        'gongzuoContext': '工作内容',
        'statusName': '状态',
        'yujing': '预警（天）',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


ProductionOrderView = partial(
    _ProductionOrderView, ProductionOrder, name='生产指令'
)
