# coding: utf-8

from __future__ import unicode_literals

from modules.forms.y5b.parking_check import ParkingCheckForm

from ..title import ParkingCheckTitle
from .tranlate_column import column_labels


def ParkingCheck():

    return {
        '_api_url': '/v1/mxp/y5b/parking-check/',
        'column_list': [
            'id', 'source', 'description', 'remark'
        ],
        'column_labels': column_labels,
        'form': ParkingCheckForm,
        'title': ParkingCheckTitle,
        'coll_name': 'parking_mx_check_y5b'
    }
