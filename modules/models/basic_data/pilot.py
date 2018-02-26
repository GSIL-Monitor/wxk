# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class Pilot(Model):

    __tablename__ = 'pilot'

    id = schema.Column(types.Integer, primary_key=True)
    code = schema.Column(types.String(255))
    name = schema.Column(types.String(255))

    @classmethod
    def get_all(cls):
        return cls.query.all()
