# encoding: utf-8

from __future__ import unicode_literals
import json

from wtforms import form
from wtforms.fields import IntegerField
from wtforms.compat import iteritems
from werkzeug import MultiDict
from werkzeug.datastructures import FileStorage
from qiniu import put_data

from modules.proxy import proxy
from util.fields import (BasicIntervalField, SpecailIntervalField,
                         BasicStartTrackingField, SpecialStartTrackingField,
                         BasicRadioIntervalField, SpecailRadioIntervalField,
                         AccessoryFileuploadField, RelateDocField)


class IntervalDescForm(form.Form):

    type_value = {'hours': 0, 'times': 1, 'date': None,
                  'retire': 5, 'torque': 6, 'gasifier': 7,
                  'turbo': 8, 'engine': 9}

    hours = BasicIntervalField('飞行小时')
    times = BasicIntervalField('起落次数')
    date = SpecailIntervalField('日历时间')

    def update_data(self, form_data, type, name, off_set_type=None):
        value = form_data.getlist('{}-value'.format(name))[0]
        max = form_data.getlist('{}-max'.format(name))[0]
        min = form_data.getlist('{}-min'.format(name))[0]
        if off_set_type is None:
            data = {'type': type, 'value': value, 'min': min, 'max': max}
        else:
            data = {'type': type, 'value': value,
                    'min': min, 'max': max, 'offsetType': off_set_type}
        return data

    def process(self, formdata=None, obj=None, data=None, **kwargs):

        if formdata:
            temp_data = {}
            for key in self._fields.keys():
                name = '{}{}'.format(self._prefix, key)
                type = self.type_value.get(key)
                if type is not None:
                    try:
                        temp_data[name] = self.update_data(formdata, type, name)
                    except:
                        temp_data[name] = None
                else:
                    try:
                        type = formdata.getlist('{}-type'.format(name))[0]
                        off_set_type = formdata.getlist(
                            '{}-offsetType'.format(name))[0]
                        temp_data[name] = self.update_data(
                            formdata, type, name, off_set_type)
                    except:
                        temp_data[name] = None
            formdata = MultiDict(temp_data)

        if obj is not None:
            class Temp:
                pass
            for x in obj:
                x_type = x.get('type')
                y_type = self.type_value.values()
                if x_type in y_type:
                    for y in self.type_value.keys():
                        if x_type == self.type_value[y]:
                            setattr(Temp, y, x)
                else:
                    setattr(Temp, 'date', x)
                super(IntervalDescForm, self).process(formdata, Temp, data)
        else:
            super(IntervalDescForm, self).process(formdata, obj, data)

    @property
    def data(self):

        data_list = []

        for name, f in iteritems(self._fields):
            if f.data is not None:
                for key in f.data:
                    # WUJG: 如果对应的值为空字符串或其他逻辑错的内容，我们可以默认设置为0
                    if key != 'type' and key != 'offsetType':
                        f.data[key] = float(f.data[key] or 0)
                    else:
                        f.data[key] = int(f.data[key] or 0)
                data_list.append(f.data)
        return data_list


class IntervalRadioDescForm(IntervalDescForm):

    hours = BasicRadioIntervalField('飞行小时')
    times = BasicRadioIntervalField('起落次数')
    date = SpecailRadioIntervalField('间隔值')


class As350IntervalDescForm(IntervalDescForm):

    torque = BasicIntervalField('扭矩循环次数')
    gasifier = BasicIntervalField('燃气发生器循环数')
    turbo = BasicIntervalField('动力涡轮循环数')


class BellIntervalDescForm(IntervalDescForm):

    retire = BasicIntervalField('退役指数')


class Y5BIntervalDescForm(IntervalDescForm):

    engine = BasicIntervalField('发动机时间')


class RelateDocForm(form.Form):

    relate = RelateDocField('文档')

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        if formdata:
            files = formdata.getlist('doc_files')[0]
            key = self._fields.keys()[0]
            name = '{}{}'.format(self._prefix, key)
            if files:
                files = json.loads(files)
                formdata = MultiDict({name: files})

        if obj and not formdata:

            class Temp:
                pass

            setattr(Temp, 'relate', obj)
            obj = Temp
        super(RelateDocForm, self).process(formdata, obj, data)

    @property
    def data(self):
        for name, f in iteritems(self._fields):
            return f.data


class TrackingDescForm(form.Form):

    type_value = {'time': 0, 'count': 1, 'date': None}

    time = BasicStartTrackingField('开始时间')
    count = BasicStartTrackingField('开始次数')
    date = SpecialStartTrackingField('开始日期')

    def process(self, formdata=None, obj=None, data=None, **kwargs):

        if formdata:
            form_data = {}
            for key in self._fields.keys():
                field_name = '{}{}'.format(self._prefix, key)
                field_value = '{}-value'.format(field_name)
                type = self.type_value.get(key)
                if type is not None:
                    try:
                        value = formdata.getlist(field_value)[0]
                        form_data[field_name] = {
                            'type': int(type), 'value': float(value)}
                    except:
                        form_data[field_name] = None
                else:
                    try:
                        field_type = '{}-type'.format(field_name)
                        type = formdata.getlist(field_type)[0]
                        value = formdata.getlist(field_value)[0]
                        form_data[field_name] = {
                            'type': int(type), 'value': float(value)}
                    except:
                        form_data[field_name] = None
            formdata = MultiDict(form_data)

        if obj is not None:
            if len(obj) != 0:
                obj = obj[0]

                class Temp:
                    pass

                type = obj.get('type')
                if type in self.type_value.values():
                    for key in self._fields.keys():
                        if self.type_value[key] == type:
                            setattr(Temp, key, obj)
                else:
                    setattr(Temp, 'date', obj)
                obj = Temp

        super(TrackingDescForm, self).process(formdata, obj, data, **kwargs)

    @property
    def data(self):
        for name, f in iteritems(self._fields):
            if f.data is not None:
                return [f.data]


class AccessoryFileForm(form.Form):

    acce = AccessoryFileuploadField('名称')

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        if formdata:
            acce = formdata.getlist('accessory-acce')[0]
            if acce.filename == '':
                try:
                    acce = formdata.getlist('accessory-old')[0]
                except:
                    acce = None
            form_data = {'accessory-acce': acce}
            formdata = MultiDict(form_data)

        if obj is not None and len(obj) != 0:
            class Temp:
                pass
            setattr(Temp, 'acce', obj[0])
            obj = Temp
        super(AccessoryFileForm, self).process(formdata, obj, data, **kwargs)

    def _save_file(self, data, file_name=None):
        if file_name:
            info = {"docType": "维修方案",
                    "fileName": file_name}
            url = "/v1/file-access/upload"
            resp = proxy.create(info, url)
            try:
                self.token = resp.json().get("token")
                self.key = resp.json().get("key")
                self.save_key = resp.json().get("saveKey")
                ret, info = put_data(self.token, self.key, data)
            except:
                raise Exception("Please contact the service maintainer.")

    @property
    def data(self):
        for name, f in iteritems(self._fields):
            if f.data is not None:
                if isinstance(f.data, FileStorage):
                    file_name = f.data.filename
                    self._save_file(f.data, file_name)
                    return [{'name': file_name, 'key': self.save_key}]
                else:
                    return [f.data]
