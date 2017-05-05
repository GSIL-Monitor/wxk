# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial\
    .airmaterial_list import AirmaterialList
from .base import AirmaterialViewBase


class _AirmaterialListView(AirmaterialViewBase):
    # 航材首页列表视图应显示的内容
    column_list = [
        'name', 'type', 'partNumber', 'sequenceNumber',
        'price', 'applicableModel', 'status', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'name': '名称',
        'type': '类别',
        'partNumber': '件号',
        'sequenceNumber': '序号',
        'price': '单价',
        'applicableModel': '适用机型',
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


AirmaterialListView = partial(
    _AirmaterialListView, AirmaterialList, name='航材首页'
)
