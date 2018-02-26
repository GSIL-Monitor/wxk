# encoding: utf-8

from __future__ import unicode_literals
from functools import partial

from sqlalchemy import or_
from flask_admin.contrib.sqla import tools
from flask_admin.contrib.sqla.filters import (FilterLike, FilterEqual, FilterNotLike)

from modules.flows.operations import View
from .stat_base import FlightlogStatBaseView, FlightLog
from modules.perms import ActionNeedPermission


_flight_time_label = '飞行时间'
_engine_time_label = '发动机时间'
_land_time_label = '起落次数'


headers = [
    '飞行日期', '飞机注册号',
    '飞行性质', '作业区域', '任务性质', '起飞机场', '降落机场',
    # '开车时间',
    '滑出时间', '起飞时间', '降落时间',
    # '关车时间',
    '停止时间', _flight_time_label, _engine_time_label,
    '机长1', '机长2', '机长3',
    _land_time_label,
]

columns = [
    dict(data='flightDate', readOnly=True),
    dict(data='aircraftId', readOnly=True),
    dict(data='flyProperty', readOnly=True),
    dict(data='workArea', readOnly=True),
    dict(data='missionType', readOnly=True),
    dict(data='departureAirport', readOnly=True),
    dict(data='landingAirport', readOnly=True),
    dict(data='skidoffTime', readOnly=True),
    dict(data='departureTime', readOnly=True),
    dict(data='landingTime', readOnly=True),
    dict(data='stopTime', readOnly=True),
    dict(data='flightTime', readOnly=True),
    dict(data='engineTime', readOnly=True),
    dict(data='captain', readOnly=True),
    dict(data='copilot', readOnly=True),
    dict(data='captain3', readOnly=True),
    dict(data='landings', readOnly=True),
]


class CaptainContainsFilter(FilterLike):

    def apply(self, query, value, alias=None):
        stmt = tools.parse_like_term(value)

        return query.filter(or_(
            FlightLog.captain.ilike(stmt),
            FlightLog.copilot.ilike(stmt),
            FlightLog.captain3.ilike(stmt),
        ))


class _FlightlogStatisticsView(FlightlogStatBaseView):
    "飞行时间统计视图"

    list_template = 'flightlog/stat.html'

    extra_js = [
        '/static/js/handsontable.min.js',
        '/static/js/flightlog_stat.js',
    ]

    def is_accessible(self):
        return ActionNeedPermission('flightlogstat', View).can()

    def extra_ctx_datas(self):
        return {
            'headers': headers,
            'columns': columns,
            'flight_time_index': headers.index(_flight_time_label),
            'engine_time_index': headers.index(_engine_time_label),
            'landings_index': headers.index(_land_time_label),
        }

    def __init__(self, *args, **kwargs):

        ori_column_filters = []
        ori_column_filters.extend(self.column_filters)
        self.column_filters = ori_column_filters

        self.column_filters.extend([
            FilterLike(column=FlightLog.departureAirport, name='起飞机场'),
            FilterNotLike(column=FlightLog.departureAirport, name='起飞机场'),
            FilterEqual(column=FlightLog.departureAirport, name='起飞机场'),

            CaptainContainsFilter(column=FlightLog.captain, name='飞行人员'),

            FilterLike(column=FlightLog.landingAirport, name='降落机场'),
            FilterNotLike(column=FlightLog.landingAirport, name='降落机场'),
            FilterEqual(column=FlightLog.landingAirport, name='降落机场'),

            FilterLike(column=FlightLog.missionType, name='任务性质'),
            FilterNotLike(column=FlightLog.missionType, name='任务性质'),
            FilterEqual(column=FlightLog.missionType, name='任务性质'),

            FilterLike(column=FlightLog.flyProperty, name='飞行性质'),
            FilterNotLike(column=FlightLog.flyProperty, name='飞行性质'),
            FilterEqual(column=FlightLog.flyProperty, name='飞行性质'),

            FilterLike(column=FlightLog.workArea, name='作业区域'),
            FilterNotLike(column=FlightLog.workArea, name='作业区域'),
            FilterEqual(column=FlightLog.workArea, name='作业区域'),
        ])

        super(_FlightlogStatisticsView, self).__init__(*args, **kwargs)


FlightlogStatisticsView = partial(
    _FlightlogStatisticsView, FlightLog, name='飞行时间统计',
    endpoint='flightlog-stat')
