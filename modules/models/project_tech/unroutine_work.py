# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class UnroutineWork(Model):
    "非例行工作的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'air_flxgz'

    id = schema.Column(types.Integer, primary_key=True)
    approveSuggestions = schema.Column(types.String(255))
    approveTime = schema.Column(types.DateTime)
    approveUserName = schema.Column(types.String(255))
    flxgzNum = schema.Column(types.String(255))
    flyJldh = schema.Column(types.String(255))
    guzhangStarTime = schema.Column(types.DateTime)
    gzAppendPlace = schema.Column(types.String(255))
    insNum = schema.Column(types.String(255))
    jihao = schema.Column(types.String(255))
    planeType = schema.Column(types.String(255))
    qxDesc = schema.Column(types.String(255))
    reviewSuggestions = schema.Column(types.String(255))
    reviewTime = schema.Column(types.DateTime)
    reviewUserName = schema.Column(types.String(255))
    statusName = schema.Column(types.String(255))
    wxtbPerson = schema.Column(types.String(255))
    yuliuCon = schema.Column(types.String(255))
    gipc = schema.Column(types.String(255))
    gjs = schema.Column(types.String(255))
    gmc = schema.Column(types.String(255))
    gsl = schema.Column(types.String(255))
    gzrq = schema.Column(types.String(255))
    gzry = schema.Column(types.String(255))
    hjs = schema.Column(types.String(255))
    hmc = schema.Column(types.String(255))
    hsl = schema.Column(types.String(255))
    jcrq = schema.Column(types.String(255))
    jcry = schema.Column(types.String(255))
    wxiu = schema.Column(types.String(255))
    bxTime = schema.Column(types.DateTime)
    bxr = schema.Column(types.String(255))
    wcqx = schema.Column(types.DateTime)
