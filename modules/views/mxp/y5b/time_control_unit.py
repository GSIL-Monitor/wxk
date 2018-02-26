# coding: utf-8

from __future__ import unicode_literals

from modules.forms.y5b.time_control_unit import TimeControlUnitForm
from .tranlate_column import column_labels
from ..title import GeneralTimeControlTitle


def TimeControlUnit():
    return {
        '_api_url': '/v1/mxp/y5b/time-control-unit/',
        'column_list': [
            'id', 'source', 'name', 'pn', 'description', 'remark'
        ],
        'column_labels': column_labels,
        'form': TimeControlUnitForm,
        'title': GeneralTimeControlTitle,
        'coll_name': 'time_control_unit_y5b'
    }
