# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class Scrap(Model, AuditModel):
    """报废单的模型定义"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'scrap'

    def _id_generator():
        return id_generator('BFSQ', Scrap, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), default=_id_generator)
    # 申请人
    applyPerson = schema.Column(types.String(255))
    # 申请日期
    applyDate = schema.Column(types.String(255), default=date_generator)
    # 报废类型
    scrapCategory = schema.Column(types.Enum('一般', '重要'), nullable=False)
    # 申请原因
    applyReason = schema.Column(types.String(255))
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


class ScrapMaterial(Model):
    """报废内容"""

    __tablename__ = 'scrap_material'

    id = schema.Column(types.Integer, primary_key=True)
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # category 类别
    category = schema.Column(types.String(255))
    # 生产厂商
    manufacturer = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # effectiveDate 库存有效期
    effectiveDate = schema.Column(types.String(255))
    # lastCheckDate 上次检查日期
    lastCheckDate = schema.Column(types.String(255))
    # nextCheckDate 下次检查日期
    nextCheckDate = schema.Column(types.String(255))

    # 外键
    application_id = schema.Column(
        types.Integer, ForeignKey('scrap.id'))
    scrap = relationship(
        'Scrap', backref='scrapMaterial')
