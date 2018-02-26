# coding: utf-8

from __future__ import unicode_literals

from flask_admin.model import InlineFormAdmin
from wtforms.validators import NumberRange


class SubFormulaInlineForm(InlineFormAdmin):

    column_labels = {
        'pesticide': '农药',
        'weight': '重量'
    }

    def postprocess_form(self, form_class):
        validators = {'validators': [NumberRange(min=0, message='重量必须为非负数')]}
        form_class.weight.kwargs.update(validators)
        return form_class

    def __init__(self, model, **kwargs):
        super(SubFormulaInlineForm, self).__init__(model, **kwargs)
