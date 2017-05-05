# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial.lend_sheet import LendSheet
from .base import AirmaterialViewBase


class _LendSheetView(AirmaterialViewBase):
    # 借出列表视图应显示的内容
    column_list = [
        'number', 'date', 'companyName', 'companyAddress',
        'contact', 'phone', 'fax', 'email',
        'formUserName', 'status', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '编号',
        'date': '日期',
        'companyName': '单位名称',
        'companyAddress': '单位地址',
        'contact': '联系人',
        'phone': '电话',
        'fax': '传真',
        'email': '邮箱',
        'formUserName': '制表人',
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


LendSheetView = partial(
    _LendSheetView, LendSheet, name='借出'
)
