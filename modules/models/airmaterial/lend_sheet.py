# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types

from ..base import Model


class LendSheet(Model):
    "航材借出的模型定义"

    # 为了兼容原外包实现的名称
    __tablename__ = 'lend_sheet'

    id = schema.Column(types.Integer, primary_key=True)
    number = schema.Column(types.String(100))
    date = schema.Column(types.String(100))
    companyName = schema.Column(types.String(100))
    companyAddress = schema.Column(types.String(100))
    contact = schema.Column(types.String(100))
    phone = schema.Column(types.String(100))
    fax = schema.Column(types.String(100))
    email = schema.Column(types.String(100))
    formUserName = schema.Column(types.String(100))
    remark = schema.Column(types.String(255))
    status = schema.Column(types.String(100))
    checkContent = schema.Column(types.String(100))
    checkUserName = schema.Column(types.String(100))
    checkDate = schema.Column(types.String(100))
    auditContent = schema.Column(types.String(100))
    auditUserName = schema.Column(types.String(100))
    auditDate = schema.Column(types.String(100))
    name = schema.Column(types.String(255))

    updateDate = schema.Column(types.DateTime)
