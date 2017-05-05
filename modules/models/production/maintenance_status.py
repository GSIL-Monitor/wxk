# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class MaintenanceStatus(Model):
    "维修状态的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'maintenance_status'

    id = schema.Column(types.Integer, primary_key=True)
    planeType = schema.Column(types.String(255))
    mxpType = schema.Column(types.String(255))
    aircraftId = schema.Column(types.String(255))
    planeState = schema.Column(types.String(255))
    mxpContent = schema.Column(types.String(255))
    scwcDate = schema.Column(types.DateTime)
    yjxcDate = schema.Column(types.DateTime)
    remainrlsj = schema.Column(types.Integer)
    remainfxsj = schema.Column(types.Integer)
    remainfxcs = schema.Column(types.Integer)
    addDate = schema.Column(types.DateTime)
    airLxgzId = schema.Column(types.Integer)

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
