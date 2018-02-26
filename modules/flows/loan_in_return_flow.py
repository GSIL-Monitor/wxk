# coding: utf-8

from __future__ import unicode_literals

from .operations import *
from .states import (InitialState, REVIEWING, Edited,
                     ReviewedFailure, Reviewed,
                     Returned, Repaired)
from .one_approval_flow import OneApprovalFlow
from modules.models.airmaterial import RepairReturnOrder


class LoanInReturnFlow(OneApprovalFlow):
    """借出归还流程"""

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'reviewed', 'Loaned', 'returned', 'repaired'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'reviewed': Reviewed,
        'returned': Returned,
        'repaired': Repaired,
    }

    def add_transition(self):
        # # 创建的出库单状态为已出库会将借入归还单置为已归还状态

        # 当申请类型为一般时复核后为复核通过
        self.machine.add_transition(ReviewApprove, 'reviewing', 'reviewed',
                                    after='update_related_change')
        # 复核通过可以新建出库单
        self.machine.add_transition(CreateIn, 'reviewed', 'reviewed',
                                    after='update_related_change')

        self.machine.add_transition(CreateIn, ['returned', 'repaired'],
                                    '=', after='update_related_change')

        super(LoanInReturnFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):
        triggers = super(
            LoanInReturnFlow, self).is_allowed_triggers(triggers)

        if isinstance(self.model, RepairReturnOrder):
            return self.can_in_store('repairReturn_id', triggers)

        return self.can_in_store('loanReturn_id', triggers)
