# coding:utf-8
# 工程技术范畴下的各模块视图定义

# from .engineering_order import EngineeringOrderView
from .maintenance_status import MaintenanceStatusView
from .production_order import ProductionOrderView
from .routine_work import RoutineWorkView
from .company_day_record import CompanyDayRecordView
from .maintenance_record import MaintenanceRecordView
from .fault_reports import FaultReportsView
from .troubleshooting import TroubleShootingView
from .examine_repair_record import ExamineRepairRecordView


__all__ = ['views']


views = [
    MaintenanceStatusView, ProductionOrderView,
    RoutineWorkView, CompanyDayRecordView,
    MaintenanceRecordView, FaultReportsView,
    TroubleShootingView, ExamineRepairRecordView
]
