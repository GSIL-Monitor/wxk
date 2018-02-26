# coding: utf-8

from __future__ import unicode_literals

from flask_security import current_user
from sqlalchemy_continuum import version_class

from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, ApprovedFailure,
                     SecApproved, SecApproving, SecApprovalFailure,
                     Loaned, Returned, Reviewed)
from .two_approval_flow import TwoApprovalFlow


class LoanApplicationFlow(TwoApprovalFlow):
    """借出申请流程"""

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'reviewed', 'approving', 'approved-failure', 'sec-approving',
        'sec-approved', 'sec-approval-failure', 'loaned',
        'returned'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'approving': APPROVING,
        'reviewed': Reviewed,
        'approved-failure': ApprovedFailure,
        'sec-approving': SecApproving,
        'sec-approved': SecApproved,
        'sec-approval-failure': SecApprovalFailure,
        'loaned': Loaned,
        'returned': Returned,
    }

    def add_transition(self):
        # 提交复核操作，可以执行复核通过操作,如果申请为重要类型，则到待审批状态
        # 如果为非重要则到二级审批通过状态
        self.machine.add_transition(ReviewApprove, 'reviewing', 'approving',
                                    conditions='is_important',
                                    after='update_allowed_change')
        # 当申请类型为一般时复核后为复核通过
        self.machine.add_transition(ReviewApprove, 'reviewing', 'reviewed',
                                    conditions='not_important',
                                    after='update_related_change')
        # 当申请类型为一般时复核通过可以准备出库
        self.machine.add_transition(CreateOut, 'reviewed', 'reviewed',
                                    after='update_allowed_change')

        # 二级审批通过的数据可以进行准备出库
        self.machine.add_transition(CreateOut, 'sec-approved', 'sec-approved',
                                    after='update_related_change')
        # 二级审批通过的数据可以上传合同文件
        self.machine.add_transition(UploadContractFile, 'sec-approved',
                                    'sec-approved',
                                    after='update_related_change')
        # 已借出状态可以新建借出归还单
        self.machine.add_transition(CreateLR, 'loaned', 'loaned',
                                    after='update_related_change')
        # 已借出状态下也可以新建出库单
        self.machine.add_transition(CreateOut, 'loaned', 'loaned',
                                    after='update_related_change')

        super(LoanApplicationFlow, self).add_transition()

    def is_important(self, **kwargs):
        if self.model.loanCategory == '重要':
            return True
        return False

    def not_important(self, **kwargs):
        if self.model.loanCategory == '一般':
            return True
        return False

    def is_allowed_triggers(self, triggers=''):
        triggers = super(
            LoanApplicationFlow, self).is_allowed_triggers(triggers)

        return self.can_out_store('loanApplication_id', triggers)
