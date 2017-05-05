# coding: utf-8

from __future__ import unicode_literals

from flask import redirect, flash, request
from flask_admin.babel import gettext
from flask_admin.base import expose
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list

from .basic import Basic
from .flight_log import FlightLog
from modules.forms.aircraft.aircraft import AircraftInformationForm
from modules.views.mongo_custom_view import MongoCustomView
from modules.roles import FlightCrew, FlightManager


class AircraftInformationView(MongoCustomView):
    "飞行器的通用视图"

    list_template = 'aircraft/list.html'

    # 为了使用datepicker相关插件
    extra_js = [
        '/static/js/bootstrap-datepicker.js',
        '/static/js/locales/bootstrap-datepicker.zh-CN.js',
    ]

    extra_css = [
        '/static/css/datepicker.css',
    ]

    accepted_roles = [FlightCrew, FlightManager]

    column_list = (
        'id', 'planeType',
        'totalHours', 'totalTimes',
        'boundedMxp',
    )

    column_labels = {
        'id': '飞机器注册号',
        'planeType': '机型名称',
        'totalHours': '总飞行时间',
        'totalTimes': '总起降次数',
        'boundedMxp': '绑定的机型维修方案'
    }

    form = AircraftInformationForm

    @expose('/details/')
    def details_view(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_view_details:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        template = self._delegate_to_sub('template')

        return self.render(template, model=model, id=id, return_url=return_url)

    @property
    def view_list(self):
        # 每一个具体的子方案在界面视图处理时应该提供下面的信息
        # 1. 子方案的名称
        # 2. 子方案对应的主键
        # 3. 子方案的集合名称（mongo）
        # 4. 一些与flask-admin相关的视图配置信息
        return {
            'basic': dict(**Basic()),
            'flightlog': dict(**FlightLog()),
            # 'due-list': dict(**DueList()),
            # 'maintain-log': dict(**MaintainLog()),
        }

    @property
    def default_subordinate_view(self):
        return 'basic'
