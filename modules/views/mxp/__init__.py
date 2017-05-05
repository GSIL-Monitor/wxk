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


AS350_NAME = 'AS350'
BELL206_NAME = 'BELL206'
BELL407_NAME = 'BELL407'
BELL429_NAME = 'BELL429'
R22_NAME = 'R22'
R44_NAME = 'R44'
DA40D_NAME = 'DA40D'
SWZ269C1_NAME = 'SWZ269c1'


def init_mxp_view(admin_obj, mongodb, category):
    # WUJG: 暂时不为各方案提供任何图标

    admin_obj.add_views(AS350View(
        mongodb, 'as350', AS350_NAME, category=category))
    admin_obj.add_views(BELL206View(
        mongodb, 'bell206', BELL206_NAME, category=category))
    admin_obj.add_views(BELL407View(
        mongodb, 'bell407', BELL407_NAME, category=category))
    admin_obj.add_views(BELL429View(
        mongodb, 'bell429', BELL429_NAME, category=category))
    admin_obj.add_views(DA40DView(
        mongodb, 'da40d', DA40D_NAME, category=category))
    admin_obj.add_views(R22View(mongodb, 'r22', R22_NAME, category=category))
    admin_obj.add_views(R44View(mongodb, 'r44', R44_NAME, category=category))
    admin_obj.add_views(SWZ269C1View(
        mongodb, 'swz269c1', SWZ269C1_NAME, category=category))
