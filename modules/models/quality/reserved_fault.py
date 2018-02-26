# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator


class ReservedFault(Model, AuditModel):
    "保留故障的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'air_blguzhang'

    def _id_generator():
        return id_generator('BLGZ', ReservedFault, 'reservedNum')

    id = schema.Column(types.Integer, primary_key=True)
    reservedNum = schema.Column(types.String(255), default=_id_generator)
    planeType = schema.Column(types.String(255))
    flyhours = schema.Column(types.Float)
    jihao = schema.Column(types.String(255))
    engineNum = schema.Column(types.String(255))
    measure = schema.Column(types.String(255))
    limit = schema.Column(types.String(255))
    proposer = schema.Column(types.String(255))
    date = schema.Column(types.String(255))
    licenceNO = schema.Column(types.String(255))
    remarks = schema.Column(types.String(255))

    description = schema.Column(types.String(255))
    expectAlter = schema.Column(types.String(255))
    reason = schema.Column(types.String(255))

    statusName = schema.Column(types.String(255))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.reservedNum
