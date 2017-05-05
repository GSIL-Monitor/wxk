# encoding: utf-8

from __future__ import unicode_literals

from wtforms import fields

from ..widgets.on_off import OnOffWidget


class OnOffField(fields.Field):
    """用于处理开关选择的正确显示。"""
    widget = OnOffWidget()

    def __init__(self, label=None, validators=None, **kwargs):
        super(OnOffField, self).__init__(label, validators, **kwargs)

    def process_formdata(self, valuelist):
        if len(valuelist) and valuelist[0] == 'on':
            self.data = True
            return
        self.data = False
