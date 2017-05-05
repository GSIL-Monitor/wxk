# coding: utf-8

from __future__ import unicode_literals

from modules.forms.as350.time_control_unit import TimeControlUnitForm
from .tranlate_column import column_labels


def TimeControlUnit():
    return {
        '_api_url': '/v1/mxp/as350/time-control-unit/',
        'column_list': [
            'id', 'name', 'pn', 'description', 'interval',
            'relateDoc', 'remark', 'accessory', 'aircraftsSers', 'reference'
        ],
        'column_labels': column_labels,
        'form': TimeControlUnitForm,
        'title': '时控件',
        'coll_name': 'time_control_unit_as350',
    }
