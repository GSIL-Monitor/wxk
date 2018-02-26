# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from flask_security import UserMixin

from ..base import Model, db
from ..audit import AuditModel


notification_users = db.Table('notification_users',
                              schema.Column('user_id', types.Integer,
                                            schema.ForeignKey('user.id')),
                              schema.Column('notification_id', types.Integer,
                                            schema.ForeignKey('mynotice.id')))


class Notice(Model):
    "短消息的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'mynotice'

    id = schema.Column(types.Integer, primary_key=True)

    title = schema.Column(types.String(500), nullable=False)
    content = schema.Column(types.String(500), nullable=False)

    role = schema.Column(types.String(500))

    recieveId = db.relationship('User', secondary=notification_users,
                                backref=db.backref('uesrs', lazy='dynamic'))

    recieveName = schema.Column(types.String(255))
    sendName = schema.Column(types.String(255))

    stateName = schema.Column(types.String(255))
    updateTime = schema.Column(types.DateTime)

    @property
    def status(self):
        return self.stateName

    @status.setter
    def status(self, value):
        self.stateName = value
