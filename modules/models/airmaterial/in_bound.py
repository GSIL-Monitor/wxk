# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class InBound(Model):
    "航材入库的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'inbound'

    id = schema.Column(types.Integer, primary_key=True)
    form_number = schema.Column(types.String(100))
    form_user_name = schema.Column(types.String(100))
    form_date = schema.Column(types.String(100))
    status = schema.Column(types.String(100))

    updateTime = schema.Column(types.DateTime)
