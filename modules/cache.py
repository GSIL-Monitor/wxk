# encoding: utf-8

from __future__ import unicode_literals

from flask_caching import Cache


# 一些特定视图或接口可以使用cache来优化性能
cache = Cache()
