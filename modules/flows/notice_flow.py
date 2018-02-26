# coding: utf-8

from flask_security import current_user

from .ss_flow import SavedSendFlow
from .operations import Create, Edit, Delete, Send, Read
from .states import InitialState, Sented


class NoticeFlow(SavedSendFlow):
    """通知流程"""

    def add_transition(self):
        # 执行完成操作，需要事先处于新建状态

        if self.support_create:
            self.machine.add_transition(Create, source='', dest='created',
                                        after='send_change')
        # 新建和编辑都可以提交
        self.machine.add_transition(trigger=Send, source='',
                                    dest='sent', after='send_change')
        self.machine.add_transition(trigger=Send, source='created',
                                    dest='sent', after='send_change')

        self.machine.add_transition(Edit, 'created', 'created',
                                    after='update_status')

        # 查看后标记短消息为已读
        self.machine.add_transition(trigger=Read, source='sent',
                                    dest='sent',
                                    after='read_change')

        self.machine.add_transition(Delete, 'created', 'created')
        self.machine.add_transition(Delete, 'sent', 'sent')

    def get_sender(self):
        if self.model.sendName == current_user.realName:
            return True
        else:
            return False

    def is_allowed_triggers(self, triggers):
        if 'send' in triggers:
            triggers.remove('send')
        if not self.get_sender():
            if Delete in triggers:
                triggers.remove(Delete)
        return triggers

    def send_change(self, **kwargs):
        self.model.status = self.status_map[self.state]
        self.model.sendName = current_user.realName

    def read_change(self, **kwargs):
        if not self.model.recieveName:
            self.model.recieveName = current_user.realName
        else:
            recieveName = self.model.recieveName
            if current_user.realName not in recieveName:
                self.model.recieveName = '{},{}'.format(recieveName.encode('UTF-8'),
                                                        current_user.realName.encode('UTF-8')).decode('UTF-8')
