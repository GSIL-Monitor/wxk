# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator


class Retain(Model, AuditModel):
    "保留工作的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'air_blgz'

    def _id_generator():
        return id_generator('BLGZ', Retain, 'retainNum')

    id = schema.Column(types.Integer, primary_key=True)
    retainNum = schema.Column(types.String(255), nullable=False,
                              default=_id_generator)
    planeType = schema.Column(types.String(255), nullable=False)
    flihtTime = schema.Column(types.Float)
    jihao = schema.Column(types.String(255))
    engineNum = schema.Column(types.String(255))
    limit = schema.Column(types.String(255), nullable=False)
    proposer = schema.Column(types.String(255))
    date = schema.Column(types.String(255), nullable=False)
    licenceNO = schema.Column(types.String(255))
    other = schema.Column(types.String(255))

    content = schema.Column(types.String(255), nullable=False)
    reseason = schema.Column(types.String(255), nullable=False)

    statusName = schema.Column(types.String(255))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.retainNum
