# coding: utf-8

from __future__ import unicode_literals

from wtforms.widgets import HTMLString, html_params

from .select import WithTypeSelect


class ComponentsDropdownsWidget(WithTypeSelect):

    def __init__(self, default='', multiple=False, *args, **kwargs):
        self._default = default
        super(ComponentsDropdownsWidget, self).__init__(multiple)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')
        kwargs.setdefault('id', field.id)

        allow_blank = getattr(field, 'allow_blank', False)

        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        if self.multiple:
            kwargs['multiple'] = True

        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        value_list = []

        if field.data:
            value_list = field.data.split(',')
        elif self._default:
            value_list = self._default.split(',')

        for val, label, _ in field.iter_choices():
            selected = False

            if val[0] in value_list:
                selected = True
            html.append(self.render_option(val[0], label, selected, **{'data-type': val[1]}))
        html.append('</select>')
        return HTMLString(''.join(html))