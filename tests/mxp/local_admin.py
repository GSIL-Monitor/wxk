#! /usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import datetime
import os

from flask import Flask, url_for
from pymongo import MongoClient
from modules.models.base import db as mysqldb
from flask_security import SQLAlchemyUserDatastore, Security
from flask_admin import Admin, helpers
from flask_principal import identity_loaded

from modules.models.user import User
from modules.models.role import Role
from modules.views import IndexView
from modules.perms import _on_identity_loaded
from modules.views.mxp import init_mxp_view
from modules.views.admin import UserAdminView, RoleAdminView

mongodb = MongoClient('192.168.100.204', 30017)['zrth-storage']
user_datastore = SQLAlchemyUserDatastore(mysqldb, User, Role)


def create_app():
    templates = os.path.join(os.path.dirname(__file__),
                             '../../', 'templates')
    settings = os.path.join(os.path.dirname(__file__),
                            '../../', 'etc/local.py')
    static_folder = os.path.join(os.path.dirname(__file__),
                                 '../../', 'assets/static')
    app = Flask(
        __name__,
        template_folder=templates,
    )
    app.config.from_pyfile(settings)

    app.static_folder = static_folder
    app.config.update({'SITE_TIME': datetime.datetime.now()})
    app.config.update({'SQLALCHEMY_ECHO': False})
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)

    admin_test = Admin(app, name='中瑞通航机务维修管理系统',
                       base_template='layout.html',
                       template_mode='bootstrap3',
                       index_view=IndexView())

    sec = Security(app, user_datastore)

    mysqldb.init_app(app)
    # mongodb.init_app(app)

    @sec.context_processor
    def security_context_processor():
        return dict(admin_base_template=admin_test.base_template,
                    admin_view=admin_test.index_view,
                    h=helpers,
                    get_url=url_for)

    identity_loaded.connect_via(app)(_on_identity_loaded)

    register_jinja(app)
    with app.app_context():
        init_mxp_view(admin_test, mongodb, category='维修方案管理')
    admin_test.add_view(UserAdminView(mysqldb.session))
    admin_test.add_view(RoleAdminView(mysqldb.session))

    return app


def register_jinja(app):
    from util.jinja_filter import format_username, province, city, county
    app.jinja_env.filters['format_username'] = format_username
    app.jinja_env.filters['province'] = province
    app.jinja_env.filters['city'] = city
    app.jinja_env.filters['county'] = county
