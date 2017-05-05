# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial.return_sheet import ReturnSheet
from .base import AirmaterialViewBase


class _ReturnSheetView(AirmaterialViewBase):
    # 退料列表视图应显示的内容
    column_list = [
        'formNumber', 'formUserName', 'formDate',
        'returnUserName', 'returnDate', 'status', 'operation'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'formNumber': '编号',
        'formUserName': '制表人',
        'formDate': '制表日期',
        'returnUserName': '退料人',
        'returnDate': '退料日期',
        'status': '状态',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


ReturnSheetView = partial(
    _ReturnSheetView, ReturnSheet, name='退料'
)
