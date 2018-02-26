# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask_admin import expose
from flask import flash, redirect, request

from modules.models.airmaterial import AirMaterialStorageList
from modules.views.operations import operation_formatter_without_flow
from modules.views.airmaterial.multi_select import MultiSelectView
from modules.flows.operations import PurchaseAppl, BorrowAppl, View
from modules.perms import ActionNeedPermission
from .expire_warning import get_check_expire_warning_cfg
from modules.views.column_formatter import checkbox_formater


warning_set = {'yellow': 1, 'orange': 2, 'red': 3, 'null': 0}


# 预警为第一排序，数量为第二排序
def list_compare_max(x, y):
    if warning_set[x.warningLevel] > warning_set[y.warningLevel]:
        return -1
    elif warning_set[x.warningLevel] > warning_set[y.warningLevel]:
        return 1
    else:
        if x.quantity < y.quantity:
            return -1
        elif x.quantity > y.quantity:
            return 1
        else:
            return 0


class _StockWarningView(MultiSelectView):

    list_template = 'storage/warning.html'
    support_flow = False
    use_inheritance_operation = False

    column_labels = {
        'category': '航材类型',
        'partNumber': '件号',
        'serialNum': '序号',
        'name': '航材名称',
        'quantity': '数量',
        'unit': '航材单位',
        'flyTime': '飞行小时',
        'engineTime': '发动机小时',
        'flightTimes': '起落架次',
        'applicableModel': '适用机型',
        'storehouse': '仓库',
        'shelf': '架位',
        'minStock': '最低库存',
        'effectiveDate': '有效日期',
        'certificateNum': '证书编号',
        'airworthinessTagNum': '适航标签号',
        'lastCheckDate': '上次检查日期',
        'nextCheckDate': '下次检查日期',
        'manufacturer': '生产厂商',
        'supplier': '供应商',
        'statusName': '状态值',
        'checkbox': '复选',
        'operations': '操作',
    }

    column_list = [
        'checkbox', 'name', 'category', 'partNumber', 'shelf',
        'minStock', 'quantity',
    ]

    column_default_sort = ('quantity', False)
    column_searchable_list = ('name', 'partNumber', 'category')

    column_formatters = {
        'checkbox': checkbox_formater(),
    }

    type_url = {
        'purchase': 'purchaseapplication.create_view',
        'lend': 'lendapplication.create_view'
    }

    def is_accessible(self):
        return ActionNeedPermission('stockwarning', View).can()

    def get_query(self):
        datas = self.model.query.filter(
            self.model.category.in_(['化工品', '消耗品']))
        return datas

    def get_sorted_data_list(self, datas):
        lv_cfg = get_check_expire_warning_cfg('stockwarning')
        if not lv_cfg:
            flash('预警失败，请先配置到期预警值!', 'error')
            for data in datas:
                data.warningLevel = 'null'
            return datas
        for data in datas:
            if data.quantity:
                if data.category == '化工品':
                    data = self.get_list_data_warningLevel(
                        data, lv_cfg, 'chemical')
                elif data.category == '消耗品':
                    data = self.get_list_data_warningLevel(
                        data, lv_cfg, 'consume')
                else:
                    data.warningLevel = 'null'
            else:
                data.warningLevel = 'null'
        datas.sort(list_compare_max)
        return datas

    def get_list_data_warningLevel(self, data, lv_cfg, category):
        if data.quantity < lv_cfg[category]['lv3']:
            data.warningLevel = 'red'
        elif data.quantity < lv_cfg[category]['lv2']:
            data.warningLevel = 'orange'
        elif data.quantity < lv_cfg[category]['lv1']:
            data.warningLevel = 'yellow'
        else:
            data.warningLevel = 'null'
        return data

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        count, datas = super(_StockWarningView, self).get_list(
            page, sort_column, sort_desc, search, filters,
            execute=True, page_size=None)
        count = self.get_query().count()
        datas = self.get_sorted_data_list(datas)
        self.index_lists = datas
        levels = [data.warningLevel for data in self.index_lists]
        self._template_args.update({
            'levels': levels,
        })
        return count, datas


StockWarningView = partial(
    _StockWarningView, AirMaterialStorageList,
    endpoint='stockwarning', name='库存预警')
