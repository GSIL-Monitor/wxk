# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial\
    .purchase_contract import PurchaseContract
from .base import AirmaterialViewBase


class _PurchaseContractView(AirmaterialViewBase):
    # 采购合同列表视图应显示的内容
    column_list = [
        'number', 'date', 'supplierId', 'contact',
        'phone', 'fax', 'email', 'formUserName',
        'consignee', 'status', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'number': '合同编号',
        'date': '采购日期',
        'supplierId': '供应商',
        'contact': '联系人',
        'phone': '电话',
        'fax': '传真',
        'email': '邮件',
        'formUserName': '制表人',
        'consignee': '收货人',
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


PurchaseContractView = partial(
    _PurchaseContractView, PurchaseContract, name='采购合同'
)
