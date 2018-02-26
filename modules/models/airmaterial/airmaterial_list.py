# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class AirmaterialList(Model):
    "航材列表的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'airmaterial_list'

    id = schema.Column(types.Integer, primary_key=True)
    # 航材件号
    partNumber = schema.Column(types.String(255))
    # 航材名称
    name = schema.Column(types.String(255))
    # category 类型
    category = schema.Column(types.String(255))
    # model 型号
    model = schema.Column(types.String(255))
    # applicableModel 适用机型
    applicableModel = schema.Column(types.String(255))
    # maintenanceRules 维修规则
    maintenanceRules = schema.Column(types.String(255))
    # mIntervalType 维修方案类型
    mIntervalType = schema.Column(types.String(255))
    # mIntervalBase 维修方案基准值
    mIntervalBase = schema.Column(types.String(255))
    # intervalup 上限
    intervalupByFlightTime = schema.Column(types.Float)
    # intervaldown 下限
    intervaldownByFlightTime = schema.Column(types.Float)
    # statusName 状态值
    statusName = schema.Column(types.String(100))


    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value
