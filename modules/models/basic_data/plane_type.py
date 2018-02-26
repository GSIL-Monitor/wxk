# encoding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from modules.models.base import Model


class PlaneType(Model):
    """机型信息"""

    __tablename__ = 'plane_type'

    id = schema.Column(types.Integer, primary_key=True)
    # 机型编号
    number = schema.Column(types.String(100))
    # 机型名称
    name = schema.Column(types.String(100))
