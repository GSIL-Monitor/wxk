# coding: utf-8

from __future__ import unicode_literals

from modules.forms.r44.scheduled_mx_check import ScheduledMxCheckForm
from .tranlate_column import column_labels


def ScheduledMxCheck():
    return {
        '_api_url': '/v1/mxp/r44/scheduled-mx-check/',
        'column_list': [
            'id', 'source', 'rii', 'forceExec', 'description',
            'interval', 'relateDoc', 'remark', 'accessory'
        ],
        'column_labels': column_labels,
        'form': ScheduledMxCheckForm,
        'title': '定期维修检查',
        'coll_name': 'scheduled_mx_check_r44'
    }
