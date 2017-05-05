# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.tech_material import TechMaterial
from .base import ProjectTechViewBase


class _TechMaterialView(ProjectTechViewBase):
    # 技术资料列表视图应显示的内容
    column_list = [
        'fileResourceNum', 'fileResourceName',
        'fileResourceType', 'relatePlanType', 'addTime', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'fileResourceNum': '编号',
        'fileResourceName': '名称',
        'fileResourceType': '类别',
        'relatePlanType': '相关机型',
        'addTime': '录入时间',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


TechMaterialView = partial(
    _TechMaterialView, TechMaterial, name='技术资料'
)
