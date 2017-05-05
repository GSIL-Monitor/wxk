# coding: utf-8

from __future__ import unicode_literals

from .tranlate_column import column_labels
from modules.forms.as350.short_long_term_parking\
    import ShortLongTermParkingForm


def ShortLongTermParking():
    return {
        '_api_url': '/v1/mxp/as350/short-long-term-parking/',
        'column_list': [
            'id', 'category', 'description', 'interval',
            'relateDoc', 'remark', 'accessory'
        ],
        'column_labels': column_labels,
        'form': ShortLongTermParkingForm,
        'title': '短/长期停放检查',
        'coll_name': 'short_long_term_parking_as350',
    }
