# coding: utf-8

from __future__ import unicode_literals

from .as350 import AS350View
from .bell206 import BELL206View
from .bell407 import BELL407View
from .bell429 import BELL429View
from .da40d import DA40DView
from .r22 import R22View
from .r44 import R44View
from .swz269c1 import SWZ269C1View
from .y5b import Y5BView


AS350_NAME = 'AS350'
BELL206_NAME = 'BELL206'
BELL407_NAME = 'BELL407'
BELL429_NAME = 'BELL429'
R22_NAME = 'R22'
R44_NAME = 'R44'
DA40D_NAME = 'DA40D'
SWZ269C1_NAME = 'SWZ269c1'
Y5B_NAME = 'Y5B'


def init_mxp_view(admin_obj, mongodb, category, allowed_mxps=[]):
    # WUJG: 暂时不为各方案提供任何图标

    # 笨办法初始化允许的维修方案内容
    for mxp_name in allowed_mxps:
        mxp_name = mxp_name.lower()
        if mxp_name == 'as350':
            admin_obj.add_views(AS350View(
                mongodb, 'as350', AS350_NAME, category=category))
        elif mxp_name == 'bell206':
            admin_obj.add_views(BELL206View(
                mongodb, 'bell206', BELL206_NAME, category=category))
        elif mxp_name == 'bell407':
            admin_obj.add_views(BELL407View(
                mongodb, 'bell407', BELL407_NAME, category=category))
        elif mxp_name == 'bell429':
            admin_obj.add_views(BELL429View(
                mongodb, 'bell429', BELL429_NAME, category=category))
        elif mxp_name == 'da40d':
            admin_obj.add_views(DA40DView(
                mongodb, 'da40d', DA40D_NAME, category=category))
        elif mxp_name == 'r22':
            admin_obj.add_views(R22View(mongodb, 'r22', R22_NAME, category=category))
        elif mxp_name == 'r44':
            admin_obj.add_views(R44View(mongodb, 'r44', R44_NAME, category=category))
        elif mxp_name == 'swz269c1':
            admin_obj.add_views(SWZ269C1View(
                mongodb, 'swz269c1', SWZ269C1_NAME, category=category))
        elif mxp_name == 'y5b':
            admin_obj.add_views(Y5BView(mongodb, 'y5b', Y5B_NAME, category=category))
