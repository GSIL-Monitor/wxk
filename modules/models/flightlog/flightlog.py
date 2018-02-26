# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from sqlalchemy.sql import exists
import date_converter

from modules.flows.states import InitialState, Edited, Finished
from util.helper import convert_hh_mm_to_float

from ..base import Model
from ..audit import AuditModel


class FlightLog(Model, AuditModel):
    "维修状态的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'flight_log'

    id = schema.Column(types.Integer, primary_key=True)

    flightlogId = schema.Column(types.String(255))
    missionType = schema.Column(types.String(255))
    flyProperty = schema.Column(types.String(255))
    captain = schema.Column(types.String(255))
    copilot = schema.Column(types.String(255))
    captain3 = schema.Column(types.String(255))
    passengers = schema.Column(types.String(255))
    aircraftId = schema.Column(types.String(255))
    # 可以不需要
    # aircraftType = schema.Column(types.String(255))
    departureAirport = schema.Column(types.String(255))
    landingAirport = schema.Column(types.String(255))
    flightDate = schema.Column(types.Date)
    crew = schema.Column(types.String(255))
    departureTime = schema.Column(types.Time)
    landingTime = schema.Column(types.Time)
    landings = schema.Column(types.String(255))
    remark = schema.Column(types.String(255))
    poweronTime = schema.Column(types.Time)
    powerdownTime = schema.Column(types.Time)
    stopTime = schema.Column(types.Time)
    skidoffTime = schema.Column(types.Time)
    flightTime = schema.Column(types.String(255))
    engineTime = schema.Column(types.String(255))
    medicinePrescription = schema.Column(types.String(255))
    weight = schema.Column(types.String(255))
    workArea = schema.Column(types.String(255))
    workAcres = schema.Column(types.Float)

    # 直接定义要求的status属性
    status = schema.Column(types.String(255))

    @property
    def business_id(self):
        return self.flightlogId

    @classmethod
    def has_related_status_by_day(cls, day_format, status=InitialState):
        "获取指定日期是否存在对应状态的数据"

        e = exists().where(cls.flightDate==date_converter.string_to_date(day_format, '%Y-%m-%d')).where(cls.status==status)
        return cls.query.filter(e).count() != 0

    @classmethod
    def get_all_data_by_day(cls, day_format):
        return cls.query.filter(cls.flightDate==date_converter.string_to_date(day_format, '%Y-%m-%d')).all()

    def to_json(self):

        def _format_time(time_field):
            return time_field.strftime('%H:%M:%S') if time_field else '00:00:00'

        return {
            'flightlogId': self.flightlogId,
            'missionType': self.missionType,
            'flyProperty': self.flyProperty,
            'captain': self.captain,
            'copilot': self.copilot,
            'captain3': self.captain3,
            'passengers': self.passengers,
            'aircraftId': self.aircraftId,
            'departureAirport': self.departureAirport,
            'landingAirport': self.landingAirport,
            'flightDate': self.flightDate.strftime('%Y-%m-%d'),
            'crew': self.crew,
            'departureTime': _format_time(self.departureTime),
            'landingTime': _format_time(self.landingTime),
            'landings': self.landings,
            'remark': self.remark,
            'poweronTime': _format_time(self.poweronTime),
            'powerdownTime': _format_time(self.powerdownTime),
            'stopTime': _format_time(self.stopTime),
            'skidoffTime': _format_time(self.skidoffTime),
            'flightTime': self.flightTime,
            'engineTime': self.engineTime,
            'medicinePrescription': self.medicinePrescription,
            'workAcres': self.workAcres,
            'workArea': self.workArea,
            'weight': self.weight,
            'status': self.status,
        }

    def to_api_data(self):
        # 将该数据转换为API所要求的格式
        if not self.flightlogId:
            raise ValueError('飞行日志编号不允许为空')
        if not self.aircraftId:
            raise ValueError('飞行日志的关联飞行器编号不能为空')
        if not self.departureTime or not self.landingTime:
            raise ValueError('起飞时间或降落时间有误')
        if not self.flightTime:
            raise ValueError('飞行小时设置有误')
        if not self.landings:
            raise ValueError('起落次数设置有误')
        if not self.engineTime:
            raise ValueError('发动机小时设置有误')

        departureTime = date_converter.string_to_timestamp(
            ' '.join([self.flightDate.strftime('%Y-%m-%d'), self.departureTime.strftime('%H:%M:%S')]),
            '%Y-%m-%d %H:%M:%S')
        landingTime = date_converter.string_to_timestamp(
            ' '.join([self.flightDate.strftime('%Y-%m-%d'), self.landingTime.strftime('%H:%M:%S')]),
            '%Y-%m-%d %H:%M:%S')
        if landingTime <= departureTime:
            raise ValueError("降落时间至少应该大于起飞时间")

        fl = convert_hh_mm_to_float(self.flightTime)
        if not fl:
            raise ValueError('飞行时间为 0 小时的日志有什么意义？')

        # TODO: 目前y5b的缘故，发动机时间应该存在
        et = convert_hh_mm_to_float(self.engineTime)
        if not et:
            raise ValueError('发动机时间为 0 小时的日志有什么意义？')

        return {
            'id': self.flightlogId,
            'aircraftId': self.aircraftId,
            'flightDate': int(date_converter.date_to_timestamp(self.flightDate)),
            'departureTime': int(departureTime),
            'landingTime': int(landingTime),
            'landings': int(self.landings),
            'remark': self.remark or '',
            'flightTime': fl,
            'engineTime': et,
            # TODO: 写死
            'aircraftType': 'y5b',
            # 下面的内容非必须，但是API端要求传输
            'departureAirport': self.departureAirport or '',
            'landingAirport': self.landingAirport or '',
            'captain': self.captain or '',
            'copilot': self.copilot or '',
            'crew': self.crew or '',
            'passengers': self.passengers or '',
        }
