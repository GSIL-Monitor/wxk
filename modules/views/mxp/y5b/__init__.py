# coding:utf-8

from .scheduled_mx_check import ScheduledMxCheck
from .flight_line_check import FlightLineCheck
from .parking_check import ParkingCheck
from .time_control_unit import TimeControlUnit
from .life_control_unit import LifeControlUnit

from ..base import MxpBaseView


class Y5BView(MxpBaseView):

    @property
    def view_list(self):
        return {
            'scheduled': dict(**ScheduledMxCheck()),
            'life-control': dict(**LifeControlUnit()),
            'flight-line-check': dict(**FlightLineCheck()),
            'parking-check': dict(**ParkingCheck()),
            'time-control-unit': dict(**TimeControlUnit()),
        }

    @property
    def default_subordinate_view(self):
        return 'scheduled'
