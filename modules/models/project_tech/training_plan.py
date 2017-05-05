# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class TrainingPlan(Model):
    "培训计划的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'train_plan'

    id = schema.Column(types.Integer, primary_key=True)
    approveSuggestions = schema.Column(types.String(255))
    approveTime = schema.Column(types.DateTime)
    approveUserName = schema.Column(types.String(255))
    reviewSuggestions = schema.Column(types.String(255))
    reviewTime = schema.Column(types.DateTime)
    reviewUserName = schema.Column(types.String(255))
    statusName = schema.Column(types.String(255))
    trainPlanContent = schema.Column(types.String(255))
    trainPlanEndTime = schema.Column(types.DateTime)
    trainPlanFileUrl = schema.Column(types.String(255))
    trainPlanGzFrom = schema.Column(types.String(255))
    trainPlanJoin = schema.Column(types.String(255))
    trainPlanNum = schema.Column(types.String(255))
    trainPlanPlace = schema.Column(types.String(255))
    trainPlanStartTime = schema.Column(types.DateTime)
    trainPlanTeacher = schema.Column(types.String(255))
    trainPlanUnit = schema.Column(types.String(255))

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
