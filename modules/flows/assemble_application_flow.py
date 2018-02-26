# coding: utf-8

from __future__ import unicode_literals

from .basic_flow import BasicFlow
from .operations import *
from .states import (
    InitialState, Edited, Finished, Assembled, AllOutStored, PartOutStored)
from modules.models.airmaterial import Assemble, AssembleApplication


class AssembleApplicationFlow(BasicFlow):
    """装机申请流程"""
    states = ['created', 'edited', 'finished', 'all-out-stored',
              'part-out-stored', 'assembled']

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'finished': Finished,
        'all-out-stored': AllOutStored,
        'part-out-stored': PartOutStored,
        'assembled': Assembled,

    }

    def add_transition(self):

        # 已提交状态创建出库单
        self.machine.add_transition(trigger=CreateOut,
                                    source=['finished', 'part-out-stored'],
                                    dest='=',
                                    after='update_related_change')

        # 完全出库状态创建装机单
        self.machine.add_transition(trigger=CreateAS, source='all-out-stored',
                                    dest='all-out-stored',
                                    after='update_related_change')

        super(AssembleApplicationFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):
        triggers = super(
            AssembleApplicationFlow, self).is_allowed_triggers(triggers)

        triggers = self.can_out_store('assemble_application_id', triggers)
        query = AssembleApplication.query.filter(
            AssembleApplication.id == self.model.id).join(
                Assemble,
                AssembleApplication.id == Assemble.assembleapplication_id)
        if query.count() and \
                CreateAS in triggers:
            triggers.remove(CreateAS)
        return triggers
