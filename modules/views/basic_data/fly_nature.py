# coding: utf-8

from __future__ import unicode_literals
from functools import partial
from wtforms.validators import Length, DataRequired

from modules.views import CustomView
from modules.models.basic_data.fly_nature import FlyNature
from util.validators.letternumber_required import LetterNumberRequired
from modules.views.operations import normal_operation_formatter
from modules.roles import SuperAdmin


class _FlyNatureView(CustomView):

    use_inheritance_operation = False

    required_roles = [SuperAdmin]

    support_flow = False

    column_details_list = ['number', 'name']

    column_list = ['number', 'name', 'operation']

    column_formatters = {
        'operation': normal_operation_formatter,
    }

    column_labels = {
        'number': '飞行性质编号',
        'name': '飞行性质名称',
    }

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.name.validators = [DataRequired()]
            form.number.validators = [LetterNumberRequired(),
                                      Length(max=12), DataRequired()]
        return super(_FlyNatureView, self).validate_form(form)

FlyNatureView = partial(
    _FlyNatureView, FlyNature, name='飞行性质'
)
