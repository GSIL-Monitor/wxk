# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial.claim_sheet import ClaimSheet
from .base import AirmaterialViewBase


class _ClaimSheetView(AirmaterialViewBase):
    # 索赔列表视图应显示的内容
    column_list = [
        'id', 'date', 'unit',
        'content', 'file', 'statusName', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'id': '编号',
        'date': '日期',
        'unit': '单位',
        'content': '内容',
        'file': '附件',
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


ClaimSheetView = partial(
    _ClaimSheetView, ClaimSheet, name='索赔'
)
