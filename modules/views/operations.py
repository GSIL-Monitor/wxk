# coding: utf-8

from __future__ import unicode_literals

from jinja2 import Markup
from flask import request
from flask_admin.model.template import TemplateLinkRowAction

from ..flows.operations import *
from ..flows import OneApprovalFlow, BasicFlow, TwoApprovalFlow
from ..perms import ActionNeedPermission
from util.compare_function import reversed_cmp
from modules.models.mixin import FlowMixin


class EditRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(EditRowAction, self).__init__('custom_op.approve_edit_row', '编辑')


class ViewRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ViewRowAction, self).__init__('custom_op.view_row', '查看')


class DeleteRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(DeleteRowAction, self).__init__('custom_op.delete_row', '删除')


class EditRowModalAction(TemplateLinkRowAction):
    def __init__(self):
        super(EditRowModalAction, self).__init__('custom_op.edit_modal_row', '编辑')


class ViewRowModalAction(TemplateLinkRowAction):
    def __init__(self):
        super(ViewRowModalAction, self).__init__('custom_op.view_modal_row', '查看')


class DeleteRowModalAction(TemplateLinkRowAction):
    def __init__(self):
        super(DeleteRowModalAction, self).__init__('custom_op.delete_modal_row', '删除')


class FinishRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(FinishRowAction, self).__init__('custom_op.finish_row', '完成')


class SendRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(SendRowAction, self).__init__('custom_op.send_row', '发送')


class SubmitReviewRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(SubmitReviewRowAction, self).__init__(
            'custom_op.submit_review_group', '提交复核')


class ReviewApproveRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ReviewApproveRowAction, self).__init__(
            'custom_op.review_approve_row', '复核通过')


class ReviewAgainRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ReviewAgainRowAction, self).__init__(
            'custom_op.review_again_group', '再次复核')


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


class SecondApprovedRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(SecondApprovedRowAction, self).__init__(
            'custom_op.sec_approved_row', '二级审批通过')


class SecondApprovedGroupAction(TemplateLinkRowAction):
    def __init__(self):
        super(SecondApprovedGroupAction, self).__init__(
            'custom_op.sec_approve_group', '二级审批')


class PutInStoreRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(PutInStoreRowAction, self).__init__(
            'custom_op.put_in_store', '准备入库')


class SecondApproveRefuseRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(SecondApproveRefuseRowAction, self).__init__(
            'custom_op.sec_approve_refuse_row', '二级审批拒绝')


class CreateEORowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateEORowAction, self).__init__(
            'custom_op.create_eo_row', '新建工程指令')


class SentRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(SentRowAction, self).__init__(
            'custom_op.sent_group', '下发')


class ReceiveRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ReceiveRowAction, self).__init__(
            'custom_op.receive_row', '接收')


class CreateSTRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateSTRowAction, self).__init__(
            'custom_op.create_st_row', '制定排故方案')


class CreateERRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateERRowAction, self).__init__(
            'custom_op.create_er_row', '新建排故检修记录')


class CreateRWRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateRWRowAction, self).__init__(
            'custom_op.create_rw_row', '新建例行工作')


class CreateRFRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateRFRowAction, self).__init__(
            'custom_op.create_rf_row', '新建保留故障')


class ReceiveAgainRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ReceiveAgainRowAction, self).__init__(
            'custom_op.reserve_again_row', '继续保留')


class CreateMRRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateMRRowAction, self).__init__(
            'custom_op.create_mr_row', '新建维护保养记录')


class UploadContractFileRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(UploadContractFileRowAction, self).__init__(
            'custom_op.upload_contract_file_row', '上传合同文件')


class UploadMeetingFileRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(UploadMeetingFileRowAction, self).__init__(
            'custom_op.upload_meeting_file_row', '上传会议纪要')


class ApproveGroupAction(TemplateLinkRowAction):
    def __init__(self):
        super(ApproveGroupAction, self).__init__('custom_op.approve_group', '审批')


class ReviewGroupAction(TemplateLinkRowAction):
    def __init__(self):
        super(ReviewGroupAction, self).__init__('custom_op.review_group', '复核')


class CreateInRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateInRowAction, self).__init__(
            'custom_op.create_in_row', '准备入库')


class CreateOutRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateOutRowAction, self).__init__(
            'custom_op.create_out_row', '准备出库')


class CreateBRRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateBRRowAction, self).__init__(
            'custom_op.create_br_row', '借入归还')


class CreateLRRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateLRRowAction, self).__init__(
            'custom_op.create_lr_row', '借出归还')


class CreateASRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateASRowAction, self).__init__(
            'custom_op.create_as_row', '准备装机')


class CreateRpRtRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateRpRtRowAction, self).__init__(
            'custom_op.create_rp_rt_row', '新建送修归还单')


class CreateScrapRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateScrapRowAction, self).__init__(
            'custom_op.create_scrap_row', '报废')


class CheckCompleteRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CheckCompleteRowAction, self).__init__(
            'custom_op.check_complete_row', '检查完成')


class CreateBorrowApplRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreateBorrowApplRowAction, self).__init__(
            'custom_op.borrow_application_row', '借入')


class CreatePurchaseApplRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(CreatePurchaseApplRowAction, self).__init__(
            'custom_op.purchase_application_row', '采购')


class OutStorePartRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(OutStorePartRowAction, self).__init__(
            'custom_op.out_store_part_group', '部分出库')


class OutStoreFinishRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(OutStoreFinishRowAction, self).__init__(
            'custom_op.out_store_finish_row', '出库完成')


class InStorePartRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(InStorePartRowAction, self).__init__(
            'custom_op.in_store_part_group', '部分入库')


class InStoreFinishRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(InStoreFinishRowAction, self).__init__(
            'custom_op.in_store_finish_row', '入库完成')


class ExportPDFRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(ExportPDFRowAction, self).__init__(
            'custom_op.export_pdf_row', '入库完成')


class RecordViewRowAction(TemplateLinkRowAction):
    def __init__(self):
        super(RecordViewRowAction, self).__init__('custom_op.record_row', '履历')



# 主键就是个名称，用于优化多个可聚合操作的查询
approve_group = ('approve', ApproveGroupAction())
sec_approved_group = ('sec_approve', SecondApprovedGroupAction())
review_group = ('review', ReviewGroupAction())
support_group = {
    # 主键是操作，值是tuple，所属的组名，对应html内容
    Approved: approve_group,
    ApproveRefuse: approve_group,
    ApproveAgain: approve_group,
    ReviewApprove: review_group,
    ReviewRefuse: review_group,
    SecondApproved: sec_approved_group,
    SecondApproveRefuse: sec_approved_group,
}

_buttons_map = {
    Edit: EditRowAction(),
    SubmitReview: SubmitReviewRowAction(),
    Cancel: CancelRowAction(),
    Finish: FinishRowAction(),
    ReviewApprove: ReviewApproveRowAction(),
    ReviewRefuse: ReviewRefuseRowAction(),
    SubmitApprove: SubmitApproveRowAction(),
    Approved: ApprovedRowAction(),
    ApproveRefuse: ApproveRefuseRowAction(),
    ReviewAgain: ReviewAgainRowAction(),
    ApproveAgain: ApproveAgainRowAction(),
    SecondApproved: SecondApprovedRowAction(),
    SecondApproveRefuse: SecondApproveRefuseRowAction(),
    Delete: DeleteRowAction(),
    Send: SendRowAction(),
    CreateEO: CreateEORowAction(),
    Sent: SentRowAction(),
    Receive: ReceiveRowAction(),
    CreateST: CreateSTRowAction(),
    createER: CreateERRowAction(),
    CreateRW: CreateRWRowAction(),
    createRF: CreateRFRowAction(),
    ReserveAgain: ReceiveAgainRowAction(),
    PutInStore: PutInStoreRowAction(),
    CreateMR: CreateMRRowAction(),
    UploadContractFile: UploadContractFileRowAction(),
    UploadMeetingFile: UploadMeetingFileRowAction(),
    CreateIn: CreateInRowAction(),
    CreateOut: CreateOutRowAction(),
    CreateBR: CreateBRRowAction(),
    CreateLR: CreateLRRowAction(),
    CreateAS: CreateASRowAction(),
    CreateRpRt: CreateRpRtRowAction(),
    CheckComplete: CheckCompleteRowAction(),
    PurchaseAppl: CreatePurchaseApplRowAction(),
    BorrowAppl: CreateBorrowApplRowAction(),
    CreateScrap: CreateScrapRowAction(),
    OutStorePart: OutStorePartRowAction(),
    OutStoreFinish: OutStoreFinishRowAction(),
    InStorePart: InStorePartRowAction(),
    InStoreFinish: InStoreFinishRowAction(),
    ExportPDF: ExportPDFRowAction(),
    AirmaterialRecord: RecordViewRowAction()
}


def custom_operation_formatter(view, ctx, model, name, buttons_map=_buttons_map):
    """遵循flask-admin的接口要求，实现特定字段的格式化。

    该实现可用于通用的基于审核操作的显示，其会根据当前模型实例所处的
    状态来决定显示什么样的内容。

    如果视图需要实现自己的按钮，请使用下面的名称约定属性格式来定义自己的template子类:

    `[action_name]_btn`其中[action_name]为流程的动作名称。

    上述属性可以直接为TemplateLinkRowAction的实例，也可是一个接受`self`和`model`参数的
    callable实例
    """
    flow = getattr(view, 'support_flow', None)
    if flow is None:
        raise ValueError('not support flow view')
    flow = apply(flow, [model])

    # 1. 先获取当前状态下允许执行的所有操作
    allowed_ops = flow.get_allowed_operations()

    allowed_ops = sorted(allowed_ops, reversed_cmp)

    # 2. 根据当前用户的具体权限，从1中剔除不允许的内容
    # 为了优化循环，可在循环的同时处理

    # 3. 将2处理后的结果正确格式化到操作显示栏中
    html = [
        '<div class="clearfix">'
        '<div class="btn-group btn-group-xs btn-group-solid">']
    for op in allowed_ops:
        perm = ActionNeedPermission(view.action_name, op)
        if perm.can():
            # 如果视图有对应操作的设置，就使用视图的，否则使用内置的
            # 下面的格式采用约定
            view_btn_name = '_'.join([op, 'btn'])
            btn_template = None
            if hasattr(view, view_btn_name):
                btn_template = getattr(view, view_btn_name)
                if callable(btn_template):
                    btn_template = btn_template(model)
            elif op in buttons_map:
                btn_template = buttons_map[op]
            if btn_template is None:
                continue
            html.append(btn_template.render_ctx(
                ctx, view.get_pk_value(model), model))

    row_id = view.get_pk_value(model)
    # 由于查看通常不在流程中处理，因此需要单独检查
    perm = ActionNeedPermission(view.action_name, View)
    if perm.can():
        btn_template = ViewRowAction()
        if hasattr(view, 'view_btn'):
            btn_template = getattr(view, 'view_btn')
            if callable(btn_template):
                btn_template = btn_template(model)
        html.append(btn_template.render_ctx(ctx, row_id, model))

    # 删除已经加入流程，不再单独处理

    html.append('</div></div>')
    return Markup(''.join(html))


def group_operation_formatter(view, ctx, model, name, buttons_map=_buttons_map):
    # 与`custom_operation`几乎一致，只是对一些细粒度的操作聚合为
    # 单个操作，且简单的重定向到对应实例的详情页

    flow = getattr(view, 'support_flow', None)
    if flow is None:
        raise ValueError('not support flow view')
    flow = apply(flow, [model])

    allowed_ops = flow.get_allowed_operations()
    allowed_ops = sorted(allowed_ops, reversed_cmp)

    row_id = view.get_pk_value(model)
    exists = dict()
    html = [
        '<div class="clearfix">'
        '<div class="btn-group btn-group-xs btn-group-solid">']

    # TODO: 该实现没有使用视图支持的button设置
    if allowed_ops:
        for op in allowed_ops:
            perm = ActionNeedPermission(view.action_name, op)
            if perm.can() and op in _buttons_map:

                if op in support_group:
                    group, template = support_group[op]
                    # 已经用过了
                    if group in exists:
                        continue

                    exists[group] = True

                    html.append(template.render_ctx(
                        ctx, view.get_pk_value(model), model))
                    continue
                if op == Cancel:
                    if hasattr(model, 'is_cancel') and not model.is_cancel():
                        break
                    # 其他非聚合操作的，仍需继续处理
                html.append(buttons_map[op].render_ctx(
                    ctx, view.get_pk_value(model), model))

    # 由于查看通常不在流程中处理，因此需要单独检查
    perm = ActionNeedPermission(view.action_name, View)
    if perm.can():
        html.append(ViewRowAction().render_ctx(ctx, row_id, model))

    # 删除改为流程控制
    # # 删除最后处理
    # perm = ActionNeedPermission(view.action_name, Delete)
    # if perm.can() and state:
    #     html.append(DeleteRowAction().render_ctx(ctx, row_id, model))

    html.append('</div></div>')
    return Markup(''.join(html))


def operation_formatter_without_flow(view, ctx, model, name, operations,
                                     buttons_map=_buttons_map,):
    html = [
    '<div class="clearfix">'
    '<div class="btn-group btn-group-xs btn-group-solid">']

    row_id = view.get_pk_value(model)
    if not isinstance(operations, list):
        operations = [operations]
    for op in operations:
        perm = ActionNeedPermission(view.endpoint, op)
        if perm.can() and op in _buttons_map:

            template = None

            template = buttons_map[op]
            if template is None:
                continue
            html.append(template.render_ctx(ctx, row_id, model))
    html.append('</div></div>')
    return Markup(''.join(html))


def normal_operation_formatter(view, ctx, model, name, operations=None):
    # 通用的操作格式化实现，通常不包含流程的操作可以使用该格式化

    # 一般的模型，通常仅支持3个操作的显示，从左到右，至多为：查看，编辑和删除
    html = [
        '<div class="clearfix">'
        '<div class="btn-group btn-group-xs btn-group-solid">']

    row_id = view.get_pk_value(model)

    # 先检查查看
    perm = ActionNeedPermission(view.action_name, View)
    if perm.can():
        html.append(ViewRowAction().render_ctx(ctx, row_id, model))

    # 再看编辑
    perm = ActionNeedPermission(view.action_name, Edit)
    if perm.can():
        html.append(EditRowAction().render_ctx(ctx, row_id, model))

    # 删除最后处理
    perm = ActionNeedPermission(view.action_name, Delete)
    if perm.can():
        html.append(DeleteRowAction().render_ctx(ctx, row_id, model))

    html.append('</div></div>')
    return Markup(''.join(html))


def scrap_operation_formatter(view, ctx, model, name):
    # 通用的操作格式化实现，通常不包含流程的操作可以使用该格式化

    # 一般的模型，通常仅支持3个操作的显示，从左到右，至多为：查看，编辑和删除
    html = [
        '<div class="clearfix">'
        '<div class="btn-group btn-group-xs btn-group-solid">']

    row_id = view.get_pk_value(model)
    html.append(CreateScrapRowAction().render_ctx(ctx, row_id, model))
    html.append('</div></div>')
    return Markup(''.join(html))


def normal_modal_operation_formatter(view, ctx, model, name):
    # 通用的操作格式化实现，通常不包含流程的操作可以使用该格式化， 且需要弹出模态对话框的场景

    # 一般的模型，通常仅支持3个操作的显示，从左到右，至多为：查看，编辑和删除
    html = [
        '<div class="clearfix">'
        '<div class="btn-group btn-group-xs btn-group-solid">']

    row_id = view.get_pk_value(model)
    # 先检查查看
    perm = ActionNeedPermission(view._action_name, View)
    if perm.can():
        html.append(ViewRowModalAction().render_ctx(ctx, row_id, model))

    # 再看编辑
    perm = ActionNeedPermission(view._action_name, Edit)
    if perm.can():
        html.append(EditRowModalAction().render_ctx(ctx, row_id, model))

    # 删除最后处理
    perm = ActionNeedPermission(view._action_name, Delete)
    if perm.can():
        html.append(DeleteRowModalAction().render_ctx(ctx, row_id, model))

    html.append('</div></div>')
    return Markup(''.join(html))
