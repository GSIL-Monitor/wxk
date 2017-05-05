# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class RepairSupplier(Model):
    "航材维修厂商的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'repair_supplier'

    id = schema.Column(types.Integer, primary_key=True)
    name = schema.Column(types.String(100))
    repairCapacity = schema.Column(types.String(100))
    address = schema.Column(types.String(100))
    contact = schema.Column(types.String(100))
    phone = schema.Column(types.String(100))
    email = schema.Column(types.String(100))
    fax = schema.Column(types.String(100))

    updateDate = schema.Column(types.DateTime)
