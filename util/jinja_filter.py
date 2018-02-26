# encoding: utf-8

from __future__ import unicode_literals

import date_converter


def get_username(user):
    return user.realName or user.nickName or user.username or user.email


def format_username(user):
    if not user or not user.is_active:
        raise ValueError('User objects is not valid')
    return get_username(user)


def province(address):
    if address is None or 'province' not in address:
        return '省份'

    need_city_append = ['北京', '天津', '上海', '重庆']

    specifal = ['广西', '宁夏', '西藏', '香港', '澳门', '新疆']

    province = address['province']

    if not province:
        return '省份'

    if province in need_city_append:
        return province + '市'

    if province in specifal:
        return address.province

    # 如果剩余的不以省结尾
    if not province.endswith('省'):
        return province + '省'

    return province


def city(address):
    if address is None or 'city' not in address:
        return '地级市'

    city = address['city']
    if city and not city.endswith('市'):
        return city + '市'

    return city or '地级市'


def county(address):
    if address is None or 'county' not in address:
        return '市、县级市'

    if address['county'] is None or address['county'] == 'None':
        return '市、县级市'

    return address['county']


def timestamp_to_date(timestamp):
    if timestamp == 0 or timestamp == -1:
        return ''

    return date_converter.timestamp_to_string(timestamp, '%Y-%m-%d')


def timestamp_to_datetimestamp(timestamp):
    if timestamp == 0 or timestamp == -1:
        return ''

    return date_converter.timestamp_to_string(timestamp, '%Y-%m-%d %H:%M:%S')
