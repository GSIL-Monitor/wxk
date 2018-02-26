# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from datetime import datetime

from ..base import db, Model
from ..audit import AuditModel
from ..id_generator import id_generator


class TechMaterial(Model, AuditModel):
    "技术资料的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'file_resource'

    def _id_generator():
        return id_generator('JSZL', TechMaterial, 'fileResourceNum')

    id = schema.Column(types.Integer, primary_key=True)
    statusName = schema.Column(types.String(255))
    fileResourceNum = schema.Column(types.String(255),
                                    default=_id_generator)
    version = schema.Column(types.String(255))
    fileResourceName = schema.Column(types.String(255))
    addTime = schema.Column(db.TIMESTAMP(True),
                            nullable=False,
                            default=datetime.now)

    fileResourceType = schema.Column(types.String(255))
    content = schema.Column(types.Text)

    relatePlanType = schema.Column(types.String(255))
    fileResourceUrl = schema.Column(types.String(1000))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.fileResourceNum
