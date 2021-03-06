# coding: utf-8

from __future__ import unicode_literals

from modules.forms.da40d.scheduled_mx_check import ScheduledMxCheckForm
from .tranlate_column import column_labels
from ..title import GeneralScheduledTitle


def ScheduledMxCheck():
    return {
        '_api_url': '/v1/mxp/da40d/scheduled-mx-check/',
        'column_list': [
            'id', 'source', 'ataCode', 'area', 'description', 'remark'
        ],
        'column_labels': column_labels,
        'form': ScheduledMxCheckForm,
        'title': GeneralScheduledTitle,
        'coll_name': 'scheduled_mx_check_da40d'
    }
