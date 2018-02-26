# coding: utf-8

from __future__ import unicode_literals

from transitions import Machine
from flask_security import current_user
from datetime import datetime

from .operations import Edit, Delete, Finish, Create, CreateIn, CreateOut, ExportPDF
from .states import (
    InitialState, Edited, Finished, AllInStored, AllOutStored)
from modules.models.user import User
from modules.models.airmaterial import Storage, PutOutStoreModel


class Flow(object):

    states = []

    status_map = {}

    def __init__(self, name, model=None, support_create=True):
        """
        ..warning:: 由于python2.x的缘故，对中文支持不是很好

        :param name: 用于描述工作流的名称，不要使用中文名
        :param model: 模型实例，需要至少拥有status属性
        """

        # 用于描述这是一个什么工作流，如“适航文件审批流”等
        self.name = name

        self.model = model

        self.support_create = support_create

        self.machine = Machine(model=self, states=self.states,
                               initial=self._get_initial_state())

        self.add_transition()

    def update_status(self, **kwargs):

        """状态发生变迁后，通常需要更新模型的对应状态。"""
        if self.state == '' and self.support_create:
            self.model.status = InitialState
            return

        self.model.status = self.status_map[self.state]

        if hasattr(self.model, 'auditStatus'):
            self.model.auditStatus = self.model.status

    def update_audit_field(self, **kwargs):

        model = self.model

        # 如果是流程审批说明，则添加相应的内容

        if hasattr(model, 'relatedUser'):
            model.relatedUser = kwargs.get('username')
        if hasattr(model, 'timestamp'):
            model.timestamp = datetime.now()
        if hasattr(model, 'suggestion'):
            val = kwargs.get('suggestion')
            if isinstance(val, list):
                val = val[0]
            model.suggestion = val

    def _get_initial_state(self):
        # 如果支持将新建也加入流程
        if not self.model.status and self.support_create:
            return ''

        for k, v in self.status_map.items():
            if v == self.model.status:
                return k

        raise ValueError('暂不支持模型所处的%s状态' % (self.model.status, ))

    def get_allowed_operations(self, state=''):
        """返回当前状态允许执行的下一步操作列表。

        :param state: 如果state没有提供，则使用流的当前状态
        """

        if not state:
            state = self.state

        triggers = self.machine.get_triggers(state)

        # 返回的操作列表通常都作为状态变迁的触发源，而非目标
        triggers = [
            trigger for trigger in triggers if not trigger.startswith('to')]

        return self.is_allowed_triggers(triggers)

    def add_transition(self):
        # 从Flow类继承的子类首先应该实现该函数
        raise NotImplementedError()

    def is_allowed_triggers(self, triggers):
        return triggers

    def first_create(self, **kwargs):

        self.update_audit_field(**kwargs)
        self.update_status()

    def update_related_change(self, **kwargs):
        self.update_status()
        self.update_audit_field(**kwargs)

    def update_allowed_change(self, **kwargs):
        self.update_related_change(**kwargs)
        if hasattr(self.model, 'allowedUser'):
            val = kwargs.get('related_user')
            if isinstance(val, list):
                val = val[0]

            user = User.query.filter_by(username=val).first()
            self.model.allowedUser = user

    def cancel_allowed_change(self, **kwargs):
        self.update_status()
        self.update_audit_field(**kwargs)
        if hasattr(self.model, 'allowedUser'):
            self.model.allowedUser = None

    @classmethod
    def get_flow_columns(self, status=InitialState):
        return []

    def can_in_store(self, foreign_key, triggers):
        # 判断动作是否应包含入库
        tt = getattr(Storage, foreign_key)
        query = Storage.query.filter(Storage.auditStatus == AllInStored).join(
            self.model.__class__, tt == self.model.id).all()
        if query and CreateIn in triggers:
            triggers.remove(CreateIn)
        return triggers

    def can_out_store(self, foreign_key, triggers):
        # 判断动作是否应包含出库
        tt = getattr(PutOutStoreModel, foreign_key)
        query = PutOutStoreModel.query.filter(
            PutOutStoreModel.auditStatus == AllOutStored).join(
                self.model.__class__, tt == self.model.id).all()
        if query and CreateOut in triggers:
            triggers.remove(CreateOut)
        return triggers


class BasicFlow(Flow):

    states = ['created', 'edited', 'finished']

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'finished': Finished,
    }

    def add_transition(self):
        # 执行完成操作，需要事先处于新建状态

        if self.support_create:
            self.machine.add_transition(Create, source='', dest='created',
                                        after='first_create')

        # 新建和编辑都可以提交
        self.machine.add_transition(trigger=Finish, source='created',
                                    dest='finished',
                                    after='update_allowed_change')
        self.machine.add_transition(trigger=Finish, source='edited',
                                    dest='finished',
                                    after='update_allowed_change')

        # 处于新建和编辑状态时，可以删除
        self.machine.add_transition(Delete, 'created', 'created')
        self.machine.add_transition(Delete, 'edited', 'edited')

        # 新建状态和编辑状态的都可以编辑
        self.machine.add_transition(Edit, 'created', 'edited',
                                    after='update_related_change')
        self.machine.add_transition(Edit, 'edited', 'edited',
                                    after='update_related_change')
        self.machine.add_transition(ExportPDF, '*', '=')

    @classmethod
    def get_flow_columns(self, status=InitialState):
        return ['createUserName', 'createTime',
                'amendUserName', 'amendTime',
                'commitUserName', 'commitTime']

