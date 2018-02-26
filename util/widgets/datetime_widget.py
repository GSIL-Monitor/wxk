# coding: utf-8

from __future__ import unicode_literals
from datetime import date
import time
import bson

from wtforms.widgets import HTMLString


class DateWidget(object):
    "日期选择窗体"
    template = (
        '<div class="input-group date datepicker"'
        ' data-date-format="yyyy-mm-dd">'
        '<input type="text" class="form-control" name="%(name)s"'
        'readonly value="%(value)s"/>'
        '<span class="add-on input-group-btn">'
        '<buttuon class="btn default" type="button">'
        '<i class="fa fa-calendar"></i>'
        '</button>'
        '</span>'
        '</div>'
    )

    def __call__(self, field=None, **kwargs):

        value, name = '', field.name
        if field is not None and field.data:
            if isinstance(field.data, date):
                value = field.data.strftime('%Y-%m-%d')
            elif isinstance(field.data, (float, int)):
                value = time.localtime(float(field.data))
                value = time.strftime('%Y-%m-%d', value)
            elif isinstance(field.data, (str, unicode)):
                value = field.data
            else:
                value = '格式化有误'

        return HTMLString(self.template % {
            'value': value,
            'name': name,
        })


class DateTimeWidget(object):
    "日期时间选择窗体"
    template = (
        '<div class="input-group datetime datepicker">'
        '<input type="text" class="form-control" name="%(name)s" '
        'value="%(value)s">'
        '<span class="add-on input-group-btn">'
        '<buttuon class="btn default" type="button">'
        '<i class="fa fa-calendar"></i>'
        '</button>'
        '</span>'
        '</div>'
    )

    def __call__(self, field=None, **kwargs):

        value, name = '', field.name

        if field is not None and field.data:
            if isinstance(field.data, date):
                value = time.strftime(
                    '%Y-%m-%d %H:%M:%S', field.data.timetuple())
            elif isinstance(field.data, (float, int, str, unicode)):
                value = time.localtime(float(field.data))
                value = time.strftime('%Y-%m-%d %H:%M:%S', value)
            else:
                value = '格式化有误'

        return HTMLString(self.template % {
            'value': value,
            'name': name,
        })


class DateIntWidget(object):
    template = (
        '<div class="input-group date datepicker">'
        '<input type="text" class="form-control" name="%(name)s" '
        'value="%(value)s">'
        '<span class="add-on input-group-btn">'
        '<buttuon class="btn default" type="button">'
        '<i class="fa fa-calendar"></i>'
        '</button>'
        '</span>'
        '</div>'
    )

    def __call__(self, field=None, **kwargs):

        value, name = '', field.name

        if field is not None and field.data:
            if isinstance(field.data, date):
                value = time.strftime('%Y-%m-%d', field.data.timetuple())
            elif isinstance(field.data, (float, int, str, unicode, bson.int64.Int64)):
                value = time.localtime(float(field.data))
                value = time.strftime('%Y-%m-%d', value)
            else:
                value = '格式化有误'

        return HTMLString(self.template % {
            'value': value,
            'name': name,
        })
