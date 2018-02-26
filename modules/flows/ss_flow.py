# coding: utf-8

from __future__ import unicode_literals

from datetime import datetime
from flask_security import current_user

from .basic_flow import Flow
from .operations import Create, Edit, Delete, Send
from .states import InitialState, Sented


class SavedSendFlow(Flow):

    states = ['created', 'sent']

    status_map = {
        'created': InitialState,
        'sent': Sented,
    }

    def add_transition(self):
        self.machine.add_transition(trigger=Create, source='',
                                    dest='created', after='update_status')

        # 新建和编辑都可以提交
        self.machine.add_transition(trigger=Send, source='',
                                    dest='sent', after='send_change')
        self.machine.add_transition(trigger=Send, source='created',
                                    dest='sent', after='send_change')

        # 处于新建和编辑状态时，可以删除
        self.machine.add_transition(Delete, 'created', 'created')

        # 新建状态和编辑状态的都可以编辑
        self.machine.add_transition(Edit, 'created', 'created',
                                    after='update_status')

    def is_allowed_triggers(self, triggers):
        if 'send' in triggers:
            triggers.remove('send')
        return triggers

    def send_change(self, **kwargs):
        self.model.status = self.status_map[self.state]
        self.model.sendUser = current_user.realName
        self.model.sendTime = datetime.now()
