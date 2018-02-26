# coding: utf-8

from __future__ import unicode_literals
import logging
import sys

from sqlalchemy import schema, types
from ..base import Model
from ..audit import AuditModel
from modules.flows.states import InitialState


reload(sys)
sys.setdefaultencoding('gbk')


class AirmaterialCategory(Model, AuditModel):
    "航材类别的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'airmaterial_category'

    id = schema.Column(types.Integer, primary_key=True)
    # partNumber 航材件号
    partNumber = schema.Column(types.String(255), nullable=False, unique=True)
    # name 航材名称
    name = schema.Column(types.String(255), nullable=False)
    # category 航材类型
    category = schema.Column(types.String(255), nullable=False)
    # miniStock 最低库存
    minStock = schema.Column(types.Integer)
    # unit 航材单位
    unit = schema.Column(types.String(255))
    # applicableModel 适用机型
    applicableModel = schema.Column(types.String(255))
    # 是否有库存有效期
    isOrNotHaveEffectiveDate = schema.Column(types.Boolean)
    # 是否有定期检查
    isOrNotHavePeriodCheck = schema.Column(types.Boolean)
    # statusName 状态值
    statusName = schema.Column(types.String(255))

    @property
    def status(self):
        return self.statusName

    @status.setter
    def status(self, value):
        self.statusName = value


def read_datas(row):

    data = {
        'partNumber': row['件号'.encode('utf-8')],
        'name': row['名称'.encode('utf-8')],
        'category': row['类别'.encode('utf-8')],
        # 'minStock': row['最低库存'.encode('utf-8')],
        'unit': row['单位'.encode('utf-8')],
        'applicableModel': "运5B(D)",
    }
    cate_list = ['一般航材', '工装设备', '消耗品', '化工品', '时控件', '时寿件']
    if not data['name'] or not data['partNumber']:
        logging.warn("件号或名称没有。 件号：%s，名称：%s" % (
            data['partNumber'], data['name'].decode("utf-8")))
        return None

    if data['category'].decode("utf-8") not in cate_list:
        logging.warn("%s的航材类别有误." % data['name'].decode("utf-8"))
        return None

    if row['最低库存'.encode('utf-8')]:
        if row['最低库存'.encode('utf-8')] <= 0:
            logging.msg("航材（%s）的最低库存应大于0" % data['name'].decode("utf-8"))
            return None
        data['minStock'] = int(row['最低库存'.encode('utf-8')])

    data['statusName'] = data['auditStatus'] = InitialState

    return data

