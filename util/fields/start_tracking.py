# encoding: utf-8

from __future__ import unicode_literals

from wtforms import fields

from ..widgets.start_tracking import BasicStartTracking, SpecialStartTracking


class BasicStartTrackingField(fields.Field):

    widget = BasicStartTracking()


class SpecialStartTrackingField(fields.Field):

    widget = SpecialStartTracking()
