# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.quality.reserved_fault import ReservedFault
from .base import QualityManagementViewBase


class _ReservedFaultView(QualityManagementViewBase):
    # 保留故障列表视图应显示的内容
    column_list = [
        'blguzhangNum', 'zhuceNum',
        'statusName', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'blguzhangNum': '编号',
        'zhuceNum': '飞机注册号',
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


ReservedFaultView = partial(
    _ReservedFaultView, ReservedFault, name='保留故障'
)
