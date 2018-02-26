# coding: utf-8

from __future__ import unicode_literals
from datetime import timedelta


def convert_hh_mm_to_float(ori):
    # 用于将飞行小时和发动机时间转换为对应的小时
    hours, minuts = ori.split(':')
    delta = timedelta(hours=int(hours), minutes=int(minuts))

    # 转为以小时计的单位
    return delta.total_seconds() / 3600
