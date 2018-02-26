# coding: utf-8

from __future__ import unicode_literals

from .base import db
from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_continuum import make_versioned
from sqlalchemy.orm import configure_mappers


make_versioned()


class AuditModel(object):

    __versioned__ = {}

    auditStatus = schema.Column(types.String(255))
    timestamp = schema.Column(types.DateTime)
    suggestion = schema.Column(types.String(255))

    @declared_attr
    def relatedUser_id(cls):
        return schema.Column('relatedUser_id', ForeignKey('user.id'))

    @declared_attr
    def relatedUser(cls):
        return relationship("User", foreign_keys=[cls.relatedUser_id])

    @declared_attr
    def allowedUser_id(cls):
        return schema.Column('allowedUser_id', ForeignKey('user.id'))

    @declared_attr
    def allowedUser(cls):
        return relationship("User", foreign_keys=[cls.allowedUser_id])

    @property
    def business_id(self):
        raise NotImplementedError()


configure_mappers()
