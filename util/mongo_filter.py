# coding: utf-8

from __future__ import unicode_literals

from flask_babelex import lazy_gettext
from flask_admin.contrib.pymongo.filters import BasePyMongoFilter


# 对原pymongo的基本扩展

class FilterGreaterEqual(BasePyMongoFilter):
    def apply(self, query, value):
        try:
            value = float(value)
        except ValueError:
            value = 0
        query.append({self.column: {'$gte': value}})
        return query

    def operation(self):
        return lazy_gettext('greater equal than')


class FilterSmallerEqual(BasePyMongoFilter):
    def apply(self, query, value):
        try:
            value = float(value)
        except ValueError:
            value = 0
        query.append({self.column: {'$lte': value}})
        return query

    def operation(self):
        return lazy_gettext('smaller equal than')
