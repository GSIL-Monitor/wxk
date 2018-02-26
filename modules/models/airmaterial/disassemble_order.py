# coding: utf-8

from __future__ import unicode_literals
from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class DisassembleOrder(Model, AuditModel):
    """拆机单的模型定义"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'disassemble_order'

    def _id_generator():
        return id_generator('CJD', DisassembleOrder, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), default=_id_generator)
    # 日期
    date = schema.Column(
        types.String(255), nullable=False, default=date_generator)
    # disassemblePerson 拆机人
    disassemblePerson = schema.Column(types.String(255))
    # disassembleData 拆机日期
    disassembleDate = schema.Column(
        types.String(255), nullable=False, default=date_generator)
    # remark 备注
    remark = schema.Column(types.String(255))
    # statusName 状态值
    statusName = schema.Column(types.String(255))

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


class DisassembleMaterial(Model):
    """拆机内容"""
    __tablename__ = 'disassemble_material'
    id = schema.Column(types.Integer, primary_key=True)
    # partNumber 件号
    partNumber = schema.Column(types.String(255), nullable=False)
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # category 航材类型
    category = schema.Column(types.String(255), nullable=False)
    # manufacturer 生产厂商
    manufacturer = schema.Column(types.String(255))
    # flyTime 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落架次
    flightTimes = schema.Column(types.Float)
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # unit 航材单位
    unit = schema.Column(types.String(255))
    # planeNum 飞机注册号
    planeNum = schema.Column(types.String(255))
    # effectiveDate 库存有效期
    effectiveDate = schema.Column(types.String(255))
    # lastCheckDate 上次检查时间
    lastCheckDate = schema.Column(types.String(255))
    # nextCheckDate 下次检查时间
    nextCheckDate = schema.Column(types.String(255))
    # 外键及关系
    disassembleOrder_id = schema.Column(
        types.Integer, ForeignKey('disassemble_order.id'))
    disassembleOrder = relationship(
        'DisassembleOrder', backref='disassembleMaterials')
