# coding: utf-8

from __future__ import unicode_literals

from .tranlate_column import column_labels
from modules.forms.as350.po_unit import POUnitForm
from ..title import POUnitTitle


def POUnit():
    return {
        '_api_url': '/v1/mxp/as350/po-unit/',
        'column_list': [
            'id', 'description', 'remark', 'aircraftsSers', 'reference'
        ],
        'column_labels': column_labels,
        'form': POUnitForm,
        'title': POUnitTitle,
        'coll_name': 'po_unit_as350',
    }
