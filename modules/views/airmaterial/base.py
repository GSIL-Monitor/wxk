# coding: utf-8

from __future__ import unicode_literals

from modules.roles import AMVM, AMMR,\
    FlightCrew, FlightManager, FlightViceManager
from modules.views import CustomView


class AirmaterialViewBase(CustomView):
    '''航材模块
        允许的部门包括：
        AMVM 航材副经理
        AMMR 航材管理员
        FlightCrew 机务组人员
        FlightManager 机务部经理
        FlightViceManager 机务部副经理
        '''

    accepted_roles = [AMVM, AMMR, FlightCrew, FlightManager, FlightViceManager]
