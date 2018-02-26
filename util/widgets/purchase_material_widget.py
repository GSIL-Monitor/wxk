# coding: utf-8

from __future__ import unicode_literals

from wtforms.widgets import HTMLString


class PurchaseInputWidget(object):

    template = (
        '<span>%(label)s</span>'
        '<input class="form-control" name="%(name)s"'
        ' id="%(name)s" value="%(value)s"/>'
    )

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        data = ''
        if field.data:
            data = field.data

        placeholder = self.template % {
            'label': field.label,
            'name': field.name,
            'value': data,
        }

        return HTMLString(placeholder)
