# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.training_material import TrainigMaterial
from .base import ProjectTechViewBase


class _TrainigMaterialView(ProjectTechViewBase):
    # 培训资料列表视图应显示的内容
    column_list = [
        'trainFileResourceName', 'trainFileResourceType',
        'trainFileResourceContent', 'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'trainFileResourceName': '资料名称',
        'trainFileResourceType': '资料类型',
        'trainFileResourceContent': '资料内容',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


TrainigMaterialView = partial(
    _TrainigMaterialView, TrainigMaterial, name='培训资料'
)
