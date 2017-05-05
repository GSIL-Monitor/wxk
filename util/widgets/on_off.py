# coding: utf-8

from __future__ import unicode_literals

from wtforms.widgets import HTMLString


class OnOffWidget(object):
    "开关选择窗体"
    template = (
        '<div class="switch switch-large">'
        '<input type="checkbox" class="onoff" name="%(name)s"'
        ' data-off-color="warning" data-handle-width="100px"'
        ' id="%(name)s" %(bool)s/>'
        '<div style="display:none">%(label)s'
        '</div></div>'
    )

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        data = ''
        if field.data:
            data = 'checked'

        placeholder = self.template % {
            'label': field.label,
            'name': field.name,
            'bool': data,
        }

        return HTMLString(placeholder)
