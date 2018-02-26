# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.production.production_order import ProductionOrder
from modules.views import CustomView


class _ProductionOrderView(CustomView):
    # 生产指令列表视图应显示的内容
    column_list = [
        'sczlNum', 'shejiPlane', 'gongzuoContext',
        'statusName', 'yujing',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'sczlNum': '编号',
        'shejiPlane': '涉及飞机',
        'gongzuoContext': '工作内容',
        'statusName': '状态',
        'yujing': '预警（天）',
    }


ProductionOrderView = partial(
    _ProductionOrderView, ProductionOrder, name='生产指令'
)
