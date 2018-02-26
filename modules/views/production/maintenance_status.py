# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.production.maintenance_status import MaintenanceStatus
from modules.views import CustomView


class _MaintenanceStatusView(CustomView):

    # 维修状态列表视图应显示的内容
    column_list = [
        'id', 'mxpContent', 'scwcDate',
        'yjxcDate', 'remainfxsj', 'remainfxcs', 'remainrlsj',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'id': '编号',
        'mxpContent': '内容描述',
        'scwcDate': '上次完成日期',
        'yjxcDate': '预计下次完成日期',
        'remainfxsj': '剩余飞行时间',
        'remainfxcs': '剩余飞行次数',
        'remainrlsj': '剩余日历时间',
    }


MaintenanceStatusView = partial(
    _MaintenanceStatusView, MaintenanceStatus, name='维修状态'
)
