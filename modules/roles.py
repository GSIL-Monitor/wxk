# encoding: utf-8

from __future__ import unicode_literals

from modules.models.role import Role, BasicAction


# 这里默认导出的是权限的名称，而非实例
__all__ = [
    'SuperAdmin',
    'ProjectTechRole',
    'FlightCrew',
    'FlightManager',
    'ChiefEngineer',
    'ChiefFlyController',
    'FlightViceManager',
    'Administrator',
    'FinancialStaff',
    'AMMR',
    'StationMaster',
    'OfficeAdministrator',
    'Officer',
    'AllAction',
]

SuperAdmin = '超级管理员'
ProjectTechRole = '工程技术员'
FlightCrew = '机务人员'
FlightManager = '机务科长'
ChiefEngineer = '总工程师'
ChiefFlyController = '航管科长'
FlightViceManager = '机务副总'
Administrator = '系统管理员'
FinancialStaff = '财务人员'
AMMR = '航材管理员'
StationMaster = '站长'
OfficeAdministrator = '办公室主任'
Officer = ' 办公室人员'
AllAction = '全权角色'


# 根据徐州机务系统用例需求配置的角色与相关视图可见度的映射关系
role_management_dict = {
    '机长信息': [SuperAdmin],
}


def init_builtin_roles():
    # 默认为超级管理员把用户、权限模型的增删改和查权限开启
    super_admin_user_action = BasicAction(
        model='user', create=True, edit=True, view=True, delete=True)
    super_admin_role_action = BasicAction(
        model='role', create=True, edit=True, view=True, delete=True)

    return [

        Role(name=SuperAdmin, description='超级管理员',
             actions=[super_admin_user_action, super_admin_role_action]),
        Role(name=ProjectTechRole, description='工程技术员'),
        Role(name=FlightCrew, description='机务人员'),
        Role(name=FlightManager, description='机务科长'),
        Role(name=ChiefEngineer, description='总工程师'),
        Role(name=ChiefFlyController, description='航管科长'),
        Role(name=FlightViceManager, description='机务副总'),
        Role(name=Administrator, description='系统管理员'),
        Role(name=FinancialStaff, description='财务人员'),
        Role(name=AMMR, description='航材管理员'),
        Role(name=StationMaster, description='站长'),
        Role(name=OfficeAdministrator, description='办公室主任'),
        Role(name=Officer, description='办公室人员')
    ]


def super_admin(session):
    return session.query(Role).filter(
        Role.name == SuperAdmin)[0]
