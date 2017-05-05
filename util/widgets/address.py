# encoding: utf-8

from __future__ import unicode_literals

from jinja2 import escape
from wtforms.widgets import HTMLString


class AddressInput(object):
    """
       渲染地址输入信息的窗体。
    """
    template = (
        '<div id="distpicker">'
        '<div class="row">'
        '<div class="col-md-2">'
        '<select name="%(marker)s-province" class="form-control"></select>'
        '</div>'
        '<div class="col-md-2">'
        '<select name="%(marker)s-city" class="form-control"></select>'
        '</div>'
        '<div class="col-md-2">'
        '<select name="%(marker)s-county" class="form-control"></select>'
        '</div>'
        '<div class="col-md-6">'
        '<input type="text" placeholder="详细地址" name="%(marker)s-detail" value="%(detail)s" class="form-control"/>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
    )

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        placeholder = ''
        data = {
            'detail': ''
        }
        if field.data and isinstance(field.data, dict):
            data = field.data

        placeholder = self.template % {
            'marker': field.name,
            'detail': data['detail'],
        }

        return HTMLString(placeholder)
