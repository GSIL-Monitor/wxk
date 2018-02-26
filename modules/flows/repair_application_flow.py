# coding: utf-8

from __future__ import unicode_literals

from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, ApprovedFailure,
                     ApprovePass, Repairing, Repaired)
from .one_approval_flow import OneApprovalFlow


class RepairApplicationFlow(OneApprovalFlow):
    """送修申请流程"""

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'approving', 'approved-failure', 'approved', 'repairing',
        'repaired'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'approving': APPROVING,
        'approved-failure': ApprovedFailure,
        'approved': ApprovePass,
        'repairing': Repairing,
        'repaired': Repaired,
    }

    def add_transition(self):
        # 审批通过的数据可以进行送修通过
        self.machine.add_transition(CreateOut,
                                    ['approved', 'repairing', 'repaired'],
                                    '=',
                                    after='update_related_change')
        # 审批通过的数据可以上传合同文件
        self.machine.add_transition(UploadContractFile, 'approved', 'approved',
                                    after='update_related_change')
        # 已送修状态可以新建送修归还单
        self.machine.add_transition(CreateRpRt, 'repairing', 'repairing',
                                    after='update_related_change')

        super(RepairApplicationFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):
        triggers = super(
            RepairApplicationFlow, self).is_allowed_triggers(triggers)

        return self.can_out_store('repair_application_id', triggers)
