# coding: utf-8

from __future__ import unicode_literals

import pytest
from transitions import MachineError

from modules.flows import BasicApprovalFlow
import modules.flows.operations as op


class FakeModel(object):

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


def test_basic_approval():

    model = FakeModel()
    model.status = '新建'
    flow = BasicApprovalFlow('Basic working flow', model)

    assert flow.state == 'created'

    flow.submit_review()
    assert flow.state == 'reviewing'
    assert model.status == '待复核'

    flow.review_approve()
    assert flow.state == 'reviewed'
    assert model.status == '已复核'

    with pytest.raises(MachineError):
        flow.review_refuse()
        assert model.status == '已复核'


def test_middle_state_of_basic_approval():
    # 检测处于中间状态时的状态变迁
    model = FakeModel()
    model.status = '已审批'
    flow = BasicApprovalFlow('Basic working flow', model)

    with pytest.raises(MachineError):
        # 处于最终态了
        flow.approve_refuse()

    # 改变为其他中间态
    model.status = '已复核'
    flow = BasicApprovalFlow('Basic working flow', model)
    flow.submit_approve()

    assert flow.state == 'approving'
    assert model.status == '待审批'

    flow.approved()
    assert flow.state == 'approved'
    assert model.status == '已审批'

    model.status = '待审批'
    flow = BasicApprovalFlow('Basic working flow', model)
    flow.approve_refuse()
    assert flow.state == 'approved-failure'


def test_allowed_operations():
    # 用于检查当前状态允许执行的操作
    model = FakeModel()
    model.status = '新建'

    flow = BasicApprovalFlow('Basic working flow', model)
    allowed_ops = flow.get_allowed_operations()

    assert len(allowed_ops) == 3
    assert op.SubmitReview in allowed_ops
    assert op.Edit in allowed_ops

    flow.submit_review()
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 4
    assert op.Cancel in allowed_ops
    assert op.ReviewApprove in allowed_ops
    assert op.ReviewRefuse in allowed_ops
    assert op.Edit in allowed_ops

    flow.review_approve()
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 1
    assert op.SubmitApprove in allowed_ops

    flow.submit_approve()
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 3
    assert op.Approved in allowed_ops
    assert op.ApproveRefuse in allowed_ops
    assert op.Cancel in allowed_ops

    flow.approved()
    allowed_ops = flow.get_allowed_operations()
    assert len(allowed_ops) == 0
