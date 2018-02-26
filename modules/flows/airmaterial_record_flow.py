# coding: utf-8

from __future__ import unicode_literals

from .basic_flow import BasicFlow
from .operations import *


class AirmaterialRecordFlow(BasicFlow):
    """航材流程"""

    def add_transition(self):

        # 新建和编辑都可以提交
        self.machine.add_transition(AirmaterialRecord, '*', '=')
        super(AirmaterialRecordFlow, self).add_transition()
