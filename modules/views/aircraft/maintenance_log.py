# coding: utf-8

from __future__ import unicode_literals

from modules.forms.aircraft.maintenance_log import MaintenanceLogForm
from .tranlate_column import column_labels


def MaintenanceLog():
    return {
        '_api_url': '/v1/%(plane_type)smaintenancelog/',
        'column_list': [
            'type', 'description', 'completeDate', 'generateTime'
        ],
        'column_labels': column_labels,
        'form': MaintenanceLogForm,
        'title': '维修日志',
        'template': 'aircraft/maintenancelog.html',
        'coll_name': 'maintenance_log',
    }
