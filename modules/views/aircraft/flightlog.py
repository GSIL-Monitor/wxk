# coding: utf-8

from __future__ import unicode_literals

from modules.forms.aircraft.flight_log import FlightLogForm


def FlightLog():
    return {
        '_api_url': '/v1/flightlog/',
        'form': FlightLogForm,
        'title': '飞行日志',
        'coll_name': 'aircraft_information',
        'template': 'aircraft/flightlog.html',
    }
