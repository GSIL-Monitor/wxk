# encoding: utf-8

from __future__ import unicode_literals

from wtforms import fields

from ..widgets.interval import BasicIntervalInput, SpecialIntervalInput
from wtforms.utils import unset_value


class BasicIntervalField(fields.Field):

    # TODO: 有的界面需要设置multiple参数为False
    widget = BasicIntervalInput()

    def get_keys(self):
        return ["{}-{}".format(self.name, x) for x in ("value", "max", "min")]

    def process(self, formdata, data=unset_value):
        self.process_errors = []

        if data is unset_value:
            try:
                data = self.default()
            except TypeError:
                data = self.default

        self.object_data = data

        try:
            self.process_data(data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

        if formdata:
            keys = self.get_keys()
            values = []
            for key in keys:
                try:
                    if key in formdata:
                        values.append({key: formdata.getlist(key)[0]})
                except ValueError as e:
                    self.process_errors.append(e.args[0])
            self.raw_data = values
            self.process_formdata(self.raw_data)

    def process_formdata(self, valuelist):

        if valuelist:
            self.data = valuelist
        else:
            self.data = None


class SpecailIntervalField(BasicIntervalField):

    widget = SpecialIntervalInput()

    def get_keys(self):
        keys = ("value", "max", "min", "type", "offsetType")
        return ["{}-{}".format(self.name, key) for key in keys]
