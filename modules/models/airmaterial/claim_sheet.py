# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class ClaimSheet(Model):
    "航材索赔的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'claim_sheet'

    id = schema.Column(types.Integer, primary_key=True)
    date = schema.Column(types.String(100))
    unit = schema.Column(types.String(100))
    content = schema.Column(types.String(255))
    status = schema.Column(types.String(255))
    file = schema.Column(types.String(255))
    company = schema.Column(types.String(255))
    contact = schema.Column(types.String(255))

    updateDate = schema.Column(types.DateTime)
