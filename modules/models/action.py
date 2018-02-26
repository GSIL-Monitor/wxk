# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from .base import Model


class ActionDescription(Model):
    """执行流程操作时涉及的各种审批说明"""

    __tablename__ = 'action_description'

    id = schema.Column(types.Integer, primary_key=True)

    # 用户信息
    author = schema.Column(types.Integer, schema.ForeignKey('user.id'))
    # 时间戳
    timestamp = schema.Column(types.DateTime)
    # 内容
    content = schema.Column(types.String(500))
    # 类别
    category = schema.Column(types.String(100))

    # 对应的模型表名
    entity_id = schema.Column(types.Integer)
