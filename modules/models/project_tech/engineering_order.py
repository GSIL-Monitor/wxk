# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Model, db
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


ins_category = types.Enum('改装', '检查', '更换', '修理', '其他')


class EngineeringOrder(Model, AuditModel):
    "工程指令的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'instruction'

    def _id_generator():
        return id_generator('GCZL', EngineeringOrder, 'insNum')

    id = schema.Column(types.Integer, primary_key=True)
    # 指令号
    insNum = schema.Column(types.String(255), nullable=False,
                           default=_id_generator)
    # 标题
    insTitle = schema.Column(types.String(255), nullable=False)
    # 指令类别
    insCategory = schema.Column(ins_category, nullable=False)
    # 受影响的机型
    planeType = schema.Column(types.String(255))
    # 受影响的飞机
    jihao = schema.Column(types.String(255))
    # 受影响部件
    effectPart = schema.Column(types.String(255))
    # 受影响的发动机
    effectEngine = schema.Column(types.String(255))
    # 发放期限
    grantTime = schema.Column(types.String(255), nullable=False,
                              default=date_generator)
    # 完成期限
    finishTime = schema.Column(types.String(255), nullable=False,
                               default=date_generator)
    # 执行日期
    executeTime = schema.Column(types.String(255), nullable=False,
                                default=date_generator)
    # 能否索赔
    isClaim = schema.Column(types.Enum('可索赔', '不可索赔'), nullable=False)
    # 工时停场时
    stopHours = schema.Column(types.Float)
    # 重复周期
    repeatePeriod = schema.Column(types.String(255))
    # ATA章节号
    ataCode = schema.Column(types.String(255))
    # 适用性
    usability = schema.Column(types.String(255))
    # 手册更改
    manualChange = schema.Column(types.Enum('是', '否'), nullable=False)
    # 是否反馈
    isFeedback = schema.Column(types.Enum('反馈', '不反馈'), nullable=False)
    # 备注/说明
    remark = schema.Column(types.String(255))
    # 概述/理由
    reason = schema.Column(types.String(255))

    # 相关文档
    relateFileUrl = schema.Column(types.String(1000))
    # 状态
    statusName = schema.Column(types.String(255))

    airworthiness_id = schema.Column(types.Integer, ForeignKey('continues.id'))
    airworthiness = relationship("Airworthiness", backref="engineeringOrders")

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.insNum

    def __str__(self):
        return self.insNum