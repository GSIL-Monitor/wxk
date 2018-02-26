# coding: utf-8

from __future__ import unicode_literals

from functools import partial
from datetime import datetime

from .two_approval_flow import TwoApprovalFlow
from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, Reviewed, ApprovedFailure,
                     SecApproving, SecApproved, SecApprovalFailure,
                     INStoring, InStored)
from ..models.base import db


class PurchaseRequestFlow(TwoApprovalFlow):
    """采购申请流程"""

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'approving', 'approved-failure', 'sec-approving',
        'sec-approved', 'sec-approval-failure', 'put-in-store'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'approving': APPROVING,
        'approved-failure': ApprovedFailure,
        'sec-approving': SecApproving,
        'sec-approved': SecApproved,
        'sec-approval-failure': SecApprovalFailure,
        'instored': InStored,
    }

    def add_transition(self):

        # 二级审批通过的数据可以进行入库
        self.machine.add_transition(CreateIn, ['sec-approved', 'instored'], '=',
                                    after='update_related_change')
        # 二级审批通过的数据可以上传合同文件
        self.machine.add_transition(UploadContractFile, 'sec-approved',
                                    'sec-approved',
                                    after='update_related_change')
        # 二级审批通过的数据可以上传会议纪要
        self.machine.add_transition(UploadMeetingFile, 'sec-approved',
                                    'sec-approved',
                                    after='update_related_change')

        super(PurchaseRequestFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):
        triggers = super(
            PurchaseRequestFlow, self).is_allowed_triggers(triggers)

        return self.can_in_store('purchaseApplication_id', triggers)
