# coding: utf-8

from __future__ import unicode_literals


__all__ = [
    'Create', 'Edit', 'View', 'Delete',
    'SubmitReview', 'ReviewApprove',
    'ReviewRefuse', 'SubmitApprove', 'Approved',
    'ApproveRefuse', 'Cancel', 'ApproveAgain',
    'ReviewAgain', 'Finish',
    'SecondApproved', 'SecondApproveRefuse', 'EditBoundStatus', 'RemoveBoundStatus',
    'Review', 'Approve', 'Submit', 'CreateEO', 'Sent', 'Receive', 'Send',
    'CreateST', 'createER', 'ReserveAgain', 'CreateRW', 'PutInStore',
    'Stored', 'CreateMR', 'createRF', 'UploadContractFile',
    'UploadMeetingFile', 'BorrowingInReturn', 'PutOutStore', 'CreateIn',
    'CreateOut', 'CreateBR', 'CreateLR', 'CreateAS', 'CreateRpRt',
    'CheckComplete', 'PurchaseAppl', 'BorrowAppl', 'CreateScrap',
    'OutStoreFinish', 'OutStorePart', 'InStoreFinish', 'InStorePart', 'ExportPDF',
    'AirmaterialRecord'
]


# 编辑
Edit = 'edit'
# 提交复核
SubmitReview = 'submit_review'
# 复核通过
ReviewApprove = 'review_approve'
# 复核拒绝
ReviewRefuse = 'review_refuse'
# 再次复核
ReviewAgain = 'review_again'
# 提交审批
SubmitApprove = 'submit_approve'
# 审批通过
Approved = 'approved'
# 审批拒绝
ApproveRefuse = 'approve_refuse'
# 再次审批
ApproveAgain = 'approve_again'
# 撤销
Cancel = 'cancel'
# 完成
Finish = 'finish'
# 编辑绑定状态
EditBoundStatus = 'edit_bound_status'
# 解除绑定状态
RemoveBoundStatus = 'remove_bound_status'
# 提交
Review = 'review'
# 审批
Approve = 'approve'
# 提交
Submit = 'submit'
# 新建工程指令
CreateEO = 'create_eo'
# 下发
Sent = 'sent'
# 接收
Receive = 'receive'
# 制定排故方案
CreateST = 'create_st'
# 新建排故检修记录
createER = 'create_er'
# 继续保留
ReserveAgain = 'reserve_again'
# 新建例行工作记录
CreateRW = 'create_rw'
# 新建维护保养记录
CreateMR = 'create_mr'
# 新建保留故障
createRF = 'create_rf'

# 已读
Read = 'read'

# 基本的操作
Create = 'create'
View = 'view'
Delete = 'delete'

# 二级审批
SecondApproved = 'second_approved'
SecondApproveRefuse = 'second_approve_refuse'


# 入库完成
Stored = 'stored'
# 上传合同文件
UploadContractFile = 'upload_contract_file'
# 长传会议纪要
UploadMeetingFile = 'upload_meeting_file'

# 新建入库单
CreateIn = 'create_in'
# 新建出库单
CreateOut = 'create_out'
# 新建借入归还单
CreateBR = 'create_br'
# 新建借出归还单 LR: loanedReturn
CreateLR = 'create_lr'
# 新建装机单
CreateAS = 'create_as'
# 新建送修归还单 RpRt: rpaireReturn
CreateRpRt = 'create_rp_rt'
# 发送操作
Send = 'send'

# 保留(暂时未用到)
# 入库动作
PutInStore = 'put_in_store'
# 借入归还
BorrowingInReturn = 'borrowing_in_return'
# 出库
PutOutStore = 'put_out_store'

# 检查完成
CheckComplete = 'check_complete'

# 采购申请
PurchaseAppl = 'purchase_application'
# 借入申请
BorrowAppl = 'borrow_application'
# 创建报废单
CreateScrap = 'create_scrap'
# 部分出库
OutStorePart = 'out_store_part'
# 出库完成
OutStoreFinish = 'out_store_finish'
# 部分出库
InStorePart = 'in_store_part'
# 出库完成
InStoreFinish = 'in_store_finish'
# 打印
ExportPDF = 'export_pdf'
# 航材履历
AirmaterialRecord = 'airmaterial_record'

all_actions = [
    Create, Edit, View, Delete,
    SubmitReview, ReviewApprove,
    ReviewRefuse, SubmitApprove, Approved,
    ApproveRefuse, Cancel, ApproveAgain,
    ReviewAgain, Finish,
    SecondApproved, SecondApproveRefuse, EditBoundStatus, RemoveBoundStatus,
    Review, Approve, Submit, CreateEO, Sent, Receive, Send,
    CreateST, createER, ReserveAgain, CreateRW, PutInStore, Stored,
    CreateMR, createRF, UploadContractFile, UploadMeetingFile,
    BorrowingInReturn, PutOutStore, CreateIn, CreateOut, CreateBR,
    CreateLR, CreateAS, CreateRpRt, CheckComplete, PurchaseAppl,
    BorrowAppl, CreateScrap, OutStoreFinish, OutStorePart, InStorePart,
    InStoreFinish, ExportPDF, AirmaterialRecord
]
