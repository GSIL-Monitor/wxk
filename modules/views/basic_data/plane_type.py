# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.views import CustomView
from modules.models.basic_data.plane_type import PlaneType

from modules.roles import SuperAdmin


class _PlaneTypeView(CustomView):

    column_display_actions = True

    required_roles = [SuperAdmin]

    support_flow = False

    column_labels = {
        'number': '机型编号',
        'name': '机型名称',
    }

PlaneTypeView = partial(
    _PlaneTypeView, PlaneType, name='机型信息'
)
