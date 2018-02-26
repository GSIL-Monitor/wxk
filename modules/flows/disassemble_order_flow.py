# coding: utf-8

from __future__ import unicode_literals

from .basic_flow import BasicFlow
from .operations import *
from .states import (InitialState, Edited, Disassembled, StoresReturned,
                     AllInStored)
from modules.models.airmaterial import Storage, DisassembleOrder


class DisassembleOrderFlow(BasicFlow):
    """拆机流程"""

    states = ['created', 'edited', 'disassembled', 'stores-returned']

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'disassembled': Disassembled,
        'stores-returned': StoresReturned

    }

    def add_transition(self):
        # 新建入库单

        self.machine.add_transition(
            CreateIn,
            ['created', 'edited', 'disassembled', 'stores-returned'],
            '=',
            after='update_related_change')

        super(DisassembleOrderFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):

        triggers = super(
            DisassembleOrderFlow, self).is_allowed_triggers(triggers)

        if isinstance(self.model, DisassembleOrder):
            return self.can_in_store('disassemble_id', triggers)
        return self.can_in_store('returnMaterial_id', triggers)
