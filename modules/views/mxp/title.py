# encoding: utf-8

from __future__ import unicode_literals

# 多数情况下，定制实现根据需要应该更改此处的内容
__all__ = [
    'GeneralScheduledTitle', 'GeneralUnscheduledTitle',
    'GeneralFlightLineTitle', 'GeneralLifeControlTitle',
    'GeneralTimeControlTitle', 'NormalTitle',
    'SpecialTitle', 'POUnitTitle', 'ShortLongTitle',
    'ParkingCheckTitle',
]

GeneralScheduledTitle = '定期维修检查'
GeneralUnscheduledTitle = '非定期/特殊检查'
GeneralFlightLineTitle = '航线检查'
GeneralLifeControlTitle = '时寿件'
GeneralTimeControlTitle = '时控件'

NormalTitle = '一般维修检查'
SpecialTitle = '特殊维修检查'

POUnitTitle = 'PO部件检查'
ShortLongTitle = '短/长期停放检查'

ParkingCheckTitle = '停放检查'
