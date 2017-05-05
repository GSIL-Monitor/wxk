# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from flask import request

from modules.models.project_tech.airworthiness import Airworthiness
from .base import ProjectTechViewBase
from modules.views.operations import basic_operation


class _AirworthinessView(ProjectTechViewBase):
    # 适航文件列表视图应显示的内容
    column_list = [
        'continusNum', 'cname', 'isExec', 'statusName', 'yujing',
        'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'continusNum': '编号',
        'cname': '名称',
        'isExec': '是否限期执行',
        'execTime': '执行期限',
        'statusName': '状态',
        'yujing': '预警',
        'operation': '操作',
    }

    @property
    def form_widget_args(self):
        if not request:
            return {}
        url = request.base_url
        if 'edit' in url:
            return {
                'cname': {
                    'disabled': True
                },
                'continusNum': {
                    'disabled': True
                },
            }

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': basic_operation
    }


AirworthinessView = partial(
    _AirworthinessView, Airworthiness, name='适航文件'
)
