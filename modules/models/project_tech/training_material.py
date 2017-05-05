# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class TrainigMaterial(Model):
    "培训资料的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'train_file_resource'

    id = schema.Column(types.Integer, primary_key=True)
    trainFileResourceNum = schema.Column(types.String(255))
    trainFileResourceName = schema.Column(types.String(255))
    trainFileResourceType = schema.Column(types.String(255))
    trainFileResourceContent = schema.Column(types.String(255))
    trainFileResourceUrl = schema.Column(types.String(255))
    addTime = schema.Column(types.DateTime)

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
