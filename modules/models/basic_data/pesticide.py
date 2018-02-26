# encoding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from modules.models.base import db, Model


class Pesticide(Model):
    """农药信息"""

    __tablename__ = 'pesticide'

    id = schema.Column(types.Integer, primary_key=True)
    # 农药编号
    number = schema.Column(types.String(100))
    # 农药名称
    name = schema.Column(types.String(100))

    sub_formula = db.relationship('SubFormula', backref="pesticide")

    def __str__(self):
        return self.name
