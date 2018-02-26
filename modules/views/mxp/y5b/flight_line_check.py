# coding: utf-8

from __future__ import unicode_literals

from modules.forms.y5b.flight_line_check import FlightLineCheckForm
from .tranlate_column import column_labels
from ..title import GeneralFlightLineTitle


def FlightLineCheck():
    return {
        '_api_url': '/v1/mxp/y5b/flight-line-check/',
        'column_list': [
            'id', 'source', 'description', 'remark'],
        'column_labels': column_labels,
        'form': FlightLineCheckForm,
        'title': GeneralFlightLineTitle,
        'coll_name': 'flight_line_check_y5b'
    }
