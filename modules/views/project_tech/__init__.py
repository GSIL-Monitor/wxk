# coding:utf-8
# 工程技术范畴下的各模块视图定义

from .airworthiness import AirworthinessView
from .engineering_order import EngineeringOrderView
from .retain import RetainView
from .oil_sample_detection import OilSampleDetectionView
# from .maintenance_program import MaintenanceProgramView
from .unroutine_work import UnroutineWorkView
from .malfuncture_statistics import MalfunctureStatisticsView
from .training_plan import TrainingPlanView
from .training_archive import TrainingArchiveView
from .training_material import TrainigMaterialView
from .tech_material import TechMaterialView


__all__ = ['views']


views = [
    AirworthinessView, EngineeringOrderView,
    RetainView, OilSampleDetectionView,
    # MaintenanceProgramView,
    UnroutineWorkView,
    MalfunctureStatisticsView, TrainingPlanView,
    TrainingArchiveView, TrainigMaterialView, TechMaterialView
]
