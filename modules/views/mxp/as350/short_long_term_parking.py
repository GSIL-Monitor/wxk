# coding: utf-8

from __future__ import unicode_literals

from .tranlate_column import column_labels
from modules.forms.as350.short_long_term_parking import ShortLongTermParkingForm
from ..title import ShortLongTitle


def ShortLongTermParking():
    return {
        '_api_url': '/v1/mxp/as350/short-long-term-parking/',
        'column_list': [
            'id', 'category', 'description', 'remark'
        ],
        'column_labels': column_labels,
        'form': ShortLongTermParkingForm,
        'title': ShortLongTitle,
        'coll_name': 'short_long_term_parking_as350',
    }
