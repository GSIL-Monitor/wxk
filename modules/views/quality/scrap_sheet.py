# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.quality.scrap_sheet import ScrapSheet
from .base import QualityManagementViewBase


class _ScrapSheetView(QualityManagementViewBase):
    # 报废列表视图应显示的内容
    column_list = [
        'formNumber', 'formUserName',
        'formDate', 'status', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'formNumber': '编号',
        'formUserName': '申请人',
        'formDate': '申请时间',
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


ScrapSheetView = partial(
    _ScrapSheetView, ScrapSheet, name='报废'
)
