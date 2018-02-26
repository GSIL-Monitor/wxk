# coding: utf-8

from __future__ import unicode_literals

import json


class EarlyWarning(object):

    key = 'predict'

    def __init__(self, cache):
        self.cache = cache

    def get_form(self, form):
        self.form = form
        self.form_data = self.form.data

    def get_value(self):
        type_map = {0: 'time', 1: 'times', 2: 'date', 9: 'hours'}
        level_map = {'lv1': '_fl', 'lv2': '_sl', 'lv3': '_tl'}
        items = self.cache.get(EarlyWarning.key)
        if not items:
            for field in self.form._fields:
                if 'type' not in field:
                    setattr(self, field, None)
        else:
            items = json.loads(items)
            for item in items:
                field = type_map[int(item)]
                for il in items[item]:
                    end_f = level_map[il]
                    try:
                        setattr(self, '{}{}'.format(field, end_f), items[item][il])
                    except:
                        setattr(self, '{}{}'.format(field, end_f), None)

    def set_redis_value(self, field_name):
        field_map = {'time': 0, 'times': 1, 'date': 2, 'hours': 9}
        level_map = {'fl': 'lv1', 'sl': 'lv2', 'tl': 'lv3'}
        field, level = field_name.split('_')
        f_type = field_map[field]
        setattr(self, field_name, self.form_data.get(field_name))
        return {f_type: {level_map[level]: getattr(self, field_name)}}

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
        self.cache.set(EarlyWarning.key, warnings)
        self.cache._user_cache.set(EarlyWarning.key, warnings)
        return warnings

    def out_put(self):
        for field in self.form._fields:
            if 'type' not in field:
                setattr(getattr(self.form, field), 'data', getattr(self, field))

    @staticmethod
    def get_predict_boundary(warn_type):
        items = self.cache.get(EarlyWarning.key)
        if items:
            return None
        items = json.loads(items)
        warnings = items.get(str(warn_type))
        l1 = warnings.get("lv1")
        l2 = warnings.get("lv2")
        l3 = warnings.get("lv3")
        return (l1, l2, l3)
