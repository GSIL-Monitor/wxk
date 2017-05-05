# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class Retain(Model):
    "保留工作的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'air_blgz'

    id = schema.Column(types.Integer, primary_key=True)
    approveSuggestions = schema.Column(types.String(255))
    approveTime = schema.Column(types.DateTime)
    approveUserName = schema.Column(types.String(255))
    blQiXian = schema.Column(types.DateTime)
    blYuanyin = schema.Column(types.String(255))
    blgzNum = schema.Column(types.String(255))
    blgzProjectContext = schema.Column(types.String(255))
    fdjxlNum = schema.Column(types.String(255))
    flyTime = schema.Column(types.String(255))
    insNum = schema.Column(types.String(255))
    needHangCai = schema.Column(types.String(255))
    needgongjushebei = schema.Column(types.String(255))
    other = schema.Column(types.String(255))
    planeType = schema.Column(types.String(255))
    reviewSuggestions = schema.Column(types.String(255))
    reviewTime = schema.Column(types.DateTime)
    reviewUserName = schema.Column(types.String(255))
    riQi = schema.Column(types.DateTime)
    shenqingPerson = schema.Column(types.String(255))
    statusName = schema.Column(types.String(255))
    xunHuan = schema.Column(types.Integer)
    yuliuCon = schema.Column(types.String(255))
    zhiZhaoHao = schema.Column(types.String(255))
    zhuceNum = schema.Column(types.String(255))
    fhblqx = schema.Column(types.DateTime)
    spblqx = schema.Column(types.DateTime)

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
