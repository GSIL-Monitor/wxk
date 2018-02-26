# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class RepairReturnOrder(Model, AuditModel):
    """送修的模型定义"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'repair_return_order'

    def _id_generator():
        return id_generator('SXGH', RepairReturnOrder, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), nullable=False,
                           default=_id_generator)
    repairApplicationNum = schema.Column(types.String(255))
    # returnDate 归还日期
    returnDate = schema.Column(types.Date, default=date_generator)
    # repaireCompany 维修厂商
    repairCompany = schema.Column(types.String(255))
    # contactPerson 联系人
    contactPerson = schema.Column(types.String(255))
    # remark 备注
    remark = schema.Column(types.String(255))
    # statusName 状态值
    statusName = schema.Column(types.String(255))

    # 外键及关系
    repairApplication_id = schema.Column(
        types.Integer, ForeignKey('repair_application.id'), nullable=False)
    repairApplication = relationship(
        'RepairApplication', backref='repairReturnOrder')

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.number

    def __str__(self):
        return self.number


class RepairReturnMaterial(Model):
    """送修归还内容"""

    __tablename__ = 'repair_return_material'
    id = schema.Column(types.Integer, primary_key=True)
    # category 航材类型
    category = schema.Column(types.String(255))
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # manufacturer 生产厂商
    manufacturer = schema.Column(types.String(255))
    # flyTime 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落次数
    flightTimes = schema.Column(types.Integer)
    # lastCheckDate 上次检查日期
    lastCheckDate = schema.Column(types.String(255))
    # 外键及关系
    application_id = schema.Column(
        types.Integer, ForeignKey('repair_return_order.id'), nullable=False)
    repairReturnOrder = relationship(
        'RepairReturnOrder', backref='repairReturnMaterials')
