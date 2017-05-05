# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class RepairContract(Model):
    "航材送修的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'repair_contract'

    id = schema.Column(types.Integer, primary_key=True)
    formNumber = schema.Column(types.String(100))
    repairManufacturerId = schema.Column(types.String(100))
    contact = schema.Column(types.String(100))
    phone = schema.Column(types.String(100))
    fax = schema.Column(types.String(100))
    email = schema.Column(types.String(100))
    formUserName = schema.Column(types.String(100))
    totalPrice = schema.Column(types.String(100))
    clause = schema.Column(types.String(255))
    status = schema.Column(types.String(255))
    checkContent = schema.Column(types.String(255))
    checkUserName = schema.Column(types.String(255))
    checkDate = schema.Column(types.String(255))
    auditContent = schema.Column(types.String(255))
    auditUserName = schema.Column(types.String(255))
    auditDate = schema.Column(types.String(255))
    formDate = schema.Column(types.String(255))

    updateDate = schema.Column(types.DateTime)
