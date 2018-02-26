# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model
from ..id_generator import id_generator
from ..audit import AuditModel


class TrainigMaterial(Model, AuditModel):
    "培训资料的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'train_file_resource'

    def _id_generator():
        return id_generator('PXZL', TrainigMaterial, 'trainNumber')

    id = schema.Column(types.Integer, primary_key=True)
    trainNumber = schema.Column(
        types.String(255), default=_id_generator)
    trainFileResourceType = schema.Column(types.String(255))
    trainFileResourceName = schema.Column(types.String(255))
    trainFileResourceContent = schema.Column(types.Text)
    addTime = schema.Column(types.DateTime)
    updateUser = schema.Column(types.String(255))
    updTime = schema.Column(types.DateTime)
    statusName = schema.Column(types.String(255))
    trainFileResourceUrl = schema.Column(types.String(1000))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value
