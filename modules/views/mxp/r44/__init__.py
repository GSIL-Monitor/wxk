# coding:utf-8

from .scheduled_mx_check import ScheduledMxCheck
from .unscheduled_mx_check import UnscheduledMxCheck
from .time_control_unit import TimeControlUnit
from .life_control_unit import LifeControlUnit
from .normal_check import NormalCheck
from .special_check import SpecialCheck

from ..base import MxpBaseView


class R44View(MxpBaseView):

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
            'unsheduled-mx-check': dict(**UnscheduledMxCheck()),
            'time-control-unit': dict(**TimeControlUnit()),
            'normai-check': dict(**NormalCheck()),
            'special-check': dict(**SpecialCheck())
        }

    @property
    def default_subordinate_view(self):
        return 'scheduled'
