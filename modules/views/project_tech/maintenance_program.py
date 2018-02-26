# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.maintenance_program import MaintenanceProgram
from modules.views import CustomView
from modules.views.operations import basic_approval_formater


class _MaintenanceProgramView(CustomView):
    # 维修方案列表视图应显示的内容
    column_list = [
        'maintenancePlanNum', 'insTitle', 'fafangDate', 'statusName', 'yujing',
        'operation',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'maintenancePlanNum': '编号',
        'insTitle': '标题',
        'fafangDate': '执行期限',
        'statusName': '状态',
        'yujing': '预警',
        'operation': '操作',
    }

    # 一些特殊的列，比如不存在的列（operation）需要自定义格式方式
    column_formatters = {
        'operation': basic_approval_formater
    }


MaintenanceProgramView = partial(
    _MaintenanceProgramView, MaintenanceProgram, name='维修方案'
)
