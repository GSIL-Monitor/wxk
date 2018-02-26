# coding: utf-8

from __future__ import unicode_literals

from wtforms import form, fields
from wtforms.validators import DataRequired, NumberRange

fields_kw = {'class': "form-control"}

data_require = '请输入数字。'
number_require = '请输入小于1000的正整数。'

validate = [DataRequired(data_require), NumberRange(1, 1000, number_require)]


class EarlyWarningForm(form.Form):
    time_fl = fields.IntegerField(validators=validate, render_kw=fields_kw)
    time_sl = fields.IntegerField(validators=validate, render_kw=fields_kw)
    time_tl = fields.IntegerField(validators=validate, render_kw=fields_kw)

    date_fl = fields.IntegerField(validators=validate, render_kw=fields_kw)
    date_sl = fields.IntegerField(validators=validate, render_kw=fields_kw)
    date_tl = fields.IntegerField(validators=validate, render_kw=fields_kw)

    times_fl = fields.IntegerField(validators=validate, render_kw=fields_kw)
    times_sl = fields.IntegerField(validators=validate, render_kw=fields_kw)
    times_tl = fields.IntegerField(validators=validate, render_kw=fields_kw)

    hours_fl = fields.IntegerField(validators=validate, render_kw=fields_kw)
    hours_sl = fields.IntegerField(validators=validate, render_kw=fields_kw)
    hours_tl = fields.IntegerField(validators=validate, render_kw=fields_kw)

    date_fl_type = fields.SelectField(coerce=int, render_kw=fields_kw,
                                      choices=[(2, '日')])
    date_sl_type = fields.SelectField(coerce=int, render_kw=fields_kw,
                                      choices=[(2, '日')])
    date_tl_type = fields.SelectField(coerce=int, render_kw=fields_kw,
                                      choices=[(2, '日')])
