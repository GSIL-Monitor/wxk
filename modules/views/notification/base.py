# coding: utf-8

from __future__ import unicode_literals

from modules.roles import ProjectTechRole,\
    EngineeringLeadEngineer, ChiefEngineer,\
    ProductionControllerRole, PMSE, ProductionViceManager,\
    QualityRole, QualityInspectorRole, FlightCrew,\
    FlightManager, AMMR, AMVM, Mechanic,\
    FlightViceManager, MaintenanceVicePresident
from modules.views import CustomView


class NotificationManagementViewBase(CustomView):
    ''' 通知模块
        允许的部门包括：
        all
    '''
    accepted_roles = [
        ProjectTechRole, EngineeringLeadEngineer, ChiefEngineer,
        ProductionControllerRole, PMSE, ProductionViceManager,
        QualityRole, QualityInspectorRole, FlightCrew,
        FlightManager, AMMR, AMVM, Mechanic,
        FlightViceManager, MaintenanceVicePresident
    ]
