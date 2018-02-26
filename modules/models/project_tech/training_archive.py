# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model
from ..id_generator import id_generator
from ..audit import AuditModel


class TrainingArchive(Model, AuditModel):
    "培训档案的模型定义"

    # 为了兼容原外包实现的名称

    __tablename__ = 'train_record'

    def _id_generator():
        return id_generator('PXDA', TrainingArchive, 'trainNumber')

    id = schema.Column(types.Integer, primary_key=True)
    trainNumber = schema.Column(types.String(255),
                                default=_id_generator)
    userName = schema.Column(types.String(255))
    trainRecordTime = schema.Column(types.DateTime)
    quarters = schema.Column(types.String(255))
    trainRecordName = schema.Column(types.String(255))
    trainRecordScore = schema.Column(types.String(255))

    statusName = schema.Column(types.String(255))

    trainRecordContent = schema.Column(types.Text)

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value
