# encoding: utf-8

from __future__ import unicode_literals

from wtforms import fields

from ..widgets.interval import BasicIntervalInput, SpecialIntervalInput


class BasicIntervalField(fields.Field):

    # TODO: 有的界面需要设置multiple参数为False
    widget = BasicIntervalInput()


class SpecailIntervalField(BasicIntervalField):

    widget = SpecialIntervalInput()


class BasicRadioIntervalField(fields.Field):

    widget = BasicIntervalInput(checkbox=False)


class SpecailRadioIntervalField(BasicIntervalField):

    widget = SpecialIntervalInput(checkbox=False)
