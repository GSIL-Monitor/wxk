# coding: utf-8

from __future__ import unicode_literals

from modules.forms.swz269c1.time_control_unit import TimeControlUnitForm
from .tranlate_column import column_labels
from ..title import GeneralTimeControlTitle


def TimeControlUnit():
    return {
        '_api_url': '/v1/mxp/swz269c1/time-control-unit/',
        'column_list': [
            'id', 'name', 'pn', 'description', 'remark'
        ],
        'column_labels': column_labels,
        'form': TimeControlUnitForm,
        'title': GeneralTimeControlTitle,
        'coll_name': 'time_control_unit_swz269c1'
    }
