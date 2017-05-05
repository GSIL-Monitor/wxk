# encoding: utf-8

from __future__ import unicode_literals

from .models.role import Role, BasicAction


# 这里默认导出的是权限的名称，而非实例
__all__ = [
    'SuperAdmin',
    'EngineeringLeadEngineer',
    'ChiefEngineer',
    'ProductionControllerRole',
    'PMSE',
    'ProductionViceManager',
    'QualityRole',
    'QualityInspectorRole',
    'FlightCrew',
    'FlightManager',
    'AMMR',
    'AMVM',
    'Mechanic',
    'FlightViceManager',
    'MaintenanceVicePresident'
]

SuperAdmin = '超级管理员'
ProjectTechRole = '工程技术员'
EngineeringLeadEngineer = '工程主管工程师'
ChiefEngineer = '总工程师'
ProductionControllerRole = '生产控制员'
# Production management supervisor engineer
PMSE = '生产管理主管工程师'
ProductionViceManager = '生产副经理'
QualityRole = '质量员'
QualityInspectorRole = '质量监察主管工程师'
FlightCrew = '机务组人员'
FlightManager = '机务部经理'
# aircraft material management role
AMMR = '航材管理员'
# aircraft material vice Manager
AMVM = '航材副经理'
Mechanic = '机械师'
FlightViceManager = '机务部副经理'
MaintenanceVicePresident = '维修副总'


def init_builtin_roles():
    # TODO: 默认为超级管理员把用户、权限模型的增删改和查权限开启
    super_admin_user_action = BasicAction(
        model='user', create=True, edit=True, view=True, delete=True)
    super_admin_role_action = BasicAction(
        model='role', create=True, edit=True, view=True, delete=True)

    return [
        Role(name=SuperAdmin, description='系统超级管理员，可对用户和权限进行设置',
             actions=[super_admin_user_action, super_admin_role_action]),
        Role(name=ProjectTechRole, description='工程技术员'),
        Role(name=EngineeringLeadEngineer, description='工程主管工程师'),
        Role(name=ChiefEngineer, description='总工程师'),
        Role(name=ProductionControllerRole, description='生产控制员'),
        Role(name=PMSE, description='生产管理主管工程师'),
        Role(name=ProductionViceManager, description='生产副经理'),
        Role(name=QualityRole, description='质量员'),
        Role(name=QualityInspectorRole, description='质量监察主管工程师'),
        Role(name=FlightCrew, description='机务组人员'),
        Role(name=FlightManager, description='机务部经理'),
        Role(name=AMMR, description='航材管理员'),
        Role(name=AMVM, description='航材副经理'),
        Role(name=Mechanic, description='机械师'),
        Role(name=FlightViceManager, description='机务部副经理'),
        Role(name=MaintenanceVicePresident, description='维修副总')
    ]


def super_admin(session):
    return session.query(Role).filter(
        Role.name == SuperAdmin)[0]
