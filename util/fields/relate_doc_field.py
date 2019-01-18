# encoding: utf-8

from __future__ import unicode_literals

import json
from wtforms import fields
from wtforms.utils import unset_value

from ..widgets.relate_doc_widget import RelateDocSelect


class RelateDocField(fields.Field):

    widget = RelateDocSelect()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist


class RoutineWorkRelateDocField(RelateDocField):

    def process_data(self, value):
        if value:
            value = json.loads(value)
        self.data = value

    def process_formdata(self, valuelist):
        if valuelist:
            valuelist = json.dumps(valuelist)
        self.data = valuelist

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
            try:
                if 'doc_files' in formdata:
                    files = formdata.getlist('doc_files')[0]
                    if files:
                        files = json.loads(files)
                        self.raw_data = files
                else:
                    self.raw_data = []
                self.process_formdata(self.raw_data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

        try:
            for filter in self.filters:
                self.data = filter(self.data)
        except ValueError as e:
            self.process_errors.append(e.args[0])
