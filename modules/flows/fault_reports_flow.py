# coding: utf-8

from __future__ import unicode_literals

from functools import partial
from datetime import datetime

from .one_approval_flow import OneApprovalFlow
from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, ApprovedFailure, ApprovePass, Finished)
from ..models.base import db
from ..models.production.troubleshooting import TroubleShooting
from ..models.production.examine_repair_record import ExamineRepairRecord


class FaultReportsFlow(OneApprovalFlow):
    """故障报告流程"""

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'approving', 'approved-failure', 'approved',
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

    def __init__(self, name, model=None, next_model=None):

        super(FaultReportsFlow, self).__init__(name, model=model)
        self._next_model = next_model

    def add_transition(self):

        # 已接收的数据可以进行创建工程指令
        self.machine.add_transition(CreateST, 'approved', 'approved',
                                    after='update_related_change')

        super(FaultReportsFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):

        triggers = super(FaultReportsFlow, self).is_allowed_triggers(triggers)

        if self.model.troubleShootings:
            query = ExamineRepairRecord.query.filter(
                ExamineRepairRecord.auditStatus == Finished
            ).join(
                TroubleShooting,
                ExamineRepairRecord.troubleShooting_id == TroubleShooting.id
            ).filter(TroubleShooting.faultReports_id == self.model.id)
            if query.count():
                for item in query:
                    if item.Soluted:
                        return []

        return triggers
