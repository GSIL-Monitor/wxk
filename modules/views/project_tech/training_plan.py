# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.training_plan import TrainingPlan
from .base import ProjectTechViewBase


class _TrainingPlanView(ProjectTechViewBase):
    # 培训计划列表视图应显示的内容
    column_list = [
        'trainPlanNum', 'trainPlanContent', 'trainPlanStartTime', 'statisFrom',
        'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'trainPlanNum': '编号',
        'trainPlanContent': '培训内容',
        'trainPlanStartTime': '培训开始时间',
        'statisFrom': '状态',
        'operation': '操作',
    }

    @staticmethod
    def operation_formatter(view, context, model, name):
        pass

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': operation_formatter
    }


TrainingPlanView = partial(
    _TrainingPlanView, TrainingPlan, name="培训计划"
)
