# coding: utf-8

from __future__ import unicode_literals
from functools import partial

import logging

from flask import flash
from flask_admin.babel import gettext
from wtforms.validators import DataRequired
from sqlalchemy.exc import IntegrityError

from modules.views import CustomView
from modules.models.basic_data.pesticide import Pesticide
from modules.views.operations import normal_operation_formatter


log = logging.getLogger("flask-admin.sqla")


class _PesticideView(CustomView):

    column_labels = {
        'number': '农药编号',
        'name': '农药名称',
    }

    column_list = ['number', 'name', 'operation']

    form_excluded_columns = ['sub_formula']

    support_flow = False
    use_inheritance_operation = False

    column_formatters = {
        'operation': normal_operation_formatter,
    }

    column_details_list = ['number', 'name']

    def delete_model(self, model):
        try:
            self.on_model_delete(model)
            sub_formulas = model.sub_formula
            for sub_f in sub_formulas:
                if not sub_f.formula_id:
                    self.session.delete(sub_f)
            self.session.flush()
            self.session.delete(model)
            self.session.commit()
        except IntegrityError as ex:
            flash(gettext('该农药在使用中，请先在配方中删除该农药。'), 'info')
            log.exception('Failed to delete record.')

            self.session.rollback()

            return False
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to delete record.')

            self.session.rollback()

            return False
        else:
            self.after_model_delete(model)

        return True

    def validate_form(self, form):
        if form.__class__.__name__ != self.get_delete_form().__name__:
            form.number.validators = [DataRequired()]
            form.name.validators = [DataRequired()]
        return super(_PesticideView, self).validate_form(form)


PesticideView = partial(
    _PesticideView, Pesticide, name='农药信息'
)
