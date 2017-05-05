# coding: utf-8

from __future__ import unicode_literals

from modules.roles import FlightCrew, FlightManager
from ..mongo_custom_view import MongoCustomView


class MxpBaseView(MongoCustomView):

    list_template = 'mxp/list.html'
    create_modal_template = 'modal/create.html'
    edit_modal_template = 'modal/create.html'

    accepted_roles = [FlightCrew, FlightManager]

    extra_css = [
        '/static/css/profile.css',
    ]

    extra_js = [
        '/static/js/metronic.js',
        '/static/js/layout.js',
    ]

    column_list = None

    create_modal = True
    edit_modal = True

    def __init__(self, db, endpoint, *args, **kwargs):

        super(MxpBaseView, self).__init__(
            db, None, 'mxp', endpoint='%s-view' % endpoint, *args, **kwargs)
