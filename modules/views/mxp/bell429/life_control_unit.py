# coding: utf-8

from __future__ import unicode_literals

from modules.forms.bell429.time_control_unit import TimeControlUnitForm
from .tranlate_column import column_labels


def LifeControlUnit():
    return {
        '_api_url': '/v1/mxp/bell429/life-control-unit/',
        'column_list': [
            'id', 'ataCode', 'name', 'pn', 'description', 'interval',
            'relateDoc', 'remark', 'accessory'
        ],
        'column_labels': column_labels,
        'form': TimeControlUnitForm,
        'title': '时寿件',
        'coll_name': 'life_control_unit_bell429'
    }