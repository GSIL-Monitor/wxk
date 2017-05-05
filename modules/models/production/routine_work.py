# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class RoutineWork(Model):
    "例行工作的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'air_lxgz'

    id = schema.Column(types.Integer, primary_key=True)
    approveSuggestions = schema.Column(types.String(255))
    approveTime = schema.Column(types.DateTime)
    approveUserName = schema.Column(types.String(255))
    contextDesc = schema.Column(types.String(255))
    insNum = schema.Column(types.String(255))
    jcAdress = schema.Column(types.String(255))
    jcTime = schema.Column(types.DateTime)
    jcType = schema.Column(types.String(255))
    jihao = schema.Column(types.String(255))
    lxgzNum = schema.Column(types.String(255))
    planeType = schema.Column(types.String(255))
    reviewSuggestions = schema.Column(types.String(255))
    reviewTime = schema.Column(types.DateTime)
    reviewUserName = schema.Column(types.String(255))
    statusName = schema.Column(types.String(255))
    yuliuCon = schema.Column(types.String(255))

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
