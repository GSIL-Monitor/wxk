# encoding: utf-8

from __future__ import unicode_literals

from wtforms import fields
from flask_admin.form.fields import Select2Field

from ..widgets import ComponentsDropdownsWidget
from modules.views.mxp.base import get_allowed_models


class ComponentsDropdownsField(Select2Field):
    widget = ComponentsDropdownsWidget(multiple=True)

    def __init__(self, default='',*args, **kwargs):
    	self.widget = ComponentsDropdownsWidget(default=default, multiple=True)
        super(ComponentsDropdownsField, self).__init__(choices=self.get_choice(),
                                                           *args, **kwargs)

    def get_choice(self):
    	from modules.helper import get_allowed_aircrafts
    	choices = []
    	for aircraft in get_allowed_aircrafts():
    	    choices.append(((aircraft.id, aircraft.model), aircraft.id))

        return choices

    def process_data(self, value):
        if value is None:
            self.data = None
        else:
            try:
                self.data = value
            except (ValueError, TypeError):
                self.data = None

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '__None':
                self.data = None
            else:
                try:
                    self.data = ','.join(valuelist)
                except ValueError:
                    raise ValueError(self.gettext(u'数据有误，请联系相关人员'))
        else:
            self.data = ''

    def pre_validate(self, form):
    	pass