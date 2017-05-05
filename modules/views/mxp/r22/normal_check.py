# coding: utf-8

from __future__ import unicode_literals

from modules.forms.r22.normal_check import NormalCheckForm
from .tranlate_column import column_labels


def NormalCheck():
    return {
        '_api_url': '/v1/mxp/r22/normal-check/',
        'column_list': ['id', 'category', 'description',
                        'relateDoc', 'remark', 'accessory'],
        'column_labels': column_labels,
        'form': NormalCheckForm,
        'title': '一般维修检查',
        'coll_name': 'normal_check_r22'
    }