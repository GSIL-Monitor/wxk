# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship, remote, foreign

from ..base import Model, db
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


category = types.Enum('适航指令(CAD/AD）', '服务通告(SB/CSB)',
                      '紧急服务通告（ASB）', '服务信函(SL)')


class Airworthiness(Model, AuditModel):
    "适航文件的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'continues'

    def _id_generator():
        return id_generator('SHWJ', Airworthiness, 'continusNum')

    id = schema.Column(types.Integer, primary_key=True)
    continusNum = schema.Column(types.String(255), nullable=False,
                                default=_id_generator)
    cname = schema.Column(types.String(255), nullable=False)
    # 生效日期
    execTime = schema.Column(types.String(255), nullable=False,
                             default=date_generator)
    # 颁布日期
    publishTime = schema.Column(types.String(255), nullable=False,
                                default=date_generator)
    # 受影响的机型
    planeType = schema.Column(types.String(255))
    # 飞机注册号
    jihao = schema.Column(types.String(255))
    # # 受影响的飞机
    # effectPlan = schema.Column(types.String(255))
    # 受影响部件
    effectPart = schema.Column(types.String(255))
    # 受影响的发动机
    effectEngine = schema.Column(types.String(255))
    # 类别
    concategory = schema.Column(category, nullable=False)
    # 出处
    fromWhere = schema.Column(types.String(255))
    # 执行费用, 单位:元
    execCost = schema.Column(types.Float)
    # 能否索赔
    isClaim = schema.Column(types.Enum('可索赔', '不可索赔'), nullable=False)
    # 执行能力
    isExec = schema.Column(types.Enum('有', '无'), nullable=False)
    # 停场时间
    stopTime = schema.Column(types.Float)
    # 所需工时
    needTime = schema.Column(types.Float)
    # 工程师意见
    engineerSuggestion = schema.Column(types.Enum('执行', '不执行'), nullable=False)
    # 状态
    statusName = schema.Column(types.String(255))
    # 适用性
    usability = schema.Column(types.String(255))
    # 备注
    remark = schema.Column(types.String(255))

    # 原文摘要
    conabstract = schema.Column(types.Text)
    # 相关文件
    relateFileUrl = schema.Column(types.String(1000))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.continusNum

    def __str__(self):
        return self.continusNum