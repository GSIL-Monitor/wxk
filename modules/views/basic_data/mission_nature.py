# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.views import CustomView
from modules.models.basic_data.mission_nature import MissionNature

from modules.roles import SuperAdmin


class _MissionNatureView(CustomView):

    column_display_actions = True

    required_roles = [SuperAdmin]

    support_flow = False

    column_labels = {
        'number': '任务性质编号',
        'name': '任务性质名称',
    }

MissionNatureView = partial(
    _MissionNatureView, MissionNature, name='任务性质'
)
