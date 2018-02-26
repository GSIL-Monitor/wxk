# encoding: utf-8

from __future__ import unicode_literals

from sqlalchemy import schema, types
from sqlalchemy.orm import relationship
from flask_security import RoleMixin

from .base import Model


class BasicAction(Model):
    "徐州实现中各模型支持的操作全集"

    __tablename__ = 'basic_action'
    id = schema.Column(types.Integer, primary_key=True)
    model = schema.Column(types.String(255))
    create = schema.Column(types.Boolean)
    edit = schema.Column(types.Boolean)
    view = schema.Column(types.Boolean)
    delete = schema.Column(types.Boolean)

    # 所属的角色
    role_id = schema.Column(types.Integer, schema.ForeignKey('role.id'))

    # 扩展操作
    submit_review = schema.Column(types.Boolean)
    review_approve = schema.Column(types.Boolean)
    review_refuse = schema.Column(types.Boolean)
    review_again = schema.Column(types.Boolean)
    approved = schema.Column(types.Boolean)
    approve_refuse = schema.Column(types.Boolean)
    cancel = schema.Column(types.Boolean)
    finish = schema.Column(types.Boolean)
    edit_bound_status = schema.Column(types.Boolean)
    remove_bound_status = schema.Column(types.Boolean)
    create_eo = schema.Column(types.Boolean)
    create_st = schema.Column(types.Boolean)
    create_er = schema.Column(types.Boolean)
    create_rw = schema.Column(types.Boolean)
    create_rf = schema.Column(types.Boolean)
    reserve_again = schema.Column(types.Boolean)
    create_mr = schema.Column(types.Boolean)

    # 用于对角色权限的分配
    review = schema.Column(types.Boolean)
    approve = schema.Column(types.Boolean)
    submit = schema.Column(types.Boolean)
    sent = schema.Column(types.Boolean)
    receive = schema.Column(types.Boolean)

    # 下面的是参考实现上新增的操作支持
    second_approved = schema.Column(types.Boolean)
    second_approve_refuse = schema.Column(types.Boolean)

    # 发送操作
    send = schema.Column(types.Boolean)
    # 入库功能
    put_in_store = schema.Column(types.Boolean)
    stored = schema.Column(types.Boolean)
    # 上传合同文件
    upload_contract_file = schema.Column(types.Boolean)
    # 上传合同文件
    upload_meeting_file = schema.Column(types.Boolean)
    # 出库完成动作

    # 新建入库单
    create_in = schema.Column(types.Boolean)
    # 新建出库单
    create_out = schema.Column(types.Boolean)
    # 新建借入归还单
    create_br = schema.Column(types.Boolean)
    # 新建借出归还单
    create_lr = schema.Column(types.Boolean)
    # 新建装机单
    create_as = schema.Column(types.Boolean)

    # 借入归还
    borrowing_in_return = schema.Column(types.Boolean)
    # 新建送修归还
    create_rp_rt = schema.Column(types.Boolean)
    # 出库

    # 检查完成
    check_complete = schema.Column(types.Boolean)
    # 新建借入申请
    borrow_application = schema.Column(types.Boolean)
    # 新建采购申请
    purchase_application = schema.Column(types.Boolean)
    # 新建报废单
    create_scrap = schema.Column(types.Boolean)
    # 部分出库
    out_store_part = schema.Column(types.Boolean)
    # 出库完成
    out_store_finish = schema.Column(types.Boolean)
    # 部分入库
    in_store_part = schema.Column(types.Boolean)
    # 入库完成
    in_store_finish = schema.Column(types.Boolean)
    # 打印
    export_pdf = schema.Column(types.Boolean)
    # 查看航材履历
    airmaterial_record = schema.Column(types.Boolean)

    def __dir__(self):
        return ['create', 'edit', 'view', 'delete', 'create_eo',
                'submit_review', 'review_approve', 'review_refuse',
                'review_again', 'approved', 'approve_refuse', 'cancel',
                'finish', 'edit_bound_status', 'review', 'approve', 'submit',
                'second_approved', 'second_approve_refuse', 'sent', 'receive',
                'send', 'create_st', 'create_er', 'create_rw',
                'create_rf', 'reserve_again', 'create_mr', 'put_in_store',
                'upload_contract_file', 'upload_meeting_file',
                'borrowing_in_return', 'create_in', 'remove_bound_status',
                'create_out', 'create_br', 'create_lr', 'create_as',
                'create_rp_rt', 'check_complete', 'borrow_application',
                'purchase_application', 'create_scrap', 'out_store_part',
                'out_store_finish', 'in_store_part', 'in_store_finish',
                'export_pdf', 'airmaterial_record']


class Role(Model, RoleMixin):
    "角色模型"

    __tablename__ = 'role'

    id = schema.Column(types.Integer, primary_key=True)
    name = schema.Column(types.String(255))
    description = schema.Column(types.String(255))

    actions = relationship('BasicAction', backref="role")

    def __str__(self):
        return self.name
