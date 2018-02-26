# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from wtforms.validators import DataRequired
from modules.views import CustomView
from modules.views.operations import normal_operation_formatter
from modules.models.basic_data.pilot import Pilot


class _PilotView(CustomView):

    use_inheritance_operation = False

    support_flow = False

    column_labels = {
        'code': '编码',
        'name': '机长姓名',
    }

    column_list = ['code', 'name', 'operation']

    column_details_list = ['code', 'name']

    column_formatters = {
        'operation': normal_operation_formatter,
    }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.code.validators = [DataRequired()]
            form.name.validators = [DataRequired()]
        return super(_PilotView, self).validate_form(form)


PilotView = partial(
    _PilotView, Pilot, name='机长信息',
)
