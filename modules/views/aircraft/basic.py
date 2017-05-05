# coding: utf-8

from __future__ import unicode_literals

from modules.forms.aircraft.aircraft import AircraftInformationForm


def Basic():
    return {
        '_api_url': '/v1/aircraft/',
        'form': AircraftInformationForm,
        'title': '基本信息',
        'coll_name': 'aircraft_information',
        'template': 'aircraft/basic.html',
    }
