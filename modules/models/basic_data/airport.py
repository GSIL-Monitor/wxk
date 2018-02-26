# encoding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from modules.models.base import Model


class Airport(Model):
    """起降机场"""
    __tablename__ = 'airport'

    id = schema.Column(types.Integer, primary_key=True)
    # 机场编号
    number = schema.Column(types.String(100))
    # 机场名称
    name = schema.Column(types.String(100))
    # 所在位置
    location = schema.Column(types.String(100))
