# coding: utf-8

from __future__ import unicode_literals

from functools import partial
from datetime import datetime

from .one_approval_flow import OneApprovalFlow
from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, ApprovedFailure, ApprovePass,
                     Receiving, Received)

from ..models.base import db


class ADFlow(OneApprovalFlow):
    """适航文件流程"""

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'approving', 'approved-failure', 'approved', 'sented', 'received'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'approving': APPROVING,
        'approved-failure': ApprovedFailure,
        'approved': ApprovePass,
        'sented': Receiving,
        'received': Received,
    }

    def __init__(self, name, model=None, next_model=None):

        super(ADFlow, self).__init__(name, model=model)
        self._next_model = next_model

    def add_transition(self):

        # 已审批的数据可以进行下发
        self.machine.add_transition(Sent, 'approved', 'sented',
                                    after='update_allowed_change')
        # 已下发的数据可以进行接收
        self.machine.add_transition(Receive, 'sented', 'received',
                                    after='update_related_change')
        # 已接收的数据可以进行创建工程指令
        self.machine.add_transition(CreateEO, 'received', 'received',
                                    after='update_related_change')

        super(ADFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):

        triggers = super(ADFlow, self).is_allowed_triggers(triggers)

        if self.model.status in [Receiving]:
            if not self.is_allowed_with_user(related_user=False):
                return []

        return triggers

    @classmethod
    def get_flow_columns(self, status=Received):

        columns = OneApprovalFlow.get_flow_columns()
        readytoReceive_colums = columns + [
            'sentPerson', 'sentTime', 'receivingUser'
        ]

        received_colums = readytoReceive_colums + ['receivePerson',
                                                   'receiveTime']
        if status == Receiving:
            return readytoReceive_colums
        if status == Received:
            return received_colums

        return OneApprovalFlow.get_flow_columns(status)
