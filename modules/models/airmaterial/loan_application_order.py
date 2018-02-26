# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class LoanMaterial(Model):
    """借出航材详情"""
    id = schema.Column(types.Integer, primary_key=True)
    # category 类别
    category = schema.Column(types.String(255))
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # manufacturer 生产厂商
    manufacturer = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # flyTime 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落架次
    flightTimes = schema.Column(types.Integer)
    # effectiveDate 有效日期
    effectiveDate = schema.Column(types.String(255))
    # lastCheckDate 上次检查时间
    lastCheckDate = schema.Column(types.String(255))
    # nextCheckDate 下次检查时间
    nextCheckDate = schema.Column(types.String(255))
    # 外键
    loanApplication_id = schema.Column(types.Integer, ForeignKey(
        'loan_application.id'), nullable=False)
    storage = relationship("LoanApplicationOrder", backref="loanMaterials")


class LoanApplicationOrder(Model, AuditModel):
    """借出申请的模型定义"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'loan_application'

    def _id_generator():
        return id_generator('JCSQ', LoanApplicationOrder, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), nullable=False,
                           default=_id_generator)
    # 申请日期
    applicationDate = schema.Column(types.String(255), default=date_generator)
    # loanCategory 借出类型
    loanCategory = schema.Column(types.Enum('一般', '重要'), nullable=False)
    # 单据日期
    date = schema.Column(types.String(255), default=date_generator)
    # applicationReason 申请原因
    applicationReason = schema.Column(types.String(255))
    # companyAddr 单位地址
    companyAddr = schema.Column(types.String(255))
    # borrowCompany 借用单位
    borrowCompany = schema.Column(types.String(255))
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
