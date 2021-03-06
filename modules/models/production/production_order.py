# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from ..base import Model
from ..audit import AuditModel


class ProductionOrder(Model, AuditModel):
    "生产指令的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'shengchanzl'

    id = schema.Column(types.Integer, primary_key=True)
    fafangTime = schema.Column(types.String(255))
    fileUrl = schema.Column(types.String(255))
    gongzuoContext = schema.Column(types.String(255))
    gongzuoProject = schema.Column(types.String(255))
    insNum = schema.Column(types.String(255))
    jiezhiTime = schema.Column(types.DateTime)
    makePerson = schema.Column(types.String(255))
    sczlNum = schema.Column(types.String(255))
    shejiPerson = schema.Column(types.String(255))
    shejiPlane = schema.Column(types.String(255))
    statusName = schema.Column(types.String(255))
    yujigzTime = schema.Column(types.DateTime)
    yujing = schema.Column(types.String(255))
    gczlNum = schema.Column(types.String(255))
    numFrom = schema.Column(types.String(255))
    jcry = schema.Column(types.String(255))
    wcqk = schema.Column(types.String(255))
    wcrq = schema.Column(types.DateTime)
