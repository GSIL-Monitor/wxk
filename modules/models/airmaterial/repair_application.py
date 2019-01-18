# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class RepairApplication(Model, AuditModel):
    """送修的模型定义"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'repair_application'

    def _id_generator():
        return id_generator('SXSQ', RepairApplication, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), nullable=False,
                           default=_id_generator)
    # 申请日期
    applicationDate = schema.Column(
        types.String(255), default=date_generator)
    # repaireCompany 维修厂商
    repairCompany = schema.Column(types.String(255))
    # contactPerson 联系人
    contactPerson = schema.Column(types.String(255))
    # telephone 联系电话
    telephone = schema.Column(types.String(255))
    # fax 传真
    fax = schema.Column(types.String(255))
    # mailbox 邮箱
    mailbox = schema.Column(types.String(255))
    # budget 预算
    budget = schema.Column(types.String(255))
    # remark 备注
    remark = schema.Column(types.String(255))
    # accessory 附件
    accessory = schema.Column(types.String(1000))
    # 合同文件
    contractFile = schema.Column(types.String(1000))
    # statusName 状态值
    statusName = schema.Column(types.String(255))

    repairAppl = relationship(
        "RepairMaterial", backref="repairApplication")

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value

    @property
    def business_id(self):
        return self.number

    def __str__(self):
        return self.number


class RepairMaterial(Model):
    """维修内容"""

    __tablename__ = 'repair_material'
    id = schema.Column(types.Integer, primary_key=True)
    # category 航材类型
    category = schema.Column(types.String(255))
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # manufacturer 生产厂商
    manufacturer = schema.Column(types.String(255))
    # effectiveDate 库存有效期
    effectiveDate = schema.Column(types.String(255))
    # lastCheckDate 上次检查日期
    lastCheckDate = schema.Column(types.String(255))
    # nextCheckDate 下次检查日期
    nextCheckDate = schema.Column(types.String(255))
    # planeNum 拆下机号
    planeNum = schema.Column(types.String(255))
    # planeType 机型
    planeType = schema.Column(types.String(255))
    # assembleDate 装上日期
    assembleDate = schema.Column(types.String(255))
    # disassembleDate 拆下日期
    disassembleDate = schema.Column(types.String(255))
    # repairedReuseDate 维修后使用时间
    repairedReuseDate = schema.Column(types.String(255))
    # totalUseTime 总使用时间
    totalUseTime = schema.Column(types.String(255))
    # flyTime 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落次数
    flightTimes = schema.Column(types.Integer)
    # 外键
    application_id = schema.Column(
        types.Integer, ForeignKey('repair_application.id'), nullable=False)
