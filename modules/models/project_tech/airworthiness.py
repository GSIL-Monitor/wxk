# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from sqlalchemy.orm import relationship, remote, foreign

from ..base import Model
from ..action import ActionDescription


class Airworthiness(Model):
    "适航文件的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'continues'

    id = schema.Column(types.Integer, primary_key=True)
    continusNum = schema.Column(types.String(255))
    cname = schema.Column(types.String(255))
    effectPlanType = schema.Column(types.String(255))
    execTime = schema.Column(types.DateTime)
    publishTime = schema.Column(types.DateTime)
    effectPlan = schema.Column(types.String(255))
    effectPart = schema.Column(types.String(255))
    effectEngine = schema.Column(types.String(255))
    conabstract = schema.Column(types.Text)
    concategory = schema.Column(types.String(255))
    fromWhere = schema.Column(types.String(255))
    execCost = schema.Column(types.Float)
    isClaim = schema.Column(types.String(255))
    isExec = schema.Column(types.String(255))
    stopTime = schema.Column(types.DateTime)
    needTime = schema.Column(types.Integer)
    isFit = schema.Column(types.String(255))
    engineerSuggestion = schema.Column(types.String(255))
    execRes = schema.Column(types.String(255))
    remark = schema.Column(types.String(255))
    relateFileUrl = schema.Column(types.String(255))
    statusName = schema.Column(types.String(255))
    conNum = schema.Column(types.String(255))
    approveSuggestions = schema.Column(types.String(255))
    approveTime = schema.Column(types.DateTime)
    approveUserName = schema.Column(types.String(255))
    reviewSuggestions = schema.Column(types.String(255))
    reviewTime = schema.Column(types.DateTime)
    reviewUserName = schema.Column(types.String(255))
    yujing = schema.Column(types.String(255))

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)

    audits = relationship('ActionDescription',
                          primaryjoin=remote(
                              ActionDescription.entity_id) == foreign(id))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value
