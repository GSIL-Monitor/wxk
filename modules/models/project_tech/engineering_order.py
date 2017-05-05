# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from sqlalchemy.orm import relationship, foreign, remote

from ..base import Model
from ..action import ActionDescription


class EngineeringOrder(Model):
    "工程指令的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'instruction'

    id = schema.Column(types.Integer, primary_key=True)
    approveSuggestions = schema.Column(types.String(255))
    approveTime = schema.Column(types.DateTime)
    approveUserName = schema.Column(types.String(255))
    ataCode = schema.Column(types.String(255))
    claimDemage = schema.Column(types.String(255))
    codeType = schema.Column(types.String(255))
    completionDate = schema.Column(types.String(255))
    effectParts = schema.Column(types.String(500))
    effectPlan = schema.Column(types.String(255))
    fafangDate = schema.Column(types.DateTime)
    feedbackRequirement = schema.Column(types.String(500))
    fileName = schema.Column(types.String(500))
    insCode = schema.Column(types.String(255))
    insNum = schema.Column(types.String(255))
    insTitle = schema.Column(types.String(255))
    manualChange = schema.Column(types.String(500))
    outlineReason = schema.Column(types.String(500))
    planType = schema.Column(types.String(255))
    remark = schema.Column(types.String(255))
    repetitionPeriod = schema.Column(types.String(255))
    reviewSuggestions = schema.Column(types.String(255))
    reviewTime = schema.Column(types.DateTime)
    reviewUserName = schema.Column(types.String(255))
    shiyongxing = schema.Column(types.String(255))
    statusName = schema.Column(types.String(255))
    workingHours = schema.Column(types.String(255))
    zhixingData = schema.Column(types.DateTime)
    zhixingresult = schema.Column(types.String(255))
    fhyj = schema.Column(types.String(255))
    spyj = schema.Column(types.String(255))
    unit = schema.Column(types.String(255))
    yujing = schema.Column(types.String(255))

    creatTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)

    audits = relationship('ActionDescription',
                          primaryjoin=remote(ActionDescription.entity_id) == \
                          foreign(id))
