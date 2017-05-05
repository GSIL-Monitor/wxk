# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class TrainingArchive(Model):
    "培训档案的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'train_record'

    id = schema.Column(types.Integer, primary_key=True)
    userName = schema.Column(types.String(255))
    trainRecordName = schema.Column(types.String(255))
    trainRecordTime = schema.Column(types.DateTime)
    trainRecordContent = schema.Column(types.String(255))
    trainRecordScore = schema.Column(types.Integer)
    trainUntil = schema.Column(types.String(255))
    other = schema.Column(types.String(255))
    flag = schema.Column(types.String(255))

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
