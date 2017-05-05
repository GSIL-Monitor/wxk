# coding: utf-8

from __future__ import unicode_literals

from jinja2 import Markup

from modules.forms.commom import interval_types


def interval_formmatter(view, ctx, model, name):

    # TODO: interval is a list
    interval_val = model[name]

    # template = '<p>%(type)s: </p> <p>%(value)d, -%(min)d, %(max)d</p>'

    # html = []
    # for val in interval_val:
    #     html.append(template % {
    #         'type': dict(interval_types('r22'))[val['type']],
    #         'value': val['value'],
    #         'min': val['min'],
    #         'max': val['max'],
    #     })
    html = []
    for val in interval_val:
        for k, v in val.items():
            html.append('<p>{}-{}</p>'.format(k, v))

    return Markup('<br />'.join(html))
