# coding: utf-8

from __future__ import unicode_literals

from modules.forms.aircraft.flight_log import FlightLogForm
from modules.forms.aircraft.flight_log import Y5bForm
from modules.forms.aircraft.flight_log import AS350FlightLogForm

from .tranlate_column import column_labels


def FlightLog():
    return {
        '_api_url': '/v1/%(plane_type)sflightlog/',
        # 不同的机型这里要相应的扩展
        'form': {
            'y5b': Y5bForm,
            'bell206': FlightLogForm,
            'da40d': FlightLogForm,
            'as350': AS350FlightLogForm,
        },
        'title': '飞行日志',
        'coll_name': 'flight_log',
        'template': 'aircraft/flightlog.html',
        'column_list': [
            'id', 'departureTime', 'landingTime',
            'operation',
        ],
        'column_labels': column_labels,
        'details_columns': [
            'aircraftId', 'aircraftType', 'departureAirport', 'formMakeTime',
            'landingAirport', 'flightDate', 'captain', 'copilot', 'crew',
            'passengers', 'departureTime', 'landingTime', 'flightTime',
            'landings', 'remark', 'logTime', 'aircraftType', 'formMaker',
        ],
    }
