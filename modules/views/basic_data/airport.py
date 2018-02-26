# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.views import CustomView
from modules.models.basic_data.airport import Airport

from modules.roles import SuperAdmin
from wtforms.validators import DataRequired
from modules.views.operations import normal_operation_formatter


class _AirportView(CustomView):

    use_inheritance_operation = False

    required_roles = [SuperAdmin]

    support_flow = False

    column_labels = {
        'number': '机场编号',
        'name': '机场名称',
        'location': '所在位置',
    }

    column_list = ['number', 'name', 'location', 'operation']

    column_formatters = {
        'operation': normal_operation_formatter,
    }

    column_details_list = ['number', 'name', 'location']

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.name.validators = [DataRequired()]
        return super(_AirportView, self).validate_form(form)

AirportView = partial(
    _AirportView, Airport, name='起降机场'
)
