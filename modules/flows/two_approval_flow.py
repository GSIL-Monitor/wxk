# coding: utf-8

from __future__ import unicode_literals

from flask_security import current_user
from sqlalchemy_continuum import version_class

from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, ApprovedFailure,
                     SecApproved, SecApproving, SecApprovalFailure)
from .one_approval_flow import OneApprovalFlow


class TwoApprovalFlow(OneApprovalFlow):

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'approving', 'approved-failure', 'sec-approving',
        'sec-approved', 'sec-approval-failure',
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'approving': APPROVING,
        'approved-failure': ApprovedFailure,
        'sec-approving': SecApproving,
        'sec-approved': SecApproved,
        'sec-approval-failure': SecApprovalFailure
    }

    def add_transition(self):

        # 处于待审批的状态可以被通过, 处于二级审批状态
        self.machine.add_transition(Approved, 'approving', 'sec-approving',
                                    after='update_allowed_change')

        # 处于一次审批的状态可以被二级审批通过
        self.machine.add_transition(SecondApproved, 'sec-approving',
                                    'sec-approved',
                                    after='update_related_change')

        # 处于二级审批状态可以被二级审批拒绝
        self.machine.add_transition(SecondApproveRefuse, 'sec-approving',
                                    'sec-approval-failure',
                                    after='update_related_change')

        # 二级审批失败的状态下，编辑可以变成新建状态
        self.machine.add_transition(Edit, 'sec-approval-failure',
                                    'edited',
                                    after='cancel_allowed_change')

        # 被拒绝的二次审批可以再次提交复核
        self.machine.add_transition(ReviewAgain, 'sec-approval-failure',
                                    'reviewing',
                                    after='update_allowed_change')

        super(TwoApprovalFlow, self).add_transition()

    def is_allowed_triggers(self, triggers=''):

        if self.model.status in [InitialState, Edited, ReviewedFailure,
                                 ApprovedFailure, SecApprovalFailure]:
            if not self.is_allowed_with_user():
                return []

        if self.model.status in [REVIEWING, APPROVING, SecApproving]:

            if not self.is_allowed_with_user(related_user=False):
                triggers = [Cancel]

            if self.model.status in [APPROVING, SecApproving] or\
                    not self.is_allowed_with_user(
                        related_user=True, current=False):

                if 'cancel' in triggers:
                    triggers.remove('cancel')

        return triggers

    def is_allowed_with_user(self, related_user=True, current=True):
        # Todo: 如果有对特殊角色的权限设置, 可以在此进行判断
        # related_user: 使用相关用户还是允许用户判断
        # current: 判断related_user与当前用户比较还是与制单人进行比较

        version = version_class(self.model.__class__)
        query = version.query.filter(
            version.id == self.model.id, version.auditStatus == InitialState)
        index = query[-1].transaction_id if query else None
        if not index:
            return False
        inst = query[-1]

        if related_user:
            if inst.relatedUser != current_user:
                return False
            return True
        user_id = current_user.id if current else inst.relatedUser_id

        status = [ReviewedFailure, ApprovedFailure, SecApprovalFailure]
        query = version.query.filter(
            version.id == self.model.id, version.auditStatus.in_(status))

        tmp_index = query[-1].transaction_id if query.count() else 0
        index = index if index > tmp_index else tmp_index

        query = version.query.filter(
            version.id == self.model.id,
            version.allowedUser_id == user_id,
            version.auditStatus == self.model.status,
            version.transaction_id >= index).all()
        if not query:
            return False

        return True

    @classmethod
    def get_flow_columns(self, status=SecApproved):

        columns = [
            'createUserName', 'createTime',
            'amendUserName', 'amendTime',
            'commitUserName', 'commitTime']

        review_colums = columns + [
            'reviewUserName', 'reviewTime',
            'reviewSuggestions', 'reviewingUser'
        ]

        approve_colums = review_colums + [
            'approveUserName', 'approveTime',
            'approveSuggestions', 'approvingUser'
        ]

        sec_approve_columns = approve_colums + [
            'secApproveUserName', 'secApproveTime',
            'secApproveSuggestions', 'secApprovingUser'
        ]

        if status == APPROVING:
            columns = review_colums
        if status == SecApproving:
            columns = approve_colums
        if status == SecApproved:
            columns = sec_approve_columns
        return columns
