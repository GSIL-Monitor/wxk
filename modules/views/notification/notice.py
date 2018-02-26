# coding: utf-8

from __future__ import unicode_literals
from flask import redirect, url_for, request, flash
from flask_admin import expose
from flask_admin.form.fields import Select2Field
from flask_admin.form.widgets import Select2Widget
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_security import current_user
from wtforms.fields import TextAreaField
from sqlalchemy import not_, or_, and_
from functools import partial

from modules.models.notification.notice import Notice
from util.fields.select import (RefreshRoleSelectFiled,
                                UserWithRoleSelectMultiField)
from modules.flows.notice_flow import NoticeFlow
from .base import NotificationManagementViewBase
from modules.views.column_formatter import content_formatter, read_formater
from modules.models.user import User
from modules.roles import SuperAdmin
from modules.views import CustomView
from modules.flows.operations import Edit, Send, Create, Read
from modules.flows.states import InitialState, Sented


class _NoticeView(NotificationManagementViewBase):

    create_template = 'announcement/create.html'
    edit_template = 'announcement/create.html'
    details_template = 'oldDetails.html'

    form_rules = ('role', 'recieveId', 'title', 'content')

    # 通知列表视图应显示的内容

    column_list = [
        'title'
    ]

    confirm_str = '是否确定发送该短消息?'

    column_details_list = ['title', 'message', 'read', 'recieveId']

    support_flow = partial(NoticeFlow, 'notice flow')

    # 对应内容的中文翻译
    column_labels = {
        'title': '标题',
        'content': '内容',
        'message': '内容',
        'read': '阅读',
        'recieveId': '接收人列表',
        'role': '角色'
    }

    form_excluded_columns = ['flag', 'recieveName', 'sendName', 'stateName']

    form_overrides = {
        'role': partial(RefreshRoleSelectFiled),
        'recieveId': partial(UserWithRoleSelectMultiField),
        'content': partial(TextAreaField, render_kw={'rows': 4, 'style': 'resize:none;'}),

    }

    column_formatters = {
        'message': content_formatter,
        'read': read_formater,
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            if 'send' in request.form:
                self._custom_action(model, form.data, Send, False)
            else:
                self._custom_action(model, form.data, Create, False)

        super(CustomView, self).on_model_change(form, model, is_created)

    def _custom_action(self, id_or_model, data, action='', direct_commit=True):
        try:
            if isinstance(id_or_model, (str, unicode)):
                models = self.model.query.filter(
                    self.model.id.in_([id_or_model])).all()
            else:
                models = [id_or_model]
            if not action:
                allowed_form_actions = (Edit, Send)

                for verb in allowed_form_actions:
                    if verb in data:
                        action = verb
                        break
            if not action:
                raise ValueError('没有指定的动作，请联系开发人员')

            for item in models:
                flow = self.support_flow(item)
                apply(getattr(flow, action), (), dict(**data))

            if direct_commit:
                self.session.commit()

        except Exception as ex:
            self.session.rollback()
            flash('无法执行指定的操作。 %s' % (unicode(ex),), category='error')

    @expose('/read/', methods=['GET', 'POST'])
    def read_view(self):
        data = {}
        return_url = url_for('.index_view')
        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)
        model = self.get_one(id)
        if model is None:
            return redirect(return_url)
        apply(getattr(self.support_flow(model), Read), (), dict(**data))
        self.session.commit()
        return redirect(return_url)

    def get_query(self):
        return self.model.query.filter(or_(and_(Notice.recieveId.any(User.username == current_user.username),
                                                Notice.stateName == Sented),
                                           Notice.sendName == current_user.realName))

    @expose('/create/', methods=['GET', 'POST'])
    def create_view(self):
        self._template_args.update({
            'create_or_edit': '创建',
            'confirm_str': self.confirm_str,
        })
        return super(_NoticeView, self).create_view()

    @expose('/approve-edit-view/', methods=['POST', 'GET'])
    def approve_edit_view(self):
        self.approve_edit_template = self.edit_template
        self._template_args.update({
            'create_or_edit': '编辑',
            'confirm_str': self.confirm_str,
        })
        return super(_NoticeView, self).approve_edit_view()


NoticeView = partial(
    _NoticeView, Notice, name='短消息'
)


def retrieve_unread_notifies(app):
    @app.context_processor
    def handle():
        if getattr(current_user, 'username', None):
            name = current_user.username
            real_name = current_user.realName
            if not real_name:
                return dict(notifies=[])
            query = Notice.query.filter(and_(Notice.recieveId.any(User.username == name),
                                             Notice.stateName == Sented))
            notice = query.filter(or_(Notice.recieveName == None,
                                      not_(Notice.recieveName.like('%' + real_name + '%')))).all()
            return dict(notifies=notice)
        else:
            return dict(Notice=[])
