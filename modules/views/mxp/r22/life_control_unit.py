# coding: utf-8

from __future__ import unicode_literals

from modules.forms.r22.life_control_unit import LifeControlUnitForm
from .tranlate_column import column_labels
from ..title import GeneralLifeControlTitle


def LifeControlUnit():
    return {
        '_api_url': '/v1/mxp/r22/life-control-unit/',
        'column_list': [
            'id', 'name', 'pn', 'description', 'remark'
        ],
        'column_labels': column_labels,
        'form': LifeControlUnitForm,
        'title': GeneralLifeControlTitle,
        'coll_name': 'life_control_unit_r22'
    }
