# coding: utf-8

from __future__ import unicode_literals

from modules.forms.as350.unscheduled_mx_check import UnscheduledMxCheckForm
from .tranlate_column import column_labels
from ..title import GeneralUnscheduledTitle


def UnscheduledMxCheck():
    return {
        '_api_url': '/v1/mxp/as350/unscheduled-mx-check/',
        'column_list': [
            'id', 'category', 'description', 'remark', 'aircraftsSers', 'reference'
        ],
        'column_labels': column_labels,
        'form': UnscheduledMxCheckForm,
        'title': GeneralUnscheduledTitle,
        'coll_name': 'unscheduled_mx_check_as350',
    }
