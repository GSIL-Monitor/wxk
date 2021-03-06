# coding: utf-8

from __future__ import unicode_literals
from functools import partial

from modules.models.project_tech.engineering_order import EngineeringOrder
from modules.views import CustomView


class _EngineeringOrderView(CustomView):
    pass


EngineeringOrderView = partial(_EngineeringOrderView, EngineeringOrder)
