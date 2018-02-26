# encoding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from modules.models.base import Model, db


class SubFormula(Model):
    "子配方信息"

    __tablename__ = 'sub_formula'

    id = schema.Column(types.Integer, primary_key=True)

    pesticide_id = schema.Column(types.Integer, schema.ForeignKey('pesticide.id'), nullable=False)
    # 重量
    weight = schema.Column(types.DECIMAL(precision=20, scale=3))

    formula_id = schema.Column(types.Integer, schema.ForeignKey('formula.id'))

    def __str__(self):
        return '农药:{}  重量:{}'.format(self.pesticide, self.weight)


class Formula(Model):
    """配方信息"""

    __tablename__ = 'formula'

    id = schema.Column(types.Integer, primary_key=True)
    # 配方编号
    number = schema.Column(types.String(100))
    # 配方名称
    name = schema.Column(types.String(100))
    # 所需农药
    sub_formula = db.relationship('SubFormula', backref="formula")
