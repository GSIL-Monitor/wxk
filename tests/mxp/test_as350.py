# coding: utf-8

from __future__ import unicode_literals

import unittest

from modules.views.mxp.as350 import (ScheduledMxCheckView, POUnitView,
                                     FlightLineCheckView,
                                     UnscheduledMxCheckView,
                                     TimeControlUnitView,
                                     LifeControlUnitView,
                                     ShortLongTermParkingView)
from suite import MxpTestCase

scheduled_test_value = {
    'id': 'wcg2000',
    'source': 'AMM',
    'environmentCategory': '正常环境',
    'ataCode': 0,
    'description': 'wcg200',
    'rii': 'y',
    'interval-0-value': 120,
    'interval-0-min': 0,
    'interval-0-max': 0,
    'remark': 'wcg2000',
    'interval-0-type': 0,
}

po_unit_test_value = {
    'id': 'wcg2000',
    'description': 'wcg200',
    'interval-0-value': 120,
    'interval-0-min': 0,
    'interval-0-max': 0,
    'remark': 'wcg2000',
    'interval-0-type': 0,
    'ataCode': 0,
}

flight_line_test_value = {
    'id': 'wcg2000',
    'category': '航前检查',
    'description': 'wcg200',
    'remark': 'wcg2000',
}

unscheduled_test_value = {
    'id': 'wcg2000',
    'category': '发动机',
    'description': 'wcg200',
    'remark': 'wcg2000',
}

time_control_test_value = {
    'id': 'wcg2000',
    'name': 'wcg200',
    'pn': 'wcg200',
    'interval-0-value': 120,
    'interval-0-min': 0,
    'interval-0-max': 0,
    'description': 'wcg2000',
    'interval-0-type': 0,
    'remark': 'wcg2000',
}

life_control_test_value = {
    'id': 'wcg2000',
    'name': 'wcg200',
    'pn': 'wcg200',
    'interval-0-value': 120,
    'interval-0-min': 0,
    'interval-0-max': 0,
    'description': 'wcg2000',
    'interval-0-type': 0,
    'remark': 'wcg2000',
}

short_long_term_parking_test_value = {
    'id': 'wcg2000',
    'category': '<1个月',
    'description': 'wcg2000',
    'remark': 'wcg2000',
}


class AS350TestCase(MxpTestCase):

    def test_scheduled_create_view(self):
        rv_data = self._create_view(scheduled_test_value, ScheduledMxCheckView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_scheduled_update_view(self):
        rv_data = self._edit_view(scheduled_test_value, ScheduledMxCheckView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_schedule_delete_view(self):
        rv_data = self._delete_view(scheduled_test_value, ScheduledMxCheckView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_po_unit_create_view(self):
        rv_data = self._create_view(po_unit_test_value, POUnitView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_po_unit_update_view(self):
        rv_data = self._edit_view(po_unit_test_value, POUnitView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_po_unit_delete_view(self):
        rv_data = self._delete_view(po_unit_test_value, POUnitView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_fligt_line_create_view(self):
        rv_data = self._create_view(flight_line_test_value,
                                    FlightLineCheckView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_fligt_line_update_view(self):
        rv_data = self._edit_view(flight_line_test_value,
                                  FlightLineCheckView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_fligt_line_delete_view(self):
        rv_data = self._delete_view(flight_line_test_value,
                                    FlightLineCheckView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_unscheduled_create_view(self):
        rv_data = self._create_view(unscheduled_test_value,
                                    UnscheduledMxCheckView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_unscheduled_update_view(self):
        rv_data = self._edit_view(unscheduled_test_value,
                                  UnscheduledMxCheckView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_unscheduled_delete_view(self):
        rv_data = self._delete_view(unscheduled_test_value,
                                    UnscheduledMxCheckView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_time_control_unit_create_view(self):
        rv_data = self._create_view(time_control_test_value,
                                    TimeControlUnitView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_time_control_unit_update_view(self):
        rv_data = self._edit_view(time_control_test_value,
                                  TimeControlUnitView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_time_control_unit_delete_view(self):
        rv_data = self._delete_view(time_control_test_value,
                                    TimeControlUnitView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_life_control_unit_create_view(self):
        rv_data = self._create_view(life_control_test_value,
                                    LifeControlUnitView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_life_control_unit_update_view(self):
        rv_data = self._edit_view(life_control_test_value,
                                  LifeControlUnitView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_life_control_unit_delete_view(self):
        rv_data = self._delete_view(life_control_test_value,
                                    LifeControlUnitView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_short_long_term_parking_create_view(self):
        rv_data = self._create_view(short_long_term_parking_test_value,
                                    ShortLongTermParkingView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_short_long_term_parking_update_view(self):
        rv_data = self._edit_view(short_long_term_parking_test_value,
                                  ShortLongTermParkingView)
        assert 'successfully'.encode('utf-8') in rv_data

    def test_short_long_term_parking_delete_view(self):
        rv_data = self._delete_view(short_long_term_parking_test_value,
                                    ShortLongTermParkingView)
        assert 'successfully'.encode('utf-8') in rv_data


if __name__ == '__main__':
    unittest.main()
