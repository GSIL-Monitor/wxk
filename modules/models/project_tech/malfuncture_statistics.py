# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class MalfunctureStatistics(Model):
    "故障统计的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'plan_fault_statistical'

    id = schema.Column(types.Integer, primary_key=True)
    ataNum = schema.Column(types.String(255))
    checkType = schema.Column(types.String(255))
    feiliNum = schema.Column(types.String(255))
    mainMeas = schema.Column(types.String(255))
    planNo = schema.Column(types.String(255))
    repoerPerson = schema.Column(types.String(255))
    statisDate = schema.Column(types.DateTime)
    statisDesc = schema.Column(types.String(255))
    statisFrom = schema.Column(types.String(255))
    flag = schema.Column(types.String(255))

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
