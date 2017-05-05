# coding: utf-8

from __future__ import unicode_literals

from modules.roles import QualityRole, QualityInspectorRole
from modules.views import CustomView


class QualityManagementViewBase(CustomView):
    ''' 质量管理模块
        允许的部门包括：
        QualityRole-质量员
        QualityInspectorRole-质量监察主管工程师
    '''
    accepted_roles = [QualityRole, QualityInspectorRole]
