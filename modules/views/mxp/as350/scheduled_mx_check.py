# coding: utf-8

from __future__ import unicode_literals

from .tranlate_column import column_labels
from modules.forms.as350.scheduled_mx_check import ScheduledMxCheckForm


def ScheduledMxCheck():
    return {
        '_api_url': '/v1/mxp/as350/scheduled-mx-check/',
        'column_list': [
            'id', 'source', 'environmentCategory', 'ataCode',
            'rii', 'forceExec', 'description', 'interval',
            'relateDoc', 'remark', 'accessory', 'aircraftsSers', 'reference'
        ],
        'column_labels': column_labels,
        'form': ScheduledMxCheckForm,
        'title': '定期维修检查',
        'coll_name': 'scheduled_mx_check_as350',
    }
