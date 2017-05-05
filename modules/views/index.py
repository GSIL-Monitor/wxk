# encoding: utf-8

from __future__ import unicode_literals

from flask import redirect, url_for, request, abort
from flask_security import current_user, logout_user
from flask_admin import AdminIndexView


class IndexView(AdminIndexView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        return True

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                logout_user()
                return abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))
