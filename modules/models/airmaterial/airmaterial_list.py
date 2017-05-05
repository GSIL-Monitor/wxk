# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class AirmaterialList(Model):
    "航材首页的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'product'

    id = schema.Column(types.Integer, primary_key=True)
    partNumber = schema.Column(types.String(100))
    sequenceNumber = schema.Column(types.String(100))
    name = schema.Column(types.String(100))
    price = schema.Column(types.String(100))
    applicableModel = schema.Column(types.String(100))
    status = schema.Column(types.String(100))
    shelf = schema.Column(types.String(100))
    source = schema.Column(types.String(100))
    use1 = schema.Column(types.String(100))
    supplierName = schema.Column(types.String(100))
    certificateNumber = schema.Column(types.String(100))
    document = schema.Column(types.String(100))
    file = schema.Column(types.String(100))
    remark = schema.Column(types.String(255))
    effectiveTime = schema.Column(types.String(100))
    unit = schema.Column(types.String(100))
    size = schema.Column(types.String(100))
    minStock = schema.Column(types.String(100))
    inboundDate = schema.Column(types.String(100))
    outboundDate = schema.Column(types.String(100))
    type = schema.Column(types.String(255))
    nextCheckDate = schema.Column(types.String(255))
    warningColor = schema.Column(types.String(255))
