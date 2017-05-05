# coding: utf-8

from __future__ import unicode_literals

"""该模块定义了界面中允许执行的操作名。并对这些操作名进行规范。"""


__all__ = [
    'Edit', 'SubmitReview', 'ReviewApprove',
    'ReviewRefuse', 'SubmitApprove', 'Approved',
    'ApproveRefuse', 'Cancel', 'ApproveAgain',
    'ReviewAgain', 'Create', 'View', 'Delete',
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

# 基本的操作
Create = 'create'
View = 'view'
Delete = 'delete'
