# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class AssembleApplicationList(Model):
    """装机申请的模型定义"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'assemble_application_list'

    id = schema.Column(types.Integer, primary_key=True)
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # category 类型
    category = schema.Column(types.String(255))
    # manufacturer 生产厂商
    manufacturer = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # unit 单位
    unit = schema.Column(types.String(255))
    # planeNum 飞机
    planeNum = schema.Column(types.String(255))
    # flyHours飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落架次
    flightTimes = schema.Column(types.Integer)
    # effectiveDate 库存有效期
    effectiveDate = schema.Column(types.String(255))
    # lastCheckDate 上次检查时间
    lastCheckDate = schema.Column(types.String(255))
    # nextCheckDate 下次检查时间
    nextCheckDate = schema.Column(types.String(255))

    assembleapplication_id = schema.Column(
        types.Integer, ForeignKey('assemble_application.id'))
    assembleapplication = relationship(
        "AssembleApplication", backref="assembleApplicationList")

    assemble_id = schema.Column(
        types.Integer, ForeignKey('assemble.id'))
    assemble = relationship(
        "Assemble", backref="assembleApplicationList")


class AssembleApplication(Model, AuditModel):
    """装机申请单"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'assemble_application'

    def _id_generator():
        return id_generator('ZJSQ',
                            AssembleApplication, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), nullable=False,
                           default=_id_generator)
    # 日期
    date = schema.Column(types.String(255), nullable=False,
                         default=date_generator)
    # applyPerson 申请人
    applyPerson = schema.Column(types.String(255))
    # applyDate 申请日期
    applyDate = schema.Column(types.String(255), nullable=False,
                              default=date_generator)
    # remark 备注
    remark = schema.Column(types.String(255))
    # statusName 状态
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
