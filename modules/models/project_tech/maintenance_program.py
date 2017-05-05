# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class MaintenanceProgram(Model):
    "维修方案的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'maintenance_plan'

    id = schema.Column(types.Integer, primary_key=True)
    maintenancePlanNum = schema.Column(types.String(255))
    ATA = schema.Column(types.String(255))
    referAta = schema.Column(types.String(255))
    isFit = schema.Column(types.String(255))
    jcsy = schema.Column(types.String(255))
    environmentType = schema.Column(types.String(255))
    isCheck = schema.Column(types.String(255))
    isExec = schema.Column(types.String(255))
    accessoryUrl = schema.Column(types.String(255))
    relateFileUrl = schema.Column(types.String(255))
    content = schema.Column(types.String(255))
    remark = schema.Column(types.String(255))
    intervalType = schema.Column(types.String(255))
    source = schema.Column(types.String(255))

    createTime = schema.Column(types.DateTime)
    updateTime = schema.Column(types.DateTime)
