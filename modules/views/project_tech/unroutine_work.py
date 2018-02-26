# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.unroutine_work import UnroutineWork
from modules.views import CustomView


class _UnroutineWorkView(CustomView):
    # 非例行工作列表视图应显示的内容
    column_list = [
        'flxgzNum', 'jihao', 'statusName',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'flxgzNum': '编号',
        'jihao': '注册号',
        'statusName': '状态',
    }


UnroutineWorkView = partial(
    _UnroutineWorkView, UnroutineWork, name='非例行工作'
)
