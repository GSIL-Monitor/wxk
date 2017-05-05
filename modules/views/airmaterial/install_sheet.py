# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial.install_sheet import InstallSheet
from .base import AirmaterialViewBase


class _InstallSheetView(AirmaterialViewBase):
    # 装机列表视图应显示的内容
    column_list = [
        'formNumber', 'formUserName', 'formDate', 'installUserName',
        'installDate', 'status', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'formNumber': '编号',
        'formUserName': '制表人',
        'formDate': '日期',
        'installUserName': '安装人',
        'installDate': '安装日期',
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


InstallSheetView = partial(
    _InstallSheetView, InstallSheet, name='装机'
)
