# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class FaultReports(Model, AuditModel):
    "故障报告的模型定义"
    __tablename__ = 'fault_reports'

    def _id_generator():
        return id_generator('GZBG', FaultReports, 'recordNum')

    id = schema.Column(types.Integer, primary_key=True)
    recordNum = schema.Column(types.String(255), default=_id_generator,
                              nullable=False)
    planeType = schema.Column(types.String(255), nullable=False)
    jihao = schema.Column(types.String(255), nullable=False)
    faultDate = schema.Column(
        types.String(255), default=date_generator, nullable=False)
    faultAdress = schema.Column(types.String(255))
    reportsMaker = schema.Column(types.String(255))
    aircraftNumber = schema.Column(types.String(255))
    remark = schema.Column(types.String(255))

    statusName = schema.Column(types.String(255))
    description = schema.Column(types.String(255))
    relateFileUrl = schema.Column(types.String(1000))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.recordNum

    def __str__(self):
        return (self.recordNum)