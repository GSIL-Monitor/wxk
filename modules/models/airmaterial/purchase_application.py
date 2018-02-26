# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from ..base import db, Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class PurchaseMaterial(Model):

    __tablename__ = 'purchase_material'

    id = schema.Column(types.Integer, primary_key=True)

    # category 航材类型
    category = schema.Column(types.String(255))

    application_id = schema.Column(types.Integer, schema.ForeignKey('purchase_application.id'), nullable=False)
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # manufacturer 生产厂商
    manufacturer = schema.Column(types.String(255))
    # unitPrice 单价
    unitPrice = schema.Column(types.Float)
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # budget 预算
    budget = schema.Column(types.String(255))


class PurchaseApplication(Model, AuditModel):
    "采购申请的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'purchase_application'

    def _id_generator():
        return id_generator('CGSQ', PurchaseApplication, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), nullable=False,
                           default=_id_generator)
    # 日期
    date = schema.Column(types.String(255), default=date_generator)
    # 申请日期
    applicationDate = schema.Column(
        types.String(255), default=date_generator)
    # supplier 供应商
    supplier = schema.Column(types.String(255))
    # contactPerson 联系人
    contactPerson = schema.Column(types.String(255))
    # telephone 联系电话
    telephone = schema.Column(types.String(255))
    # fax 传真
    fax = schema.Column(types.String(255))
    # mailbox 邮箱
    mailbox = schema.Column(types.String(255))
    # receiver 收货人
    receiver = schema.Column(types.String(255))
    # remark 备注
    remark = schema.Column(types.String(255))
    # applicationInstruction 申请说明
    applicationInstruction = schema.Column(types.String(255))
    # accessory 附件
    accessory = schema.Column(types.String(1000))
    # statusName 状态值
    statusName = schema.Column(types.String(255))
    # 合同文件
    contractFile = schema.Column(types.String(1000))
    # 会议纪要
    meetingFile = schema.Column(types.String(1000))

    purchase = db.relationship('PurchaseMaterial', backref="application")

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
