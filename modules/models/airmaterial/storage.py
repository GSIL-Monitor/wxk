# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class StorageList(Model):
    "库存可增行删行的内容"

    __tablename__ = "storage_list"

    id = schema.Column(types.Integer, primary_key=True)
    # category 航材类型
    category = schema.Column(types.String(255))
    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 航材名称
    name = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # unitPrice 单价
    unitPrice = schema.Column(types.Float)
    # unit 航材单位
    unit = schema.Column(types.String(255))
    # flyTime 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落架次
    flightTimes = schema.Column(types.Integer)
    # applicableModel 适用机型
    applicableModel = schema.Column(types.String(255))
    # storehouse 仓库
    storehouse = schema.Column(types.String(255))
    # shelf 架位
    shelf = schema.Column(types.String(255))
    # disassembleDate 拆下日期
    disassembleDate = schema.Column(types.String(255))
    # effectiveDate 有效日期
    effectiveDate = schema.Column(types.String(255))
    # certificateNum 证书编号
    certificateNum = schema.Column(types.String(255))
    # airworthinessTagNum 适航标签号
    airworthinessTagNum = schema.Column(types.String(255))
    # lastCheckDate 上次检查日期
    lastCheckDate = schema.Column(types.String(255))
    # nextCheckDate 下次检查日期
    nextCheckDate = schema.Column(types.String(255))
    # checkInstruction 检查说明
    checkInstruction = schema.Column(types.String(255))
    # manufacturer 生产厂商
    manufacturer = schema.Column(types.String(255))
    # supplier 供应商
    supplier = schema.Column(types.String(255))
    # planeNum 拆下机号
    planeNum = schema.Column(types.String(255))
    # 外键
    storage_id = schema.Column(types.Integer, ForeignKey(
        'put_storage.id'))
    storage = relationship("Storage", backref="storageList")


class Storage(Model, AuditModel):
    "入库的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'put_storage'

    def _id_generator():
        return id_generator('PXJH', Storage, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), default=_id_generator)
    # 日期
    date = schema.Column(types.String(255), default=date_generator)
    # 入库类别
    instoreCategory = schema.Column(types.String(255))
    # 入库日期
    instorageDate = schema.Column(types.String(255), default=date_generator)
    # remark 备注
    remark = schema.Column(types.String(255))
    # accessory 附件
    accessory = schema.Column(types.String(1000))
    # statusName 状态值
    statusName = schema.Column(types.String(100))

    # 借入申请->入库单
    borrow_id = schema.Column(types.Integer, ForeignKey('lend_application.id'))
    borrow = relationship("LendApplication", backref="storage")
    # 借出归还->入库单
    loanReturn_id = schema.Column(
        types.Integer, ForeignKey('loan_return_order.id'))
    loanReturn = relationship('LoanReturnOrder', backref='storage')

    # 拆机单->入库单
    disassemble_id = schema.Column(
        types.Integer, ForeignKey('disassemble_order.id'))
    disassemble = relationship("DisassembleOrder", backref="storage")

    # 退料单->入库单
    returnMaterial_id = schema.Column(
        types.Integer, ForeignKey('return_material_order.id'))
    returnMaterial = relationship("ReturnMaterialOrder", backref="storage")

    # 送修归还->入库单
    repairReturn_id = schema.Column(
        types.Integer, ForeignKey('repair_return_order.id'))
    repairReturnOrder = relationship('RepairReturnOrder', backref='storage')

    # 采购入库->入库单
    purchaseApplication_id = schema.Column(
        types.Integer, ForeignKey('purchase_application.id'))
    purchaseApplication = relationship(
        'PurchaseApplication', backref='storage')

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
