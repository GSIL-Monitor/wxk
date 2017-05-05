# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class OutBound(Model):
    "航材出库的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'outbound'

    id = schema.Column(types.Integer, primary_key=True)
    formNumber = schema.Column(types.String(100))
    formUserName = schema.Column(types.String(100))
    formDate = schema.Column(types.String(100))
    status = schema.Column(types.String(100))

    updateDate = schema.Column(types.DateTime)
