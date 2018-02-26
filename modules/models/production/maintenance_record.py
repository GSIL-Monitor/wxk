# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


checkType = types.Enum('航前检查', '航后检查', '定期检查', '航线检查')


class MaintenanceRecord(Model, AuditModel):
    "维护保养记录的模型定义"
    __tablename__ = 'maintenance_record'

    def _id_generator():
        return id_generator('WHJL', MaintenanceRecord, 'recordNum')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    recordNum = schema.Column(types.String(255), default=_id_generator)
    # 机型
    planeType = schema.Column(types.String(255))
    # 飞机注册号
    jihao = schema.Column(types.String(255))
    # 检查类型
    checkType = schema.Column(checkType, default='航前检查')
    # 检查地点
    checkPlace = schema.Column(types.String(255))
    # 受影响部件
    effectPart = schema.Column(types.String(255))
    # 受影响的发动机
    effectEngine = schema.Column(types.String(255))
    # 工时停场时
    stopTime = schema.Column(types.Float)
    # 涉及人员
    involvePerson = schema.Column(types.String(255))
    # 检查日期
    checkDate = schema.Column(types.String(255), nullable=False,
                              default=date_generator)
    # 检查内容
    checkContent = schema.Column(types.String(255))

    statusName = schema.Column(types.String(255))

    faultReports_id = schema.Column(types.Integer, ForeignKey('instruction.id'))
    faultReports = relationship("EngineeringOrder",
                                backref="maintenanceRecord",
                                uselist=False)


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
