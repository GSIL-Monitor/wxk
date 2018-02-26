# coding: utf-8

from __future__ import unicode_literals

from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, Reviewed, ApprovedFailure,
                     SecApproving, SecApproved, SecApprovalFailure,
                     Borrowed, Returned, Scrapped)
from .two_approval_flow import TwoApprovalFlow


class ScrapFlow(TwoApprovalFlow):
    """报废流程"""

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
        'scrapped': Scrapped
    }

    def add_transition(self):
        # 备注: 当报废新建的出库单状态为已出库时,则在出库流程中将该报废单置成已出库状态

        # 提交复核操作，可以执行复核通过操作,如果申请为重要类型，则到待审批状态
        # 如果为非重要则到二级审批通过状态
        self.machine.add_transition(ReviewApprove, 'reviewing', 'approving',
                                    conditions='is_important',
                                    after='update_allowed_change')
        # 当申请类型为一般时复核后为复核通过
        self.machine.add_transition(ReviewApprove, 'reviewing', 'reviewed',
                                    conditions='not_important',
                                    after='update_related_change')

        # 当状态为一般时复核通过或三级审批通过可以出库
        self.machine.add_transition(CreateOut,
                                    ['reviewed', 'sec-approved', 'scrapped'],
                                    '=',
                                    after='update_allowed_change')

        super(ScrapFlow, self).add_transition()

    def is_important(self, **kwargs):
        if self.model.scrapCategory == '重要':
            return True
        return False

    def not_important(self, **kwargs):
        if self.model.scrapCategory == '一般':
            return True
        return False

    def is_allowed_triggers(self, triggers=''):
        triggers = super(
            ScrapFlow, self).is_allowed_triggers(triggers)

        return self.can_out_store('scrap_id', triggers)
