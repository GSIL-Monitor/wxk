# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial\
    .repair_supplier import RepairSupplier
from .base import AirmaterialViewBase


class _RepairSupplierView(AirmaterialViewBase):
    # 送修列表视图应显示的内容
    column_list = [
        'name', 'repairCapacity', 'address',
        'contact', 'phone', 'email', 'fax', 'operation'
    ]
    # 对应内容的中文翻译
    column_labels = {
        'name': '名称',
        'repairCapacity': '维修能力',
        'address': '地址',
        'contact': '联系人',
        'phone': '电话',
        'email': '邮件',
        'fax': '传真',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


RepairSupplierView = partial(
    _RepairSupplierView, RepairSupplier, name='维修厂商'
)
