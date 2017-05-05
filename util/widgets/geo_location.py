# encoding: utf-8

from __future__ import unicode_literals

from jinja2 import escape
from mongoengine.fields import GeoPointField
from wtforms.widgets import HTMLString


class GeoPointInput(object):
    """
       渲染经纬度的输入窗体。
    """
    template = (
        '<div class="col-md-4">'
        '<label class="sr-only">经度</label>'
        '<input type="text" class="form-control input-medium" placeholder="经度" name="%(marker)s-lng" value="%(lng)s" />'
        '</div>'
        '<div class="col-md-4">'
        '<label class="sr-only">纬度</label>'
        '<input type="text" class="form-control input-medium" placeholder="纬度" name="%(marker)s-lat" value="%(lat)s" />'
        '</div>'
    )

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        placeholder = ''
        data = ['', '']
        if field.data and isinstance(field.data, (list, tuple)) and len(field.data) >= 2:
            data = field.data

        placeholder = self.template % {
            'marker': field.name,
            'lng': str(data[0]),
            'lat': str(data[1]),
        }

        return HTMLString(placeholder)
