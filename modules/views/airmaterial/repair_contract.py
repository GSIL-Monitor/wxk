# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial\
    .repair_contract import RepairContract
from .base import AirmaterialViewBase


class _RepairContractView(AirmaterialViewBase):
    # 送修列表视图应显示的内容
    column_list = [
        'formNumber', 'repairManufacturerId', 'contact',
        'totalPrice', 'status', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'formNumber': '合同编号',
        'repairManufacturerId': '维修厂商编号',
        'contact': '联系人',
        'totalPrice': '总价',
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


RepairContractView = partial(
    _RepairContractView, RepairContract, name='送修'
)
