# encoding: utf-8

from __future__ import unicode_literals
from copy import deepcopy

from sqlalchemy import or_
from flask_security import current_user

from ..perms import ActionNeedPermission
from modules.flows.states import (
    REVIEWING, APPROVING, Receiving,
    SecApproving, Reviewed, SecApproved, ApprovePass)
from modules.flows.operations import (
    ReviewApprove, Approved, Receive,
    SecondApproved, CreateIn, CreateOut)


# 待办项里需要处理的状态，及对应状态应该执行的操作
# 前者为操作，后者为对应状态（用于数据查询）
perm_status = {
    ReviewApprove: REVIEWING,
    Approved: APPROVING,
    Receive: Receiving,
    SecondApproved: SecApproving,
}


action_map = {
    'review_approve': 'review',
    'review_refuse': 'review',
    'approved': 'approve',
    'approve_refuse': 'approve',
    'second_approve_refuse': 'second_approved'
}


def pending_list(models, allowed_status=perm_status, max_count=None):

    def query_status(model, status, limit=None, allowed_filter=True):

        critiers = or_(
            *[(m.model_class.statusName == st) for st in status])
        query = model.query.filter(critiers)

        if allowed_filter:
            query = query.filter(model.allowedUser_id == current_user.id)

        if limit:
            return query[0: limit-1]
        return query

    result = []
    for m in models:

        # 一些特殊的模型不是sql格式
        if m[0] in ['aircraft', 'flightlog', 'mxp']:
            continue

        # 判断数据是否达到配置的数量
        if len(result) > max_count:
            break

        actions = allowed_status.keys()
        status = []
        for action in actions:

            val = deepcopy(action)
            if val in action_map.keys():
                val = action_map[val]

            if val in m[2] and ActionNeedPermission(m[0], action).can():
                # 如果允许该操作，则设置相应的状态条件
                status.append(allowed_status[action])

        # 如果没有对应的状态，则无需处理对应的数据

        if len(status):
            # TODO: 如果不包含对应的字段？
            # 使用or查询

            # 通过状态条件处理对应的查询
            found = query_status(
                m.model_class, status, max_count - len(result))

            result.extend(map(lambda f: dict(view=m[0], title=m[1], inst=f),
                          found))

        storage = CreateIn in m[2] and ActionNeedPermission(
            m[0], CreateIn).can()
        put_out = CreateOut in m[2] and ActionNeedPermission(
            m[0], CreateOut).can()

        if storage or put_out:
            status = [Reviewed, ApprovePass, SecApproved]
            found = query_status(m.model_class, status,
                                 max_count - len(result), False)
            result.extend(map(lambda f: dict(view=m[0], title=m[1], inst=f),
                              found))

    return result
