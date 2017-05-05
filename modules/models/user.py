# encoding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from flask_security import UserMixin

from .base import Model, db


roles_users = db.Table('roles_users',
                       schema.Column('user_id', types.Integer,
                                     schema.ForeignKey('user.id')),
                       schema.Column('role_id', types.Integer,
                                     schema.ForeignKey('role.id')))


class User(Model, UserMixin):
    "用户模型"

    __tablename__ = 'user'

    id = schema.Column(types.Integer, primary_key=True)
    # 真实姓名
    realName = schema.Column(types.String(255))
    # 昵称
    nickName = schema.Column(types.String(255))
    # 用户名
    username = schema.Column(types.String(255))
    # 口令
    password = schema.Column(types.String(512))
    email = schema.Column(types.String(255))
    phone = schema.Column(types.String(255))
    active = schema.Column(types.Boolean)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('uesrs', lazy='dynamic'))

    confirmed_at = schema.Column(types.DateTime)

    last_login_at = schema.Column(types.DateTime)
    current_login_at = schema.Column(types.DateTime)
    last_login_ip = schema.Column(types.String(255))
    current_login_ip = schema.Column(types.String(255))
    login_count = schema.Column(types.Integer)

    def __str__(self):
        return (self.realName or self.nickName or self.username or
                self.email)
