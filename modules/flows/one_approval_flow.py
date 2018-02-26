# coding: utf-8

from __future__ import unicode_literals

from flask_security import current_user
from sqlalchemy_continuum import version_class

from .basic_flow import Flow
from .operations import *
from .states import (InitialState, REVIEWING, APPROVING, Edited,
                     ReviewedFailure, ApprovedFailure, ApprovePass)


class OneApprovalFlow(Flow):

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'approving', 'approved-failure', 'approved'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'approving': APPROVING,
        'approved-failure': ApprovedFailure,
        'approved': ApprovePass,
    }

    def add_transition(self):

        self.machine.add_transition(ExportPDF, '*', '=')

        if self.support_create:
            self.machine.add_transition(Create, source='',
                                        dest='created',
                                        after='first_create')

        # 新建状态可以编辑
        self.machine.add_transition(Edit, 'created', 'edited',
                                    after='update_related_change')

        # 新建状态可以删除
        self.machine.add_transition(Delete, 'created', 'created')

        # 编辑状态可以删除
        self.machine.add_transition(Delete, 'edited', 'edited')

        # 编辑状态可以编辑
        self.machine.add_transition(Edit, 'edited', 'edited',
                                    after='update_related_change')

        # 提交复核操作，需要事先处于新建状态
        self.machine.add_transition(trigger=SubmitReview, source='created',
                                    dest='reviewing',
                                    after='update_allowed_change')

        # 提交复核操作，需要事先处于新建状态
        self.machine.add_transition(trigger=SubmitReview, source='edited',
                                    dest='reviewing',
                                    after='update_allowed_change')

        # 处于待复核的状态，撤销后变为新建状态
        self.machine.add_transition(Cancel, 'reviewing', 'created',
                                    after='cancel_allowed_change')

        # 提交复核操作，可以执行复核通过操作
        self.machine.add_transition(ReviewApprove, 'reviewing', 'approving',
                                    after='update_allowed_change')

        # 提交复核操作，可以执行拒绝复核操作
        self.machine.add_transition(ReviewRefuse, 'reviewing',
                                    'reviewed-failure',
                                    after='update_related_change')

        # 复核失败的状态下，编辑可以变成新建状态
        self.machine.add_transition(Edit, 'reviewed-failure', 'created',
                                    after='cancel_allowed_change')

        # 被拒绝的复核可以再次交复核
        self.machine.add_transition(ReviewAgain, 'reviewed-failure',
                                    'reviewing', after='update_allowed_change')

        # 处于待审批的状态可以被通过也可以被拒绝
        self.machine.add_transition(Approved, 'approving', 'approved',
                                    after='update_related_change')

        self.machine.add_transition(ApproveRefuse, 'approving',
                                    'approved-failure',
                                    after='update_related_change')

        # 审批失败的状态下，编辑可以变成新建状态
        self.machine.add_transition(Edit, 'approved-failure',
                                    'created',
                                    after='cancel_allowed_change')

        # 被拒绝的审批可以再次提交复核
        self.machine.add_transition(ReviewAgain, 'approved-failure',
                                    'reviewing',
                                    after='update_allowed_change')

    def is_allowed_triggers(self, triggers=''):

        if self.model.status in [InitialState, Edited, ReviewedFailure, ApprovedFailure]:
            if not self.is_allowed_with_user():
                return []

        if self.model.status in [REVIEWING, APPROVING]:
            # 允许的用户和当前的用户比较,如果不是,只剩下撤销权限
            if not self.is_allowed_with_user(related_user=False):
                triggers = [Cancel]

            # 审批状态没有撤销, 创建人不是当前用户没有撤销
            if self.model.status == APPROVING or not self.is_allowed_with_user(
                    related_user=True, current=False):

                if 'cancel' in triggers:
                    triggers.remove('cancel')

        return triggers

    def is_allowed_with_user(self, related_user=True, current=True):
        # Todo: 如果有对特殊角色的权限设置, 可以在此进行判断
        # related_user: 使用相关用户还是允许用户判断
        # current: 判断related_user与当前用户比较还是与制单人进行比较

        version = version_class(self.model.__class__)
        # 这里先查询有没有最新的新建状态的数据，如果没有则证明有误，直接返回false
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

        status = [ReviewedFailure, ApprovedFailure]
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
    def get_flow_columns(self, status=ApprovePass):

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

        if status == APPROVING:
            columns = review_colums
        if status == ApprovePass:
            columns = approve_colums
        return columns
