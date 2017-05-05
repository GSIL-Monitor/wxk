# coding: utf-8

from __future__ import unicode_literals

from modules.roles import ProjectTechRole
from modules.views import CustomView


class ProjectTechViewBase(CustomView):

    required_roles = [ProjectTechRole]
