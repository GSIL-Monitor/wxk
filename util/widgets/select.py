# coding: utf-8

from __future__ import unicode_literals

try:
    from html import escape
except ImportError:
    from cgi import escape

from wtforms.widgets import HTMLString, html_params
from wtforms.compat import text_type


# 一些下拉选项框需要提供额外的数据用于额外的js操作
class WithTypeSelect(object):
    # 该控件要求对应字段的值为一个tuple，前者为值，第二个为类别

    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        for val, label, _ in field.iter_choices():
            selected = field.data == val[0]
            html.append(self.render_option(val[0], label, selected, **{'data-type': val[1]}))
        html.append('</select>')
        return HTMLString(''.join(html))

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        if value is True:
            # Handle the special case of a 'True' value.
            value = text_type(value)

        options = dict(kwargs, value=value)
        if selected:
            options['selected'] = True
        return HTMLString('<option %s>%s</option>' % (html_params(**options), escape(text_type(label), quote=False)))


class WithTypeSelect2(WithTypeSelect):

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
            value_list = [d.realName for d in field.data]
        for val, label, _ in field.iter_choices():
            selected = False
            if val[0] in value_list:
                selected = True
            html.append(self.render_option(val[0], label, selected, **{'data-type': val[1]}))
        html.append('</select>')
        return HTMLString(''.join(html))
