# coding: utf-8

from __future__ import unicode_literals

from modules.forms.bell206.unscheduled_mx_check import UnscheduledMxCheckForm
from .tranlate_column import column_labels


def UnscheduledMxCheck():
    return {
        '_api_url': '/v1/mxp/da40d/unscheduled-mx-check/',
        'column_list': [
            'id', 'category', 'description',
            'relateDoc', 'remark', 'accessory',
        ],
        'column_labels': column_labels,
        'form': UnscheduledMxCheckForm,
        'title': '非定期/特殊检查',
        'coll_name': 'unscheduled_mx_check_da40d'
    }
