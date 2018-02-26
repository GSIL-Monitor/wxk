# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class Assemble(Model, AuditModel):
    """装机单"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'assemble'

    def _id_generator():
        return id_generator('ZJSQ',
                            Assemble, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), nullable=False,
                           default=_id_generator)
    # 日期
    date = schema.Column(types.String(255), default=date_generator)
    # applyPerson 联系人
    assemblePerson = schema.Column(types.String(255))
    # applyDate 申请日期
    assembleDate = schema.Column(types.String(255), default=date_generator)

    assembleapplication_id = schema.Column(
        types.Integer, ForeignKey('assemble_application.id'))
    assembleApplication = relationship(
        "AssembleApplication", backref="assemble")
    # statusName 状态
    statusName = schema.Column(types.String(255))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.number

    def __str__(self):
        return self.number
