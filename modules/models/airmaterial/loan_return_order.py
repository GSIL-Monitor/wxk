# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class LoanReturnOrder(Model, AuditModel):
    """借出归还单"""

    __tablename__ = 'loan_return_order'

    def _id_generator():
        return id_generator('JCGH', LoanReturnOrder, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), default=_id_generator)
    # 日期
    date = schema.Column(types.DateTime, default=date_generator)
    # 借出类别
    loanCategory = schema.Column(types.Enum('一般', '重要'), nullable=False)
    # 归还单位
    borrowCompany = schema.Column(types.String(255))
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
    # returnDate 归还日期
    returnDate = schema.Column(types.String(255), default=date_generator)
    # statusName 状态值
    statusName = schema.Column(types.String(100))
    # 借出申请-->借出归还
    loanApplication_id = schema.Column(types.Integer, ForeignKey(
        'loan_application.id'), nullable=False)
    loanApplication = relationship(
        'LoanApplicationOrder', backref='loanReturnOrders')

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


class LoanReturnMaterial(Model):
    """借出归还内容"""

    __tablename__ = 'loan_return_material'
    id = schema.Column(types.Integer, primary_key=True)
    # category 类型
    category = schema.Column(types.String(255))
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # manufacturer 生成厂商
    manufacturer = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # flyTime 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落架次
    flightTimes = schema.Column(types.Integer)
    # lastCheckDate 上次检查时间
    lastCheckDate = schema.Column(types.String(255))
    # 外键
    loanReturnOrder_id = schema.Column(types.Integer, ForeignKey(
        'loan_return_order.id'))
    loanReturnOrder = relationship(
        "LoanReturnOrder", backref="loanReturnMaterials")
