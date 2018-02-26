# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class LendApplication(Model, AuditModel):
    "借入申请的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'lend_application'

    def _id_generator():
        return id_generator('JRSQ', LendApplication, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), nullable=False,
                           default=_id_generator)
    # lendCategory 借入类型
    lendCategory = schema.Column(types.Enum('一般航材', '重要航材'), nullable=False)
    # 单据日期
    date = schema.Column(types.String(255), default=date_generator)
    # 申请日期
    applicationDate = schema.Column(
        types.String(255), default=date_generator)
    # companyName 单位名称
    companyName = schema.Column(types.String(255))
    # companyAddr 单位地址
    companyAddr = schema.Column(types.String(255))
    # contactPerson 联系人
    contactPerson = schema.Column(types.String(255))
    # telephone 联系电话
    telephone = schema.Column(types.String(255))
    # fax 传真
    fax = schema.Column(types.String(255))
    # mailbox 邮箱
    mailbox = schema.Column(types.String(255))
    # remark 备注
    remark = schema.Column(types.String(255))
    # statusName 状态值
    statusName = schema.Column(types.String(255))
    # 合同文件
    contractFile = schema.Column(types.String(1000))

    # applicationReason 申请原因
    applicationReason = schema.Column(types.String(255))
    # accessory 附件
    accessory = schema.Column(types.String(1000))

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


class LendApplicationMaterial(Model):
    """借入申请内容"""

    __tablename__ = 'lend_application_material'
    id = schema.Column(types.Integer, primary_key=True)
    # category 类型
    category = schema.Column(types.String(255))
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # flyTime 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # 外键
    lendApplication_id = schema.Column(
        types.Integer, ForeignKey('lend_application.id'))
    lendApplication = relationship(
        "LendApplication", backref="lendApplicationMaterials")
