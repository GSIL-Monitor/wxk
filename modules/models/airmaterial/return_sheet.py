# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class ReturnSheet(Model):
    "航材退料单的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'return_sheet'

    id = schema.Column(types.Integer, primary_key=True)
    formNumber = schema.Column(types.String(100))
    formUserName = schema.Column(types.String(100))
    formDate = schema.Column(types.String(100))
    returnDate = schema.Column(types.String(100))
    returnUserName = schema.Column(types.String(100))
    status = schema.Column(types.String(100))

    updateDate = schema.Column(types.DateTime)
