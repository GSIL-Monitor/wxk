# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.notification.notice import Notice
from .base import NotificationManagementViewBase
from modules.views.operations import basic_operation


class _NoticeView(NotificationManagementViewBase):
    column_display_actions = True

    # 通知列表视图应显示的内容
    column_list = [
        'id', 'title', 'sendName',
        'pubTime', 'statusName', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'id': '编号',
        'title': '名称',
        'sendName': '来源',
        'pubTime': '发布时间',
        'statusName': '状态',
        'operation': '操作',
    }

    column_exclude_list = ['flag']

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': basic_operation,
    }


NoticeView = partial(
    _NoticeView, Notice, name='通知管理'
)


def retrieve_unread_notifies(app):
    @app.context_processor
    def handle():
        return dict(notifies=Notice.query.all())
