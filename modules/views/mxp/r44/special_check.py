# coding: utf-8

from __future__ import unicode_literals

from modules.forms.r44.special_check import SpecialCheckForm
from .tranlate_column import column_labels


def SpecialCheck():
    return {
        '_api_url': '/v1/mxp/r44/special-check/',
        'column_list': [
            'id', 'category', 'description',
            'relateDoc', 'remark', 'accessory'
        ],
        'column_labels': column_labels,
        'form': SpecialCheckForm,
        'title': '特殊维修检查',
        'coll_name': 'special_check_r44'
    }
