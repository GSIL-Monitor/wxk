# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class TechMaterial(Model):
    "技术资料的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'file_resource'

    id = schema.Column(types.Integer, primary_key=True)
    fileResourceNum = schema.Column(types.String(255))
    fileResourceName = schema.Column(types.String(255))
    fileResourceUrl = schema.Column(types.String(255))
    fileResourceType = schema.Column(types.String(255))
    version = schema.Column(types.String(255))
    relatePlanType = schema.Column(types.String(255))
    addTime = schema.Column(types.DateTime)
    flag = schema.Column(types.String(255))

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
