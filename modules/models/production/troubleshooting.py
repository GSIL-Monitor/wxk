# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class TroubleShooting(Model, AuditModel):
    "排故方案的模型定义"
    __tablename__ = 'trouble_shooting'

    def _id_generator():
        return id_generator('PGFA', TroubleShooting, 'shootingNum')

    id = schema.Column(types.Integer, primary_key=True)
    shootingNum = schema.Column(types.String(255), default=_id_generator,
                                nullable=False)
    planeType = schema.Column(types.String(255), nullable=False)
    jihao = schema.Column(types.String(255), nullable=False)
    formulateDate = schema.Column(
        types.String(255), default=date_generator, nullable=False)
    formulatePerson = schema.Column(types.String(255))
    enforceDate = schema.Column(
        types.String(255), nullable=False, default=date_generator)
    enforceStaff = schema.Column(types.String(255), nullable=False)
    remark = schema.Column(types.String(255))

    shootingFileUrl = schema.Column(types.String(1000))
    description = schema.Column(types.Text, nullable=False)
    maintainStep = schema.Column(types.Text, nullable=False)

    statusName = schema.Column(types.String(255))

    faultReports_id = schema.Column(types.Integer, ForeignKey('fault_reports.id'))
    faultReports = relationship("FaultReports", backref="troubleShootings")

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.shootingNum

    def __str__(self):
        return self.shootingNum
