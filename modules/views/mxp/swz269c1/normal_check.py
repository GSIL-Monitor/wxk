# coding: utf-8

from __future__ import unicode_literals

from modules.forms.swz269c1.normal_check import NormalCheckForm
from .tranlate_column import column_labels
from ..title import NormalTitle


def NormalCheck():
    return {
        '_api_url': '/v1/mxp/swz269c1/normal-check/',
        'column_list': [
            'id', 'category', 'description', 'remark'],
        'column_labels': column_labels,
        'form': NormalCheckForm,
        'title': NormalTitle,
        'coll_name': 'normal_check_swz269c1'
    }
