# coding:utf-8
# 工程技术范畴下的各模块视图定义

from .scrap_sheet import ScrapSheetView
from .reserved_fault import ReservedFaultView


__all__ = ['views']


views = [
    ScrapSheetView, ReservedFaultView
]
