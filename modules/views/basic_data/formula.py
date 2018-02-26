# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import logging

from flask import flash
from flask_admin import expose
from flask_admin.babel import gettext
from wtforms.validators import DataRequired
from sqlalchemy.exc import IntegrityError

from modules.views import CustomView
from modules.models.basic_data.formula import Formula, SubFormula
from .inline_form import SubFormulaInlineForm
from modules.roles import SuperAdmin
from modules.views.column_formatter import formula_formatter
from modules.views.operations import normal_operation_formatter


log = logging.getLogger("flask-admin.sqla")


class _FormulaView(CustomView):

    support_flow = False
    use_inheritance_operation = False

    required_roles = [SuperAdmin]

    details_template = 'formula/details.html'

    column_labels = {
        'number': '配方编号',
        'name': '配方名称',
        'formula': '所需农药',
        'sub_formula': '所需农药',
    }

    one_line_columns = ['sub_formula']

    column_list = ['number', 'name', 'operation']

    column_formatters = {
        'formula': formula_formatter,
        'operation': normal_operation_formatter,
    }

    column_details_list = ['number', 'name', 'formula']

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.name.validators = [DataRequired()]
        return super(_FormulaView, self).validate_form(form)

    inline_models = (SubFormulaInlineForm(SubFormula),)

    @expose('/details/')
    def details_view(self):
        self._template_args.update({
            'formula': formula_formatter,
        })
        return super(_FormulaView, self).details_view()


FormulaView = partial(
    _FormulaView, Formula, name='配方信息'
)
