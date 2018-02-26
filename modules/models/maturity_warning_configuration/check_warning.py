# coding: utf-8

from __future__ import unicode_literals

import json


class CheckWarning(object):

    key = 'checkwarning'

    def __init__(self, cache, key=None):
        self.cache = cache
        if key:
            self.key = key

    def get_form(self, form):
        self.form = form
        self.form_data = self.form.data

    def get_value(self):
        level_map = {'lv1': '_yellow', 'lv2': '_orange', 'lv3': '_red'}
        items = self.cache.get(self.key)
        if not items:
            for field in self.form._fields:
                if 'type' not in field:
                    setattr(self, field, None)
        else:
            items = json.loads(items)
            for item in items:
                end_f = level_map[item]
                try:
                    setattr(self, '{}{}'.format(
                        'warningfiled', end_f), items[item])
                except:
                    setattr(self, '{}{}'.format('warning_filed', end_f), None)

    def set_redis_value(self, field_name):
        level_map = {'yellow': 'lv1', 'orange': 'lv2', 'red': 'lv3'}
        field, level = field_name.split('_')
        setattr(self, field_name, self.form_data.get(field_name))
        return {level_map[level]: getattr(self, field_name)}

    def set_warning(self):
        warnings = {}
        for field in self.form._fields:
            if 'type' not in field:
                warn = self.set_redis_value(field)
                warn_type = warn.keys()[0]
                if warn_type in warnings:
                    warnings[warn_type].update(warn[warn_type])
                else:
                    warnings.update(warn)
        warnings = json.dumps(warnings)
        self.cache.set(self.key, warnings)
        self.cache._user_cache.set(self.key, warnings)
        return warnings

    def out_put(self):
        for field in self.form._fields:
            if 'type' not in field:
                setattr(getattr(self.form, field), 'data', getattr(self, field))

    @staticmethod
    def get_predict_boundary(warn_type):
        pass
