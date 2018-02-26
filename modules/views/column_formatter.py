# coding: utf-8

from __future__ import unicode_literals

from jinja2 import Markup
from flask import url_for
from flask_security import current_user
from wtforms.widgets import HTMLString, html_params
import json
from sqlalchemy_continuum import version_class

from ..flows.states import *


column_map = {
    'relatedUser': ['createUserName', 'reviewUserName', 'approveUserName',
                    'amendUserName', 'commitUserName', 'secApproveUserName',
                    'sentPerson', 'receivePerson'],
    'timestamp': ['createTime', 'reviewTime', 'approveTime', 'amendTime',
                  'commitTime', 'secApproveTime',
                  'sentTime', 'receiveTime'],
    'suggestion': ['reviewSuggestions', 'approveSuggestions',
                   'secApproveSuggestions'],
    'allowedUser': ['reviewingUser', 'approvingUser', 'secApprovingUser',
                    'receivingUser'],

}


def cancel_formatter(view, context, model, name):
    url = view.get_url('.index_view')
    html = ['<div class="btn-group btn-group-xs btn-group-solid">'
            '<a href="{}" '.format(url)]
    html.append('class="btn btn-group-item btn-success" '
                'role="button">'
                '<i class="fa fa-level-up">返回</i></a>'
                '</div>')
    return Markup(''.join(html))


def formula_formatter(model):
    items = []
    for p in model.sub_formula:
        items.append({p.pesticide.name: p.weight})
    return items, len(items)


def accessory_formatter(field_name):

    def formatter(view, context, model, name):
        show = '<a class="btn default" target="_blank" %(href)s>%(name)s</a>'
        acce_str = getattr(model, field_name)
        filelist = ''
        if not acce_str:
            return HTMLString('')
        for item in json.loads(acce_str):
            href = {}
            href.setdefault('href', url_for('.download_view', key=item.get('key')))
            each = HTMLString(show % {
                'href': html_params(**href),
                'name': item.get('name'),
            })
            filelist += each
        return Markup(HTMLString(filelist))

    return formatter


def relate_doc_formatter(field_name):

    def formatter(view, context, model, name):
        show = '<a class="btn default" target="_blank" %(href)s>%(name)s</a>'
        acce_str = getattr(model, field_name)
        if acce_str is None:
            acce_str = 'null'
        acce_json = json.loads(acce_str)
        filelist = ''
        if not acce_json:
            return HTMLString('')
        try:
            for item in acce_json:
                href = {}
                href.setdefault('href', url_for(
                    '.download_view', key=item.get('key')))
                each = HTMLString(show % {
                    'href': html_params(**href),
                    'name': item.get('name'),
                })
                filelist += each
            return Markup(HTMLString(filelist))
        except:
            raise Exception('Please contact the service maintainer.')

    return formatter


def content_formatter(view, context, model, name):
    html = []
    contents = model.content.split('\r\n')
    for con in contents:
        html.append('<div>'+con+'</div>')
    return Markup(''.join(html))


def get_key_from_value(search_dict, data):
    for key, value in search_dict.iteritems():
        if isinstance(value, list) and data in value:
            return key
        if data == value:
            return key
    return None


def get_last_create_index(model, status, name):

    if not isinstance(status, list):
        status = status.split(",")

    version = version_class(model.__class__)
    query = version.query.filter(
        version.id == model.id, version.auditStatus == InitialState)
    index = query[-1].transaction_id if query else None
    if not index:
        return ''
    inst = version.query.filter(
        version.id == model.id,
        version.auditStatus.in_(status),
        version.transaction_id >= index).all()
    val = get_key_from_value(column_map, name)
    value = getattr(inst[-1], val) if inst else ''
    return value


def creat_information_formater(view, ctx, model, name):
    # 创建人

    value = get_last_create_index(model, InitialState, name)
    return value


def amend_information_formater(view, ctx, model, name):
    # 修改
    status = [Edited]
    return get_last_create_index(model, status, name)


def commit_information_formater(view, ctx, model, name):
    # 提交人

    value = get_last_create_index(model, [REVIEWING, Finished], name)
    return value


def reviewing_user_name_formater(view, ctx, model, name):
    # 允许的复核人
    value = get_last_create_index(model, REVIEWING, name)
    return value


def review_information_formater(view, ctx, model, name):
    # 复核人

    status = [ReviewedFailure, APPROVING, Reviewed]
    if model.auditStatus == REVIEWING:
        return ''
    value = get_last_create_index(model, status, name)
    return value


def approving_user_name_formater(view, ctx, model, name):
    # 允许的审批人
    status = [APPROVING]
    value = get_last_create_index(model, status, name)
    return value


def approved_information_formater(view, ctx, model, name):
    # 审批人
    status = [ApprovePass, ApprovedFailure, SecApproving, RetainPeriod]
    if model.auditStatus in [REVIEWING, APPROVING]:
        return ''
    value = get_last_create_index(model, status, name)
    return value


def sec_approving_user_name_formater(view, ctx, model, name):
    # 允许的二级审批人
    status = [SecApproving]
    value = get_last_create_index(model, status, name)
    return value


def sec_approved_information_formater(view, ctx, model, name):
    # 二级审批人
    status = [SecApproved, SecApprovalFailure]
    value = get_last_create_index(model, status, name)
    return value


def sent_information_formater(view, ctx, model, name):
    # 待接收
    status = [Receiving]
    value = get_last_create_index(model, status, name)
    return value


def receive_information_formater(view, ctx, model, name):
    # 已接收
    status = [Received]
    value = get_last_create_index(model, status, name)
    return value


def receiving_user_information_formater(view, ctx, model, name):
    # 允许的接收人
    status = [Receiving]
    value = get_last_create_index(model, status, name)
    return value

def auditStatus_formater(view, ctx, model, name):

    if model.auditStatus == Edited:
        return InitialState
    return model.auditStatus


def read_formater(view, ctx, model, name):
    read = []
    if model.recieveName:
        read = model.recieveName.split(',')

    if model.sendName == current_user.realName:
        html = []
        if read and len(read):
            for r in read:
                html.append('<span class="badge badge-info badge-roundless">' + r + '</span> ')
        return Markup(''.join(html))
    else:
        if read and len(read):
            if current_user.realName in read:
                return Markup('<span class="badge badge-info badge-roundless">已读过</span>')
        url = url_for('.read_view', id=model.id)
        return Markup('<a class="btn btn-xs blue" href="' + url + '">阅读</a>')


def checkbox_formater(check_storage=False):

    able = '<input type="checkbox" name="rowid" value="{}" />'
    disable = ('<input type="checkbox" name="rowid"'
               'disabled="disabled" value="{}" />')

    def checkbox(view, ctx, model, name):
        value = view.get_pk_value(model)
        html = able.format(value)
        if check_storage and hasattr(model, 'quantity') \
                and hasattr(model, 'freezingQuantity'):
            if model.quantity <= model.freezingQuantity:
                html = disable.format(value)

        return Markup(html)

    return checkbox


def plane_type_formatter(view, context, model, name):
    if model.planeType == 'y5b':
        return '运5B(D)'

    return getattr(model, name, '')
