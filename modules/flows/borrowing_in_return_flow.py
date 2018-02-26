# coding: utf-8

from __future__ import unicode_literals

from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, Reviewed, ApprovedFailure,
                     SecApproving, SecApproved, SecApprovalFailure,
                     Borrowed, Returned)
from .one_approval_flow import OneApprovalFlow


class BorrowInReturnFlow(OneApprovalFlow):
    """借入归还流程"""

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'reviewed', 'borrowed', 'returned'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'reviewed': Reviewed,
        'returned': Returned
    }

    def add_transition(self):
        # # 创建的出库单状态为已出库会将借入归还单置为已归还状态

        # 当申请类型为一般时复核后为复核通过
        self.machine.add_transition(ReviewApprove, 'reviewing', 'reviewed',
                                    after='update_related_change')
        # 复核通过可以新建出库单
        self.machine.add_transition(CreateOut, ['reviewed', 'returned'], '=',
                                    after='update_related_change')

        super(BorrowInReturnFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):
        triggers = super(
            BorrowInReturnFlow, self).is_allowed_triggers(triggers)

        return self.can_out_store('borrowingInReturn_id', triggers)
