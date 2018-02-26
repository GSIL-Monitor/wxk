# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.oil_sample_detection import OilSampleDetection
from modules.views import CustomView


class _OilSampleDetectionView(CustomView):
    # 油样检测列表视图应显示的内容
    column_list = [
        'id', 'oilName', 'banbenTime', 'statusName',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'id': '编号',
        'oilName': '油样名称',
        'banbenTime': '报告日期',
        'statusName': '状态',
    }


OilSampleDetectionView = partial(
    _OilSampleDetectionView, OilSampleDetection, name='油样检测'
)
