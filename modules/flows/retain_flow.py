# coding: utf-8

from __future__ import unicode_literals

from .one_approval_flow import OneApprovalFlow
from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, ApprovedFailure, ApprovePass)


class RetainFlow(OneApprovalFlow):
    """保留工作流程"""

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'approving', 'approved-failure', 'approved'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'approving': APPROVING,
        'approved-failure': ApprovedFailure,
        'approved': ApprovePass,
    }

    def __init__(self, name, model=None, support_create=True, create_action=None):
        if not create_action:
            raise Exception('must give the create_action')
        self.create_action = create_action
        super(RetainFlow, self).__init__(name, model, support_create)

    def add_transition(self):

        # 处于待审批的状态可以被通过
        self.machine.add_transition(Approved, 'approving', 'approved',
                                    after='update_related_change')

        # 处于保留未到期可以继续保留
        self.machine.add_transition(ReserveAgain, 'approved', 'created',
                                    after='cancel_allowed_change')

        # 处于保留未到期可以新建记录
        self.machine.add_transition(self.create_action, 'approved', 'approved',
                                    after='update_related_change')
        super(RetainFlow, self).add_transition()
