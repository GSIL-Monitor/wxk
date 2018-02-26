# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.malfuncture_statistics import MalfunctureStatistics
from modules.views import CustomView


class _MalfunctureStatisticsView(CustomView):
    # 故障统计列表视图应显示的内容
    column_list = [
        'statisDate', 'feiliNum', 'checkType', 'statisFrom', 'ataNum',
    ]
    # 对应内容的中文翻译
    column_labels = {
        'statisDate': '故障日期',
        'feiliNum': '飞机号',
        'checkType': '检查类别',
        'statisFrom': '故障来源',
        'ataNum': 'ATA章节号',
    }


MalfunctureStatisticsView = partial(
    _MalfunctureStatisticsView, MalfunctureStatistics, name='故障统计'
)
