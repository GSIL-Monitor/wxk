# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..audit import AuditModel
from ..base import Model


class Manufacturer(Model, AuditModel):
    """生产厂商模型定义"""
    __tablename__ = 'manufacturer'

    id = schema.Column(types.Integer, primary_key=True)
    # 名称
    name = schema.Column(types.String(100), nullable=False,)
    # 经营范围
    businessScope = schema.Column(types.String(100))
    # 地址·
    address = schema.Column(types.String(100))
    # 联系人
    contact = schema.Column(types.String(100))
    # 电话
    phone = schema.Column(types.String(100))
    # 邮箱
    email = schema.Column(types.String(100))
    # 传真
    fax = schema.Column(types.String(100))
    # 附件
    fileResourceUrl = schema.Column(types.String(1000))

    # statusName 状态
    statusName = schema.Column(types.String(255))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    def __str__(self):
        return self.name
