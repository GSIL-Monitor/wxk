# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
import time

from modules.flows.states import InitialState
from flask import request
from sqlalchemy.sql import exists
from ..base import Model
from ..audit import AuditModel


class CompanyDayRecord(Model, AuditModel):
    "单位日运行记录的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'day_record'

    def _getts():
        ts = float(request.args.get('timestamp'))
        timeori = time.strftime("%Y-%m-%d", time.localtime(ts))
        return timeori

    id = schema.Column(types.Integer, primary_key=True)
    serialNum = schema.Column(types.String(255))
    flightDate = schema.Column(types.String(255), default=_getts)
    planeNum = schema.Column(types.String(255))
    windDirction = schema.Column(types.String(255))
    flySpeed = schema.Column(types.Float)
    airPressure = schema.Column(types.Float)
    visibility = schema.Column(types.Float)
    cloudCover = schema.Column(types.String(255))
    temperature = schema.Column(types.Float)
    highFrequencyWorkStatus = schema.Column(types.String(255))
    communicationWorkStatus = schema.Column(types.String(255))
    flyPlanApplicant = schema.Column(types.String(255))
    flyPlanApplicationDate = schema.Column(types.DateTime)
    actulizeApplicant = schema.Column(types.String(255))
    actulizeApplicationDate1 = schema.Column(types.DateTime)
    actulizeApplicationDate2 = schema.Column(types.DateTime)
    actulizeApplicationDate3 = schema.Column(types.DateTime)
    actulizeApplicationDate4 = schema.Column(types.DateTime)
    actulizeRecord = schema.Column(types.String(255))
    xuzhouFlyTime = schema.Column(types.DateTime)
    hefeiFlyTime = schema.Column(types.DateTime)
    nanjingFlyTime = schema.Column(types.DateTime)
    jinanFlyTime = schema.Column(types.DateTime)
    xuzhouFlyEndTime = schema.Column(types.DateTime)
    hefeiFlyEndTime = schema.Column(types.DateTime)
    nanjingFlyEndTime = schema.Column(types.DateTime)
    jinanFlyEndTime = schema.Column(types.DateTime)
    fileResourceUrl = schema.Column(types.String(1000))
    statusName = schema.Column(types.String(255))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @classmethod
    def has_related_status_by_day(cls, day_format, status=InitialState):
        "获取指定日期是否存在对应状态的数据"

        e = exists().where(cls.flightDate==day_format).where(cls.statusName==status)
        return cls.query.filter(e).count() != 0

    @classmethod
    def get_all_data_by_day(cls, day_format):
        return cls.query.filter(cls.flightDate == day_format).all()
