# encoding: utf-8

from flask_security import current_user
from flask_admin.base import MenuLink


class AuthenticatedMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated
