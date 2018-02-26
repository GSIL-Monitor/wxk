# coding: utf-8

from __future__ import unicode_literals

from functools import partial
from datetime import datetime

from .ad_flow import ADFlow
from .operations import *
from .states import InitialState, REVIEWING, APPROVING, Edited, Receiving
from ..models.base import db


class EOFlow(ADFlow):
    """工程指令流程"""

    def add_transition(self):

        # 已接收的数据可以进行创建工程指令
        self.machine.add_transition(CreateMR, 'received', 'received',
                                    after='update_related_change')

        super(EOFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):

        triggers = super(ADFlow, self).is_allowed_triggers(triggers)

        if self.model.status in [Receiving] and \
            not self.is_allowed_with_user(related_user=False):
            return []
        if self.model.maintenanceRecord:
            return []

        return triggers
