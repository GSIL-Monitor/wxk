# coding: utf-8

from __future__ import unicode_literals

import json

from .one_approval_flow import OneApprovalFlow
from .operations import *
from .states import InitialState, REVIEWING, Edited, ReviewedFailure, Reviewed
from util.broker import file_move
from util.str_to_dict import updateFileStr
from util.exception import BackendServiceError


class ApproveCanEdit(OneApprovalFlow):

    states = [
        'created', 'edited', 'reviewing', 'reviewed-failure',
        'reviewed'
    ]

    status_map = {
        'created': InitialState,
        'edited': Edited,
        'reviewing': REVIEWING,
        'reviewed-failure': ReviewedFailure,
        'reviewed': Reviewed,
    }

    def add_transition(self):
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
        self.machine.add_transition(Cancel, 'reviewing', 'edited',
                                    after='update_status')

        # 提交复核操作，可以执行复核通过操作
        self.machine.add_transition(ReviewApprove, 'reviewing', 'reviewed',
                                    after='reviewed_change')

        # 提交复核操作，可以执行拒绝复核操作
        self.machine.add_transition(ReviewRefuse, 'reviewing',
                                    'reviewed-failure',
                                    after='update_related_change')

        # 复核失败的状态下，编辑可以变成新建状态
        self.machine.add_transition(Edit, 'reviewed-failure', 'edited',
                                    after='update_related_change')

        # 被拒绝的复核可以再次交复核
        self.machine.add_transition(ReviewAgain, 'reviewed-failure',
                                    'reviewing', after='update_allowed_change')
        # 复核后还可以有编辑权限
        self.machine.add_transition(Edit, 'reviewed', 'edited',
                                    after='update_related_change')

    def is_allowed_triggers(self, triggers=''):

        if not self.is_allowed_with_user():
            if Edit in triggers:
                triggers.remove(Edit)

        return super(ApproveCanEdit, self).is_allowed_triggers(triggers)

    def reviewed_change(self, **kwargs):
        super(ApproveCanEdit, self).update_allowed_change(**kwargs)
        model = self.model
        file_type = model.fileResourceType
        file_str = model.fileResourceUrl
        if file_str:
            file_list = json.loads(file_str)
            res = []
            for file_val in file_list:
                try:
                    tmp = updateFileStr(file_val, file_type)
                    res.append(tmp.get('update'))
                    file_move(source=tmp.get('source'), target=tmp.get('target'))
                except:
                    raise BackendServiceError('RabbitMq has something wrong')
            model.fileResourceUrl = json.dumps(res)

    @classmethod
    def get_flow_columns(self, status=Reviewed):
        columns = [
            'createUserName', 'createTime',
            'amendUserName', 'amendTime',
            'commitUserName', 'commitTime']

        if status == Reviewed:
            columns = columns + [
                'reviewUserName', 'reviewTime',
                'reviewSuggestions', 'reviewingUser'
            ]

        return columns
