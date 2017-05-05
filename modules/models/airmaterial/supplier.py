# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class Supplier(Model):
    "航材供应商的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'supplier'

    id = schema.Column(types.Integer, primary_key=True)
    name = schema.Column(types.String(100))
    businessScope = schema.Column(types.String(100))
    address = schema.Column(types.String(100))
    contact = schema.Column(types.String(100))
    phone = schema.Column(types.String(100))
    email = schema.Column(types.String(100))
    fax = schema.Column(types.String(100))

    updateDate = schema.Column(types.DateTime)
