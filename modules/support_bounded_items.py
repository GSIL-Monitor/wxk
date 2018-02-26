# coding: utf-8

from __future__ import unicode_literals
import copy

from modules.views.mxp.title import *


# WUJG: 注意，下面的主键不能随便定义，必须与API端相符，具体请联系
# 机务通用REST API接口的开发人员
# 第三个参数表示是否具有时间间隔内容
common = [
    ('scheduled', GeneralScheduledTitle, True),
    ('timecontrol', GeneralTimeControlTitle, True),
    ('lifecontrol', GeneralLifeControlTitle, True),
    ('flightline', GeneralFlightLineTitle, False),
    ('unscheduled', GeneralUnscheduledTitle, False),
]

r_serial = copy.deepcopy(common)
del r_serial[3]
r_serial.append(('special', SpecialTitle, False))
r_serial.append(('normal', NormalTitle, False))


as_serial = copy.deepcopy(common)
as_serial.append(('pounit', POUnitTitle, False))
as_serial.append(('shortlongtermparking', ShortLongTitle, False))

y5b = copy.deepcopy(common)
del y5b[4]
y5b.append(('parking', ParkingCheckTitle, False))


support_due_list = {
    'da40d': common,
    'as350': as_serial,
    'bell206': common,
    'bell407': common,
    'bell429': common,
    'r22': r_serial,
    'r44': r_serial,
    'y5b': y5b,
}
