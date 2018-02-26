# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from datetime import datetime, date
import json
from flask import current_app, flash
from modules.models.airmaterial import AirMaterialStorageList
from modules.views.operations import operation_formatter_without_flow
from modules.perms import ActionNeedPermission
from modules.flows.operations import View
from modules.views.airmaterial.multi_select import MultiSelectView
from modules.flows.operations import CreateScrap
from modules.views.column_formatter import checkbox_formater


def get_check_expire_warning_cfg(redis_key):
    redisCache = current_app.redis_cache
    items = redisCache.get(redis_key)
    if not items:
        return None
    items = json.loads(items)
    return items


class _ExpireWarningView(MultiSelectView):

    list_template = 'storage/expire_warning.html'
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
        'checkbox', 'name', 'category', 'partNumber', 'serialNum',
        'shelf', 'effectiveDate',
    ]
    column_default_sort = ('effectiveDate', False)
    column_formatters = {
        'checkbox': checkbox_formater(),
    }
    column_searchable_list = ('name', 'partNumber')

    type_url = {
        'scrap': 'scrap.create_view',
    }

    def is_accessible(self):
        return ActionNeedPermission('expirewarning', View).can()

    def get_query(self):
        return super(_ExpireWarningView, self).get_query().filter(
            self.model.effectiveDate != '')

    def get_sorted_data_list(self, datas):
        lv_cfg = get_check_expire_warning_cfg('expirewarning')
        if not lv_cfg:
            flash('预警失败，请先配置到期预警值!', 'error')
            for data in datas:
                data.warningLevel = ''
            return datas
        for data in datas:
            if data.effectiveDate:
                effect_date = datetime.strptime(data.effectiveDate, '%Y-%m-%d')
                if (effect_date.date() - date.today()).days <= lv_cfg['lv3']:
                    data.warningLevel = 'red'
                elif (effect_date.date() - date.today()).days <= lv_cfg['lv2']:
                    data.warningLevel = 'orange'
                elif (effect_date.date() - date.today()).days <= lv_cfg['lv1']:
                    data.warningLevel = 'yellow'
                else:
                    data.warningLevel = ''
            else:
                data.warningLevel = ''
        return datas

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        sort_column = 'effectiveDate'
        count, datas = super(_ExpireWarningView, self).get_list(
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


ExpireWarningView = partial(
    _ExpireWarningView, AirMaterialStorageList,
    endpoint='expirewarning', name='到期预警')
