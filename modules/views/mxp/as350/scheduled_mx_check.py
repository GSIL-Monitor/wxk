# coding: utf-8

from __future__ import unicode_literals

from .tranlate_column import column_labels
from modules.forms.as350.scheduled_mx_check import ScheduledMxCheckForm
from ..title import GeneralScheduledTitle


def ScheduledMxCheck():
    return {
        '_api_url': '/v1/mxp/as350/scheduled-mx-check/',
        'column_list': [
            'id', 'source', 'environmentCategory', 'ataCode',
            'description', 'remark', 'aircraftsSers', 'reference'
        ],
        'column_labels': column_labels,
        'form': ScheduledMxCheckForm,
        'title': GeneralScheduledTitle,
        'coll_name': 'scheduled_mx_check_as350',
    }
