# coding: utf-8

from __future__ import unicode_literals
from functools import wraps
from datetime import date, datetime, timedelta
import date_converter
import math

from flask import request, jsonify

from util.jinja_filter import timestamp_to_date


def fullcanlendar_events(f, timestamp_format='%Y-%m-%d'):

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        start = request.args.get('start')
        end = request.args.get('end')

        if not start or not end:
            return jsonify(code=400, message='请求的时间区间不正确'), 400

        start_obj = date_converter.string_to_date(start, timestamp_format)
        end_obj = date_converter.string_to_date(end, timestamp_format)

        # 超过了当天时间
        events = []
        if start_obj > date.today():
            return jsonify(events)

        if end_obj < date.today() or (date.today().day == 1 and start_obj.month != date.today().month):
            # 区间[start, end), end通常为下个月的1号
            total_day = (end_obj - start_obj).days
        else:
            # 需要含当天
            total_day = (date.today() - start_obj).days + 1

        for idx in range(total_day):
            str_fmt = start_obj.replace(
                day=start_obj.day + idx).strftime(timestamp_format)
            timestamp = date_converter.string_to_timestamp(
                str_fmt, timestamp_format)
            ret = f(self, str_fmt, timestamp)
            if ret is None:
                continue

            url, title, className = ret

            events.append(
                dict(title=title, start=str_fmt, url=url, className=className))

        return jsonify(events)

    return wrapper


def specified_day(func, timestamp_format='%Y-%m-%d'):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            dt = request.args.get('timestamp', None)
            if dt is None:
                return jsonify(
                    code=400, message='请求的URL中应该包含日期信息。')

            timestamp = date_converter.string_to_datetime(dt, timestamp_format)
            if not timestamp:
                return jsonify(
                    code=400, message='飞行日期的格式有误，请不要使用错误的URL内容。')

            if timestamp > datetime.now():
                return jsonify(
                    code=400, message='指定的飞行日期过大。')

            code, message, data = func(self, dt, *args, **kwargs)

            return jsonify(code=code, message=message, **data)
        except Exception as ex:
            return jsonify(code=400, message=unicode(ex))

    return wrapper


def convert_float_to_hh_mm(ori, d1=':', d2=''):
    # 传入的内容认为是小时
    int_portion = int(ori)
    float_portion = int(round((ori - int_portion) * 60))
    if float_portion >= 60:
        float_portion = 59

    return '%02d%s%02d%s' % (int_portion, d1, float_portion, d2)


def hour_formater(view, ctx, model, name):
    return convert_float_to_hh_mm(model[name], '小时', '分')


def timestamp_to_date_formater(view, ctx, model, name):
    value = getattr(model, name, 0)
    if isinstance(value, (str, unicode)):
        value = float(value)

    if value is None:
        value = 0

    return timestamp_to_date(value)


def serial_number_formatter(view, ctx, model, name):
    val = getattr(model, name, '')
    # 向后兼容
    return '' if val == 'null' else val
