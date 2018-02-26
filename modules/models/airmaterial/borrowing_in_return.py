# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class BorrowingInReturnModel(Model, AuditModel):
    """借入归还的模型定义"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'borrowing_in_return'

    def _id_generator():
        return id_generator('JRGH', BorrowingInReturnModel, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), nullable=False,
                           default=_id_generator)
    # lendCategory 借入类型
    lendCategory = schema.Column(types.String(255))
    # returnDate 归还日期
    returnDate = schema.Column(types.String(255), default=date_generator)
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

    # 借入申请->借入归还
    borrow_in = schema.Column(types.Integer, ForeignKey('lend_application.id'))
    borrow = relationship("LendApplication", backref="borrowingInReturn")

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


class BorrowingInReturnMaterial(Model):
    """借入归还内容"""

    __tablename__ = 'borrowing_in_return_material'

    id = schema.Column(types.Integer, primary_key=True)
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # category 类别
    category = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # flyTime 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落次数
    flightTimes = schema.Column(types.Integer)
    # effectiveDate 库存有效期
    effectiveDate = schema.Column(types.String(255))
    # lastCheckDate 上次检查日期
    lastCheckDate = schema.Column(types.String(255))
    # nextCheckDate 下次检查日期
    nextCheckDate = schema.Column(types.String(255))

    # 外键
    borrowInReturn_id = schema.Column(
        types.Integer, ForeignKey('borrowing_in_return.id'))
    borrowInReturn = relationship(
        "BorrowingInReturnModel", backref="borrowingInReturnMaterials")
