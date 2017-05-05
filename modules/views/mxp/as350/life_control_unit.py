# coding: utf-8

from __future__ import unicode_literals

from .tranlate_column import column_labels
from modules.forms.as350.life_control_unit import LifeControlUnitForm


def LifeControlUnit():
    return {
        '_api_url': '/v1/mxp/as350/life-control-unit/',
        'column_list': [
            'id', 'name', 'pn',
            'description', 'interval', 'relateDoc',
            'remark', 'accessory', 'aircraftsSers', 'reference'
        ],
        'column_labels': column_labels,
        'form': LifeControlUnitForm,
        'title': '时寿件',
        'coll_name': 'life_control_unit_as350',
    }
