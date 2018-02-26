# coding: utf-8

from __future__ import unicode_literals

import pytest
from transitions import MachineError

from modules.flows import BasicFlow, OneApprovalFlow
import modules.flows.operations as op


class FakeModel(object):

    def __init__(self):
        self._status = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


def test_basic_approval():

    model = FakeModel()
    model.status = '新建'
    flow = OneApprovalFlow('Basic working flow', model)

    assert flow.state == 'created'

    flow.submit_review()
    assert flow.state == 'reviewing'
    assert model.status == '待复核'

    flow.review_approve()
    assert flow.state == 'approving'
    assert model.status == '待审批'

    with pytest.raises(MachineError):
        flow.review_refuse()
        assert model.status == '已复核'


def test_middle_state_of_basic_approval():
    # 检测处于中间状态时的状态变迁
    model = FakeModel()
    model.status = '已审批'
    flow = OneApprovalFlow('Basic working flow', model)

    with pytest.raises(MachineError):
        # 处于最终态了
        flow.approve_refuse()

    # 改变为其他中间态
    model.status = '待复核'
    flow = OneApprovalFlow('Basic working flow', model)
    flow.review_approve()

    assert flow.state == 'approving'
    assert model.status == '待审批'

    flow.approved()
    assert flow.state == 'approved'
    assert model.status == '已审批'

    model.status = '待审批'
    flow = OneApprovalFlow('Basic working flow', model)
    flow.approve_refuse()
    assert flow.state == 'approved-failure'


def test_allowed_operations():
    # 用于检查当前状态允许执行的操作
    model = FakeModel()
    model.status = '新建'

    flow = OneApprovalFlow('Basic working flow', model)
    allowed_ops = flow.get_allowed_operations()

    assert len(allowed_ops) == 3
    assert op.SubmitReview in allowed_ops
    assert op.Edit in allowed_ops

    flow.submit_review()
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 3
    assert op.Cancel in allowed_ops
    assert op.ReviewApprove in allowed_ops
    assert op.ReviewRefuse in allowed_ops

    flow.review_approve()
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 2
    assert op.Approved in allowed_ops

    # flow.submit_approve()
    # allowed_ops = flow.get_allowed_operations()
    # assert len(allowed_ops) == 3
    # assert op.Approved in allowed_ops
    # assert op.ApproveRefuse in allowed_ops
    # assert op.Cancel in allowed_ops

    flow.approved()
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 0


def test_basic_flow():
    model = FakeModel()
    # 如果一开始不为模型设置状态

    flow = BasicFlow('support create flow', model, support_create=True)
    allowed_ops = flow.get_allowed_operations()

    assert len(allowed_ops) == 1
    assert op.Create in allowed_ops

    flow.create()
    assert flow.state == 'created'
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 3
    assert op.Edit in allowed_ops
    assert op.Delete in allowed_ops
    assert op.Finish in allowed_ops

    flow.edit()
    assert flow.state == 'edited'
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 3
    assert op.Edit in allowed_ops
    assert op.Delete in allowed_ops
    assert op.Finish in allowed_ops

    # 还可以继续编辑
    flow.edit()
    assert flow.state == 'edited'
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 3
    assert op.Edit in allowed_ops
    assert op.Delete in allowed_ops
    assert op.Finish in allowed_ops


def test_basic_flow2():
    model = FakeModel()
    # 如果一开始不为模型设置状态

    model.actionRecords = []
    flow = BasicFlow('support create flow', model, support_create=True)

    flow.create(username='username')
    assert len(model.actionRecords) == 1
    assert model.actionRecords[0].createUserName == 'username'

    flow.edit(username='username2')
    assert len(model.actionRecords) == 1
    assert model.actionRecords[0].createUserName == 'username'
    assert model.actionRecords[0].amendUserName == 'username2'

    flow.edit(username='username3')
    assert len(model.actionRecords) == 1
    assert model.actionRecords[0].createUserName == 'username'
    assert model.actionRecords[0].amendUserName == 'username3'
