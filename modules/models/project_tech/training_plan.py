# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model, db
from ..id_generator import id_generator
from ..audit import AuditModel


class TrainingPlan(Model, AuditModel):
    "培训计划的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'train_plan'

    def _id_generator():
        return id_generator('PXJH', TrainingPlan, 'trainPlanNum')

    id = schema.Column(types.Integer, primary_key=True)
    trainPlanNum = schema.Column(types.String(255),
                                 default=_id_generator)
    trainPlanStartTime = schema.Column(types.DateTime)
    trainPlanEndTime = schema.Column(types.DateTime)
    trainPlanGzFrom = schema.Column(types.String(255))
    trainPlanPlace = schema.Column(types.String(255))
    trainPlanTeacher = schema.Column(types.String(255))
    trainPlanJoin = schema.Column(types.String(255))
    trainPlanContent = schema.Column(types.String(255))
    trainPlanFileUrl = schema.Column(types.String(1000))

    statusName = schema.Column(types.String(255))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.trainPlanNum
