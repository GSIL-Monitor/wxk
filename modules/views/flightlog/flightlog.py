# coding: utf-8

from __future__ import unicode_literals
from functools import partial
import time

from flask import request
from flask_admin import expose

from modules.views.mongo_custom_view import MongoCustomView
from modules.views.aircraft.tranlate_column import column_labels
from modules.forms.aircraft.flight_log import Y5bForm
from modules.views.aircraft.aircraft import aircrafttype_formatter
from modules.views.operations import normal_operation_formatter

from modules.helper import get_allowed_aircrafts
from util.jinja_filter import (
    timestamp_to_datetimestamp,
    timestamp_to_date
)
from util.fields.select import WithTypeSelectField


flightlog_aircrafttype_formatter = partial(
    aircrafttype_formatter, id_name='aircraftId')


class FlightlogView(MongoCustomView):
    "飞行日志的通用视图"
    create_template = 'flightlog/list.html'
    list_template = 'flightlog/date.html'
    extra_js = [
        '/static/js/bootstrap-datetimepicker.min.js',
        '/static/js/datetimepicker.zh-cn.js',
        '/static/js/custom_action.js',
        '/static/js/str_date.js',
        # page level
        '/static/js/flightlog.js',
        '/static/js/moment.min.js',
        '/static/js/fullcalendar.js',
        # '/static/js/dataTables.bootstrap.js',
        # '/static/js/table-editable.js',

    ]

    extra_css = [
        '/static/css/bootstrap-datetimepicker.min.css',
        '/static/css/bootstrap.min.css',
        '/static/css/jquery-ui.css',
        '/static/css/fullcalendar.css',
    ]

    details_columns = [
        'aircraftId', 'aircraftType', 'departureAirport', 'formmakeTime',
        'landingAirport', 'flightDate', 'captain', 'copilot', 'crew',
        'passengers', 'departureTime', 'landingTime', 'flightTime',
        'landings', 'remark', 'logTime', 'aircraftType', 'formMaker',
    ]

    column_labels = column_labels

    column_list = [
        'flightDate', 'operation',
    ]

    column_details_list = [
        'aircraftId', 'aircraftType', 'departureAirport',
        'formmakeTime', 'landingAirport', 'flightDate',
        'captain', 'copilot', 'crew', 'passengers',
        'departureTime', 'landingTime', 'flightTime', 'landings',
        'remark', 'logTime', 'aircraftType', 'formMaker',
    ]

    # column_filters = [
    #     FilterGreaterEqual('flightDate', '飞行日期'),
    #     FilterSmallerEqual('flightDate', '飞行日期'),
    # ]

    def __init__(
        self, db, coll_name='flight_log', action_name='flightlog',
            *args, **kwargs):

            self.column_formatters = self.column_formatters or {}
            self.column_formatters.update({
                'operation': normal_operation_formatter,
                'departureTime': self.date_formatter,
                'landingTime': self.date_formatter,
                'flightDate': self.date_formatter_date,
                'logTime': self.date_formatter,
                'formmakeTime': self.date_formatter,
                'aircraftType': flightlog_aircrafttype_formatter,
            })

            super(FlightlogView, self).__init__(
                db, coll_name=coll_name, action_name=action_name,
                *args, **kwargs)

    @property
    def form_widget_args(self):
        return {
            'aircraftId': {
                'readonly': True
            }
        }

    def get_details_columns(self):
        only_columns = (self.column_details_list or
                        self.scaffold_list_columns())

        return self.get_column_names(
            only_columns=only_columns,
            excluded_columns=self.column_details_exclude_list,
        )

    def date_formatter(self, view, ctx, model, name):
        return timestamp_to_datetimestamp(model[name])

    def date_formatter_date(self, view, ctx, model, name):
        return timestamp_to_date(model[name])

    @property
    def _details_columns(self):
        return self.get_details_columns()

    @property
    def default_subordinate_view(self):
        return 'y5b'

    @property
    def view_list(self):
        return {
            'y5b': {
                '_api_url': '/v1/%(y5b)sflightlog/',
                'coll_name': 'flight_log',
                'form': Y5bForm,
            }
        }

    def get_real_url(self, url, model):

        requestPath = request.path.split('/')
        if 'delete' in requestPath:
            url = url % {'y5b': ''}
        else:
            url = url % {'y5b': model['aircraftType'] + '/'}
        return url

    @expose('/new/', methods=['GET', 'POST'])
    def create_view(self):
        self._create_form_class.aircraftId = WithTypeSelectField(
            '飞行器注册号', choices=[
                ((aircraft.id, aircraft.model),
                    aircraft.id) for aircraft in get_allowed_aircrafts()])

        return super(MongoCustomView, self).create_view()

    @expose('/edit/', methods=['GET', 'POST'])
    def edit_view(self):

        return super(MongoCustomView, self).edit_view()

    def verify_and_modify_data(self, obj):

        obj = super(FlightlogView, self).verify_and_modify_data(obj)

        if 'new' in request.url:
            obj['formmakeTime'] = int(time.time())
            obj['modifyTime'] = None

        if 'edit' in request.url:
            obj['modifyTime'] = int(time.time())
            obj['formmakeTime'] = None

        return obj
