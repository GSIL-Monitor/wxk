# encoding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from sqlalchemy.orm import relationship, backref
from flask_security import RoleMixin

from .base import Model


class BasicAction(Model):
    "基本的操作"

    __tablename__ = 'basic_action'
    id = schema.Column(types.Integer, primary_key=True)
    model = schema.Column(types.String(255))
    create = schema.Column(types.Boolean)
    edit = schema.Column(types.Boolean)
    view = schema.Column(types.Boolean)
    delete = schema.Column(types.Boolean)

    # 所属的角色
    role_id = schema.Column(types.Integer, schema.ForeignKey('role.id'))

    # 扩展操作
    submit_review = schema.Column(types.Boolean)
    review_approve = schema.Column(types.Boolean)
    review_refuse = schema.Column(types.Boolean)
    review_again = schema.Column(types.Boolean)
    submit_approve = schema.Column(types.Boolean)
    approved = schema.Column(types.Boolean)
    approve_refuse = schema.Column(types.Boolean)
    approve_again = schema.Column(types.Boolean)
    cancel = schema.Column(types.Boolean)

    def __dir__(self):
        return ['create', 'edit', 'view', 'delete',
                'submit_review', 'review_approve', 'review_refuse',
                'review_again', 'submit_approve', 'approved',
                'approve_again', 'approve_refuse', 'cancel',
        ]


class Role(Model, RoleMixin):
    "角色模型"

    __tablename__ = 'role'

    id = schema.Column(types.Integer, primary_key=True)
    name = schema.Column(types.String(255))
    description = schema.Column(types.String(255))

    actions = relationship('BasicAction', backref="role")

    def __str__(self):
        return self.name
