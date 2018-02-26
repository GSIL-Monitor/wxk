# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model, db
from ..audit import AuditModel


class Announcement(db.Model, AuditModel):
    "通知公告的模型定义"

    __tablename__ = 'announcement'

    id = schema.Column(types.Integer, primary_key=True)

    title = schema.Column(types.String(255))
    content = schema.Column(types.Text)
    statusName = schema.Column(types.String(255))

    sendTime = schema.Column(types.DateTime)
    sendUser = schema.Column(types.String(255))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value
