# coding: utf-8

from __future__ import unicode_literals

from modules.forms.bell407.flight_line_check import FlightLineCheckForm
from .tranlate_column import column_labels


def FlightLineCheck():
    return {
        '_api_url': '/v1/mxp/bell407/flight-line-check/',
        'column_list': [
            'id', 'category', 'description',
            'relateDoc', 'remark', 'accessory',
        ],
        'column_labels': column_labels,
        'form': FlightLineCheckForm,
        'title': '航线检查',
        'coll_name': 'flight_line_check_bell407',
    }
