# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.production\
    .maintenance_status import MaintenanceStatus
from .base import PMViewBase


class _MaintenanceStatusView(PMViewBase):
    # 维修状态列表视图应显示的内容
    column_list = [
        'id', 'mxpContent', 'scwcDate',
        'yjxcDate', 'remainfxsj', 'remainfxcs', 'remainrlsj', 'operation',
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
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


MaintenanceStatusView = partial(
    _MaintenanceStatusView, MaintenanceStatus, name='维修状态'
)
