# encoding: utf-8

from __future__ import unicode_literals

from flask_mongoengine.wtf import orm
from flask_admin.contrib.mongoengine.form import CustomModelConverter

from .fields import GeoLocationField


class GeoLocationSupportConverter(CustomModelConverter):

    def __init__(self, view):
        super(GeoLocationSupportConverter, self).__init__(view)

    @orm.converts('GeoPointField')
    def conv_geo_point(self, model, field, kwargs):
        return GeoLocationField(**kwargs)
