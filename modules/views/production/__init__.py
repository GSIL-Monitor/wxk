# coding:utf-8
# 工程技术范畴下的各模块视图定义

# from .engineering_order import EngineeringOrderView
from .maintenance_status import MaintenanceStatusView
from .production_order import ProductionOrderView
from .routine_work import RoutineWorkView


__all__ = ['views']


views = [
    MaintenanceStatusView, ProductionOrderView,
    RoutineWorkView
]
