# coding: utf-8

from __future__ import unicode_literals

import json


class StockWarning(object):

    key = 'stockwarning'

    def __init__(self, cache):
        self.cache = cache

    def get_form(self, form):
        self.form = form
        self.form_data = self.form.data

    def get_value(self):
        level_map = {'lv1': '_yellow', 'lv2': '_orange', 'lv3': '_red'}
        items = self.cache.get(StockWarning.key)
        if not items:
            for field in self.form._fields:
                if 'type' not in field:
                    setattr(self, field, None)
        else:
            items = json.loads(items)
            for item in items:
                for key in items[item]:
                    end_f = level_map[key]
                    try:
                        setattr(self, '{}{}'.format(
                            item + 'warningfiled', end_f), items[item][key])
                    except:
                        setattr(self, '{}{}'.format(
                            item + 'warningfiled', end_f), None)

    def set_redis_value(self, field_name):
        field_map = {'chemicalwarningfiled': 'chemical',
                     'consumewarningfiled': 'consume'}
        level_map = {'yellow': 'lv1', 'orange': 'lv2', 'red': 'lv3'}
        field, level = field_name.split('_')
        setattr(self, field_name, self.form_data.get(field_name))
        return {field_map[field]: {level_map[level]: getattr(self, field_name)}}

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
        self.cache.set(StockWarning.key, warnings)
        self.cache._user_cache.set(StockWarning.key, warnings)
        return warnings

    def out_put(self):
        for field in self.form._fields:
            if 'type' not in field:
                setattr(getattr(self.form, field), 'data', getattr(self, field))

    @staticmethod
    def get_predict_boundary(warn_type):
        pass
