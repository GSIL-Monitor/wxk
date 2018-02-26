# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types, ForeignKey
from sqlalchemy.orm import relationship

from ..base import Model
from ..audit import AuditModel
from ..id_generator import id_generator, date_generator


class PutOutStoreModel(Model, AuditModel):
    """出库的模型定义"""

    # 为了兼容原外包实现的名称
    __tablename__ = 'put_out_store'

    def _id_generator():
        return id_generator('HCRK', PutOutStoreModel, 'number')

    id = schema.Column(types.Integer, primary_key=True)
    # 编号
    number = schema.Column(types.String(255), default=_id_generator)
    # 出库日期
    outDate = schema.Column(types.String(255), default=date_generator)
    # 单据日期
    date = schema.Column(types.String(255), default=date_generator)
    # 出库类别
    outStoreCategory = schema.Column(types.String(255))
    # 借出类型
    loanCategory = schema.Column(types.String(255))
    # 借用单位
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
    # accessory 附件
    accessory = schema.Column(types.String(1000))
    # statusName 状态值
    statusName = schema.Column(types.String(100))

    # 借入归还->出库
    borrowingInReturn_id = schema.Column(
        types.Integer, ForeignKey("borrowing_in_return.id"))
    borrowingInReturn = relationship(
        "BorrowingInReturnModel", backref="putOutStore")

    # 借出申请->出库
    loanApplication_id = schema.Column(
        types.Integer, ForeignKey("loan_application.id"))
    loanApplication = relationship(
        "LoanApplicationOrder", backref="putOutStore")

    # 装机->出库
    assemble_application_id = schema.Column(
        types.Integer, ForeignKey("assemble_application.id"))
    assembleApplication = relationship(
        "AssembleApplication", backref="putOutStore")

    # 报废->出库
    scrap_id = schema.Column(
        types.Integer, ForeignKey("scrap.id"))
    scrap = relationship(
        "Scrap", backref="putOutStore")

    # 送修申请->出库
    repair_application_id = schema.Column(
        types.Integer, ForeignKey("repair_application.id"))
    repairApplication = relationship(
        "RepairApplication", backref='putOutStore')

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


class PutOutStoreMaterial(Model):
    """出库航材列表模型定义"""

    __tablename__ = 'put_out_store_material'
    id = schema.Column(types.Integer, primary_key=True)

    # partNumber 件号
    partNumber = schema.Column(types.String(255))
    # serialNum 序号
    serialNum = schema.Column(types.String(255))
    # name 名称
    name = schema.Column(types.String(255))
    # category 类型
    category = schema.Column(types.String(255))
    # quantity 数量
    quantity = schema.Column(types.Integer)
    # unit 单位
    unit = schema.Column(types.String(255))
    # manufacturer 生产厂商
    manufacturer = schema.Column(types.String(255))
    # supplier 供应商
    supplier = schema.Column(types.String(255))
    # flyTimes 飞行小时
    flyTime = schema.Column(types.String(255))
    # engineTime 发动机小时
    engineTime = schema.Column(types.String(255))
    # flightTimes 起落架次
    flightTimes = schema.Column(types.Integer)
    # effectiveDate 库存有效期
    effectiveDate = schema.Column(types.String(255))
    # lastCheckDate 上次检查日期
    lastCheckDate = schema.Column(types.String(255))
    # nextCheckDate 下次检查日期
    nextCheckDate = schema.Column(types.String(255))
    # planeNum 飞机注册号
    planeNum = schema.Column(types.String(255))
    # 报废原因
    scrapReason = schema.Column(types.String(255))
    # repairCompany 送修单位
    repairCompany = schema.Column(types.String(255))
    # 外键
    putOutStorage_id = schema.Column(types.Integer, ForeignKey(
        'put_out_store.id'))
    putOutStore = relationship(
        "PutOutStoreModel", backref="putOutStoreMaterials")
