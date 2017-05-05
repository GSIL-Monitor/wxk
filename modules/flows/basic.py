# coding: utf-8

from __future__ import unicode_literals

from transitions import Machine

from .operations import *


_basic_status_map = {
    'created': '新建',
    'reviewing': '待复核',
    'reviewed': '已复核',
    'reviewed-failure': '复核未通过',
    'approving': '待审批',
    'approved-failure': '审批未通过',
    'approved': '已审批',
}


class BasicApprovalFlow(object):
    """基本的带审批流程的工作流定义。"""

    # 通常涉及的状态
    # 由于使用python2的第三方unix库对中文支持不是很好，这里使用英文来
    # 做状态映射处理
    states = [
        'created', 'reviewing', 'reviewed', 'reviewed-failure',
        'approving', 'approved-failure', 'approved',
    ]

    def __init__(self, name, model=None):
        """
        ..warning:: 由于python2.x的缘故，对中文支持不是很好

        :param name: 用于描述工作流的名称，不要使用中文名
        :param model: 模型实例，需要至少拥有status属性
        """

        # 用于描述这是一个什么工作流，如“适航文件审批流”等
        self.name = name

        self.model = model

        self.machine = Machine(model=self, states=BasicApprovalFlow.states,
                               initial=self._get_initial_state())

        # 执行提交复核操作，需要事先处于新建状态
        self.machine.add_transition(trigger=SubmitReview, source='created',
                                    dest='reviewing', after='update_status')

        # 处于新建状态时，可以删除
        self.machine.add_transition(Delete, 'created', 'created')

        # 执行复核通过操作
        self.machine.add_transition(ReviewApprove, 'reviewing', 'reviewed',
                                    after='update_status')

        # 执行拒绝复核操作
        self.machine.add_transition(ReviewRefuse, 'reviewing',
                                    'reviewed-failure', after='update_status')

        # 被拒绝的复核可以再次交复核
        self.machine.add_transition(ReviewAgain, 'reviewed-failure',
                                    'reviewing', after='update_status')

        # 处于复核过的状态可以提交审批
        self.machine.add_transition(SubmitApprove, 'reviewed', 'approving',
                                    after='update_status')

        # 处于待审批的状态可以被通过也可以被拒绝
        self.machine.add_transition(Approved, 'approving', 'approved',
                                    after='update_status')
        self.machine.add_transition(ApproveRefuse, 'approving',
                                    'approved-failure', after='update_status')

        # 被拒绝的审批可以再次提交审批
        self.machine.add_transition(ApproveAgain, 'approved-failure',
                                    'approving', after='update_status')

        # 下述几种状态可以执行“撤销”
        # 1. 处于待审批的状态，撤销后变为已复核状态
        self.machine.add_transition(Cancel, 'approving', 'reviewed',
                                    after='update_status')
        # 2. 处于待复核的状态，撤销后变为新建状态
        self.machine.add_transition(Cancel, 'reviewing', 'created',
                                    after='update_status')

        # 下面几种状态允许编辑
        # 1. 新建的通常可以编辑
        self.machine.add_transition(Edit, 'created', 'created')

        # 2. 处于待复核的状态可以编辑
        self.machine.add_transition(Edit, 'reviewing', 'reviewing')

    def update_status(self):
        """状态发生变迁后，通常需要更新模型的对应状态。"""

        self.model.status = _basic_status_map[self.state]

    def _get_initial_state(self):
        for k, v in _basic_status_map.items():
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
        return [
            trigger for trigger in triggers if not trigger.startswith('to')]
