# coding: utf-8

from __future__ import unicode_literals

from .tranlate_column import column_labels
from modules.forms.as350.flight_line_check import FlightLineCheckForm


def MaintainLog():
    return {
        '_api_url': '/v1/mxp/as350/flight-line-check/',
        'column_list': [
            'id', 'category', 'description',
            'relateDoc', 'remark', 'accessory', 'aircraftsSers', 'reference'
        ],
        'column_labels': column_labels,
        'form': FlightLineCheckForm,
        'title': '维修日志',
        'coll_name': 'flight_line_check_as350',
    }
