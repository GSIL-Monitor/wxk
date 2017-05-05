# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class OilSampleDetection(Model):
    "油样检测的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'oil_sample'

    id = schema.Column(types.Integer, primary_key=True)
    ataNum = schema.Column(types.String(30))
    banbenTime = schema.Column(types.DateTime)
    detectionCause = schema.Column(types.String(255))
    detectionUnit = schema.Column(types.String(255))
    evaluationBasis = schema.Column(types.String(255))
    evaluationOpinion = schema.Column(types.String(255))
    reviewTime = schema.Column(types.DateTime)
    reviewUserName = schema.Column(types.String(255))
    reviewSuggestions = schema.Column(types.String(255))
    jcTime = schema.Column(types.DateTime)
    oiUseTime = schema.Column(types.DateTime)
    oil = schema.Column(types.String(255))
    oilName = schema.Column(types.String(255))
    planNo = schema.Column(types.String(255))
    relateFileUrl = schema.Column(types.String(255))
    reportNo = schema.Column(types.String(255))
    approveTime = schema.Column(types.DateTime)
    approveUserName = schema.Column(types.String(255))
    approveSuggestions = schema.Column(types.String(255))
    statusName = schema.Column(types.String(255))
    treatmentOpinion = schema.Column(types.String(255))
    oilNum = schema.Column(types.String(255))

    creatTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
