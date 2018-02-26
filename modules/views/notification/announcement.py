# coding: utf-8

from __future__ import unicode_literals

from functools import partial
from flask import flash, request
from wtforms.fields import TextAreaField
from wtforms.validators import DataRequired
from flask_admin import expose
from flask_security import current_user

from modules.views.custom import CustomView
from modules.models.notification.announcement import Announcement
from modules.flows.ss_flow import SavedSendFlow
from modules.flows.operations import Edit, Send, Create


class _AnnouncementView(CustomView):

    create_template = 'announcement/create.html'
    edit_template = 'announcement/create.html'
    details_template = 'announcement/details.html'

    confirm_str = '是否确定发送该通知公告?'

    support_flow = partial(SavedSendFlow, 'send flow')

    column_list = [
        'title'
    ]

    form_overrides = {
        'content': partial(TextAreaField,
                           render_kw={'rows': 25, 'style': 'resize:none;'}),

    }
    column_labels = {
        'title': '标题',
        'content': '内容',
    }

    form_excluded_columns = ['sendTime', 'sendUser']

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.title.validators = [DataRequired()]
            form.content.validators = [DataRequired()]
        return super(_AnnouncementView, self).validate_form(form)

    @expose('/create/', methods=['GET', 'POST'])
    def create_view(self):
        self._template_args.update({
            'create_or_edit': '创建',
            'confirm_str': self.confirm_str,
        })
        return super(_AnnouncementView, self).create_view()

    @expose('/approve-edit-view/', methods=['POST', 'GET'])
    def approve_edit_view(self):
        self.approve_edit_template = self.edit_template
        self._template_args.update({
            'create_or_edit': '编辑',
            'confirm_str': self.confirm_str,
        })
        return super(_AnnouncementView, self).approve_edit_view()

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
                self._before_custom_action(item, action, **data)
                flow = self.support_flow(item)
                apply(getattr(flow, action), (), dict(
                    username=current_user, **data))

            if direct_commit:
                self.session.commit()

        except Exception as ex:
            self.session.rollback()
            flash('无法执行指定的操作。 %s' % (unicode(ex),), category='error')

    def on_model_change(self, form, model, is_created):
        flow = self.support_flow
        if is_created and flow:
            if not flow.keywords or 'support_create' not in flow.keywords or\
                    flow.keywords['support_create']:
                if 'send' in request.form:
                    self._custom_action(model, form.data, Send, False)
                else:
                    self._custom_action(model, form.data, Create, False)

        super(CustomView, self).on_model_change(form, model, is_created)

AnnouncementView = partial(
    _AnnouncementView, Announcement, name='通知公告'
)
