# coding: utf-8

from __future__ import unicode_literals

from modules.roles import PMSE,\
    ProductionControllerRole, ProductionViceManager
from modules.views import CustomView


# ProductionManagement
class PMViewBase(CustomView):
    ''' 生产管理模块
        允许的部门包括：
        PMSE-生产管理主管工程师
        ProductionControllerRole-生产控制员
        ProductionViceManager-生产副经理
    '''
    accepted_roles = [PMSE, ProductionControllerRole, ProductionViceManager]
