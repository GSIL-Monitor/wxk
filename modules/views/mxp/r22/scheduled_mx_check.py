# coding: utf-8

from __future__ import unicode_literals

from modules.forms.r22.scheduled_mx_check import ScheduledMxCheckForm
from .tranlate_column import column_labels
from ..title import GeneralScheduledTitle


def ScheduledMxCheck():
    return {
        '_api_url': '/v1/mxp/r22/scheduled-mx-check/',
        'column_list': [
            'id', 'source', 'description', 'remark'
        ],
        'column_labels': column_labels,
        'form': ScheduledMxCheckForm,
        'title': GeneralScheduledTitle,
        'coll_name': 'scheduled_mx_check_r22'
    }
