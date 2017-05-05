# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class ScrapSheet(Model):
    "报废的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'scrap_sheet'

    id = schema.Column(types.Integer, primary_key=True)
    formNumber = schema.Column(types.String(100))
    formUserName = schema.Column(types.String(100))
    formDate = schema.Column(types.DateTime)
    status = schema.Column(types.String(100))
    checkContent = schema.Column(types.String(100))
    checkUserName = schema.Column(types.String(100))
    checkDate = schema.Column(types.DateTime)
    auditContent = schema.Column(types.String(100))
    auditUserName = schema.Column(types.String(100))
    auditDate = schema.Column(types.DateTime)

    updateTime = schema.Column(types.DateTime)
