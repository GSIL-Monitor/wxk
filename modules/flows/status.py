# coding: utf-8

from __future__ import unicode_literals


"""该模块包含有一般流程中，各模型实例可能处于的状态定义。"""


__all__ = [
    'Created', 'Reviewing', 'Reviewed', 'ReviewedFailure',
    'Approving', 'ApprovedFailure', 'Approved',
]


Created = '新建'
Reviewing = '待复核'
Reviewed = '已复核'
ReviewedFailure = '复核未通过'
Approving = '待审批'
ApprovedFailure = '审批未通过'
Approved = '已审批'
