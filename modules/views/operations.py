# coding: utf-8

from __future__ import unicode_literals

from jinja2 import Markup
from flask_admin.model.template import TemplateLinkRowAction

from modules.flows import BasicApprovalFlow
from modules.flows.operations import *
from modules.perms import ActionNeedPermission


class EditRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(EditRowAction, self).__init__('custom_op.edit_row', '编辑')


class ViewRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ViewRowAction, self).__init__('custom_op.view_row', '查看')


class DeleteRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(DeleteRowAction, self).__init__('custom_op.delete_row', '删除')


class SubmitReviewRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(SubmitReviewRowAction, self).__init__(
            'custom_op.submit_review_row', '提交复核')


class ReviewApproveRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ReviewApproveRowAction, self).__init__(
            'custom_op.review_approve_row', '复核通过')


class ReviewAgainRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ReviewAgainRowAction, self).__init__(
            'custom_op.review_again_row', '再次复核')


class SubmitApproveRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(SubmitApproveRowAction, self).__init__(
            'custom_op.submit_approve_row', '提交审批')


class ApprovedRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ApprovedRowAction, self).__init__(
            'custom_op.approved_row', '审批通过')


class ApproveAgainRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ApproveAgainRowAction, self).__init__(
            'custom_op.approve_again_row', '再次审批')


class CancelRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CancelRowAction, self).__init__(
            'custom_op.cancel_row', '撤销')


class ReviewRefuseRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ReviewRefuseRowAction, self).__init__(
            'custom_op.review_refuse_row', '复核拒绝')


class ApproveRefuseRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ApproveRefuseRowAction, self).__init__(
            'custom_op.approve_refuse_row', '审批拒绝')


_buttons_map = {
    Edit: EditRowAction(),
    SubmitReview: SubmitReviewRowAction(),
    Cancel: CancelRowAction(),
    ReviewApprove: ReviewApproveRowAction(),
    ReviewRefuse: ReviewRefuseRowAction(),
    SubmitApprove: SubmitApproveRowAction(),
    Approved: ApprovedRowAction(),
    ApproveRefuse: ApproveRefuseRowAction(),
    ReviewAgain: ReviewAgainRowAction(),
    ApproveAgain: ApproveAgainRowAction(),
}


def basic_operation(view, ctx, model, name):
    """遵循flask-admin的接口要求，实现特定字段的格式化。

    该实现可用于通用的基于审核操作的显示，其会根据当前模型实例所处的
    状态来决定显示什么样的内容。
    """
    flow = BasicApprovalFlow('General working flow', model)

    # 1. 先获取当前状态下允许执行的所有操作
    allowed_ops = flow.get_allowed_operations()

    # 2. 根据当前用户的具体权限，从1中剔除不允许的内容
    # 为了优化循环，可在循环的同时处理

    # 3. 将2处理后的结果正确格式化到操作显示栏中
    html = ['<div class="clearfix"><div class="btn-group btn-group-xs btn-group-solid">']
    for op in allowed_ops:
        perm = ActionNeedPermission(model.__class__.__name__.lower(), op)
        if perm.can() and op in _buttons_map:
            html.append(_buttons_map[op].render_ctx(
                ctx, view.get_pk_value(model), model))

    # 由于查看通常不在流程中处理，因此需要单独检查
    row_id = view.get_pk_value(model)
    perm = ActionNeedPermission(model.__class__.__name__.lower(), View)
    if perm.can():
        html.append(ViewRowAction().render_ctx(ctx, row_id, model))

    # 删除最后处理
    perm = ActionNeedPermission(model.__class__.__name__.lower(), Delete)
    if perm.can():
        html.append(DeleteRowAction().render_ctx(ctx, row_id, model))

    html.append('</div></div>')
    return Markup(''.join(html))
