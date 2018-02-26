# coding: utf-8

from __future__ import unicode_literals

from wtforms import SelectField

from util.fields.select import WithTypeSelectField
from modules.views.mxp.base import get_allowed_models
from modules.helper import get_allowed_aircrafts


class PlaneTypeSelectableMixin(object):

    def select_override(self, form_class, model=None):
        the_form_class = getattr(self, form_class)

        the_form_class.planeType = SelectField('机型', choices=[
            (model.value, model.label) for model in get_allowed_models()])
        
        choices = []
        for aircraft in get_allowed_aircrafts():
            choices.append(((aircraft.id, aircraft.model), aircraft.id))
        the_form_class.jihao = WithTypeSelectField('飞行器注册号', choices=choices)

        return the_form_class
