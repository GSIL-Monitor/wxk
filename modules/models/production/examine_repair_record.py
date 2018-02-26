# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator

fault_type = types.Enum('一般故障', '严重故障')


class ExamineRepairRecord(Model, AuditModel):
    "排故检修记录的模型定义"
    __tablename__ = 'examine_repair_record'

    def _id_generator():
        return id_generator('PGJX', ExamineRepairRecord, 'recordNum')

    id = schema.Column(types.Integer, primary_key=True)
    recordNum = schema.Column(types.String(255), default=_id_generator)
    faultType = schema.Column(fault_type, nullable=False, default='一般故障')
    planeType = schema.Column(types.String(255), nullable=False)
    jihao = schema.Column(types.String(255))
    faultDate = schema.Column(
        types.String(255), default=date_generator, nullable=False)
    faultAdress = schema.Column(types.String(255))
    reportsMaker = schema.Column(types.String(255))
    aircraftNumber = schema.Column(types.String(255))
    maintainDate = schema.Column(types.String(255), default=date_generator)
    maintainStaff = schema.Column(types.String(255))
    checkDate = schema.Column(types.String(255), default=date_generator)
    checkStaff = schema.Column(types.String(255))
    Soluted = schema.Column(types.Boolean)
    remark = schema.Column(types.String(255))
    description = schema.Column(types.Text)
    maintainStep = schema.Column(types.Text)
    repairFileUrl = schema.Column(types.String(1000))

    statusName = schema.Column(types.String(255))

    troubleShooting_id = schema.Column(types.Integer,
                                       ForeignKey("trouble_shooting.id"))
    troubleShooting = relationship("TroubleShooting",
                                   backref="erRecord",
                                   uselist=False)

    reservedFault_id = schema.Column(types.Integer, ForeignKey('air_blguzhang.id'))
    reservedFault = relationship('ReservedFault', backref='erRecord', uselist=False)

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
        return self.recordNum
