# coding:utf-8

from .scheduled_mx_check import ScheduledMxCheck
from .flight_line_check import FlightLineCheck
from .unscheduled_mx_check import UnscheduledMxCheck
from .time_control_unit import TimeControlUnit
from .life_control_unit import LifeControlUnit

from ..base import MxpBaseView


class BELL429View(MxpBaseView):

    @property
    def view_list(self):
        # 每一个具体的子方案在界面视图处理时应该提供下面的信息
        # 1. 子方案的名称
        # 2. 子方案对应的主键
        # 3. 子方案的集合名称（mongo）
        # 4. 一些与flask-admin相关的视图配置信息
        return {
            'scheduled': dict(**ScheduledMxCheck()),
            'life-control': dict(**LifeControlUnit()),
            'flight-line-check': dict(**FlightLineCheck()),
            'unsheduled-mx-check': dict(**UnscheduledMxCheck()),
            'time-control-unit': dict(**TimeControlUnit()),
        }

    @property
    def default_subordinate_view(self):
        return 'scheduled'
