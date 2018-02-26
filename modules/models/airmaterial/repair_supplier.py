# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..audit import AuditModel
from ..base import Model


class RepairSupplier(Model, AuditModel):
    """航材维修厂商的模型定义"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'repair_supplier'

    id = schema.Column(types.Integer, primary_key=True)
    # name 名称
    name = schema.Column(types.String(100))
    # firmCategory 厂商类型
    firmCategory = schema.Column(types.String(100))
    # 地址
    address = schema.Column(types.String(100))
    # 联系人
    contact = schema.Column(types.String(100))
    # 电话
    phone = schema.Column(types.String(100))
    # 邮箱
    email = schema.Column(types.String(100))
    # 传真
    fax = schema.Column(types.String(100))
    # repairCapacity 维修能力
    repairCapacity = schema.Column(types.String(255))
    # fileResourceUrl 附件
    fileResourceUrl = schema.Column(types.String(1000))
    # statusName
    statusName = schema.Column(types.String(255))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    def __str__(self):
        return self.name
