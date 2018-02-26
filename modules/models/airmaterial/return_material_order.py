# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator
from ..id_generator import date_generator


class ReturnMaterialOrder(Model, AuditModel):
    "退料单的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'return_material_order'

    def _id_generator():
        return id_generator('TLD', ReturnMaterialOrder, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), default=_id_generator)
    # 单据日期
    date = schema.Column(types.String(255), default=date_generator)
    # returnPerson 退料人
    returnPerson = schema.Column(types.String(255))
    # returnDate 退料日期
    returnDate = schema.Column(types.String(255), default=date_generator)
    # returnReason 退料原因
    returnReason = schema.Column(types.Text)
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


class ReturnMaterial(Model):
    """退料内容"""
    __tablename__ = 'return_material'
    id = schema.Column(types.Integer, primary_key=True)
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # category 类别
    category = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # unit 单位
    unit = schema.Column(types.String(255))
    # flightNum 飞机号
    flightNum = schema.Column(types.String(255))
    # 外键
    application_id = schema.Column(
        types.Integer, ForeignKey('return_material_order.id'))
    returnMaterialOrder = relationship(
        'ReturnMaterialOrder', backref='returnMaterials')
