# coding: utf-8

from __future__ import unicode_literals

from .tranlate_column import column_labels
from modules.forms.as350.po_unit import POUnitForm


def POUnit():
    return {
        '_api_url': '/v1/mxp/as350/po-unit/',
        'column_list': [
            'id', 'description', 'interval',
            'relateDoc', 'remark', 'accessory',
            'aircraftsSers', 'reference'
        ],
        'column_labels': column_labels,
        'form': POUnitForm,
        'title': 'PO部件检查',
        'coll_name': 'po_unit_as350',
    }
