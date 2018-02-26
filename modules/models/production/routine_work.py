# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Model
from ..id_generator import id_generator, date_time_stramp
from ..audit import AuditModel


class RoutineWork(Model, AuditModel):
    "例行工作的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'air_lxgz'

    def _id_generator():
        return id_generator('LXGZ', RoutineWork, 'lxgzNum')

    id = schema.Column(types.Integer, primary_key=True)
    boundedid = schema.Column(types.String(1000))
    planeType = schema.Column(types.String(255))
    lxgzNum = schema.Column(
        types.String(255), default=_id_generator)
    jcType = schema.Column(types.String(255))
    jihao = schema.Column(types.String(255))
    mxId = schema.Column(types.String(255))
    aircraftPn = schema.Column(types.String(255))
    serialNumber = schema.Column(types.String(255))
    description = schema.Column(types.String(255))
    jcTime = schema.Column(types.String(255), default=date_time_stramp)
    jcAdress = schema.Column(types.String(255))
    contextDesc = schema.Column(types.String(255))
    approveSuggestions = schema.Column(types.String(255))
    approveTime = schema.Column(types.DateTime)
    approveUserName = schema.Column(types.String(255))
    insNum = schema.Column(types.String(255))
    statusName = schema.Column(types.String(255))
    yuliuCon = schema.Column(types.String(255))
    user = schema.Column(types.String(255))
    relateDoc = schema.Column(types.Text)
    fileUrl = schema.Column(types.String(1000))

    retain_id = schema.Column(types.Integer, ForeignKey('air_blgz.id'))
    retain = relationship("Retain", backref="routineWorks")

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.lxgzNum
