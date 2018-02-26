# coding: utf-8

from __future__ import unicode_literals

from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, Reviewed, ApprovedFailure,
                     SecApproving, SecApproved, SecApprovalFailure,
                     Borrowed, Returned)
from .two_approval_flow import TwoApprovalFlow


class BorrowRequestFlow(TwoApprovalFlow):
    """借入申请流程"""

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'reviewed', 'approving', 'approved-failure', 'sec-approving',
        'sec-approved', 'sec-approval-failure', 'borrowed', 'returned'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'reviewed': Reviewed,
        'approving': APPROVING,
        'approved-failure': ApprovedFailure,
        'sec-approving': SecApproving,
        'sec-approved': SecApproved,
        'sec-approval-failure': SecApprovalFailure,
        'borrowed': Borrowed,
        'returned': Returned
    }

    def add_transition(self):

        # 备注: 创建的入库单状态为已入库会将借入申请单置为已借入状态
        #       创建的出库单状态为已出库会将借入申请单置为已归还状态

        # 提交复核操作，可以执行复核通过操作,如果申请为重要类型，则到待审批状态
        # 如果为非重要则到二级审批通过状态
        self.machine.add_transition(ReviewApprove, 'reviewing', 'approving',
                                    conditions='is_important',
                                    after='update_allowed_change')
        # 当申请类型为一般时复核后为复核通过
        self.machine.add_transition(ReviewApprove, 'reviewing', 'reviewed',
                                    conditions='not_important',
                                    after='update_related_change')
        # 当申请类型为一般时复核通过可以入库
        self.machine.add_transition(CreateIn, 'reviewed', 'reviewed',
                                    after='update_allowed_change')

        # 二级审批通过的数据可以进行入库
        self.machine.add_transition(CreateIn, 'sec-approved', 'sec-approved',
                                    after='update_related_change')
        # 二级审批通过的数据可以上传合同文件
        self.machine.add_transition(UploadContractFile, 'sec-approved',
                                    'sec-approved',
                                    after='update_related_change')

        # 已借入状态也可以新建入库单
        self.machine.add_transition(CreateIn, ['borrowed', 'returned'], '=',
                                    after='update_related_change')

        super(BorrowRequestFlow, self).add_transition()

    def is_important(self, **kwargs):
        if self.model.lendCategory == '重要航材':
            return True
        return False

    def not_important(self, **kwargs):
        if self.model.lendCategory == '一般航材':
            return True
        return False

    def is_allowed_triggers(self, triggers=''):
        triggers = super(
            BorrowRequestFlow, self).is_allowed_triggers(triggers)
        return self.can_in_store('borrow_id', triggers)
