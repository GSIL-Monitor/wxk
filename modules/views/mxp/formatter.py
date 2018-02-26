# coding: utf-8

from __future__ import unicode_literals

from jinja2 import Markup


def interval_formmatter(view, ctx, model, name):
    try:
        interval_val = model[name]
    except:
        return
    html = []
    html.append('<div>')
    for val in interval_val:
        html.append('<p>')
        for k, v in val.items():
            html.append(' {}:{} '.format(k, v))
        html.append('</p>')
    html.append('</div>')

    return Markup(''.join(html))
