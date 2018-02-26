# coding: utf-8

from __future__ import unicode_literals


from util.api_request import WXKAPIProxy


# 提供一个兼容于Flask扩展的实现，其他模块可以直接使用该全局实例
proxy = WXKAPIProxy()


