# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.airmaterial.airmaterial_list import AirmaterialList
from modules.views import CustomView


class _AirmaterialListView(CustomView):
    # 航材首页列表视图应显示的内容
    column_list = [
        'name', 'type', 'partNumber', 'sequenceNumber',
        'price', 'applicableModel', 'status',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'name': '名称',
        'type': '类别',
        'partNumber': '件号',
        'sequenceNumber': '序号',
        'price': '单价',
        'applicableModel': '适用机型',
        'status': '状态',
    }

    can_view = True

AirmaterialListView = partial(
    _AirmaterialListView, AirmaterialList, name='航材首页'
)
