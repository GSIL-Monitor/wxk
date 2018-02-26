# encoding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from modules.models.base import Model


class MissionNature(Model):
    """任务性质信息"""

    __tablename__ = 'mission_nature'

    id = schema.Column(types.Integer, primary_key=True)
    # 任务性质编号
    number = schema.Column(types.Integer)
    # 任务性质名称
    name = schema.Column(types.String(100))
