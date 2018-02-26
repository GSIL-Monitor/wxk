# coding: utf-8

from __future__ import unicode_literals
import time

from datetime import datetime


def id_generator(prefix='', model_class=None, field=''):

    prefix_gen = ''.join([prefix, time.strftime('%Y%m%d', time.localtime())])
    prefix_where = ''.join(['%', prefix_gen, '%'])
    if model_class is not None and field:
        query = model_class.query.filter(getattr(model_class, field).like(prefix_where))
        count = query.count()
        if count != 0:
            last = query.order_by(field + " desc").first()
            last_field = getattr(last, field)
            number = int(last_field.replace(prefix_gen, ''))
            return ''.join([prefix_gen, '%03d' % (number + 1,)])
        else:
            return ''.join([prefix_gen, '%03d' % (count + 1,)])

    return prefix_gen


def date_generator():
    return datetime.today()


def date_time_stramp():
    return str(int(time.mktime(datetime.today().timetuple())))
