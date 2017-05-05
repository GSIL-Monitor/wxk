# coding: utf-8

from __future__ import unicode_literals
from datetime import date

from jinja2 import escape
from wtforms.widgets import HTMLString


class DateWidget(object):
    "日期选择窗体"
    template = (
        '<div class="input-group input-medium date datepicker"'
        ' data-date-format="yyyy-mm-dd">'
        '<input type="text" class="form-control" name="%(name)s" readonly value="%(value)s"/>'
        '<span class="input-group-btn">'
        '<buttuon class="btn default" type="button">'
        '<i class="fa fa-calendar"></i>'
        '</button>'
        '</span>'
        '</div>'
    )

    def __call__(self, field=None, **kwargs):

        value, name = '', field.name
        if field is not None and field.data:
            value = date.fromtimestamp(field.data).strftime('%Y-%m-%d')

        return HTMLString(self.template % {
            'value': value,
            'name': name,
        })
