# coding: utf-8

from .user import UserAdminView
from .role import RoleAdminView


__all__ = [
    'admin_view'
]


admin_view = [
    UserAdminView, RoleAdminView
]
