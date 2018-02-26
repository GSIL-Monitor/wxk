# encoding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from modules.models.base import Model


class FlyNature(Model):
    """飞行性质信息"""

    __tablename__ = 'fly_nature'

    id = schema.Column(types.Integer, primary_key=True)
    # 飞行性质编号
    number = schema.Column(types.String(100))
    # 飞行性质名称
    name = schema.Column(types.String(100))
