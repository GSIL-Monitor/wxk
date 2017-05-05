# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial.in_bound import InBound
from .base import AirmaterialViewBase


class _InBoundView(AirmaterialViewBase):
    # 入库列表视图应显示的内容
    column_list = [
        'form_number', 'form_user_name', 'form_date',
        'statusName', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'form_number': '编号',
        'form_user_name': '制表人',
        'form_date': '日期',
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


InBoundView = partial(
    _InBoundView, InBound, name='入库'
)
